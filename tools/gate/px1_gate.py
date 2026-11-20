#!/usr/bin/env python3
"""PX1 gate — одна независимая проверка всей сборки, итог PASS / WARN / HOLD / FAIL.

Работает по STEP-файлу сборки, а не по коду генератора, поэтому одинаково
проверяет CadQuery-мастер (current/CAD/PX1_Current_Master.step.gz) и любую
другую сборку (например FreeCAD-модель M1), если в STEP у каждой детали
есть имя (PRODUCT). Контракт имён и осей — tools/gate/README.md.

Проверки:
  geometry      — все тела валидны, объём > 0; сверка объёмов с реестром (если есть)
  census        — 6 колёс, 10×Z50, Z16/Z40, 2 мотора (по именам)
  interference  — попарные пересечения тел (AABB → Boolean), классы HOLD как в release_tools.py
  pipe_dn150    — поза краулера на колёсах в трубе Ø150 и зазор каждой детали до стенки
  mass_cog      — масса и центр тяжести (плотности — из tools/traction/px1_traction_budget.py)
  stability     — ЦТ ниже оси трубы (самовыравнивание), боковое смещение ЦТ, доли нагрузки на оси
  domain        — существующие расчёты проекта: чертежи, тяга, мощность, кабель, лифт

Выход: <out>/gate_report.json, gate_report.md, gate_views.png.
Код возврата: 0 — нет FAIL (WARN/HOLD допускаются), 1 — есть FAIL, 2 — ошибка запуска.
Это экран CAD-модели, а не квалификация изготовления, герметичности или тяги.
"""
from __future__ import annotations

import argparse
import gzip
import importlib.util
import json
import math
import multiprocessing as mp
import os
import re
import shutil
import subprocess
import sys
import tempfile
import time
from pathlib import Path

import numpy as np

ROOT = Path(__file__).resolve().parents[2]
SPEC_DEFAULT = Path(__file__).with_name('px1_gate_spec.json')
STEP_DEFAULT = ROOT / 'current/CAD/PX1_Current_Master.step.gz'
REGISTRY_DEFAULT = ROOT / 'current/component_registry.json'
AXIS = {'X': 0, 'Y': 1, 'Z': 2}
ORDER = {'PASS': 0, 'INFO': 0, 'SKIP': 0, 'HOLD': 1, 'WARN': 2, 'FAIL': 3}


# ---------------------------------------------------------------- STEP loading
def load_step(path: Path):
    """Return [(name, located TopoDS_Shape)] for every leaf product in the STEP."""
    from OCP.STEPCAFControl import STEPCAFControl_Reader
    from OCP.TDocStd import TDocStd_Document
    from OCP.XCAFDoc import XCAFDoc_DocumentTool
    from OCP.TDF import TDF_LabelSequence, TDF_Label
    from OCP.TDataStd import TDataStd_Name
    from OCP.TCollection import TCollection_ExtendedString
    from OCP.TopLoc import TopLoc_Location
    from OCP.IFSelect import IFSelect_RetDone

    tmp = None
    if path.suffix == '.gz':
        tmp = tempfile.NamedTemporaryFile(suffix='.step', delete=False)
        with gzip.open(path, 'rb') as src:
            shutil.copyfileobj(src, tmp)
        tmp.close()
        path = Path(tmp.name)
    try:
        doc = TDocStd_Document(TCollection_ExtendedString('XmlOcaf'))
        reader = STEPCAFControl_Reader()
        reader.SetNameMode(True)
        if reader.ReadFile(str(path)) != IFSelect_RetDone:
            raise RuntimeError(f'STEP не читается: {path}')
        reader.Transfer(doc)
    finally:
        if tmp:
            os.unlink(tmp.name)
    tool = XCAFDoc_DocumentTool.ShapeTool_s(doc.Main())

    def name_of(label):
        attr = TDataStd_Name()
        if label.FindAttribute(TDataStd_Name.GetID_s(), attr):
            return attr.Get().ToExtString()
        return ''

    parts = []

    def walk(label, loc, inst_name=''):
        if tool.IsAssembly_s(label):
            comps = TDF_LabelSequence()
            tool.GetComponents_s(label, comps)
            for i in range(1, comps.Length() + 1):
                comp = comps.Value(i)
                ref = TDF_Label()
                if tool.GetReferredShape_s(comp, ref):
                    walk(ref, loc.Multiplied(tool.GetLocation_s(comp)), name_of(comp))
        else:
            shape = tool.GetShape_s(label)
            name = name_of(label) or inst_name or f'UNNAMED_{len(parts)}'
            parts.append((name, shape.Moved(loc)))

    roots = TDF_LabelSequence()
    tool.GetFreeShapes(roots)
    for i in range(1, roots.Length() + 1):
        walk(roots.Value(i), TopLoc_Location())
    # Duplicate names get a suffix so every part stays addressable.
    seen = {}
    out = []
    for name, shape in parts:
        k = seen.get(name, 0)
        seen[name] = k + 1
        out.append((name if k == 0 else f'{name}#{k}', shape))
    return out


def props(shape):
    from OCP.GProp import GProp_GProps
    from OCP.BRepGProp import BRepGProp
    from OCP.BRepCheck import BRepCheck_Analyzer
    from OCP.Bnd import Bnd_Box
    from OCP.BRepBndLib import BRepBndLib
    from OCP.TopExp import TopExp_Explorer
    from OCP.TopAbs import TopAbs_SOLID
    g = GProp_GProps()
    BRepGProp.VolumeProperties_s(shape, g)
    c = g.CentreOfMass()
    box = Bnd_Box()
    BRepBndLib.Add_s(shape, box)
    exp = TopExp_Explorer(shape, TopAbs_SOLID)
    solids = 0
    while exp.More():
        solids += 1
        exp.Next()
    return {'volume_mm3': g.Mass(), 'centroid': [c.X(), c.Y(), c.Z()],
            'bbox': list(box.Get()), 'valid': BRepCheck_Analyzer(shape).IsValid(), 'solids': solids}


def mesh(shape, deflection):
    """Vertices (N×3) and triangles (M×3 indices) of the located shape."""
    from OCP.BRepMesh import BRepMesh_IncrementalMesh
    from OCP.TopExp import TopExp_Explorer
    from OCP.TopAbs import TopAbs_FACE
    from OCP.TopoDS import TopoDS
    from OCP.BRep import BRep_Tool
    from OCP.TopLoc import TopLoc_Location
    BRepMesh_IncrementalMesh(shape, deflection, False, 0.25, True)
    verts, tris, base = [], [], 0
    exp = TopExp_Explorer(shape, TopAbs_FACE)
    while exp.More():
        face = TopoDS.Face_s(exp.Current())
        loc = TopLoc_Location()
        tri = BRep_Tool.Triangulation_s(face, loc)
        if tri is not None:
            trsf = loc.Transformation()
            n = tri.NbNodes()
            for i in range(1, n + 1):
                p = tri.Node(i).Transformed(trsf)
                verts.append((p.X(), p.Y(), p.Z()))
            for i in range(1, tri.NbTriangles() + 1):
                a, b, c = tri.Triangle(i).Get()
                tris.append((base + a - 1, base + b - 1, base + c - 1))
            base += n
        exp.Next()
    return np.asarray(verts, float).reshape(-1, 3), np.asarray(tris, int).reshape(-1, 3)


# ---------------------------------------------------------------- interference
_PARTS = None


def _common_volume(pair):
    from OCP.BRepAlgoAPI import BRepAlgoAPI_Common
    from OCP.GProp import GProp_GProps
    from OCP.BRepGProp import BRepGProp
    i, j = pair
    try:
        op = BRepAlgoAPI_Common(_PARTS[i][1], _PARTS[j][1])
        if not op.IsDone():
            return i, j, None, 'boolean not done'
        g = GProp_GProps()
        BRepGProp.VolumeProperties_s(op.Shape(), g)
        return i, j, g.Mass(), None
    except Exception as exc:  # noqa: BLE001 — reported, never hidden
        return i, j, None, repr(exc)


def boxes_overlap(a, b, tol=1e-6):
    return all(a[k] <= b[k + 3] + tol and b[k] <= a[k + 3] + tol for k in range(3))


def classify(rules, a, b):
    for r in rules:
        ra, rb = re.compile(r['a']), re.compile(r['b'])
        if (ra.search(a) and rb.search(b)) or (ra.search(b) and rb.search(a)):
            return r['class']
    return None


def check_interference(parts, info, spec, jobs):
    global _PARTS
    _PARTS = parts
    n = len(parts)
    pairs = [(i, j) for i in range(n) for j in range(i + 1, n)
             if boxes_overlap(info[i]['bbox'], info[j]['bbox'])]
    t0 = time.time()
    ctx = mp.get_context('fork')
    with ctx.Pool(jobs) as pool:
        results = list(pool.imap_unordered(_common_volume, pairs, chunksize=4))
    thr = spec['threshold_mm3']
    fails, holds, errors = [], [], []
    for i, j, vol, err in results:
        a, b = parts[i][0], parts[j][0]
        if err:
            errors.append({'a': a, 'b': b, 'error': err})
        elif vol > thr:
            cls = classify(spec['hold_rules'], a, b)
            row = {'a': a, 'b': b, 'volume_mm3': round(vol, 5)}
            (holds if cls else fails).append(dict(row, **({'class': cls} if cls else {})))
    fails.sort(key=lambda r: -r['volume_mm3'])
    holds.sort(key=lambda r: -r['volume_mm3'])
    status = 'FAIL' if fails or errors else ('HOLD' if holds else 'PASS')
    return {'status': status, 'pairs_total': n * (n - 1) // 2, 'pairs_boolean_after_aabb': len(pairs),
            'threshold_mm3': thr, 'fails': fails, 'holds': holds, 'errors': errors,
            'hold_classes': {c: sum(1 for h in holds if h['class'] == c) for c in sorted({h['class'] for h in holds})},
            'seconds': round(time.time() - t0, 1)}


# ---------------------------------------------------------------- pipe pose
def pipe_pose(meshes, names, spec, axes):
    """Lowest pose of the crawler in a straight pipe: pipe axis as high as the wheels allow."""
    R = spec['inner_diameter_mm'] / 2
    lat, up = AXIS[axes['lateral']], AXIS[axes['up']]
    contact = re.compile(spec['contact_regex'])
    wheel_idx = [k for k, n in enumerate(names) if contact.search(n)]
    if not wheel_idx:
        return None, {'status': 'FAIL', 'detail': 'нет колёс по contact_regex'}
    wv = np.vstack([meshes[k][0] for k in wheel_idx])
    y0 = 0.5 * (wv[:, lat].min() + wv[:, lat].max())
    dy = wv[:, lat] - y0
    if np.abs(dy).max() >= R:
        return None, {'status': 'FAIL', 'detail': f'колёса шире трубы: |dy| {np.abs(dy).max():.2f} ≥ R {R}'}
    s = np.sqrt(R * R - dy * dy)
    zc = float(np.min(wv[:, up] + s))           # each wheel point needs zc - z <= s
    if zc < float(np.max(wv[:, up] - s)) - 1e-9:
        return None, {'status': 'FAIL', 'detail': 'колёса не вписываются в окружность трубы'}
    return (y0, zc), {'status': 'PASS', 'axis_lateral_mm': round(y0, 3), 'axis_up_mm': round(zc, 3), 'R_mm': R}


def pipe_clearance(meshes, names, axis_yz, spec, axes):
    R = spec['inner_diameter_mm'] / 2
    lat, up = AXIS[axes['lateral']], AXIS[axes['up']]
    contact = re.compile(spec['contact_regex'])
    rows = []
    for (v, _), name in zip(meshes, names):
        if contact.search(name) or len(v) == 0:
            continue
        d = np.hypot(v[:, lat] - axis_yz[0], v[:, up] - axis_yz[1])
        k = int(np.argmax(d))
        gap = R - float(d[k])
        st = 'FAIL' if gap < spec['fail_below_mm'] else 'WARN' if gap < spec['warn_below_mm'] else 'PASS'
        rows.append({'part': name, 'gap_mm': round(gap, 3), 'status': st,
                     'at': [round(float(x), 2) for x in v[k]]})
    rows.sort(key=lambda r: r['gap_mm'])
    worst = max((ORDER[r['status']] for r in rows), default=0)
    status = [s for s, o in ORDER.items() if o == worst and s in ('PASS', 'WARN', 'FAIL')][0]
    return {'status': status, 'min_gap_mm': rows[0]['gap_mm'] if rows else None,
            'fail_below_mm': spec['fail_below_mm'], 'warn_below_mm': spec['warn_below_mm'],
            'mesh_deflection_mm': spec['mesh_deflection_mm'],
            'count': {s: sum(r['status'] == s for r in rows) for s in ('FAIL', 'WARN', 'PASS')},
            'closest': rows[:12], 'all': rows}


# ---------------------------------------------------------------- mass / CoG / stability
def density_rules():
    path = ROOT / 'tools/traction/px1_traction_budget.py'
    if not path.exists():
        return {}, []
    spec = importlib.util.spec_from_file_location('px1_traction_budget', path)
    mod = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(mod)
    return dict(mod.DENSITY), list(mod.NAME_DENSITY)


def mass_cog(names, info, registry, mspec):
    by_cat, by_name = density_rules()
    cats = {r['id']: r['category'] for r in registry}
    total, moment, assumed, rows = 0.0, np.zeros(3), [], []
    for name, p in zip(names, info):
        base = name.split('#')[0]
        rho, why = None, None
        for sub, d, reason in by_name:
            if sub in base:
                rho, why = d, reason
                break
        if rho is None and base in cats and cats[base] in by_cat:
            rho, why = by_cat[cats[base]], f'категория {cats[base]}'
        if rho is None:
            rho, why = mspec['default_density_g_cm3'], 'НЕТ ПРАВИЛА — плотность по умолчанию'
            assumed.append(name)
        m = p['volume_mm3'] * rho * 1e-6   # mm3 * g/cm3 -> kg
        total += m
        moment += m * np.asarray(p['centroid'])
        rows.append({'part': name, 'kg': round(m, 4), 'rho': rho, 'rule': why})
    cog = moment / total if total else np.zeros(3)
    rows.sort(key=lambda r: -r['kg'])
    tgt = mspec['target_kg']
    dev = 100 * (total - tgt) / tgt
    status = 'WARN' if abs(dev) > mspec['warn_outside_pct'] or assumed else 'PASS'
    return {'status': status, 'mass_kg': round(total, 3), 'target_kg': tgt, 'deviation_pct': round(dev, 1),
            'cog_mm': [round(float(c), 2) for c in cog], 'parts_without_density_rule': assumed,
            'heaviest': rows[:10]}, cog


def stability(cog, axis_yz, wheel_x, sspec, axes):
    fwd, lat, up = AXIS[axes['forward']], AXIS[axes['lateral']], AXIS[axes['up']]
    h = axis_yz[1] - cog[up]          # >0: CoG below pipe axis → crawler rights itself
    off = cog[lat] - axis_yz[0]
    xs = np.asarray(sorted(set(round(x, 2) for x in wheel_x)))
    xm = xs.mean()
    shares = 1 / len(xs) + (xs - xm) * (cog[fwd] - xm) / np.sum((xs - xm) ** 2) if len(xs) > 1 else np.ones(1)
    checks = []
    st = 'FAIL' if h <= sspec['righting_fail_at_or_below_mm'] else 'WARN' if h < sspec['righting_warn_below_mm'] else 'PASS'
    checks.append({'check': 'righting_height_mm', 'value': round(float(h), 2), 'status': st,
                   'meaning': 'ЦТ ниже оси трубы на эту величину; при крене краулер возвращается сам'})
    st = 'WARN' if abs(off) > sspec['lateral_offset_warn_mm'] else 'PASS'
    checks.append({'check': 'lateral_cog_offset_mm', 'value': round(float(off), 2), 'status': st,
                   'meaning': 'смещение ЦТ вбок от плоскости симметрии — постоянный крен'})
    mn = float(shares.min())
    st = 'FAIL' if mn <= sspec['axle_share_fail_below'] else 'WARN' if mn < sspec['axle_share_warn_below'] else 'PASS'
    checks.append({'check': 'axle_load_shares', 'value': [round(float(s), 3) for s in shares],
                   'axle_x_mm': [float(x) for x in xs], 'cog_x_mm': round(float(cog[fwd]), 2), 'status': st,
                   'meaning': 'доли веса на оси (жёсткая 3-осная схема, плоский контакт); 0 — ось висит'})
    worst = max(ORDER[c['status']] for c in checks)
    return {'status': ['PASS', 'HOLD', 'WARN', 'FAIL'][worst], 'checks': checks,
            'limitations': 'Сложенный лифт, номинальная поза, жёсткие шины. Поднятый лифт, натяжение кабеля и уклон не учтены.'}


# ---------------------------------------------------------------- domain checks
def run(cmd, timeout=600):
    t0 = time.time()
    try:
        p = subprocess.run(cmd, cwd=ROOT, capture_output=True, text=True, timeout=timeout)
        return p.returncode, (p.stdout + p.stderr).strip().splitlines(), round(time.time() - t0, 1)
    except subprocess.TimeoutExpired:
        return 124, ['timeout'], timeout


def domain_checks(out: Path, tspec):
    py = sys.executable
    rows = []

    def add(key, title, cmd, ok_note, path_needed):
        if not (ROOT / path_needed).exists():
            rows.append({'check': key, 'title': title, 'status': 'SKIP', 'detail': f'нет {path_needed}'})
            return None
        code, lines, sec = run(cmd)
        tail = next((l for l in reversed(lines) if l.strip()), '').split(' -> ')[0]
        rows.append({'check': key, 'title': title, 'status': ok_note if code == 0 else 'FAIL',
                     'detail': tail[:200], 'exit': code, 'seconds': sec})
        return code

    add('drawings', 'Мастер против чертежей Mini-Cam', [py, 'tools/drawing_measure/check_master_vs_drawings.py'],
        'PASS', 'tools/drawing_measure/check_master_vs_drawings.py')
    lpath = 'tools/lift/check_lift_kinematics.py'
    if (ROOT / lpath).exists():
        code, lines, sec = run([py, lpath])
        try:
            d = json.loads('\n'.join(lines[lines.index('{'):] if '{' in lines else lines))
            bad = [k for k, v in d.get('checks', {}).items() if v is not True]
            n = len(d.get('checks', {}))
            st = 'PASS' if code == 0 and d.get('status') == 'PASS' and not bad else 'FAIL'
            detail = (f"{n - len(bad)}/{n} проверок (радиусы изгиба кабеля ≥5×D/3×D, запас длины, газовая пружина, "
                      f"зазор при подъёме {d.get('swept_min_clearance_mm', float('nan')):.2f} мм)"
                      + (f"; не прошли: {', '.join(bad)}" if bad else ''))
        except (ValueError, json.JSONDecodeError):
            st, detail = ('INFO' if code == 0 else 'FAIL'), (lines or [''])[-1][:200]
        rows.append({'check': 'lift_kinematics', 'title': 'Лифт камеры и кабель', 'status': st,
                     'detail': detail, 'exit': code, 'seconds': sec})
    add('tether_power_tests', 'Тесты расчёта питания по кабелю', [py, 'current/05_TETHER_REEL/test_tether_power_calc.py'],
        'PASS', 'current/05_TETHER_REEL/test_tether_power_calc.py')
    add('power_budget', 'Бюджет мощности 24 В', [py, 'tools/power/power_budget.py', '--json', str(out / 'power_budget.json')],
        'INFO', 'tools/power/power_budget.py')

    # Traction: the script only calculates; the gate applies the project requirement (40 m now, 100–150 m later).
    tpath = 'tools/traction/px1_traction_budget.py'
    if (ROOT / tpath).exists():
        tjson = out / 'traction_budget.json'
        code, lines, sec = run([py, tpath, '--out', str(tjson), '--label', 'gate'])
        if code != 0 or not tjson.exists():
            rows.append({'check': 'traction', 'title': 'Тяга', 'status': 'FAIL', 'detail': (lines or ['?'])[-1]})
        else:
            t = json.loads(tjson.read_text())
            case = t['cases']['PX1_CAD_estimate']
            notes, status = [], 'PASS'
            for row in case['by_tether_length']:
                L = row['tether_m']
                bad = [s for s, ok in row['ok'].items() if not ok]
                bad_c = [s for s, ok in row['ok_conservative'].items() if not ok]
                if L == tspec['required_tether_m']:
                    if bad:
                        status = 'FAIL'
                    elif bad_c:
                        status = max(status, 'WARN', key=ORDER.get)
                if L in tspec['future_tether_m'] and (bad or bad_c):
                    status = max(status, 'WARN', key=ORDER.get)
                worst = min(row['margin_N'].items(), key=lambda kv: kv[1])
                notes.append(f"{L} м: запас {worst[1]:+.1f} Н ({worst[0]})"
                             + (f"; осторожный кабель: {', '.join(bad_c)} не тянет" if bad_c else ''))
            rows.append({'check': 'traction', 'title': 'Тяга: 40 м сейчас, 100–150 м потом', 'status': status,
                         'detail': '; '.join(notes), 'mass_kg_used': case['mass_kg'],
                         'motor_limited_force_N': t['derived'].get('motor_limited_force_N'),
                         'speed_rated_m_min': t['derived'].get('speed_rated_m_min')})

    build = ROOT / '_cloud_build'
    if (build / 'component_registry.json').exists() and (ROOT / 'scripts/cloud/check_integrated.py').exists():
        code, lines, sec = run([py, 'scripts/cloud/check_integrated.py', '_cloud_build', '--require-pipe-service'], 900)
        rows.append({'check': 'integrated_build', 'title': 'Интегральная проверка сборки (после build_current.sh)',
                     'status': 'PASS' if code == 0 else 'FAIL', 'detail': (lines or [''])[-1][:200]})
    else:
        rows.append({'check': 'integrated_build', 'title': 'Интегральная проверка сборки', 'status': 'SKIP',
                     'detail': 'нужна свежая сборка scripts/cloud/build_current.sh (~9 мин); STEP-проверки выше её дублируют'})
    return rows


# ---------------------------------------------------------------- picture
def raster(meshes, colors, u, v, extent, ppm, order):
    from PIL import Image, ImageDraw
    (u0, u1), (v0, v1) = extent
    W, H = int((u1 - u0) * ppm), int((v1 - v0) * ppm)
    img = Image.new('RGB', (W, H), (255, 255, 255))
    draw = ImageDraw.Draw(img)
    for k in order:
        verts, tris = meshes[k]
        if len(tris) == 0:
            continue
        px = np.column_stack(((verts[:, u] - u0) * ppm, (v1 - verts[:, v]) * ppm))
        col = colors[k]
        for t in tris:
            draw.polygon([tuple(px[t[0]]), tuple(px[t[1]]), tuple(px[t[2]])], fill=col)
    return np.asarray(img)


def picture(path, pic_meshes, names, axis_yz, pipe_rows, cog, wheel_x, stab, pspec, axes, mass):
    import matplotlib
    matplotlib.use('Agg')
    import matplotlib.pyplot as plt
    fwd, lat, up = AXIS[axes['forward']], AXIS[axes['lateral']], AXIS[axes['up']]
    R = pspec['inner_diameter_mm'] / 2
    contact = re.compile(pspec['contact_regex'])
    status = {r['part']: r['status'] for r in pipe_rows}
    pal = {'FAIL': (214, 39, 40), 'WARN': (255, 160, 40), 'PASS': (175, 182, 192), 'WHEEL': (55, 60, 70)}
    colors, rank = [], []
    for n in names:
        key = 'WHEEL' if contact.search(n) else status.get(n, 'PASS')
        colors.append(pal[key])
        rank.append({'PASS': 0, 'WHEEL': 1, 'WARN': 2, 'FAIL': 3}[key])
    order = sorted(range(len(names)), key=lambda k: rank[k])

    y0, zc = axis_yz
    fig, (a1, a2) = plt.subplots(1, 2, figsize=(13, 6.2), gridspec_kw={'width_ratios': [1, 1.55]})
    ext = ((y0 - R - 6, y0 + R + 6), (zc - R - 12, zc + R + 6))
    img = raster(pic_meshes, colors, lat, up, ext, 6, order)
    a1.imshow(img, extent=(ext[0][0], ext[0][1], ext[1][0], ext[1][1]))
    th = np.linspace(0, 2 * np.pi, 400)
    a1.plot(y0 + R * np.cos(th), zc + R * np.sin(th), color='#1f4e79', lw=2)
    a1.plot([y0], [zc], marker='+', color='#1f4e79', ms=14, mew=2)
    a1.plot([cog[lat]], [cog[up]], marker='o', color='#d62728', ms=9, mec='white', mew=1.5)
    h = stab['checks'][0]['value']
    a1.text(y0, zc - R - 3.5, f'+ ось трубы, ● центр тяжести: ниже оси на {h:.1f} мм', fontsize=9,
            ha='center', va='top', color='#333333')
    a1.set_title(f'Сечение в трубе Ø{pspec["inner_diameter_mm"]:.0f} (вид спереди)', fontsize=11)
    a1.set_aspect('equal')
    a1.set_xlabel('Y, мм')
    a1.set_ylabel('Z, мм')

    allv = np.vstack([m[0] for m in pic_meshes if len(m[0])])
    ext2 = ((allv[:, fwd].min() - 8, allv[:, fwd].max() + 8), (zc - R - 4, zc + R + 4))
    img2 = raster(pic_meshes, colors, fwd, up, ext2, 4, order)
    a2.imshow(img2, extent=(ext2[0][0], ext2[0][1], ext2[1][0], ext2[1][1]))
    for zline, label in ((zc - R, 'дно трубы'), (zc + R, 'верх трубы')):
        a2.axhline(zline, color='#1f4e79', lw=2)
        a2.text(ext2[0][0] + 3, zline + (2 if zline < zc else -2), label, fontsize=8, color='#1f4e79',
                va='bottom' if zline < zc else 'top')
    a2.axhline(zc, color='#1f4e79', lw=0.8, ls='--')
    a2.text(ext2[0][1] - 3, zc + 1.5, 'ось трубы', fontsize=8, color='#1f4e79', ha='right', va='bottom')
    a2.plot([cog[fwd]], [cog[up]], marker='o', color='#d62728', ms=9, mec='white', mew=1.5)
    wz = min(float(m[0][:, up].min()) for m, n in zip(pic_meshes, names) if contact.search(n) and len(m[0]))
    sh = stab['checks'][2]
    for x, s in zip(sh['axle_x_mm'], sh['value']):
        a2.text(x, wz - 2, f'{100 * s:.0f}%', ha='center', va='top', fontsize=9, fontweight='bold')
    a2.set_title(f'Сбоку: масса {mass:.2f} кг, ЦТ X{cog[fwd]:.0f} Z{cog[up]:.0f}; % — нагрузка на оси', fontsize=11)
    a2.set_aspect('equal')
    a2.set_xlabel('X, мм')
    from matplotlib.patches import Patch
    a2.legend(handles=[Patch(color=np.array(pal[k]) / 255, label=l) for k, l in
                       (('FAIL', f'зазор < {pspec["fail_below_mm"]:g} мм'),
                        ('WARN', f'зазор {pspec["fail_below_mm"]:g}–{pspec["warn_below_mm"]:g} мм'),
                        ('PASS', f'зазор ≥ {pspec["warn_below_mm"]:g} мм'), ('WHEEL', 'колёса'))],
              loc='lower right', fontsize=8, framealpha=0.9)
    fig.tight_layout()
    fig.savefig(path, dpi=130)
    plt.close(fig)


# ---------------------------------------------------------------- report
def overall(sections):
    worst = max(ORDER[s] for s in sections.values())
    return [k for k in ('PASS', 'HOLD', 'WARN', 'FAIL') if ORDER[k] == worst][0]


def write_md(path, rep):
    S = rep['sections']
    g, c, i, p, m, s = (S.get(k, {}) for k in ('geometry', 'census', 'interference', 'pipe_dn150', 'mass_cog', 'stability'))
    L = [f"# PX1 gate — {rep['verdict']}", '',
         f"Сборка: `{rep['step']}` ({rep['parts']} деталей), {rep['generated']}. "
         'Это экран CAD-модели: не изготовление, не герметичность, не реальная тяга.', '',
         '| Проверка | Итог | Коротко |', '|---|---|---|']
    L.append(f"| Геометрия тел | {g['status']} | невалидных {len(g.get('invalid', []))}, "
             f"сверка с реестром: {g.get('registry_match', '—')} |")
    L.append(f"| Состав (колёса, Z50, Z16/Z40, моторы) | {c['status']} | "
             + ', '.join(f"{r['label']} {r['found']}/{r['count']}" for r in c.get('rows', [])) + ' |')
    if i:
        if 'pairs_boolean_after_aabb' in i:
            L.append(f"| Пересечения деталей | {i['status']} | жёстких {len(i['fails'])}, ошибок {len(i['errors'])}, "
                     f"HOLD {len(i['holds'])} ({', '.join(f'{k} {v}' for k, v in i['hold_classes'].items()) or '—'}); "
                     f"Boolean-пар {i['pairs_boolean_after_aabb']} |")
        else:
            L.append(f"| Пересечения деталей | {i['status']} | {i.get('detail', '')} |")
    if p.get('min_gap_mm') is not None:
        cl = p['closest'][0]
        L.append(f"| Зазор до стенки DN150 | {p['status']} | минимум {p['min_gap_mm']:.2f} мм — {cl['part']}; "
                 f"<{p['fail_below_mm']:g}: {p['count']['FAIL']}, {p['fail_below_mm']:g}–{p['warn_below_mm']:g}: {p['count']['WARN']} |")
    L.append(f"| Масса | {m['status']} | {m['mass_kg']:.2f} кг при цели {m['target_kg']} ({m['deviation_pct']:+.1f} %) |")
    if s:
        h, off, ax = s['checks']
        L.append(f"| Устойчивость в трубе | {s['status']} | ЦТ ниже оси на {h['value']:.1f} мм, вбок {off['value']:+.1f} мм, "
                 f"оси {' / '.join(f'{100 * v:.0f}%' for v in ax['value'])} |")
    for d in rep['sections'].get('domain', {}).get('rows', []):
        L.append(f"| {d['title']} | {d['status']} | {d.get('detail', '')} |")
    L += ['', 'PASS — требование выполнено; WARN — выполнено с малым запасом или не та цель; '
          'HOLD — контакт по замыслу, нужна отдельная проверка; FAIL — нарушение; INFO — расчёт без критерия; SKIP — не запускалось.', '']
    if p.get('closest'):
        L += ['## Ближе всего к стенке трубы', '', '| Деталь | Зазор, мм | Итог |', '|---|---|---|']
        L += [f"| {r['part']} | {r['gap_mm']:.2f} | {r['status']} |" for r in p['closest'][:8]]
        L.append('')
    if i.get('fails'):
        L += ['## Жёсткие пересечения', '', '| A | B | мм³ |', '|---|---|---|']
        L += [f"| {r['a']} | {r['b']} | {r['volume_mm3']} |" for r in i['fails'][:20]]
        L.append('')
    L += ['## Самые тяжёлые детали', '', '| Деталь | кг | плотность | правило |', '|---|---|---|---|']
    L += [f"| {r['part']} | {r['kg']:.3f} | {r['rho']} | {r['rule'][:60]} |" for r in m['heaviest'][:8]]
    L += ['', f"Ограничения устойчивости: {s.get('limitations', '')}", '',
          'Повторить: `python3 tools/gate/px1_gate.py` (≈5–10 мин). Требования: `tools/gate/px1_gate_spec.json`.']
    path.write_text('\n'.join(L) + '\n', encoding='utf8')


# ---------------------------------------------------------------- main
def main():
    ap = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    ap.add_argument('--step', type=Path, default=STEP_DEFAULT, help='STEP сборки (.step или .step.gz)')
    ap.add_argument('--spec', type=Path, default=SPEC_DEFAULT)
    ap.add_argument('--registry', type=Path, default=REGISTRY_DEFAULT, help='реестр деталей для категорий и сверки объёмов')
    ap.add_argument('--out', type=Path, default=ROOT / '_gate')
    ap.add_argument('--jobs', type=int, default=os.cpu_count() or 2)
    ap.add_argument('--skip-interference', action='store_true')
    ap.add_argument('--skip-domain', action='store_true', help='только STEP-проверки (для чужой сборки)')
    a = ap.parse_args()

    spec = json.loads(a.spec.read_text(encoding='utf8'))
    axes = spec['axes']
    a.out.mkdir(parents=True, exist_ok=True)
    registry = json.loads(a.registry.read_text()) if a.registry and a.registry.exists() else []
    t0 = time.time()
    print(f'[gate] читаю {a.step}', flush=True)
    parts = load_step(a.step)
    names = [n for n, _ in parts]
    print(f'[gate] деталей {len(parts)} ({time.time() - t0:.0f} с)', flush=True)
    info = [props(s) for _, s in parts]
    sections = {}

    # geometry + registry cross-check (proves the loader reads what the generator wrote)
    invalid = [n for n, p in zip(names, info) if not p['valid'] or p['volume_mm3'] <= 0]
    reg_match = '—'
    if registry:
        rv = {r['id']: r['volume_mm3'] for r in registry}
        common = [n for n in names if n in rv]
        dv = [abs(info[names.index(n)]['volume_mm3'] - rv[n]) / max(rv[n], 1e-9) for n in common]
        missing = sorted(set(rv) - set(names))
        reg_match = (f'{len(common)}/{len(rv)} имён, макс. расхождение объёма {100 * max(dv, default=0):.3f} %'
                     + (f', нет в STEP: {len(missing)}' if missing else ''))
    sections['geometry'] = {'status': 'FAIL' if invalid else 'PASS', 'invalid': invalid, 'registry_match': reg_match}

    rows = []
    for c in spec['census']:
        rx = re.compile(c['regex'])
        found = sum(1 for n in names if rx.search(n))
        rows.append(dict(c, found=found, status='PASS' if found == c['count'] else 'FAIL'))
    sections['census'] = {'status': 'FAIL' if any(r['status'] == 'FAIL' for r in rows) else 'PASS', 'rows': rows}

    if a.skip_interference:
        sections['interference'] = {'status': 'SKIP', 'detail': '--skip-interference'}
    else:
        print('[gate] пересечения…', flush=True)
        sections['interference'] = check_interference(parts, info, spec['interference'], a.jobs)
        print(f"[gate]   {sections['interference']['status']} за {sections['interference']['seconds']} с", flush=True)

    print('[gate] сетка и труба…', flush=True)
    pspec = spec['pipe']
    # Coarse mesh for the picture first: a finer triangulation made later replaces it, not vice versa.
    pic = [mesh(s, 0.4) for _, s in parts]
    meshes = [mesh(s, pspec['mesh_deflection_mm']) for _, s in parts]
    axis_yz, pose = pipe_pose(meshes, names, pspec, axes)
    if axis_yz is None:
        sections['pipe_dn150'] = pose
    else:
        sections['pipe_dn150'] = dict(pipe_clearance(meshes, names, axis_yz, pspec, axes), pose=pose)

    m, cog = mass_cog(names, info, registry, spec['mass'])
    sections['mass_cog'] = m
    contact = re.compile(pspec['contact_regex'])
    wheel_x = [info[k]['centroid'][AXIS[axes['forward']]] for k, n in enumerate(names) if contact.search(n)]
    if axis_yz is not None:
        sections['stability'] = stability(cog, axis_yz, wheel_x, spec['stability'], axes)

    if not a.skip_domain:
        print('[gate] расчёты проекта…', flush=True)
        drows = domain_checks(a.out, spec['traction'])
        worst = max(ORDER[r['status']] for r in drows)
        sections['domain'] = {'status': [k for k in ('PASS', 'HOLD', 'WARN', 'FAIL') if ORDER[k] == worst][0],
                              'rows': drows}

    rep = {'tool': 'tools/gate/px1_gate.py', 'step': str(a.step.relative_to(ROOT) if a.step.is_relative_to(ROOT) else a.step),
           'spec': str(a.spec.relative_to(ROOT) if a.spec.is_relative_to(ROOT) else a.spec),
           'generated': time.strftime('%Y-%m-%d %H:%M'), 'parts': len(parts),
           'seconds': round(time.time() - t0, 1),
           'verdict': overall({k: v['status'] for k, v in sections.items()}),
           'section_status': {k: v['status'] for k, v in sections.items()}, 'sections': sections}
    (a.out / 'gate_report.json').write_text(json.dumps(rep, ensure_ascii=False, indent=1), encoding='utf8')
    write_md(a.out / 'gate_report.md', rep)
    if axis_yz is not None:
        print('[gate] картинка…', flush=True)
        picture(a.out / 'gate_views.png', pic, names, axis_yz, sections['pipe_dn150'].get('all', []), cog,
                wheel_x, sections['stability'], pspec, axes, m['mass_kg'])
    print(f"[gate] ИТОГ {rep['verdict']}  " + '  '.join(f'{k}={v}' for k, v in rep['section_status'].items()))
    print(f"[gate] {a.out / 'gate_report.md'}  ({rep['seconds']} с)")
    return 1 if rep['verdict'] == 'FAIL' else 0


if __name__ == '__main__':
    sys.exit(main())
