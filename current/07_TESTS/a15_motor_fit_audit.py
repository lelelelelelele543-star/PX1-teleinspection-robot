#!/usr/bin/env python3
"""PX1: reproduce motor/plate collision in October A1.5 prototype.

This is a RELEASE BLOCKER diagnostic, not a test of a working robot.
Source test geometry: A1.5 digital ZIP dated 2026-10-21.
Motor envelope: Pololu #5707 Ø25 × 54 mm, 24 V (candidate only).
"""
from pathlib import Path
import json
import math
import os
import cadquery as cq

out = Path(os.getenv("PX1_MOTOR_AUDIT_OUT", "."))
out.mkdir(parents=True, exist_ok=True)
motor_centers = (-13.5,13.5)
plate_centers = (-25.5,25.5)
motor_face_x = 208.
wheel_axial_inner_y = 52.
motor_d = 25.
motor_length = 54.
plate_t = 6.
z_axis = 45.

def box(x,y,z,dx,dy,dz):
    return cq.Workplane("XY").box(dx,dy,dz).translate((x,y,z))
def cyl_y(x,y,z,r,h):
    return cq.Workplane("XY").newObject([
        cq.Solid.makeCylinder(r,h,cq.Vector(x,y,z),cq.Vector(0,1,0))
    ])

def original_a15_plate(center_y):
    # Same geometry and subtractive operations as 2026-10-21 A1.5.
    p=box(150,center_y,45,260,6,74)
    for x in (75,125,175,225):
        p=p.cut(box(x,center_y,45,14,6.2,32))
    for x in (50,100,150,200,250):
        p=p.cut(cyl_y(x,center_y-3.1,45,14.1,6.2))
        for z in (23,67):
            p=p.cut(cyl_y(x,center_y-3.1,z,2.1,6.2))
    for x,z in ((30,15),(150,75),(270,15)):
        p=p.cut(cyl_y(x,center_y-3.1,z,2.6,6.2))
    return p.val()

plates={y:original_a15_plate(y) for y in plate_centers}
collisions=[]
for y in motor_centers:
    motor=cq.Solid.makeCylinder(
        motor_d/2,motor_length,
        cq.Vector(motor_face_x-motor_length,y,z_axis),
        cq.Vector(1,0,0))
    for py,plate in plates.items():
        vol=motor.intersect(plate).Volume()
        if vol>0.001:
            collisions.append(dict(motor_center_y_mm=y,plate_center_y_mm=py,
                                   collision_mm3=round(vol,3)))

plate_inner_abs=25.5-plate_t/2
motor_outer_abs=13.5+motor_d/2
r90_pipe_dist=math.hypot(57,45+abs(z_axis-52.0480547))
r80_pipe_dist=math.hypot(57,40+abs(z_axis-52.0480547))
report=dict(
    original_design="2026-10-21 PX1 A1.5 OPEN FRAME (not the pressure housing)",
    motor_candidate="Pololu #5707 24V Ø25×54 (not sourced/approved for Russian procurement)",
    model_assumptions=dict(output_face_x_mm=motor_face_x, motor_centers_y_mm=motor_centers,
                           motor_center_z_mm=z_axis, inner_plate_abs_y_mm=25.5),
    motor_plate_nominal_clearance_mm=round(plate_inner_abs-motor_outer_abs,3),
    collisions=collisions,
    status="BLOCKED: A1.5 plate arrangement cannot contain these motors" if collisions else "MOTOR_SCREEN_ONLY_PASS",
    candidate_reposition=dict(
        inner_plate_center_abs_y_mm=30.5,outer_plate_center_abs_y_mm=52.5,
        revised_motor_plate_nominal_clearance_mm=1.5,
        predicted_90mm_tire_at_y57_DN150_clearance_mm=round(75-r90_pipe_dist,3),
        predicted_80mm_tire_at_y57_DN150_clearance_mm=round(75-r80_pipe_dist,3),
        note="A screen, not validated CAD. Wider panels force complete wheel/shaft/gear redesign."
    ),
    release=False,
    unsolved=["motor mounting", "real matched bevel Z16/Z40","axial retention",
              "DN150 tire with actual tread","seal/pressure enclosure","physical torque test"]
)
(out/"PX1_MOTOR_FIT_AUDIT.json").write_text(json.dumps(report,indent=2,ensure_ascii=False),encoding="utf8")
assert len(collisions)==2, f"Expected to reproduce existing A1.5 blocker, got: {collisions}"
assert report["motor_plate_nominal_clearance_mm"]<0
print(json.dumps(report,ensure_ascii=False,indent=2))
print("AUDIT OK: original A1.5 collision reproduced; production release remains BLOCKED.")
