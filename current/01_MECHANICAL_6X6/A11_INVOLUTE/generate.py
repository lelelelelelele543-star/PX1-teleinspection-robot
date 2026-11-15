"""PX1 A11: analytical 2D involute teeth; not manufacturing geometry."""
import math
from pathlib import Path
M=1.5; A=math.radians(20); S=5.4
def gear(z,cx,cy,phase):
    rp=M*z/2; rb=rp*math.cos(A); ra=rp+M; rf=rp-1.25*M
    inv=lambda a: math.tan(a)-a
    def half(r):
        t=math.acos(min(1,rb/r))
        return math.pi/(2*z)+inv(A)-inv(t)
    p=[]
    for k in range(z):
        c=phase+2*math.pi*k/z
        def add(r,t): p.append((cx+S*r*math.cos(t),cy-S*r*math.sin(t)))
        add(rf,c-half(rb))
        for j in range(13):
            r=rb+(ra-rb)*j/12;add(r,c-half(r))
        for j in range(1,6): add(ra,c-half(ra)+2*half(ra)*j/5)
        for j in range(12,-1,-1):
            r=rb+(ra-rb)*j/12;add(r,c+half(r))
        add(rf,c+half(rb))
        end=c+2*math.pi/z-half(rb)
        for j in range(1,7):add(rf,c+half(rb)+(end-c-half(rb))*j/6)
    return 'M '+' L '.join(f'{x:.3f},{y:.3f}' for x,y in p)+' Z',rp,len(p)
g1,r1,n1=gear(16,210,265,0)
g2,r2,n2=gear(40,210+42*S,265,math.pi/40)
assert abs(r1+r2-42)<1e-9 and n1==624 and n2==1560
svg=f'''<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 720 540">
<rect width="720" height="540" fill="white"/>
<text x="25" y="35" font-family="sans-serif" font-size="19">PX1 A11 | involute Z16 / Z40</text>
<text x="25" y="56" font-family="sans-serif" font-size="12">ASSUMED m1.5, alpha20, zero shift, centers 42 mm</text>
<path d="{g1}" fill="#dceafa" stroke="#175a91" stroke-width="1"/>
<path d="{g2}" fill="#e5f3e7" stroke="#217a48" stroke-width="1"/>
<circle cx="210" cy="265" r="{r1*S}" fill="none" stroke="#2563eb" stroke-dasharray="5 4"/>
<circle cx="{210+42*S}" cy="265" r="{r2*S}" fill="none" stroke="#16803c" stroke-dasharray="5 4"/>
<text x="25" y="485" font-family="sans-serif" font-size="13">Pitch radii 12/30 mm; outside radii 13.5/31.5 mm</text>
<text x="25" y="510" font-family="sans-serif" font-size="12" fill="#a33">2D outlines ONLY: mesh phase, undercut, fillets, backlash and strength unverified</text>
</svg>'''
Path(__file__).with_name('px1_a11_involute_preview.svg').write_text(svg)
print('PASS: pitch centers and sampled tooth contours')
