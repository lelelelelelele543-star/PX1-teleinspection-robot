"""A23: axial X-envelope screen; all dimensions DESIGN ASSUMED, mm.
No 3D collision/strength or manufacturer geometry is claimed.
"""
from pathlib import Path
P=dict(motor_start=100.,motor_length=32.,output_extension=8.,
       axle_x=150.,axle_radius=6.,gear_face=10.,
       motor_extension_plus=1.,axle_position_minus=.5,
       axle_radius_plus=.2,gear_face_plus=.4)
def clearance_to_axle(p=P):
    return (p["axle_x"]-p["axle_position_minus"]-p["axle_radius"]-p["axle_radius_plus"])-(p["motor_start"]+p["motor_length"]+p["output_extension"]+p["motor_extension_plus"])
def clearance_to_gear(p=P):
    return (p["axle_x"]-p["axle_position_minus"]-(p["gear_face"]+p["gear_face_plus"])/2)-(p["motor_start"]+p["motor_length"]+p["output_extension"]+p["motor_extension_plus"])
assert abs(clearance_to_axle()-2.3)<1e-9
assert abs(clearance_to_gear()-3.3)<1e-9
assert clearance_to_axle()>0 and clearance_to_gear()>0
print("PASS assumed X-only interval screen",clearance_to_axle(),clearance_to_gear())
print("SKIPPED real 3D boolean; NEEDS_PHYSICAL_CHECK motor/gear/axle dimensions")
