"""PX1 A37: FreeCAD shaft with two annular grooves. ALL dimensions ASSUMED.
Run with FreeCAD Python: FreeCADCmd px1_a37_freecad.py
No DIN 471 compliance or pressure seal claim.
"""
import FreeCAD as App
import Part
from pathlib import Path
D=12.0
ROOT_D=11.0
WIDTH=1.1
LENGTH=42.0
CENTERS=(-15.0,15.0)
assert D>ROOT_D>0 and WIDTH>0
for c in CENTERS:
    assert abs(c)+WIDTH/2<LENGTH/2
doc=App.newDocument("PX1_A37_X150")
shape=Part.makeCylinder(D/2,LENGTH,App.Vector(-LENGTH/2,0,0),App.Vector(1,0,0))
for c in CENTERS:
    start=App.Vector(c-WIDTH/2,0,0)
    outer=Part.makeCylinder(D/2+1,WIDTH,start,App.Vector(1,0,0))
    inner=Part.makeCylinder(ROOT_D/2,WIDTH,start,App.Vector(1,0,0))
    shape=shape.cut(outer.cut(inner))
assert shape.isValid() and len(shape.Solids)==1
obj=doc.addObject("PartDesign::Feature","X150_shaft_grooved")
obj.Shape=shape
out=Path(__file__).parent
Part.export([obj],str(out/"px1_a37_shaft.step"))
doc.saveAs(str(out/"px1_a37_shaft.FCStd"))
print("PASS: valid single solid; STEP and FCStd exported")
