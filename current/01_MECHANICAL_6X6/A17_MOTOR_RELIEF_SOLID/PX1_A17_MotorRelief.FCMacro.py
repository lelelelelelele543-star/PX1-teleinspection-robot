"""PX1 A17 - FreeCAD solid construction, two local internal plates.
ASSUMED dimensions in mm; not pressure boundary; no manufacturing release.
Run with FreeCAD Python (FreeCADCmd or GUI Python console).
"""
import FreeCAD as App
import Part
from FreeCAD import Vector

P = dict(x0=90.0, length=50.0, inner_y=22.5, plate_t=6.0,
         z0=-20.0, height=40.0, motor_y=13.5, motor_r=12.5,
         radial_clearance=0.5, motor_x0=100.0, motor_length=32.0)
doc=App.newDocument("PX1_A17_motor_relief")
solids=[]
for side in (-1,1):
    # Solid plate from Y=22.5..28.5 (mirror for negative Y).
    y0=P["inner_y"] if side==1 else -P["inner_y"]-P["plate_t"]
    plate=Part.makeBox(P["length"],P["plate_t"],P["height"],
                       Vector(P["x0"],y0,P["z0"]))
    cutter=Part.makeCylinder(P["motor_r"]+P["radial_clearance"],
                            P["motor_length"],
                            Vector(P["motor_x0"],side*P["motor_y"],0),
                            Vector(1,0,0))
    relief=plate.cut(cutter)
    assert relief.isValid() and len(relief.Solids)==1
    assert relief.Volume>0 and relief.Volume<plate.Volume
    obj=doc.addObject("PartDesign::Feature","Plate_%s"%("R" if side==1 else "L"))
    obj.Shape=relief
    obj.addProperty("App::PropertyString","Status")
    obj.Status="ASSUMED: A17 motor-envelope relief, NOT production approved"
    solids.append(obj)
    print("PASS",obj.Name,"volume mm3",round(relief.Volume,3),
          "removed mm3",round(plate.Volume-relief.Volume,3))
assert P["inner_y"]-(P["motor_y"]+P["motor_r"]+P["radial_clearance"]) == -4.0
assert P["plate_t"]-4.0 == 2.0
doc.recompute()
import os
out=os.path.dirname(os.path.abspath(__file__))
doc.saveAs(os.path.join(out,"PX1_A17_MotorRelief.FCStd"))
Part.export(solids,os.path.join(out,"PX1_A17_MotorRelief.step"))
print("PASS geometry; NEEDS_PHYSICAL_CHECK web strength and true motor dimensions")
print("SKIPPED: full crawler collision, shaft X150, bearings, fastener checks")
