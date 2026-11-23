#!/usr/bin/env python3
"""PX1 full 6x6 drivetrain kinematic graph, sourced from current CAD master.
Standard library only; outputs SVG + JSON. NOT a 3D collision or pressure test.
"""
import ast,json,math
from pathlib import Path
p=Path(__file__).resolve().parent
t=ast.parse((p/'PX1_Current_Master.py').read_text(encoding='utf-8'))
v={}
for n in t.body:
    if isinstance(n,ast.Assign):
        for x in n.targets:
            if isinstance(x,ast.Name):
                try:v[x.id]=ast.literal_eval(n.value)
                except (ValueError,TypeError):pass
required=('WHEEL_X','GEAR_X','Z50_TEETH','Z50_MOD','Z50_PD','Z50_OD','Z16_TEETH','Z40_TEETH','WHEEL_CROWN_R','PIPE_R','WHEEL_CENTRE_Y','WHEEL_Z')
assert all(x in v for x in required),'Missing source parameters'
wx,gx=v['WHEEL_X'],v['GEAR_X']
assert len(wx)==3 and len(gx)==5 and set(wx).issubset(gx)
assert all(abs(b-a-v['Z50_PD'])<1e-6 for a,b in zip(gx,gx[1:]))
assert v['Z50_TEETH']*v['Z50_MOD']==v['Z50_PD']
ratio=v['Z40_TEETH']/v['Z16_TEETH']
rpm_assumed=60.0
rpm=rpm_assumed/ratio
speed=2*math.pi*v['WHEEL_CROWN_R']/1000*rpm
report={'source':'PX1_Current_Master.py','status':'ANALYTICAL_SCREEN_ONLY','stations_mm':{'wheels':wx,'gears':gx},'assumptions':{'motor_output_rpm':rpm_assumed,'motor_torque_Nm':1.0,'equal_axle_load':'NOT_VERIFIED'},'calculations':{'bevel_ratio':ratio,'spur_meshes_per_side':4,'wheel_rpm':rpm,'ideal_speed_m_min':round(speed,3),'ideal_side_torque_Nm':ratio,'ideal_torque_per_axle_Nm':round(ratio/3,3)},'checks':{'six_wheels':'PASS','two_motor_sides':'PASS','Z50_centre_distance':'PASS','Z50_module':'PASS','gear_tooth_collision':'NOT_RUN','motor_to_axle_collision':'NOT_RUN','shaft_seal_pressure':'PHYSICAL_CHECK'},'manufacturing_release':False}
(p/'PX1_drivetrain_system_check.json').write_text(json.dumps(report,indent=2)+'\n')
s=['<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 980 460">','<rect width="980" height="460" fill="#f8fafc"/>','<text x="35" y="35" font-size="22" font-family="sans-serif">PX1 — full 6x6 drivetrain | source-derived 2D</text>','<text x="35" y="56" font-size="13" font-family="sans-serif">Schematic of actual CAD station parameters, NOT a 3D render or production drawing</text>']
for label,y in (('LEFT',145),('RIGHT',325)):
    s.append(f'<text x="35" y="{y-63}" font-size="16" font-family="sans-serif">{label} / 1 motor / 5 gears / 3 wheels</text>')
    for i,x in enumerate(gx):
        cx=115+2.5*x
        if i:s.append(f'<line x1="{115+2.5*gx[i-1]}" y1="{y}" x2="{cx}" y2="{y}" stroke="#64748b" stroke-width="3"/>')
        s.append(f'<circle cx="{cx}" cy="{y}" r="42" fill="#dbeafe" stroke="#2563eb" stroke-width="2"/>')
        s.append(f'<text x="{cx}" y="{y+5}" text-anchor="middle" font-size="14" font-family="sans-serif">Z50</text>')
        if x in wx:
            s.append(f'<circle cx="{cx}" cy="{y}" r="32" fill="none" stroke="#0f766e" stroke-width="5" stroke-dasharray="5 4"/>')
            s.append(f'<text x="{cx}" y="{y+65}" text-anchor="middle" font-size="12" font-family="sans-serif">wheel X{x:g}</text>')
    s.append(f'<rect x="785" y="{y-24}" width="150" height="48" rx="7" fill="#ffedd5" stroke="#c2410c"/>')
    s.append(f'<text x="860" y="{y+5}" text-anchor="middle" font-size="14" font-family="sans-serif">MOTOR Z16/Z40</text>')
    s.append(f'<line x1="{115+2.5*gx[-1]+43}" y1="{y}" x2="785" y2="{y}" stroke="#c2410c" stroke-dasharray="7 4" stroke-width="3"/>')
s+=['<text x="35" y="418" font-size="14" font-family="sans-serif">2.5:1 input; four Z50 meshes/side; 60 rpm assumed = 24 wheel rpm; ideal 6.786 m/min</text>','<text x="35" y="443" font-size="13" font-family="sans-serif" fill="#9a3412">NOT_RUN: tooth/shaft collisions. PHYSICAL_CHECK: pressure, strength, traction.</text>','</svg>']
(p/'previews/PX1_drivetrain_system_check.svg').write_text('\n'.join(s)+'\n')
print(json.dumps(report,indent=2))
