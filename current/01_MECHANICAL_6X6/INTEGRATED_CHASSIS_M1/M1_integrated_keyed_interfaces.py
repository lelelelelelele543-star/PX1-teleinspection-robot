"""PX1 M1 integrated keyed wheel + driven spur interfaces.
Run with FreeCADCmd after PX1_Integrated_6x6_M1_interface_repair.py.
DESIGN ASSUMPTION: 3 mm wide rectangular keys, NOT DIN-qualified.
Only 6 driven Z50 and 6 wheels; idlers intentionally free.
"""
import os, FreeCAD as App, Part
from FreeCAD import Vector as V
ROOT=os.path.dirname(os.path.abspath(__file__))
source=os.path.join(ROOT,"PX1_Integrated_6x6_M1.FCStd")
if not os.path.isfile(source):
    raise RuntimeError("NOT_RUN: base FCStd missing; run existing M1 generator first")
doc=App.openDocument(source)
report=[]
def box(x,y,z,dx,dy,dz): return Part.makeBox(dx,dy,dz,V(x,y,z))
def object_named(name):
    obj=doc.getObject(name)
    if obj is None: raise RuntimeError("FAIL missing "+name)
    return obj
for side,sgn in (("L",-1),("R",1)):
    for station in range(3):
        gear_index=2*station+1
        x=(-100,0,100)[station]
        axle=object_named("Wheel_axle_%s_%d"%(side,station+1))
        gear=object_named("Z50_pitch_PROXY_%s_%d"%(side,gear_index))
        wheel=object_named("Wheel_%s_%d"%(side,station+1))
        # Keyway at positive X radial direction; key width Z=3 mm.
        # Driven gear axial Y=27..33 (R), -33..-27 (L).
        # Wheel Y=46..60 (R), -60..-46 (L).
        gear_y=27 if sgn>0 else -33
        wheel_y=46 if sgn>0 else -60
        # Axle terminates at |Y|=59, hence wheel key is 13 mm long.
        key_regions=[("spur",gear,gear_y,6),("wheel",wheel,wheel_y+(0 if sgn>0 else 1),13)]
        for kind,hub,y0,ln in key_regions:
            shaft_cut=box(x+3.5,y0,-1.5,1.7,ln,3)
            hub_cut=box(x+4.8,y0,-1.5,1.9,ln,3)
            axle.Shape= axle.Shape.cut(shaft_cut)
            hub.Shape=hub.Shape.cut(hub_cut)
            key=doc.addObject("PartDesign::Feature","KEY_PROXY_%s_%d_%s"%(side,station+1,kind))
            key.Shape=box(x+3.5,y0,-1.5,3.1,ln,3)
            key.ViewObject.ShapeColor=(0.88,0.7,0.2)
            if not axle.Shape.isValid() or not hub.Shape.isValid() or not key.Shape.isValid():
                raise RuntimeError("FAIL invalid key geometry "+key.Name)
            if axle.Shape.common(key.Shape).Volume>1e-5:
                raise RuntimeError("FAIL key/shaft material collision "+key.Name)
            if hub.Shape.common(key.Shape).Volume>1e-5:
                raise RuntimeError("FAIL key/hub material collision "+key.Name)
            report.append(key.Name)
doc.recompute()
assert len(report)==12
out=os.path.join(ROOT,"PX1_Integrated_6x6_M1_keyed.FCStd")
doc.saveAs(out)
# Export with explicit output names, do not overwrite the baseline.
Part.export([o for o in doc.Objects if o.TypeId=="PartDesign::Feature"],
            os.path.join(ROOT,"PX1_Integrated_6x6_M1_keyed.step"))
print("PASS 12 geometric key slots and 12 keys, 6 driven gears + 6 wheels")
print("NOT_RUN torque capacity, tolerances, full assembly collision, dynamic gear mesh")
print("PHYSICAL_CHECK pressurized shaft seals, key shear, bearing load, wheel retention")
