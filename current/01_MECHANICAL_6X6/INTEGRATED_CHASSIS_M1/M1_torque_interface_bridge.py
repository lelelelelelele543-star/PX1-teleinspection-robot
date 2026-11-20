"""PX1 M1 torque interface bridge: run after M1_run_integrated_chassis.py. ASSUMED geometry."""
from pathlib import Path
import FreeCAD as App, Part
from FreeCAD import Vector as V
ROOT=Path(__file__).resolve().parent
source=ROOT/'PX1_Integrated_6x6_M1_keyed.FCStd'
if not source.exists(): raise RuntimeError('NOT_RUN: keyed assembly missing')
doc=App.openDocument(str(source))
made=[]
def annulus(name,x,y0,y1,outer=9,inner=5):
    a=Part.makeCylinder(outer,y1-y0,V(x,y0,0),V(0,1,0))
    b=Part.makeCylinder(inner,y1-y0,V(x,y0,0),V(0,1,0))
    shape=a.cut(b)
    if not shape.isValid() or shape.Volume<=0: raise RuntimeError('FAIL '+name)
    o=doc.addObject('PartDesign::Feature',name);o.Shape=shape
    o.ViewObject.ShapeColor=(0.75,0.45,0.18);made.append(o)
    return o
for side,sgn in [('L',-1),('R',1)]:
    bevel=doc.getObject('Bevel_Z40_PROXY_'+side)
    if bevel is None or abs(bevel.Shape.BoundBox.XCenter-100)>1e-5:
        raise RuntimeError('FAIL rear bevel axis')
    bb=bevel.Shape.BoundBox
    bevel.Shape=bevel.Shape.cut(Part.makeCylinder(5,bb.YLength,V(100,bb.YMin,0),V(0,1,0)))
    if not bevel.Shape.isValid(): raise RuntimeError('FAIL bevel bore')
    y0,y1=sorted((sgn*24.,sgn*30.))
    annulus('Rear_Z40_Z50_HUB_PROXY_'+side,100,y0,y1)
    for idx,x in enumerate((-50.,50.),1):
        annulus('Idler_BEARING_GEAR_HUB_PROXY_%s_%d'%(side,idx),x,y0,y1)
for side in ('L','R'):
    for i in (1,2):
        g=doc.getObject('Z50_pitch_PROXY_%s_%d'%(side,2*i))
        h=doc.getObject('Idler_BEARING_GEAR_HUB_PROXY_%s_%d'%(side,i))
        if g is None or h is None or g.Shape.common(h.Shape).Volume<=0:
            raise RuntimeError('FAIL idler hub/gear connection')
    g=doc.getObject('Z50_pitch_PROXY_%s_5'%side)
    h=doc.getObject('Rear_Z40_Z50_HUB_PROXY_'+side)
    if g.Shape.common(h.Shape).Volume<=0:
        raise RuntimeError('FAIL rear hub/gear connection')
assert len(made)==6
doc.recompute()
doc.saveAs(str(ROOT/'PX1_Integrated_6x6_M1_bridged.FCStd'))
Part.export([o for o in doc.Objects if o.TypeId=='PartDesign::Feature'],str(ROOT/'PX1_Integrated_6x6_M1_bridged.step'))
print('PASS 6 geometrical hub bridges; NOT_RUN true rolling bearings, bevel mesh, pressure, torque')
