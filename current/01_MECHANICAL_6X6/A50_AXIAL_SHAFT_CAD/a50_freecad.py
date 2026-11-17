# PX1 A50 assumed shaft/bearing envelopes; FreeCAD macro
import FreeCAD as App, Part
from FreeCAD import Vector
D=App.newDocument("PX1_A50_AXIAL_SHAFTS")
rear=250.0; ends={"L":120.0,"R":215.0}; ys={"L":-18.0,"R":18.0}
for side,end in ends.items():
 y=ys[side]; x=234.0-3.5
 shaft=Part.makeCylinder(4.0,rear-4.0-end,Vector(end,y,0),Vector(1,0,0))
 o=D.addObject("PartDesign::Feature","Shaft_"+side);o.Shape=shaft
 outer=Part.makeCylinder(11.0,7.0,Vector(x,y,0),Vector(1,0,0))
 inner=Part.makeCylinder(4.0,7.0,Vector(x,y,0),Vector(1,0,0))
 b=D.addObject("PartDesign::Feature","BearingEnvelope_"+side);b.Shape=outer.cut(inner)
 assert shaft.isValid() and b.Shape.isValid()
D.recompute()
D.saveAs(__file__.replace("a50_freecad.py","a50.FCStd"))
Part.export([o for o in D.Objects if hasattr(o,"Shape")],__file__.replace("a50_freecad.py","a50.step"))
