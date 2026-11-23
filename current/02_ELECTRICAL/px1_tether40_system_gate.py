#!/usr/bin/env python3
"""PX1 40 m tether: integrated supply / video / RS485 feasibility screen.
Run: python3 current/02_ELECTRICAL/px1_tether40_system_gate.py
All component limits are DESIGN ASSUMPTIONS until vendor and bench validation.
"""
from pathlib import Path
import json, math
L=40.0; RHO=0.0175; ALPHA=0.00393; TEMP=60.0
V_SUPPLY=24.0; MIN_LOAD_V=20.0  # assumed, NOT a verified motor/DC-DC limit
I_CONT=2.0; I_PEAK=4.0          # assumed, NOT measured
SIZES=(0.5,0.75,1.0,1.5)
CORE_ASSIGNMENT=("PWR+","PWR-","485 A","485 B","CVBS","VIDEO RETURN")
# Signal conductors share one jacket but are not twisted or coaxial.
# Video and RS485 feasibility cannot be certified by DC calculations.
def resistance(area, temp=TEMP):
    return 2*L*RHO*(1+ALPHA*(temp-20.0))/area
def case(area, current):
    r=resistance(area)
    drop=r*current
    return dict(area_mm2=area,current_A=current,loop_ohm=round(r,4),
                drop_V=round(drop,3),load_V=round(V_SUPPLY-drop,3),
                dissipated_W=round(current*current*r,2),
                dc_screen="PASS" if V_SUPPLY-drop>=MIN_LOAD_V else "FAIL")
rows=[case(a,i) for a in SIZES for i in (I_CONT,I_PEAK)]
assert len(CORE_ASSIGNMENT)==6 and len(set(CORE_ASSIGNMENT))==6
assert math.isclose(resistance(.5,20),2.8)
assert case(1.5,2)["load_V"]>case(.5,2)["load_V"]
assert all(case(a,4)["load_V"]<case(a,2)["load_V"] for a in SIZES)
# Geometry of diagram comes directly from CORE_ASSIGNMENT and calculated rows.
out=Path(__file__).resolve().parent
data=dict(status="CALCULATED_ONLY",length_m=L,supply_V=V_SUPPLY,
 assumptions={"hot_conductor_C":TEMP,"minimum_load_V":MIN_LOAD_V,
 "continuous_A":I_CONT,"peak_A":I_PEAK,"copper_rho20":RHO,"alpha":ALPHA,
 "motor_driver_DC_DC_limits":"NOT_VERIFIED"},
 cores=CORE_ASSIGNMENT,cases=rows,
 checks={"arithmetic":"PASS","dc_2A_1p5mm2":case(1.5,2)["dc_screen"],
 "dc_4A_1p5mm2":case(1.5,4)["dc_screen"],
 "CVBS_40m":"PHYSICAL_CHECK","RS485_40m":"PHYSICAL_CHECK",
 "motor_startup":"PHYSICAL_CHECK","cable_thermal":"PHYSICAL_CHECK",
 "connector_drop":"NOT_RUN","system_qualification":"NOT_RUN"},
 next_step="Measure motor peak current and validate cable+video+RS485 under PWM load")
(out/"px1_tether40_system_gate.json").write_text(json.dumps(data,ensure_ascii=False,indent=2)+"\n")
def esc(s): return str(s).replace("&","&amp;").replace("<","&lt;")
svg=['<svg xmlns="http://www.w3.org/2000/svg" width="1050" height="650" viewBox="0 0 1050 650">',
'<rect width="1050" height="650" fill="#fff"/>',
'<text x="32" y="43" font-family="sans-serif" font-size="24" font-weight="bold">PX1 | 40 m / 6-core integrated electrical screen</text>',
'<text x="32" y="68" font-family="sans-serif" font-size="14">DESIGN ASSUMPTIONS: 24 V, copper at 60 C, 2 A continuous / 4 A peak, min load 20 V</text>',
'<rect x="40" y="105" width="190" height="335" rx="12" fill="#edf3fa" stroke="#345"/>',
'<rect x="810" y="105" width="200" height="335" rx="12" fill="#edf3fa" stroke="#345"/>',
'<text x="57" y="133" font-family="sans-serif" font-size="18">Console / reel</text>',
'<text x="830" y="133" font-family="sans-serif" font-size="18">Robot / PX1</text>']
colors=("#bb3030","#333","#297ab9","#e18a2e","#278b55","#9256a9")
for idx,(name,color) in enumerate(zip(CORE_ASSIGNMENT,colors)):
    y=170+idx*44
    svg += [f'<line x1="230" y1="{y}" x2="810" y2="{y}" stroke="{color}" stroke-width="4"/>',
            f'<text x="405" y="{y-8}" font-family="sans-serif" font-size="15" fill="{color}">{idx+1}. {esc(name)}</text>']
svg += ['<text x="450" y="440" font-family="sans-serif" font-size="16">40 m copper; no coax / no twisted pairs</text>',
'<text x="40" y="485" font-family="sans-serif" font-size="19" font-weight="bold">Voltage at robot, 60 C (assumed currents)</text>']
for idx,a in enumerate(SIZES):
    y=519+idx*30
    c2=case(a,2);c4=case(a,4)
    svg += [f'<text x="48" y="{y}" font-family="monospace" font-size="16">{a:.2f} mm2 | 2A: {c2["load_V"]:5.2f} V ({c2["dc_screen"]}) | 4A: {c4["load_V"]:5.2f} V ({c4["dc_screen"]})</text>']
svg += ['<text x="580" y="520" font-family="sans-serif" font-size="14">CVBS / RS485 / PWM EMC: PHYSICAL_CHECK</text>',
'<text x="580" y="544" font-family="sans-serif" font-size="14">Connector losses / motor datasheet: NOT_RUN</text>',
'<text x="580" y="568" font-family="sans-serif" font-size="14">DC screen is NOT a cable qualification</text>','</svg>']
(out/"px1_tether40_system_gate.svg").write_text("\n".join(svg)+"\n")
print("PASS: 8 electrical calculations; video/RS485/peak current require physical check")
