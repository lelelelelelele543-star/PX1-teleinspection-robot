#!/usr/bin/env python3
"""Fail CI for damaged, non-manifold, incorrectly oriented A1 print STLs.

Checks test fixtures, not wheel torque coupling, OEM gears or pressure integrity.
"""
import json
import sys
from pathlib import Path
import trimesh

directory = Path(sys.argv[1] if len(sys.argv) > 1 else 'a1_generated')
expected = {
    'PX1_A1_SidePlate.stl': ((260,74,6), -42),
    'PX1_A1_Crossbar_1.stl': ((14,45,12), 0),
    'PX1_A1_Z50_m1_PA20_TEST.stl': ((52,52,4), 0),
}
for filename,(bbox,euler) in expected.items():
    path=directory / filename
    assert path.is_file() and path.stat().st_size > 1000, f'missing/empty: {path}'
    mesh=trimesh.load_mesh(path, force='mesh')
    assert mesh.is_watertight, f'open surface: {filename}'
    assert mesh.is_winding_consistent, f'inverted surface: {filename}'
    assert len(mesh.split())==1, f'disconnected solids: {filename}'
    assert mesh.euler_number == euler, f'wrong through-hole count: {filename}, euler={mesh.euler_number}'
    for measured,nominal in zip(mesh.extents,bbox):
        assert abs(float(measured)-nominal) < 0.2, f'wrong print orientation/size: {filename}, {mesh.extents}'
    print('PASS',filename,mesh.extents.round(2), 'Euler',mesh.euler_number)

validation=json.loads((directory/'PX1_A1_Validation.json').read_text(encoding='utf8'))
b=validation['bench_substitutions']
assert b['window_bearing_min_ligament_mm'] >= 3.8
assert b['gear_axial_nominal_clearance_each_side_mm'] >= .8
assert b['crossbar_bolt_datums_mm'] == [[30,15],[150,75],[270,15]]
assert b['crossbar_through_bore_mm'] == 5.2
assert validation['frozen']['wheel_x_mm'] == [50,150,250]
assert validation['frozen']['gear_x_mm'] == [50,100,150,200,250]
print('PASS: A1 print-pack mesh QA and mechanical fixture datums; physical tests pending')
