#!/usr/bin/env python3
"""PX1 shaft pressure boundary: analytical 2D screen, NOT a qualified seal design.
All dimensions in mm, forces N. Standard-library only. Generates SVG/JSON.
No changes to PX1_Current_Master.py; interface is wheel station X50/150/250.
"""
import json, math
from pathlib import Path
P=Path(__file__).resolve().parent
# DESIGN ASSUMPTIONS, not Mini-Cam factory dimensions or certified seal ratings:
pressure_bar=0.7
shaft_d=18.0
seal_bore_d=30.0
bearing_od=30.0
wheel_stations=(50,150,250)
sides=(-1,1)
# Design concept: isolate pressure from rolling bearing with a separate,
# pressure-qualified rotary lip seal; its catalogue rating remains UNVERIFIED.
# A standard low-pressure 12x22x7 seal must NOT be treated as qualified.
pressure_mpa=pressure_bar*0.1
axial_force_per_shaft=pressure_mpa*math.pi*shaft_d**2/4
radial_seal_projected_load=pressure_mpa*shaft_d*7.0 # nominal 7mm contact band SCREEN ONLY
checks={
 'six_shaft_boundaries': 'PASS' if len(wheel_stations)*len(sides)==6 else 'FAIL',
 'shaft_smaller_than_seal_bore': 'PASS' if shaft_d<seal_bore_d else 'FAIL',
 'seal_bore_vs_bearing_od': 'PHYSICAL_CHECK', # identical OD does NOT imply same seat
 'rotary_seal_pressure_rating': 'PHYSICAL_CHECK',
 'seal_direction_and_lubrication': 'PHYSICAL_CHECK',
 'pressure_body_leak_test': 'PHYSICAL_CHECK',
 'shaft_to_motor_3d_collision': 'NOT_RUN',
}
assert axial_force_per_shaft>0 and checks['six_shaft_boundaries']=='PASS'
report={'source':'PX1 shaft pressure interface design screen','assumptions':{
 'pressure_bar_gauge':pressure_bar,'shaft_d_mm':shaft_d,'seal_housing_d_mm':seal_bore_d,
 'seal_nominal_width_mm':7.0,'bearing_od_mm':bearing_od,
 'shaft_stations_x_mm':wheel_stations,'shaft_sides':sides},
 'calculations':{'axial_force_per_shaft_N':round(axial_force_per_shaft,3),
 'axial_force_six_shafts_N':round(6*axial_force_per_shaft,3),
 'projected_band_load_per_shaft_N_screen_only':round(radial_seal_projected_load,3)},
 'checks':checks,'manufacturing_release':False,
 'critical_note':'No selected seal is rated here for 0.7 bar; do not machine seal seats from this drawing.'}
(P/'PX1_shaft_pressure_interface.json').write_text(json.dumps(report,indent=2)+'\n')
print(json.dumps(report,indent=2))
