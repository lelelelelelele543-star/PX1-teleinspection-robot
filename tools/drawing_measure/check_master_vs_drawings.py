#!/usr/bin/env python3
"""Compare PX1_Current_Master.py constants against dimensions recovered from Mini-Cam drawings.

The master is NOT imported or executed (it needs CadQuery and builds geometry).
Top-level assignments are parsed with ``ast`` and evaluated with a restricted
evaluator (literals, arithmetic, names already evaluated, math.*, len/min/max/abs).
Anything that cannot be evaluated is simply absent.

Reference table: drawing_reference.json (same folder). Tags:
  CONFIRMED  - drawing callout / spec / catalogue / project requirement
  DERIVED    - measured from a scaled view or computed
  ESTIMATED  - engineering choice
Status per check: PASS / FAIL / SKIP. A missing constant is SKIP, except for
CONFIRMED entries, where it is FAIL. Exit code 0 only if there is no FAIL.

Drawings themselves stay on the user's Google Drive; this public repo holds only numbers.
"""
from __future__ import annotations
import argparse
import ast
import hashlib
import json
import math
import operator
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[2]
HERE = Path(__file__).resolve().parent

_BIN = {ast.Add: operator.add, ast.Sub: operator.sub, ast.Mult: operator.mul,
        ast.Div: operator.truediv, ast.FloorDiv: operator.floordiv,
        ast.Pow: operator.pow, ast.Mod: operator.mod}
_UN = {ast.USub: operator.neg, ast.UAdd: operator.pos}
_FUNCS = {'len': len, 'min': min, 'max': max, 'abs': abs, 'sum': sum,
          'float': float, 'int': int, 'tuple': tuple}


class Missing(Exception):
    """A referenced name is not available from the master."""


def safe_eval(node, env):
    if isinstance(node, ast.Expression):
        return safe_eval(node.body, env)
    if isinstance(node, ast.Constant) and isinstance(node.value, (int, float, str)):
        return node.value
    if isinstance(node, (ast.Tuple, ast.List)):
        return tuple(safe_eval(e, env) for e in node.elts)
    if isinstance(node, ast.Name):
        if node.id in env:
            return env[node.id]
        raise Missing(node.id)
    if isinstance(node, ast.BinOp) and type(node.op) in _BIN:
        return _BIN[type(node.op)](safe_eval(node.left, env), safe_eval(node.right, env))
    if isinstance(node, ast.UnaryOp) and type(node.op) in _UN:
        return _UN[type(node.op)](safe_eval(node.operand, env))
    if isinstance(node, ast.Subscript):
        return safe_eval(node.value, env)[safe_eval(node.slice, env)]
    if isinstance(node, ast.Attribute) and isinstance(node.value, ast.Name) and node.value.id == 'math':
        v = getattr(math, node.attr, None)
        if isinstance(v, float):
            return v
    if isinstance(node, ast.Call) and not node.keywords:
        f = node.func
        if isinstance(f, ast.Attribute) and isinstance(f.value, ast.Name) and f.value.id == 'math' \
                and f.attr in ('sqrt', 'atan2', 'cos', 'sin', 'tan', 'acos', 'asin', 'atan', 'hypot', 'radians', 'degrees', 'pi'):
            return getattr(math, f.attr)(*[safe_eval(a, env) for a in node.args])
        if isinstance(f, ast.Name) and f.id in _FUNCS:
            return _FUNCS[f.id](*[safe_eval(a, env) for a in node.args])
    raise ValueError(f'unsupported expression: {ast.dump(node)[:80]}')


def read_master(path: Path) -> dict:
    env = {}
    for node in ast.parse(path.read_text(encoding='utf-8')).body:
        if not isinstance(node, ast.Assign):
            continue
        try:
            value = safe_eval(node.value, env)
        except (Missing, ValueError, TypeError, ZeroDivisionError, IndexError, KeyError):
            continue
        for target in node.targets:
            if isinstance(target, ast.Name):
                env[target.id] = value
    return env


def ev(expr: str, env: dict):
    return safe_eval(ast.parse(expr, mode='eval'), env)


def _flat(v):
    if isinstance(v, (list, tuple)):
        out = []
        for x in v:
            out.extend(_flat(x))
        return out
    return [v]


def compare(actual, expected, tol):
    a, e = _flat(actual), _flat(expected)
    if len(a) != len(e):
        return False, None
    dev = max((abs(float(x) - float(y)) for x, y in zip(a, e)), default=0.0)
    return dev <= tol + 1e-9, dev


# ---------------------------------------------------------------- derived checks

def side_seal_track_length(env):
    """Centreline length of the lobed side-cover seal, same construction as lobed_seal_face(o=0):
    arcs radius R about each Z50 centre, joined by concave fillets of radius rf whose
    inner-most point is CUSP from the axis."""
    R, c, gx = env['SIDE_SEAL_R'], env['SIDE_SEAL_CUSP'], list(env['GEAR_X'])
    steps = {round(b - a, 9) for a, b in zip(gx, gx[1:])}
    if len(steps) != 1:
        raise ValueError(f'GEAR_X not uniformly spaced: {gx}')
    half = steps.pop() / 2
    n = len(gx)
    rf = ((c * c + half * half) - R * R) / (2 * (R - c))
    zc = c + rf
    phi = math.atan2(zc, half)
    lobes = R * (2 * (2 * math.pi - 2 * phi) + (n - 2) * 2 * (math.pi - 2 * phi))
    fillets = 2 * (n - 1) * rf * (math.pi - 2 * phi)
    return lobes + fillets, {'fillet_r_mm': rf, 'tangent_angle_deg': math.degrees(phi),
                             'lobe_arcs_mm': lobes, 'fillet_arcs_mm': fillets}


def tyre_gap(env):
    """Vertex bound from scripts/cloud/check_pipe_pose.py::profile_screen: for each meridian
    vertex (r, y) the farthest point of its revolution from the pipe axis is
    hypot(WHEEL_CENTRE_Y+y, r+|PIPE_CENTER_Z-WHEEL_Z|); segment maxima lie at vertices."""
    pr, wy, wz, pz = env['PIPE_R'], env['WHEEL_CENTRE_Y'], env['WHEEL_Z'], env['PIPE_CENTER_Z']
    prof = [tuple(p) for p in env['WHEEL_PROFILE']]
    delta = abs(pz - wz)
    crown = max(r for r, _ in prof)
    gaps = []
    for r, y in prof:
        if y == 0 and r == crown:
            continue
        gaps.append((pr - math.hypot(wy + y, r + delta), r, y))
    g, r, y = min(gaps)
    contact = pr - math.hypot(wy, crown + delta)
    return g, {'worst_vertex_r_y': [r, y], 'crown_contact_gap_mm': contact, 'pipe_center_z_mm': pz}


def run_derived(d, env):
    kind = d['kind']
    if kind == 'side_seal_track':
        length, info = side_seal_track_length(env)
        idd, cs = env['SIDE_ORING']
        ring = math.pi * (idd + cs)
        stretch = (length / ring - 1) * 100
        ok = d['min_pct'] - 1e-9 <= stretch <= d['max_pct'] + 1e-9
        return ok, round(stretch, 3), f"{d['min_pct']}..{d['max_pct']} %", dict(
            info, track_centreline_mm=length, oring_centreline_mm=ring, stretch_pct=stretch)
    if kind == 'gland':
        cs, w, dep = ev(d['cs'], env), ev(d['width'], env), ev(d['depth'], env)
        squeeze = (cs - dep) / cs * 100
        fill = math.pi * (cs / 2) ** 2 / (w * dep) * 100
        lo, hi = d['squeeze_pct']
        ok = lo <= squeeze <= hi and fill <= d['max_fill_pct']
        return ok, f'sq {squeeze:.1f} % / fill {fill:.1f} %', f"sq {lo}-{hi} %, fill <={d['max_fill_pct']} %", dict(
            squeeze_pct=squeeze, fill_pct=fill, cs_mm=cs, groove_w_mm=w, groove_d_mm=dep)
    if kind == 'tyre_gap':
        g, info = tyre_gap(env)
        req = env['WHEEL_MIN_NONCONTACT_GAP']
        return g >= req - 1e-9, round(g, 3), f'>= {req}', dict(info, min_noncontact_gap_mm=g)
    if kind == 'wheel_width':
        w = 2 * (env['WHEEL_CENTRE_Y'] + max(abs(y) for _, y in env['WHEEL_PROFILE']))
        ok, dev = compare(w, d['expected'], d['tol_mm'])
        return ok, w, f"{d['expected']} ±{d['tol_mm']}", {'deviation_mm': dev}
    if kind == 'expr_range':
        v = ev(d['expr'], env)
        lo, hi = d['range']
        ok = (lo is None or v >= lo - 1e-9) and (hi is None or v <= hi + 1e-9)
        return ok, round(v, 4), f"{'' if lo is None else lo}..{'' if hi is None else hi} {d.get('units', '%')}", {'expr': d['expr']}
    raise ValueError(f'unknown derived kind {kind}')


# ---------------------------------------------------------------- main

def main():
    ap = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    ap.add_argument('--master', type=Path, default=ROOT / 'current/CAD/PX1_Current_Master.py')
    ap.add_argument('--reference', type=Path, default=HERE / 'drawing_reference.json')
    ap.add_argument('--out', type=Path, default=ROOT / '_cloud_build/drawing_check.json')
    ap.add_argument('--quiet', action='store_true', help='print only FAIL/SKIP rows and the summary')
    args = ap.parse_args()

    env = read_master(args.master)
    ref = json.loads(args.reference.read_text(encoding='utf-8'))
    results = []

    for c in ref['checks']:
        row = {'id': c['id'], 'tag': c['tag'], 'master_constant': c['master_constant'], 'source': c['source']}
        try:
            actual = ev(c['master_constant'], env)
        except Missing as m:
            row.update(status='FAIL' if c['tag'] == 'CONFIRMED' else 'SKIP', actual=None,
                       note=f'constant {m} not found in master')
            results.append(row)
            continue
        row['actual'] = actual
        if 'min' in c:
            ok = float(actual) >= c['min'] - 1e-9
            row.update(expected=f">= {c['min']}", status='PASS' if ok else 'FAIL')
        else:
            ok, dev = compare(actual, c['expected'], c['tol_mm'])
            row.update(expected=c['expected'], tol_mm=c['tol_mm'], deviation_mm=dev,
                       status='PASS' if ok else 'FAIL')
            if dev is None:
                row['note'] = 'shape mismatch'
        results.append(row)

    for d in ref.get('derived_checks', []):
        row = {'id': d['id'], 'tag': d['tag'], 'kind': d['kind'], 'source': d['source']}
        try:
            ok, actual, expected, detail = run_derived(d, env)
            row.update(status='PASS' if ok else 'FAIL', actual=actual, expected=expected, detail=detail)
        except (Missing, KeyError) as m:
            row.update(status='FAIL' if d['tag'] == 'CONFIRMED' else 'SKIP', actual=None,
                       note=f'constant {m} not found in master')
        results.append(row)

    counts = {s: sum(r['status'] == s for r in results) for s in ('PASS', 'FAIL', 'SKIP')}
    report = {'tool': 'tools/drawing_measure/check_master_vs_drawings.py',
              'master': str(args.master.relative_to(ROOT)) if args.master.resolve().is_relative_to(ROOT) else str(args.master),
              'master_sha256': hashlib.sha256(args.master.read_bytes()).hexdigest(),
              'reference_sha256': hashlib.sha256(args.reference.read_bytes()).hexdigest(),
              'status': 'PASS' if counts['FAIL'] == 0 else 'FAIL',
              'counts': counts, 'n_checks': len(results),
              'note': 'Reference values come from Mini-Cam drawings on the user Google Drive and catalogues; '
                      'the drawings are not stored in this public repo. Not a manufacturing release.',
              'results': results}
    args.out.parent.mkdir(parents=True, exist_ok=True)
    args.out.write_text(json.dumps(report, indent=2, ensure_ascii=False, default=str), encoding='utf-8')

    def fmt(v):
        if isinstance(v, float):
            return f'{v:.4g}'
        if isinstance(v, (list, tuple)):
            return '(' + ','.join(fmt(x) for x in v) + ')'
        return str(v)
    print(f"{'status':6} {'tag':9} {'id':36} {'actual':>26}  expected")
    for r in results:
        if args.quiet and r['status'] == 'PASS':
            continue
        exp = r.get('expected')
        if 'tol_mm' in r and r['tol_mm']:
            exp = f"{fmt(exp)} ±{r['tol_mm']}"
        print(f"{r['status']:6} {r['tag']:9} {r['id']:36} {fmt(r.get('actual'))[:26]:>26}  {fmt(exp)}"
              + (f"  [{r['note']}]" if r.get('note') else ''))
    print(f"\n{report['status']}: {len(results)} checks, PASS {counts['PASS']}, FAIL {counts['FAIL']}, SKIP {counts['SKIP']} -> {args.out}")
    return 0 if counts['FAIL'] == 0 else 1


if __name__ == '__main__':
    sys.exit(main())
