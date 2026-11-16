"""A29 CadQuery 3D Boolean: gear Z50, shaft X150 and motor. All positions ASSUMED."""
import math
import cadquery as cq
from pathlib import Path
P=Path(__file__).resolve().parent
z=50;m=1.5;rp=37.5;rb=rp*math.cos(math.radians(20));ra=39;rf=35.625
tp=math.sqrt((rp/rb)**2-1);base=math.pi/(2*z)+tp-math.atan(tp)
def pol(r,a):return(r*math.cos(a),r*math.sin(a))
def flank(r,s):
 t=math.sqrt(max(0,(r/rb)**2-1));return pol(r,s*(base-t+math.atan(t)))
def rot(p,a):return(p[0]*math.cos(a)-p[1]*math.sin(a),p[0]*math.sin(a)+p[1]*math.cos(a))
p=[pol(rf,-base),pol(rb,-base)]+[flank(rb+(ra-rb)*i/32,-1) for i in range(1,33)]
a0=math.atan2(p[-1][1],p[-1][0]);a1=math.atan2(flank(ra,1)[1],flank(ra,1)[0])
p += [pol(ra,a0+(a1-a0)*i/12) for i in range(1,13)]
p += [flank(rb+(ra-rb)*i/32,1) for i in range(31,-1,-1)]
p.append(pol(rf,base))
outline=[]
for j in range(z):
 a=2*math.pi*j/z;outline.extend(rot(q,a) for q in p)
 outline.extend(pol(rf,a+base+(2*math.pi/z-2*base)*i/8) for i in range(1,8))
gear=cq.Workplane('XY').polyline(outline).close().extrude(8).union(cq.Workplane('XY').workplane(offset=8).circle(12).extrude(4)).cut(cq.Workplane('XY').circle(6).extrude(12)).val()
shaft=cq.Solid.makeCylinder(6,30,cq.Vector(0,0,-9),cq.Vector(0,0,1))
motor=cq.Solid.makeCylinder(12.5,48,cq.Vector(55,-24,4),cq.Vector(0,1,0))
assert gear.isValid() and len(gear.Solids())==1
assert gear.intersect(motor).Volume()<1e-5
assert gear.intersect(shaft).Volume()<1e-5
negative=gear.intersect(motor.translate(cq.Vector(-25,0,0))).Volume()
assert negative>1.0
cq.exporters.export(cq.Compound.makeCompound([gear,shaft,motor]),str(P/'px1_a29_assembly.step'))
print('PASS: 0 mm3 gear/motor, 0 mm3 gear/shaft, negative test',round(negative,3),'mm3; radial envelope gap 3.5 mm')
