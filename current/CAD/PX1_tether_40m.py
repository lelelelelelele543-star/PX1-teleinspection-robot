#!/usr/bin/env python3
"""PX1 40 m six-core copper tether: parametric power, signal and video screening.
All cable dimensions and electrical performance are design assumptions, not measured.
"""
from pathlib import Path
import json,math
p=Path(__file__).resolve().parent
L=40.0
A=1.5 # assumed mm2 per conductor
RHO=0.0175 # copper nominal ohm mm2/m at 20 C
I=2.0 # assumed operating current, not motor stall current
r=2*L*RHO/A
alloc=["DC +24V","DC return","RS485 A","RS485 B","CVBS balanced +","CVBS balanced -"]
assert len(alloc)==6 and math.isclose(r,0.9333333333333333)
report={"source":"PX1_tether_40m.py","release":False,
"design_assumptions":{"length_m":L,"copper_cores":6,"area_mm2_per_core":A,"current_A":I,
"rho_ohm_mm2_per_m":RHO,"kevlar":"required, geometry unverified",
"no_coax":True,"no_twisted_pair":True},
"wiring":dict(enumerate(alloc,1)),
"calculations":{"dc_loop_ohm":round(r,4),"dc_drop_V":round(I*r,4),
"cable_heat_W":round(I*I*r,4),"24V_received_V":round(24-I*r,4)},
"design_note":"Two non-twisted cores carry balanced CVBS only with active video Tx/Rx; actual bandwidth, SNR, crosstalk and impedance must be measured. RS485 transceivers require line testing. No 48V substitution is approved.",
"checks":{"allocation":"PASS","power_arithmetic":"PASS","motor_peak_current":"NOT_RUN",
"video_quality":"NOT_RUN","RS485_noise":"NOT_RUN","cable_thermal":"PHYSICAL_CHECK",
"pressure_feedthrough":"PHYSICAL_CHECK"}}
(p/"PX1_tether_40m.json").write_text(json.dumps(report,indent=2,ensure_ascii=False)+"\n",encoding="utf-8")
s=['<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 1100 490">',
'<rect width="1100" height="490" fill="#f8fafc"/>',
'<text x="30" y="40" font-size="25" font-family="sans-serif">PX1 / 40m / six-core tether</text>',
'<text x="30" y="67" font-size="15" font-family="sans-serif">PARAMETRIC 2D electrical schematic; assumed 1.5 mm2 copper cores, not OEM cable geometry</text>']
colors=['#b91c1c','#1d4ed8','#059669','#047857','#9333ea','#7c3aed']
for j,(label,color) in enumerate(zip(alloc,colors)):
 y=110+j*48
 s.extend([f'<text x="30" y="{y+5}" font-family="sans-serif" font-size="17">{j+1}: {label}</text>',
 f'<line x1="320" y1="{y}" x2="820" y2="{y}" stroke="{color}" stroke-width="5"/>'])
s.extend(['<rect x="300" y="85" width="540" height="288" rx="12" fill="none" stroke="#64748b" stroke-width="2" stroke-dasharray="8 6"/>',
'<text x="30" y="427" font-family="sans-serif" font-size="16">40m DC loop: 0.933 ohm; 2A -> 1.867V drop, 3.733W loss (20 C assumptions)</text>',
'<text x="30" y="461" font-family="sans-serif" font-size="15" fill="#b45309">NOT_RUN: CVBS video quality, RS485 EMI, motor peak load. PHYSICAL_CHECK: cable and pressure entry.</text>',
'</svg>'])
(p/"previews").mkdir(exist_ok=True)
(p/"previews/PX1_tether_40m.svg").write_text("\n".join(s)+"\n",encoding="utf-8")
print(json.dumps(report["checks"],indent=2))
