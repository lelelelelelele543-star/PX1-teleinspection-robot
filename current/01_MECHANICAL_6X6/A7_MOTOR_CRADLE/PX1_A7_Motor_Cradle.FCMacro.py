# PX1 A7 - preliminary motor cradle. FreeCAD Python macro, mm.
# All dimensions DESIGN ASSUMPTIONS, not measured Mini-Cam or motor vendor data.
import FreeCAD as App, Part, math, os
from FreeCAD import Vector
L,W,T=44.0,26.0,3.0
HOLE_D=3.2
MOTOR_D=24.0
V_HEIGHT=9.0
doc=App.newDocument("PX1_A7_Motor_Cradle")
base=Part.makeBox(L,W,T,Vector(0,-W/2,0))
# mounting holes in base, outside cradle support regions
for x in (5.0,39.0):
    for y in (-9.5,9.5):
        base=base.cut(Part.makeCylinder(HOLE_D/2,T,Vector(x,y,0)))
# two transverse V supports: notch is explicit polygon extruded along x
# V surface bottom at z=5 and top at z=12 at y=+-11.
for x in (12.0,28.0):
    block=Part.makeBox(4,W,V_HEIGHT,Vector(x,-W/2,T))
    polygon=[Vector(x-0.1,-11,12),Vector(x-0.1,0,5),
             Vector(x-0.1,11,12),Vector(x-0.1,11,17),
             Vector(x-0.1,-11,17)]
    wire=Part.makePolygon(polygon+[polygon[0]])
    notch=Part.Face(wire).extrude(Vector(4.2,0,0))
    block=block.cut(notch)
    base=base.fuse(block)
base=base.removeSplitter()
obj=doc.addObject("PartDesign::Feature","Cradle")
obj.Label="A7 motor cradle (assumed)"
obj.Shape=base
doc.recompute()
assert not base.isNull() and base.isValid()
assert len(base.Solids)==1
out=os.path.dirname(os.path.abspath(__file__))
doc.saveAs(os.path.join(out,"PX1_A7_Motor_Cradle.FCStd"))
Part.export([obj],os.path.join(out,"PX1_A7_Motor_Cradle.step"))
Part.export([obj],os.path.join(out,"PX1_A7_Motor_Cradle.stl"))
print("A7 geometry valid; CAD export created. Motor/strap interference NOT validated.")
