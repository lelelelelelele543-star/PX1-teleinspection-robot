"""A46 transverse motor/plate envelope; design assumptions, NOT 3D collision test."""
from pathlib import Path
import csv
R=12.5; MOTOR_AXIS=13.5; PLATE_INNER=22.5; TARGET_GAP=1.5
intrusion=max(0,MOTOR_AXIS+R-PLATE_INNER)
new_inner=MOTOR_AXIS+R+TARGET_GAP
assert abs(intrusion-3.5)<1e-9
assert abs(new_inner-27.5)<1e-9
assert abs(new_inner-PLATE_INNER-5)<1e-9
p=Path(__file__).parent
with (p/'results.csv').open('w',newline='') as f:
 w=csv.writer(f);w.writerow(['metric','mm','status'])
 w.writerows([['motor_diameter',2*R,'ASSUMED'],['axis_offset',MOTOR_AXIS,'ASSUMED'],['plate_inner',PLATE_INNER,'DERIVED_A15'],['existing_intrusion_each_side',intrusion,'PASS_2D'],['target_inner_face',new_inner,'DESIGN_TARGET'],['required_plate_shift',new_inner-PLATE_INNER,'PASS_2D']])
print('PASS 2D envelope; SKIPPED 3D Boolean; NEEDS_PHYSICAL_CHECK full CAD')
