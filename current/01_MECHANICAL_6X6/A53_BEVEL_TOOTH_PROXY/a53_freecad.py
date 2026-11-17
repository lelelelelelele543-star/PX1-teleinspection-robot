"""FreeCAD: straight-bevel sector PROXY, NOT conjugate involute bevel geometry.
Exports FCStd/STEP only if executed in FreeCAD. Do not manufacture these teeth.
"""
import math
from pathlib import Path
import FreeCAD as App
import Part
P=Path(__file__).resolve().parent
m=1.5; zs=(16,40); face=8.0; R=m*math.hypot(*zs)/2
doc=App.newDocument("PX1_A53_BEVEL_PROXY")
objs=[]
for index,z in enumerate(zs):
    delta=math.atan2(z,zs[1-index]); outer=m*z/2
    inner=(R-face)*math.sin(delta); half=math.pi/(2*z)
    teeth=[]
    for k in range(z):
        theta=2*math.pi*k/z
        sections=[]
        for station,r in ((0,outer),(face,inner)):
            scale=r/outer
            lo=r-0.5*m*scale; hi=r+0.5*m*scale
            points=[App.Vector(rad*math.cos(ang),rad*math.sin(ang),station)
                for rad,ang in ((lo,theta-half),(hi,theta-half),(hi,theta+half),(lo,theta+half))]
            points.append(points[0])
            sections.append(Part.makePolygon(points))
        teeth.append(Part.makeLoft(sections,True,False))
    core=Part.makeCone(outer-0.8*m,inner-0.8*m,face)
    obj=doc.addObject("PartDesign::Feature","Gear_Z%d_PROXY"%z)
    obj.Shape=Part.makeCompound([core]+teeth)
    obj.Label="Z%d radial sector proxy (NOT tooth geometry)"%z
    obj.Placement.Base=App.Vector(index*100,0,0)
    objs.append(obj)
doc.recompute()
doc.saveAs(str(P/"a53_proxy.FCStd"))
Part.export(objs,str(P/"a53_proxy.step"))
