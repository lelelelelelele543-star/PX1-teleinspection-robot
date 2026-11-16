"""PX1 A27 - FreeCAD solid from assumed involute Z50 outline. Run inside FreeCAD Python console or as macro.
Geometry is NOT production qualified: radial root transitions are sharp; no root fillets/backlash.
"""
import math, csv, json
from pathlib import Path
import FreeCAD as App
import Part
V=App.Vector
OUT=Path(__file__).resolve().parent
Z=50; MOD=1.5; ALPHA=math.radians(20); THICKNESS=8.0
BORE_D=12.0; HUB_D=24.0; HUB_EXTRA=4.0
rp=MOD*Z/2; rb=rp*math.cos(ALPHA); ra=rp+MOD; rf=rp-1.25*MOD
half=math.pi/(2*Z)
def inv(t): return t-math.atan(t)
tp=math.sqrt((rp/rb)**2-1)
baseangle=half+inv(tp)
def flank(r, side):
    t=math.sqrt(max(0,(r/rb)**2-1))
    a=side*(baseangle-inv(t))
    return (r*math.cos(a),r*math.sin(a))
def polar(r,a):return (r*math.cos(a),r*math.sin(a))
def rot(p,a):return (p[0]*math.cos(a)-p[1]*math.sin(a),p[0]*math.sin(a)+p[1]*math.cos(a))
def tooth_points():
    p=[polar(rf,-baseangle),polar(rb,-baseangle)]
    p.extend(flank(rb+(ra-rb)*i/32,-1) for i in range(1,33))
    left=math.atan2(p[-1][1],p[-1][0])
    right=math.atan2(flank(ra,1)[1],flank(ra,1)[0])
    p.extend(polar(ra,left+(right-left)*i/12) for i in range(1,13))
    p.extend(flank(rb+(ra-rb)*i/32,1) for i in range(31,-1,-1))
    p.append(polar(rf,baseangle))
    return p
outline=[]
tooth=tooth_points()
for j in range(Z):
    theta=2*math.pi*j/Z
    outline.extend(rot(p,theta) for p in tooth)
    # root-circle gap to next tooth; 8 segments, excluding next root start
    end=theta+baseangle; nxt=theta+2*math.pi/Z-baseangle
    outline.extend(polar(rf,end+(nxt-end)*i/8) for i in range(1,8))
assert len(outline)>4000
doc=App.newDocument("PX1_A27_Z50")
poly=[V(x,y,0) for x,y in outline]
wire=Part.makePolygon(poly+[poly[0]])
face=Part.Face(Part.Wire(wire.Edges))
gear=face.extrude(V(0,0,THICKNESS))
hub=Part.makeCylinder(HUB_D/2,HUB_EXTRA,V(0,0,THICKNESS))
solid=gear.fuse(hub).removeSplitter()
bore=Part.makeCylinder(BORE_D/2,THICKNESS+HUB_EXTRA+2,V(0,0,-1))
solid=solid.cut(bore).removeSplitter()
assert solid.isValid() and len(solid.Solids)==1 and solid.Volume>0
obj=doc.addObject("PartDesign::Feature","Z50_Assumed")
obj.Shape=solid
doc.recompute()
doc.saveAs(str(OUT/"px1_a27_z50.FCStd"))
Part.export([obj],str(OUT/"px1_a27_z50.step"))
with (OUT/"assumptions.csv").open("w",newline="",encoding="utf8") as f:
    w=csv.writer(f);w.writerow(["parameter","value_mm","status","verification"])
    for k,v in [("module",MOD),("pitch_diameter",2*rp),("outside_diameter",2*ra),("root_diameter",2*rf),("thickness",THICKNESS),("bore",BORE_D),("hub_diameter",HUB_D),("hub_extra_height",HUB_EXTRA)]:
        w.writerow([k,v,"ASSUMED / design target","Check against drivetrain envelope and selected shaft/catalogue"])
print("PASS FreeCAD solid valid",solid.Volume,"mm3")
