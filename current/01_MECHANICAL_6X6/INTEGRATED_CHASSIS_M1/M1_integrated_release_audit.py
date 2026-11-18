#!/usr/bin/env python3
"""PX1 M1 source-derived audit; stdlib only. Run next to the existing FreeCAD generator."""
import ast,json,math,pathlib
root=pathlib.Path(__file__).resolve().parent
src=root/'PX1_Integrated_6x6_M1_interface_repair.py'
tree=ast.parse(src.read_text(encoding='utf8'))
p=next({k.arg:ast.literal_eval(k.value) for k in n.value.keywords} for n in tree.body if isinstance(n,ast.Assign) and any(isinstance(t,ast.Name) and t.id=='P' for t in n.targets))
checks=[]
def test(name,ok,detail):checks.append(dict(name=name,status='PASS' if ok else 'FAIL',detail=detail))
test('six wheels',tuple(p['stations'])==(-110,0,110),'three stations per side')
test('ten Z50',tuple(p['gear_x'])==(-110,-55,0,55,110),'five stations per side')
test('Z50 pitch',all(abs(p['gear_x'][i+1]-p['gear_x'][i]-50*p['gear_m'])<1e-6 for i in range(4)),'pitch circles only')
test('DN150 conservative wheel envelope',math.hypot(43+p['wheel_W'],p['wheel_D']/2)<=75,'rectangular corner bound')
test('motor/Z50 Y clearance',p['gear_y']-p['gear_thick']/2-(p['motor_y']+p['motor_D']/2)>=2,'envelopes only')
test('motor pair Y clearance',2*p['motor_y']-p['motor_D']>=2,'envelopes only')
test('gear pitch/bottom',p['gear_z']-25*p['gear_m']>=-p['body_H']/2+p['wall']+1,'pitch circle, not addendum')
for name,detail in [
 ('pressure-rated dynamic shaft seals','No modeled shaft seal grooves or rated seal parts'),
 ('real Z16/Z40 bevel mesh','Cylindrical proxies, no bevel teeth/contact'),
 ('Z40/Z50 torque coupling','Independent hub proxy; no keyed/splined joint validation'),
 ('idler bearing support','Idler stubs have no bearings')]:
 test(name,False,detail)
checks.extend([dict(name='FreeCAD/STEP/Boolean',status='NOT_RUN',detail='Requires FreeCADCmd'),dict(name='pressure 0.4–0.7 bar',status='PHYSICAL_CHECK',detail='Qualified seals and safe pressure test'),dict(name='motor Ø22×42',status='PHYSICAL_CHECK',detail='Unverified design envelope')])
s=2.15;X=lambda x:400+x*s;Y=lambda y:220-y*s
v=['<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 820 520">','<rect width="820" height="520" fill="#f7fafc"/>','<text x="25" y="34" font-family="sans-serif" font-size="20">PX1 M1 | Source-derived top view (XY)</text>','<text x="25" y="56" font-family="sans-serif" font-size="12">ASSUMED geometry. NOT a FreeCAD render. Orange circles are pitch proxies, not teeth.</text>']
v.append(f'<rect x="{X(-p["body_L"]/2):.1f}" y="{Y(p["body_W"]/2):.1f}" width="{p["body_L"]*s:.1f}" height="{p["body_W"]*s:.1f}" fill="#d7e4ed" stroke="#526d7f" stroke-width="2"/>')
for sign in (-1,1):
 for x in p['stations']:
  v.append(f'<rect x="{X(x-p["wheel_D"]/2):.1f}" y="{Y(sign*52+p["wheel_W"]/2):.1f}" width="{p["wheel_D"]*s:.1f}" height="{p["wheel_W"]*s:.1f}" fill="#343f49" opacity=".85" rx="5"/>')
 for x in p['gear_x']:
  v.append(f'<circle cx="{X(x):.1f}" cy="{Y(sign*p["gear_y"]):.1f}" r="{25*p["gear_m"]*s:.1f}" fill="none" stroke="#bd742e" stroke-width="2" stroke-dasharray="5 4"/>')
 v.append(f'<rect x="{X(35):.1f}" y="{Y(sign*p["motor_y"]+p["motor_D"]/2):.1f}" width="{p["motor_L"]*s:.1f}" height="{p["motor_D"]*s:.1f}" rx="9" fill="#4b88ad"/>')
v.extend(['<text x="25" y="460" font-family="sans-serif" font-size="13">Grey: body | Black: wheels | Orange: Z50 pitch | Blue: motors</text>','<text x="25" y="482" font-family="sans-serif" font-size="12" fill="#a32626">FAIL: shaft seals, bevel mesh, torque joint, idler bearings not validated</text>','<text x="25" y="502" font-family="sans-serif" font-size="11">Plan-view overlaps are projections; no manufacturing approval.</text>','</svg>'])
(root/'M1_integrated_release_audit.svg').write_text('\n'.join(v),encoding='utf8')
(root/'M1_integrated_release_audit.json').write_text(json.dumps({'source':src.name,'parameters':p,'checks':checks},indent=2),encoding='utf8')
print({k:sum(c['status']==k for c in checks) for k in ('PASS','FAIL','NOT_RUN','PHYSICAL_CHECK')})
