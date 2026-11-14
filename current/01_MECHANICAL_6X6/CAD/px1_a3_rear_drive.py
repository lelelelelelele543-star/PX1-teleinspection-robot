#!/usr/bin/env python3
"""PX1 A3 — independently designed rear drive STEP study, not an OEM copy.

Usage: python -m pip install cadquery shapely; python px1_a3_rear_drive.py
Output: A3_rear_drive.step, A3_m1_z50.step, A3_result.json
All custom dimensions are design assumptions. Standard bearing/seal envelopes are
catalog-backed; the depicted generic 12x22x7 lip seal is NOT pressure-qualified
for PX1's 0.4–0.7 bar internal overpressure.
"""
import json, math
from pathlib import Path
import cadquery as cq
from shapely.geometry import Polygon
from shapely.affinity import translate

OUT=Path("A3_outputs"); OUT.mkdir(exist_ok=True)
MODULE=1.0
TEETH=50
ANGLE=math.radians(20)
PITCH_R=MODULE*TEETH/2
BASE_R=PITCH_R*math.cos(ANGLE)
TIP_R=PITCH_R+MODULE
ROOT_R=PITCH_R-1.25*MODULE
FACE=6
AXLE_X=250
IDLER_X=200
RPIPE=75
WHEEL_OD=70
WHEEL_WIDTH=12
WHEEL_INNER_Y=53
ZAXLE=RPIPE-math.sqrt(RPIPE**2-(WHEEL_INNER_Y+WHEEL_WIDTH)**2)+WHEEL_OD/2

def inv(r):
    a=math.acos(BASE_R/r)
    return math.tan(a)-a

def outline(phase=0):
    """Piecewise-linear sample of genuine involute flanks, not pitch disks.
    No tooth-root fillets, tolerance grades, or backlash allowances.
    """
    pitch=2*math.pi/TEETH
    half_pitch=math.pi/(2*TEETH)
    def half(r):return half_pitch+inv(PITCH_R)-inv(r)
    pts=[]
    for i in range(TEETH):
        th=i*pitch+phase
        radii=[ROOT_R+(TIP_R-ROOT_R)*j/8 for j in range(9)]
        for rr in radii:
            aa=th-half(rr)
            pts.append((rr*math.cos(aa),rr*math.sin(aa)))
        for j in range(1,6):
            aa=th-half(TIP_R)+2*half(TIP_R)*j/5
            pts.append((TIP_R*math.cos(aa),TIP_R*math.sin(aa)))
        for rr in reversed(radii[:-1]):
            aa=th+half(rr)
            pts.append((rr*math.cos(aa),rr*math.sin(aa)))
        root_right=th+half(ROOT_R)
        root_next=th+pitch-half(ROOT_R)
        for j in range(1,5):
            aa=root_right+(root_next-root_right)*j/5
            pts.append((ROOT_R*math.cos(aa),ROOT_R*math.sin(aa)))
    return pts

def gear(cx,phase=0):
    solid=(cq.Workplane("XY").polyline(outline(phase)).close()
           .extrude(FACE).rotate((0,0,0),(1,0,0),-90)
           .translate((cx,44,ZAXLE)).val())
    return solid.cut(cyl(6,43.8,6.4,cx))

def cyl(radius,yy,length,cx=AXLE_X):
    return cq.Solid.makeCylinder(radius,length,
        cq.Vector(cx,yy,ZAXLE),cq.Vector(0,1,0))

def ring(ro,ri,yy,length,cx=AXLE_X):
    return cyl(ro,yy,length,cx).cut(cyl(ri,yy-.1,length+.2,cx))

# Radial envelope and two-gear mesh screening.
p1=Polygon(outline(0))
p2=translate(Polygon(outline(math.pi/TEETH)),xoff=50)
mesh_intrusion=p1.intersection(p2).area
corner_radius=max(math.hypot(65,ZAXLE-35-75),
                  math.hypot(65,ZAXLE+35-75))
assert corner_radius<=75+1e-6
assert abs(AXLE_X-IDLER_X-TEETH*MODULE)<1e-9
assert mesh_intrusion<0.05
assert AXLE_X-22-212.4>0

model=cq.Assembly(name="PX1_A3_REAR_OUTPUT_STUDY")
def add(shape,name,r,g,b):
    assert shape.isValid(),name
    model.add(shape,name=name,color=cq.Color(r,g,b))

# Two 6001 ring envelopes. This sketch omits ball/cage internal physics.
shaft=cyl(6,4,65)
add(shaft,"shaft_d12",.63,.7,.75)
house=(cq.Workplane("XY").box(44,31,46)
       .translate((250,28.5,ZAXLE)).val())
house=house.cut(cyl(14.03,12.5,23.5))
house=house.cut(cyl(11.03,35.9,8.3))
for dx in [-16,16]:
    for dz in [-16.5,16.5]:
        drill=cq.Solid.makeCylinder(2.15,32,
            cq.Vector(250+dx,12.5,ZAXLE+dz),cq.Vector(0,1,0))
        house=house.cut(drill)
add(house,"bearing_and_seal_housing_concept",.47,.65,.72)

for i,yy in enumerate([14,27],1):
    add(ring(14,12.2,yy,8),f"6001_{i}_outer_envelope",.8,.84,.88)
    add(ring(8,6,yy,8),f"6001_{i}_inner_envelope",.75,.79,.82)
add(ring(11,6,36,7),"12x22x7_generic_seal_ENVELOPE_NOT_PRESSURE_QUALIFIED",.15,.26,.31)

outgear=gear(250,0)
# 4mm keyway is a DESIGN assumption, not a finalized ISO fit.
slot=(cq.Workplane("XY").box(3,6.4,4)
      .translate((256.7,47,ZAXLE)).val())
outgear=outgear.cut(slot)
add(outgear,"Z50_m1_rear_custom_bore12",.84,.63,.22)
add(gear(200,math.pi/TEETH),"Z50_idler_meshing_study_only",.84,.61,.21)
add(ring(22,6,53,12),"wheel_hub_d44",.65,.69,.72)
add(ring(35,22.15,53,12),"removable_tire_d70",.18,.2,.23)
add(ring(10,6,5,6),"bevel_input_placeholder_collar",.6,.64,.68)

model.save(str(OUT/"PX1_A3_RearDrive.step"),exportType="STEP")
cq.exporters.export(outgear,str(OUT/"PX1_A3_Z50_TEST.step"))
result={
 "pitch_d_mm":50,"outer_d_mm":52,"module":1,
 "mesh_intersection_mm2":round(mesh_intrusion,6),
 "wheel_envelope_radius_mm":round(corner_radius,6),
 "bearing_pair":"2x 6001 12x28x8","seal_envelope":"12x22x7",
 "motor_rear_clearance_mm":15.6,
 "manufacturing_release":False,
 "unresolved":["shaft shoulder and circlip","seal type 0.7 bar",
 "hub torque connection","bevel drive","housing stack tolerance"]
}
(OUT/"validation.json").write_text(json.dumps(result,indent=2)+"\n")
print(json.dumps(result,indent=2))
