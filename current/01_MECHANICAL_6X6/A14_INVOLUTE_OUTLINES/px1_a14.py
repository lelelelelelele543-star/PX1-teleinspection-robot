#!/usr/bin/env python3
"""PX1 A14: reproducible involute outline SVG. Root transitions approximate; NOT machining-ready."""
import math,pathlib
P=pathlib.Path(__file__).resolve().parent
M=1.5; ALPHA=math.radians(20); CENTER=42; PAIR=[(16,.20),(40,-.20)]
def inv(r,rb):
    a=math.acos(rb/r)
    return math.tan(a)-a
def gear(z,x):
    rp=M*z/2; rb=rp*math.cos(ALPHA); ra=M*(z/2+1+x); rf=M*(z/2-1.25+x)
    half=M*(math.pi/2+2*x*math.tan(ALPHA))/(2*rp)
    start=max(rb,rf); pts=[]
    def angle(r,side): return side*(half+inv(rp,rb)-inv(r,rb))
    for j in range(z):
        t=2*math.pi*j/z
        seq=[(rf,-1),(start,-1)]+[(start+(ra-start)*k/12,-1) for k in range(13)]
        for r,side in seq:
            a=t+angle(max(r,start),side);pts.append((r*math.cos(a),r*math.sin(a)))
        for k in range(1,7):
            a=t+angle(ra,-1)+(angle(ra,1)-angle(ra,-1))*k/6
            pts.append((ra*math.cos(a),ra*math.sin(a)))
        for k in range(12,-1,-1):
            r=start+(ra-start)*k/12;a=t+angle(r,1);pts.append((r*math.cos(a),r*math.sin(a)))
        a=t+angle(start,1);pts.append((rf*math.cos(a),rf*math.sin(a)))
    return pts,dict(z=z,x=x,rp=rp,rb=rb,ra=ra,rf=rf)
def main():
    (p1,g1),(p2,g2)=[gear(z,x) for z,x in PAIR]
    assert len(p1)==560 and len(p2)==1400
    assert abs(g1['rp']+g2['rp']-CENTER)<1e-9
    eps=(math.sqrt(g1['ra']**2-g1['rb']**2)+math.sqrt(g2['ra']**2-g2['rb']**2)-CENTER*math.sin(ALPHA))/(math.pi*M*math.cos(ALPHA))
    assert 1.57<eps<1.58
    scale=8.1;cx1=260;cy=265;cx2=cx1+CENTER*scale
    def shape(points,cx):
        return 'M '+' L '.join(f'{cx+scale*x:.2f},{cy-scale*y:.2f}' for x,y in points)+' Z'
    svg=f"""<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 980 560" width="980" height="560"><rect width="980" height="560" fill="#f7fafc"/><text x="35" y="38" font-family="sans-serif" font-size="23">PX1 A14 — involute profiles Z16 / Z40</text><text x="35" y="63" font-family="sans-serif" font-size="14">DESIGN ONLY: root transitions approximate; mesh phase/contact unverified</text><path d="{shape(p1,cx1)}" fill="#b7d7f3" stroke="#1d5c91"/><path d="{shape(p2,cx2)}" fill="#e2c5a7" stroke="#98632b"/><circle cx="{cx1}" cy="{cy}" r="{g1['rp']*scale}" fill="none" stroke="#1d5c91" stroke-dasharray="5 5"/><circle cx="{cx2}" cy="{cy}" r="{g2['rp']*scale}" fill="none" stroke="#98632b" stroke-dasharray="5 5"/><line x1="{cx1}" y1="{cy}" x2="{cx2}" y2="{cy}" stroke="#dc3545" stroke-dasharray="5 4"/><text x="110" y="490" font-family="sans-serif" font-size="17">Z16 x=+0.20</text><text x="585" y="490" font-family="sans-serif" font-size="17">Z40 x=-0.20</text><text x="110" y="520" font-family="sans-serif" font-size="15">m=1.5 mm | a=42 mm | alpha=20 deg | analytical epsilon={eps:.4f}</text></svg>"""
    (P/'px1_a14_preview.svg').write_text(svg,encoding='utf8')
    print(f'PASS: {len(p1)}/{len(p2)} vertices; a={CENTER}; analytical epsilon={eps:.5f}')
    print('SKIPPED: contact simulation, hob-generated trochoids, 3D, STEP, physical testing')
if __name__=='__main__':main()
