"""Source-bound drivetrain drawing: read constants from actual master without CadQuery."""
import ast
from pathlib import Path
from xml.sax.saxutils import escape
here=Path(__file__).resolve().parent
tree=ast.parse((here/'PX1_Current_Master.py').read_text(encoding='utf-8'))
wanted={'WHEEL_X','GEAR_X','WHEEL_Z','BODY_L_SOURCE_SCREEN','BODY_HALF_W_SCREEN','BODY_Z0','BODY_TOP','WHEEL_CENTRE_Y','WHEEL_CROWN_R','MOTOR_FACE','MOTOR_LEN','MOTOR_OD','MOTOR_Y','Z50_PD','Z50_TEETH','Z50_MOD'}
v={}
for node in tree.body:
    if isinstance(node,ast.Assign):
        for target in node.targets:
            if isinstance(target,ast.Name) and target.id in wanted:
                try:v[target.id]=ast.literal_eval(node.value)
                except (TypeError,ValueError):pass
assert wanted<=v.keys(),f"Missing master datums: {wanted-v.keys()}"
assert len(v['WHEEL_X'])==3 and len(v['GEAR_X'])==5
assert v['Z50_PD']==v['Z50_TEETH']*v['Z50_MOD']
X=lambda a:110+a*2
Y=lambda a:210+a*2
Z=lambda a:540-a*2
s=['<svg xmlns="http://www.w3.org/2000/svg" width="1050" height="670" viewBox="0 0 1050 670">','<rect width="1050" height="670" fill="#101b29"/>','<g font-family="Arial" fill="#d9e7f2">','<text x="45" y="43" font-size="24">PX1 · CURRENT MASTER · SOURCE-BOUND 2D</text>','<text x="45" y="69" font-size="14">Top and side drivetrain datums extracted from PX1_Current_Master.py — NOT a 3D CAD render</text>','<text x="45" y="106" font-size="18">TOP · X/Y</text>']
s.append(f'<rect x="{X(18)}" y="{Y(-34)}" width="{278*2}" height="{68*2}" rx="8" fill="#2c4655" stroke="#9fc4d8"/>')
for sign in (-1,1):
    for gx in v['GEAR_X']:
        s.append(f'<circle cx="{X(gx)}" cy="{Y(sign*39)}" r="{v["Z50_PD"]}" stroke="#e5b35c" fill="#e5b35c" fill-opacity=".14"/>')
    for wx in v['WHEEL_X']:
        s.append(f'<rect x="{X(wx)-24}" y="{Y(sign*54.5)-24}" width="48" height="48" rx="7" fill="#677786" stroke="#c3d4e0"/>')
    s.append(f'<rect x="{X(v["MOTOR_FACE"]-v["MOTOR_LEN"])}" y="{Y(sign*v["MOTOR_Y"])-v["MOTOR_OD"]}" width="{v["MOTOR_LEN"]*2}" height="{v["MOTOR_OD"]*2}" rx="12" fill="#247e7e" stroke="#76d6ce"/>')
s.extend(['<text x="735" y="160" font-size="15">Gold: 10 × Z50 stations</text>','<text x="735" y="186" font-size="15">Grey: 6 wheel stations</text>','<text x="735" y="212" font-size="15">Teal: 2 motor envelopes</text>','<text x="45" y="368" font-size="18">SIDE · X/Z</text>'])
s.append(f'<rect x="{X(18)}" y="{Z(v["BODY_TOP"])}" width="556" height="{(v["BODY_TOP"]-v["BODY_Z0"])*2}" rx="8" fill="#2c4655" stroke="#9fc4d8"/>')
for wx in v['WHEEL_X']:
    s.append(f'<circle cx="{X(wx)}" cy="{Z(v["WHEEL_Z"])}" r="{v["WHEEL_CROWN_R"]*2}" fill="#4f5d6b" stroke="#c2d1db" stroke-width="2"/>')
    s.append(f'<circle cx="{X(wx)}" cy="{Z(v["WHEEL_Z"])}" r="44" fill="#8799a5" stroke="#d8e4ec"/>')
    s.append(f'<text x="{X(wx)}" y="638" text-anchor="middle" font-size="14">X{wx:g}</text>')
s.extend(['<text x="45" y="662" font-size="12">Engineering datum view only; covers, tooth involutes, shafts, bearings, seals and lift are not depicted.</text>','</g></svg>'])
out=here/'previews'/'px1_master_drivetrain_source_bound.svg';out.parent.mkdir(exist_ok=True)
out.write_text('\n'.join(s),encoding='utf-8')
print('PASS',out)
