"""PX1 A28: CadQuery STEP/STL real involute polygon solid; ESTIMATED design, not production qualified."""
import math,cadquery as cq
from pathlib import Path
P=Path(__file__).resolve().parent
z=50;m=1.5;alpha=math.radians(20);rp=m*z/2;rb=rp*math.cos(alpha);ra=rp+m;rf=rp-1.25*m
half=math.pi/(2*z);tp=math.sqrt((rp/rb)**2-1);baseangle=half+tp-math.atan(tp)
def polar(r,a):return(r*math.cos(a),r*math.sin(a))
def flank(r,side):
 t=math.sqrt(max(0,(r/rb)**2-1));return polar(r,side*(baseangle-(t-math.atan(t))))
def rot(p,a):return(p[0]*math.cos(a)-p[1]*math.sin(a),p[0]*math.sin(a)+p[1]*math.cos(a))
p=[polar(rf,-baseangle),polar(rb,-baseangle)]
p += [flank(rb+(ra-rb)*i/32,-1) for i in range(1,33)]
a0=math.atan2(p[-1][1],p[-1][0]);a1=math.atan2(flank(ra,1)[1],flank(ra,1)[0])
p += [polar(ra,a0+(a1-a0)*i/12) for i in range(1,13)]
p += [flank(rb+(ra-rb)*i/32,1) for i in range(31,-1,-1)]
p.append(polar(rf,baseangle))
outline=[]
for j in range(z):
 a=2*math.pi*j/z;outline.extend(rot(q,a) for q in p)
 outline.extend(polar(rf,a+baseangle+(2*math.pi/z-2*baseangle)*i/8) for i in range(1,8))
gear=cq.Workplane('XY').polyline(outline).close().extrude(8)
hub=cq.Workplane('XY').workplane(offset=8).circle(12).extrude(4)
solid=gear.union(hub).cut(cq.Workplane('XY').circle(6).extrude(12))
shape=solid.val()
assert shape.isValid() and len(shape.Solids())==1
assert abs(shape.Volume()-35563.3982)<1.0
cq.exporters.export(solid,str(P/'px1_a28_z50.step'))
cq.exporters.export(solid,str(P/'px1_a28_z50.stl'))
scale=5.8;cx=260;cy=260
path=' '.join(('M' if i==0 else 'L')+f'{cx+x*scale:.3f},{cy-y*scale:.3f}' for i,(x,y) in enumerate(outline))+' Z'
svg=f'<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 840 540"><rect width="840" height="540" fill="white"/><text x="20" y="30" font-size="22">PX1 A28 — Z50 solid / exact top projection</text><text x="20" y="52" font-size="13">CadQuery solid: involute polygon extruded 8 mm + hub 4 mm; Ø12 bore</text><path d="{path}" fill="#b5d5e5" stroke="#24526b" stroke-width=".7"/><circle cx="{cx}" cy="{cy}" r="{12*scale}" fill="#91b6c9" stroke="#24526b"/><circle cx="{cx}" cy="{cy}" r="{6*scale}" fill="white" stroke="#24526b"/><text x="520" y="140" font-size="16">Z50 m1.5 / tip Ø78</text><text x="520" y="180" font-size="16">Hub Ø24 x 4 / bore Ø12</text><text x="520" y="220" font-size="16">ASSUMED / not production</text></svg>'
(P/'px1_a28_preview.svg').write_text(svg,encoding='utf8')
print('PASS: CadQuery valid single solid',len(outline),'outline vertices',shape.Volume(),'mm3')
