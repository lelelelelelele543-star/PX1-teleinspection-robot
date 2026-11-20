#!/usr/bin/env python3
"""F27: what ballast can and cannot do for mass, CoG height and axle loads (from the gate report).

Free cavity space: part bounding boxes +0.5 mm (conservative, same method as F17), cavity box X24..288
Y±26.5 Z24..75.1 from the master, motor vertical-extraction column X91.6..207.1 above Z32 kept clear,
1 voxel off the cavity walls and floor. 1 mm voxels. Existing ballast blocks are treated as removable.
ESTIMATED screen, not a CAD placement: real blocks are boxes and need fixing, wiring and thermal room.
"""
import json
from pathlib import Path
import numpy as np

ROOT = Path(__file__).resolve().parents[3]
rep = json.loads((ROOT / 'current/09_RELEASE/gate_20261120/gate_report.json').read_text())['sections']
M = rep['mass_cog']['mass_kg']; C = np.array(rep['mass_cog']['cog_mm']); ZC = rep['pipe_dn150']['pose']['axis_up_mm']
BOX = [(25.0, -21.5, 25.0, 90.0, -11.5, 66.0), (25.0, 11.5, 25.0, 90.0, 21.5, 66.0), (117.0, -25.5, 25.0, 188.0, 25.5, 30.0),
       (266.0, 10.5, 25.0, 287.0, 25.5, 68.0), (270.0, -25.5, 25.0, 287.0, -10.5, 55.75), (266.0, -25.5, 39.0, 270.0, -10.5, 55.75)]
STEEL, LEAD, WALLOY, STAINLESS = 7.85, 11.3, 17.5, 7.9
AX = np.array([50, 150, 250.])


def shares(x):
    return 1 / 3 + (AX - 150) * (x - 150) / np.sum((AX - 150) ** 2)


def row(tag, m, c):
    s = shares(c[0])
    return {'variant': tag, 'mass_kg': round(m, 2), 'righting_mm': round(ZC - c[2], 1),
            'axles_pct': [int(round(100 * v)) for v in s]}


reg = json.loads((ROOT / 'current/component_registry.json').read_text())
X0, X1, Y0, Y1, Z0, Z1 = 24, 288, -26.5, 26.5, 24, 75.1
xs, ys, zs = np.arange(X0 + .5, X1), np.arange(Y0 + .5, Y1), np.arange(Z0 + .5, Z1)
occ = np.zeros((len(xs), len(ys), len(zs)), bool)
for i in reg:
    if i['id'].startswith(('HOLD_PRESSURE_BODY', 'HOLD_BALLAST')):
        continue
    b = i['bbox_mm']
    ix, iy, iz = (xs > b[0] - .5) & (xs < b[3] + .5), (ys > b[1] - .5) & (ys < b[4] + .5), (zs > b[2] - .5) & (zs < b[5] + .5)
    if ix.any() and iy.any() and iz.any():
        occ[np.ix_(ix, iy, iz)] = True
occ[np.ix_((xs > 91.1) & (xs < 207.6), np.ones(len(ys), bool), zs > 31.5)] = True
occ[:, :1, :] = occ[:, -1:, :] = occ[:, :, :1] = True
free = ~occ
X, Y, Z = np.meshgrid(xs, ys, zs, indexing='ij')

bm = [(b[3] - b[0]) * (b[4] - b[1]) * (b[5] - b[2]) * STEEL * 1e-6 for b in BOX]
bc = [np.array([(b[0] + b[3]) / 2, (b[1] + b[4]) / 2, (b[2] + b[5]) / 2]) for b in BOX]
m0 = M - sum(bm); c0 = (M * C - sum(m * c for m, c in zip(bm, bc))) / m0
plate_v = (272 - 24.5) * 50.3 * 12; plate_c = np.array([148.25, 0, 17.0])


def fill(mask, rho):
    m = mask.sum() * rho * 1e-6
    return m, np.array([X[mask].mean(), Y[mask].mean(), Z[mask].mean()])


vol = int(round(sum(bm) / STEEL * 1e6))
order = np.argsort((Z + 0.15 * (288 - X))[free])[:vol]
low = np.zeros(free.sum(), bool); low[order] = True
best = np.zeros_like(free); best[free] = low

out = [row('F25 сейчас: сталь, 6 блоков', M, C)]
mb, cb = fill(best, STEEL); out.append(row('сталь, те же 0,74 кг переставить ниже и в корму (предел)', m0 + mb, (m0 * c0 + mb * cb) / (m0 + mb)))
ma, ca = fill(free, STEEL); out.append(row(f'сталь во ВСЮ свободную полость ({free.sum() / 1000:.0f} см³)', m0 + ma, (m0 * c0 + ma * ca) / (m0 + ma)))
for name, rho in (('свинец в капсуле', LEAD), ('вольфрамовый сплав', WALLOY)):
    dm = plate_v * (rho - STAINLESS) * 1e-6
    out.append(row(f'плита FSS-002-060: {name} {rho} (+{dm:.2f} кг)', M + dm, (M * C + dm * plate_c) / (M + dm)))
    out.append(row(f'  + перестановка стального балласта', m0 + mb + dm, (m0 * c0 + mb * cb + dm * plate_c) / (m0 + mb + dm)))
res = {'pipe_axis_z_mm': ZC, 'free_cavity_cm3': round(free.sum() / 1000, 1), 'targets': 'масса 9,25±10 %, ЦТ ≥5 мм ниже оси, задняя ось ≥20 %',
       'rows': out}
print(json.dumps(res, ensure_ascii=False, indent=1))
(Path(__file__).with_name('ballast_options.json')).write_text(json.dumps(res, ensure_ascii=False, indent=1))
