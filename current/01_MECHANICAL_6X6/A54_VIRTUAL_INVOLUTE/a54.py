"""PX1 A54: planar virtual-spur involute sections; NOT conjugate bevel teeth."""
import math,json
from pathlib import Path
P=Path(__file__).resolve().parent
m,zs,b,alpha=1.5,(16,40),8.0,math.radians(20)
R=m*math.hypot(*zs)/2
assert 0<b<=R/3
gears=[]
for z,other in ((16,40),(40,16)):
 d=math.atan2(z,other); zv=z/math.cos(d)**3
 rp=m*zv/2; rb=rp*math.cos(alpha); ra=rp+m
 def invol(t):return math.tan(t)-t
 def ang(r):
  t=math.sqrt(max(0,(r/rb)**2-1))
  return math.pi/(2*zv)+invol(alpha)-(t-math.atan(t))
 points=[(rb+(ra-rb)*i/44,ang(rb+(ra-rb)*i/44)) for i in range(45)]
 gears.append(dict(z=z,delta_deg=math.degrees(d),virtual_teeth=zv,virtual_pitch_radius=rp,virtual_base_radius=rb,virtual_addendum_radius=ra,outer_pitch_radius=m*z/2,inner_pitch_radius=(R-b)*math.sin(d),points=points))
assert abs(sum(g['delta_deg'] for g in gears)-90)<1e-9
assert all(g['virtual_base_radius']<g['virtual_pitch_radius']<g['virtual_addendum_radius'] for g in gears)
limit=2/math.sin(alpha)**2
result=dict(status='PASS_ANALYTIC_ONLY',module_assumed_mm=m,pressure_angle_assumed_deg=20,face_width_assumed_mm=b,cone_distance_mm=R,undercut_virtual_threshold=limit,gears=[{k:v for k,v in g.items() if k!='points'} for g in gears],warning='Virtual planar tooth sections only; NOT real bevel tooth surfaces or contact validation')
(P/'a54_result.json').write_text(json.dumps(result,indent=2)+'\n')
svg=['<svg xmlns="http://www.w3.org/2000/svg" width="1100" height="650" viewBox="0 0 1100 650">','<rect width="1100" height="650" fill="#f8fafc"/>','<text x="30" y="42" font-size="25">PX1 A54 — virtual involute tooth sections</text>','<text x="30" y="70" font-size="15">ASSUMED m=1.5 mm, alpha=20 deg, b=8 mm. NOT real bevel teeth.</text>']
for j,g in enumerate(gears):
 cx,cy,s=280+540*j,350,5 if j==0 else 2.3
 for k,c in [('virtual_base_radius','#64748b'),('virtual_pitch_radius','#0f766e'),('virtual_addendum_radius','#c2410c')]:
  svg.append(f'<circle cx="{cx}" cy="{cy}" r="{s*g[k]:.3f}" fill="none" stroke="{c}" stroke-dasharray="5 5"/>')
 for sign in (-1,1):
  pts=' '.join(f'{cx+s*r*math.cos(math.pi/2+sign*a):.2f},{cy-s*r*math.sin(math.pi/2+sign*a):.2f}' for r,a in g['points'])
  svg.append(f'<polyline points="{pts}" fill="none" stroke="#1d4ed8" stroke-width="3"/>')
 svg.append(f'<text x="{cx-185}" y="565" font-size="18">Z{g["z"]}: zv={g["virtual_teeth"]:.2f}, delta={g["delta_deg"]:.2f} deg</text>')
svg.append('<text x="30" y="625" font-size="15" fill="#9a3412">Planar virtual spur approximation ONLY. No bevel mesh, no contact, no manufacturing release.</text></svg>')
(P/'a54_preview.svg').write_text('\n'.join(svg))
print(json.dumps(result,indent=2))
