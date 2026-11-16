"""PX1 A26: analytical involute Z50; assumed module 1.5 mm, alpha 20 degrees, zero shift. Not a production gear."""
import math,csv
from pathlib import Path
P=Path(__file__).resolve().parent
z=50;m=1.5;alpha=math.radians(20)
rp=m*z/2;rb=rp*math.cos(alpha);ra=rp+m;rf=rp-1.25*m
half=math.pi/(2*z)
def involute(t):return t-math.atan(t)
tp=math.sqrt((rp/rb)**2-1)
def flank(r,side):
 t=math.sqrt(max(0,(r/rb)**2-1))
 a=side*(half+involute(tp)-involute(t))
 return (r*math.cos(a),r*math.sin(a))
def rotate(p,a):
 return (p[0]*math.cos(a)-p[1]*math.sin(a),p[0]*math.sin(a)+p[1]*math.cos(a))
baseangle=half+involute(tp)
tooth=[(rf*math.cos(baseangle),-rf*math.sin(baseangle))]
for i in range(41):tooth.append(flank(rb+(ra-rb)*i/40,-1))
for i in range(1,13):
 a0=math.atan2(tooth[-1][1],tooth[-1][0]);a1=math.atan2(flank(ra,1)[1],flank(ra,1)[0]);a=a0+(a1-a0)*i/12
 tooth.append((ra*math.cos(a),ra*math.sin(a)))
for i in range(39,-1,-1):tooth.append(flank(rb+(ra-rb)*i/40,1))
tooth.append((rf*math.cos(baseangle),rf*math.sin(baseangle)))
outline=[rotate(p,2*math.pi*j/z) for j in range(z) for p in tooth]
assert len(outline)==4750
assert abs(2*ra-78)<1e-10 and abs(2*rf-71.25)<1e-10
assert abs(math.atan2(flank(rp,1)[1],flank(rp,1)[0])-math.atan2(flank(rp,-1)[1],flank(rp,-1)[0])-math.pi/z)<1e-10
with (P/'outline.csv').open('w',newline='') as f:
 w=csv.writer(f);w.writerow(['x_mm','y_mm']);w.writerows((f'{x:.8f}',f'{y:.8f}') for x,y in outline)
S=5.2;CX=260;CY=255
path=' '.join(('M' if i==0 else 'L')+f'{CX+x*S:.3f},{CY-y*S:.3f}' for i,(x,y) in enumerate(outline))+' Z'
svg=f'<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 800 530"><rect width="800" height="530" fill="white"/><text x="24" y="32" font-size="21">PX1 A26 — involute Z50 / assumed geometry</text><text x="24" y="57" font-size="13">m=1.5 mm; alpha=20 deg; z=50. No root fillets, bore or hub.</text><path d="{path}" fill="#c6ddeb" stroke="#174966" stroke-width="1"/><circle cx="{CX}" cy="{CY}" r="{rp*S}" fill="none" stroke="#d07826" stroke-dasharray="5 4"/><circle cx="{CX}" cy="{CY}" r="{rb*S}" fill="none" stroke="#7a4e99" stroke-dasharray="2 5"/><g font-size="16"><text x="510" y="140">Pitch diameter 75 mm</text><text x="510" y="170">Base diameter {2*rb:.3f} mm</text><text x="510" y="200">Tip diameter 78 mm</text><text x="510" y="230">Root diameter 71.25 mm</text><text x="510" y="350">Analytical 2D outline</text><text x="510" y="374">NOT a FreeCAD solid</text><text x="24" y="505" font-size="13">A25 used pitch diameter 75 mm, not actual tip diameter 78 mm.</text></g></svg>'
(P/'px1_a26_preview.svg').write_text(svg,encoding='utf8')
print('PASS: 50 teeth, 4750 points, pitch thickness and diameters; SKIPPED: CAD boolean, fillet, manufacturing')
