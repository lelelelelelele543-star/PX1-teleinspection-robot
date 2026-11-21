#!/usr/bin/env python3
"""PX1 integrated tether supply / drivetrain start sequencing design screen.
Pure Python, no hardware authorization. Run: python PX1_drive_power_envelope.py
Uses approved 40m / 6-core / 24V architecture. All currents are ASSUMED.
"""
import math, json
from pathlib import Path
L=40.0; AREA=1.5; RHO=0.0175; ALPHA=0.00393
SUPPLY=24.0; MIN_V=20.0; AUX_A=0.8
MOTOR_RUN_A=2.0; MOTOR_START_A=4.0
def resistance(temp_c):
    return 2*L*RHO/AREA*(1+ALPHA*(temp_c-20))
def voltage(current_a,temp_c):
    return SUPPLY-current_a*resistance(temp_c)
def scenario(name,left_a,right_a,temp_c):
    total=AUX_A+left_a+right_a
    v=voltage(total,temp_c)
    return dict(name=name,temp_C=temp_c,left_A=left_a,right_A=right_a,
                total_A=round(total,3),robot_V=round(v,3),
                loss_W=round(total*total*resistance(temp_c),3),
                voltage_status="PASS" if v>=MIN_V else "FAIL")
cases=[]
for temp in (20,60):
    for name,l,r in (("idle",0,0),("one_motor_running",2,0),
                     ("both_running",2,2),("one_start_one_run",4,2),
                     ("both_start",4,4)):
        cases.append(scenario(name,l,r,temp))
limits={str(t):round((SUPPLY-MIN_V)/resistance(t),3) for t in (20,60)}
# Sequencing does not solve steady-state undervoltage: separate hard FAIL.
assert math.isclose(resistance(20),0.9333333333333333)
assert next(c for c in cases if c["name"]=="both_running" and c["temp_C"]==60)["voltage_status"]=="FAIL"
assert next(c for c in cases if c["name"]=="one_motor_running" and c["temp_C"]==60)["voltage_status"]=="PASS"
assert limits["60"]<limits["20"]
report={"model":"DESIGN_ASSUMPTIONS_ONLY","release":False,
"architecture":{"tether_m":40,"cores":6,"power_cores":2,"rs485_cores":2,
"balanced_cvbs_cores":2,"coax":False,"twisted_pair":False,
"source_V":SUPPLY,"minimum_robot_V_assumed":MIN_V},
"assumptions":{"copper_mm2":AREA,"auxiliary_A":AUX_A,
"motor_running_A_each":MOTOR_RUN_A,"motor_start_A_each":MOTOR_START_A,
"motor_values_are_not_datasheet_ratings":True},
"max_total_current_A":limits,"cases":cases,
"checks":{"model_math":"PASS","both_motors_steady_60C":"FAIL",
"motor_start_60C":"FAIL","driver_peak_limit":"NOT_RUN",
"motor_datasheet":"NOT_RUN","CVBS_RS485_interference":"NOT_RUN",
"cable_temperature":"PHYSICAL_CHECK","pressure_feedthrough":"PHYSICAL_CHECK"},
"engineering_decision":"Do not treat sequential start as solution to 4.8A steady draw. Keep 24V architecture provisionally; choose measured motors/load, thicker power cores if physically possible, or validated remote DC-DC power architecture. BTS7960 requires independent current protection and undervoltage logic."}
p=Path(__file__).resolve().parent
(p/"PX1_drive_power_envelope.json").write_text(json.dumps(report,ensure_ascii=False,indent=2)+"\n")
W=1100; H=650
s=[f'<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 {W} {H}">',
'<rect width="1100" height="650" fill="#fff"/>',
'<text x="38" y="45" font-family="sans-serif" font-size="26">PX1 6-core tether / integrated drive power envelope</text>',
'<text x="38" y="72" font-family="sans-serif" font-size="15">40m, 1.5 mm², 24V / calculated 2D; currents ASSUMED, not measured</text>',
'<line x1="80" y1="145" x2="1020" y2="145" stroke="#111827" stroke-width="2"/>',
'<text x="40" y="123" font-family="sans-serif" font-size="16">Robot voltage (V) — 60°C cable</text>']
vals=[c for c in cases if c["temp_C"]==60]
for i,c in enumerate(vals):
    x=70+i*208; y=520-(c["robot_V"]-10)*24
    s.extend([f'<rect x="{x}" y="{y:.1f}" width="125" height="{520-y:.1f}" fill="{("#0f766e" if c["voltage_status"]=="PASS" else "#b91c1c")}"/>',
    f'<text x="{x}" y="{y-10:.1f}" font-family="sans-serif" font-size="19">{c["robot_V"]:.2f} V</text>',
    f'<text x="{x}" y="547" font-family="sans-serif" font-size="13">{c["name"].replace("_"," ")}</text>',
    f'<text x="{x}" y="567" font-family="sans-serif" font-size="13">{c["total_A"]} A total</text>'])
threshold_y=520-(20-10)*24
s.extend([f'<line x1="40" y1="{threshold_y}" x2="1050" y2="{threshold_y}" stroke="#b91c1c" stroke-dasharray="8 6" stroke-width="2"/>',
f'<text x="880" y="{threshold_y-8}" font-family="sans-serif" font-size="16">20 V assumed threshold</text>',
'<text x="38" y="615" font-family="sans-serif" font-size="15">FAIL at both motors steady: staged startup alone is insufficient. Physical validation required.</text>',
'</svg>'])
(p/"previews").mkdir(exist_ok=True)
(p/"previews/PX1_drive_power_envelope.svg").write_text("\n".join(s)+"\n")
print(json.dumps(report["checks"],ensure_ascii=False))
