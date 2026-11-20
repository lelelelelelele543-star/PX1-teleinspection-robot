#!/usr/bin/env python3
"""Проверка проверяющего: px1_gate.py должен ловить заведомые ошибки.

Строит маленькую синтетическую сборку с известным ответом и запускает гейт:
  INTRUDER врезан в корпус на 2×10×10 = 200 мм³     -> interference FAIL с этой парой
  MAST торчит к стенке трубы (зазор ≈0,94 мм)        -> pipe_dn150 FAIL на MAST
  LOWBAR у стенки с зазором ≈3,94 мм                 -> WARN
  колёс 6, моторов 0                                 -> census: колёса PASS, моторы FAIL
  масса и ЦТ                                          -> совпадают с ручным расчётом
Без сети и без файлов проекта, ~1 мин.
"""
from __future__ import annotations

import json
import math
import subprocess
import sys
import tempfile
from pathlib import Path

import cadquery as cq

HERE = Path(__file__).resolve().parent
R = 75.0


def build(step: Path):
    asm = cq.Assembly(name='SELFTEST')
    # Wheels Ø90×20 at X 50/150/250, Y ±45, axis Z 45 → lowest point of each wheel Z 0.
    for side in (-1, 1):
        for x in (50, 150, 250):
            w = cq.Workplane('XZ').circle(45).extrude(10, both=True).translate((x, side * 45, 45))
            asm.add(w, name=f'TEST_WHEEL_{side}_{x}')
    body = cq.Workplane('XY').box(260, 60, 50).translate((150, 0, 45))   # Z 20..70, Y ±30
    asm.add(body, name='BODY')
    intruder = cq.Workplane('XY').box(10, 10, 10).translate((150, 0, 70 + 5 - 2))  # 2 mm into body top
    asm.add(intruder, name='INTRUDER')
    step.parent.mkdir(parents=True, exist_ok=True)
    asm.export(str(step))
    return asm


def main():
    tmp = Path(tempfile.mkdtemp(prefix='px1_gate_selftest_'))
    step = tmp / 'selftest.step'
    asm = build(step)

    # Pipe pose for this geometry: wheel outer faces Y ±55, wheel circle centre Z45 R45.
    # The gate finds the axis analytically; place MAST/LOWBAR relative to that axis afterwards.
    spec = json.loads((HERE / 'px1_gate_spec.json').read_text(encoding='utf8'))
    spec['census'] = [{'label': 'колёса', 'regex': 'WHEEL_-?1_', 'count': 6},
                      {'label': 'моторы', 'regex': 'TRACTION_MOTOR', 'count': 2}]
    spec_path = tmp / 'spec.json'
    spec_path.write_text(json.dumps(spec, ensure_ascii=False))
    probe = subprocess.run([sys.executable, str(HERE / 'px1_gate.py'), '--step', str(step), '--spec', str(spec_path),
                            '--registry', str(tmp / 'none.json'), '--out', str(tmp / 'probe'),
                            '--skip-domain', '--skip-interference'], capture_output=True, text=True)
    pose = json.loads((tmp / 'probe/gate_report.json').read_text())['sections']['pipe_dn150']['pose']
    zc = pose['axis_up_mm']
    # Binding wheel point: bottom of the outer rim (Y ±55, Z 0) → zc = 0 + sqrt(R² − 55²) = 50.990.
    best = math.sqrt(R * R - 55 * 55)
    assert abs(zc - best) < 0.08, f'ось трубы {zc} != ожидаемая {best:.3f}'

    mast_top = zc + R - 1.0            # 1 mm from the pipe crown → FAIL
    asm.add(cq.Workplane('XY').box(6, 6, mast_top - 70).translate((100, 0, 70 + (mast_top - 70) / 2)), name='MAST')
    low = zc - R + 4.0                 # 4 mm above the invert, on the axis line → WARN
    asm.add(cq.Workplane('XY').box(6, 6, 20 - low).translate((200, 0, low + (20 - low) / 2)), name='LOWBAR')
    asm.export(str(step))

    out = tmp / 'run'
    p = subprocess.run([sys.executable, str(HERE / 'px1_gate.py'), '--step', str(step), '--spec', str(spec_path),
                        '--registry', str(tmp / 'none.json'), '--out', str(out), '--skip-domain', '--jobs', '2'],
                       capture_output=True, text=True)
    rep = json.loads((out / 'gate_report.json').read_text())
    S = rep['sections']
    errors = []

    def want(cond, msg):
        if not cond:
            errors.append(msg)

    want(p.returncode == 1 and rep['verdict'] == 'FAIL', f"итог должен быть FAIL/exit 1, а {rep['verdict']}/{p.returncode}")
    pairs = {frozenset((f['a'], f['b'])): f['volume_mm3'] for f in S['interference']['fails']}
    v = pairs.get(frozenset(('BODY', 'INTRUDER')))
    want(v is not None and abs(v - 200) < 0.5, f'пересечение BODY×INTRUDER 200 мм³ не найдено: {pairs}')
    want(not any('WHEEL' in a for k in pairs for a in k), 'ложное пересечение с колесом')
    gaps = {r['part']: r for r in S['pipe_dn150']['all']}
    # Bar corners sit at Y ±3, so the exact gap is R − hypot(3, R − nominal).
    g_mast, g_low = R - math.hypot(3, R - 1.0), R - math.hypot(3, R - 4.0)
    want(gaps['MAST']['status'] == 'FAIL' and abs(gaps['MAST']['gap_mm'] - g_mast) < 0.06, f"MAST {gaps['MAST']} ≠ {g_mast:.3f}")
    want(gaps['LOWBAR']['status'] == 'WARN' and abs(gaps['LOWBAR']['gap_mm'] - g_low) < 0.06, f"LOWBAR {gaps['LOWBAR']} ≠ {g_low:.3f}")
    cen = {r['label']: r['status'] for r in S['census']['rows']}
    want(cen == {'колёса': 'PASS', 'моторы': 'FAIL'}, f'состав: {cen}')
    # Mass with the default density 2.7 (no registry, no name rules match): sum V·ρ, CoG = Σ m·c / Σ m.
    vols = {'BODY': (260 * 60 * 50, (150, 0, 45)), 'INTRUDER': (1000, (150, 0, 73)),
            'MAST': (36 * (mast_top - 70), (100, 0, (70 + mast_top) / 2)),
            'LOWBAR': (36 * (20 - low), (200, 0, (low + 20) / 2))}
    wv = math.pi * 45 ** 2 * 20
    for side in (-1, 1):
        for x in (50, 150, 250):
            vols[f'W{side}{x}'] = (wv, (x, side * 45, 45))
    m = sum(vv for vv, _ in vols.values()) * 2.7e-6
    cz = sum(vv * c[2] for vv, c in vols.values()) / sum(vv for vv, _ in vols.values())
    want(abs(S['mass_cog']['mass_kg'] - m) < 0.002, f"масса {S['mass_cog']['mass_kg']} != {m:.3f}")
    want(abs(S['mass_cog']['cog_mm'][2] - cz) < 0.05, f"ЦТ Z {S['mass_cog']['cog_mm'][2]} != {cz:.2f}")
    h = S['stability']['checks'][0]['value']
    want(abs(h - (zc - cz)) < 0.05, f'высота самовыравнивания {h} != {zc - cz:.2f}')

    print(json.dumps({'selftest': 'PASS' if not errors else 'FAIL', 'errors': errors,
                      'pipe_axis_z': zc, 'mast_gap': gaps['MAST']['gap_mm'], 'lowbar_gap': gaps['LOWBAR']['gap_mm'],
                      'intruder_mm3': v, 'mass_kg': S['mass_cog']['mass_kg']}, ensure_ascii=False, indent=1))
    return 0 if not errors else 1


if __name__ == '__main__':
    sys.exit(main())
