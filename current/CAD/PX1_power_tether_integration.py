#!/usr/bin/env python3
"""PX1 integrated 24V tether/power feasibility screen. ASSUMPTIONS, not certified hardware data.
Run: python current/CAD/PX1_power_tether_integration.py
No external packages. Creates JSON and a dimensioned 2D SVG from the same parameters.
"""
from pathlib import Path
import json, math
ROOT=Path(__file__).resolve().parent
OUT=ROOT/"previews"
OUT.mkdir(exist_ok=True)
LENGTH_M=40.0
RHO20=0.0175 # Ohm*mm2/m, nominal copper at 20C, design assumption
ALPHA=0.00393 # copper temperature coefficient, assumed
AREA_MM2=1.5 # each of six conductors, assumed; actual cable unverified
SUPPLY_V=24.0 # nominal, NOT a validated supply rating
MIN_RX_V=20.0 # provisional acceptance criterion, not module datasheet
CASES_A={"idle_0p5A":0.5,"nominal_2A":2.0,"combined_4A":4.0,"peak_8A":8.0}
ALLOCATION={1:"24V supply",2:"DC return",3:"RS485 A",4:"RS485 B",5:"CVBS differential +",6:"CVBS differential -"}
assert len(ALLOCATION)==6 and len(set(ALLOCATION))==6
assert LENGTH_M>0 and AREA_MM2>0
def loop_resistance(temp_c):
    return 2*LENGTH_M*RHO20*(1+ALPHA*(temp_c-20))/AREA_MM2
results={}
for t in (20,60):
    r=loop_resistance(t)
    results[str(t)+"C"]={}
    for name,i in CASES_A.items():
        drop=i*r
        rx=SUPPLY_V-drop
        results[str(t)+"C"][name]={"current_A":i,"loop_ohm":round(r,4),
          "drop_V":round(drop,3),"received_V":round(rx,3),
          "cable_heat_W":round(i*i*r,3),
          "screen":"PASS" if rx>=MIN_RX_V else "FAIL"}
assert math.isclose(loop_resistance(20),0.9333333333333333,rel_tol=1e-9)
assert results["20C"]["combined_4A"]["screen"]=="PASS"
assert results["60C"]["combined_4A"]["screen"]=="FAIL"
assert results["20C"]["peak_8A"]["screen"]=="FAIL"
report={"status":"DESIGN_SCREEN_ONLY","release":False,"basis":"PX1_tether_40m.py + AGENTS.md; does not modify PX1_Current_Master.py",
"assumptions":{"length_m":LENGTH_M,"area_mm2_each":AREA_MM2,"rho20_ohm_mm2_per_m":RHO20,
"alpha_per_C":ALPHA,"supply_V":SUPPLY_V,"provisional_min_received_V":MIN_RX_V,
"motor_current_cases_A":"scenario values only, not measured","no_coax":True,"no_twisted_pair":True},
"allocation":ALLOCATION,"results":results,
"checks":{"six_core_allocation":"PASS","dc_arithmetic":"PASS","4A_at_60C_provisional_voltage":"FAIL",
"8A_at_20C_provisional_voltage":"FAIL","motor_start_current":"NOT_RUN",
"CVBS_40m_signal_quality":"NOT_RUN","RS485_common_mode_and_EMI":"NOT_RUN",
"cable_bend_thermal":"PHYSICAL_CHECK","pressurized_feedthrough":"PHYSICAL_CHECK"},
"next":"Measure motor startup/stall and electronics current; validate CVBS and RS485 over actual 40m cable; assess DC distribution and surge protection."}
(ROOT/"PX1_power_tether_integration.json").write_text(json.dumps(report,ensure_ascii=False,indent=2)+"\n",encoding="utf-8")
def esc(s):
    return str(s).replace("&","&amp;").replace("<","&lt;")
svg=['<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 1180 650">',
'<rect width="1180" height="650" fill="#f8fafc"/>',
'<text x="32" y="46" font-family="sans-serif" font-size="26" font-weight="bold">PX1 / 40 m six-core tether / 24 V feasibility</text>',
'<text x="32" y="73" font-family="sans-serif" font-size="16">Parametric electrical 2D schematic. ALL currents and cable sizes are design assumptions.</text>',
'<rect x="35" y="113" width="190" height="285" rx="12" fill="#e2e8f0" stroke="#334155"/>',
'<text x="55" y="150" font-family="sans-serif" font-size="19">Console / 24 V</text>',
'<rect x="945" y="113" width="200" height="285" rx="12" fill="#e2e8f0" stroke="#334155"/>',
'<text x="962" y="150" font-family="sans-serif" font-size="19">Robot / loads</text>']
labels=list(ALLOCATION.values())
colors=["#dc2626","#2563eb","#059669","#047857","#7c3aed","#9333ea"]
for j,(label,color) in enumerate(zip(labels,colors)):
    y=181+j*39
    svg.extend([f'<line x1="225" y1="{y}" x2="945" y2="{y}" stroke="{color}" stroke-width="4"/>',
      f'<rect x="410" y="{y-23}" width="330" height="26" fill="#f8fafc"/>',
      f'<text x="418" y="{y-5}" font-family="sans-serif" font-size="17">{j+1}. {esc(label)}</text>'])
svg.extend(['<text x="390" y="430" font-family="sans-serif" font-size="17">40 m / six independent copper conductors / no coax</text>',
'<text x="32" y="470" font-family="sans-serif" font-size="19" font-weight="bold">DC screening (24 V supply, provisional 20 V minimum at robot)</text>'])
for j,(temp,key) in enumerate(((20,"nominal_2A"),(20,"combined_4A"),(60,"combined_4A"),(20,"peak_8A"))):
    x=35+j*287
    v=results[str(temp)+"C"][key]
    col="#166534" if v["screen"]=="PASS" else "#b91c1c"
    svg.extend([f'<rect x="{x}" y="490" width="273" height="92" rx="8" fill="#fff" stroke="#cbd5e1"/>',
    f'<text x="{x+12}" y="516" font-family="sans-serif" font-size="16">{temp} C / {v["current_A"]} A / {v["screen"]}</text>',
    f'<text x="{x+12}" y="542" font-family="sans-serif" font-size="16" fill="{col}">Robot: {v["received_V"]:.3f} V</text>',
    f'<text x="{x+12}" y="565" font-family="sans-serif" font-size="14">Cable heat: {v["cable_heat_W"]:.2f} W</text>'])
svg.extend(['<text x="32" y="621" font-family="sans-serif" font-size="15" fill="#9a3412">NOT_RUN: motor startup, RS485 EMI, CVBS video. PHYSICAL_CHECK: cable, thermal and pressure feedthrough.</text>','</svg>'])
(OUT/"PX1_power_tether_integration.svg").write_text("\n".join(svg)+"\n",encoding="utf-8")
print(json.dumps(report["checks"],ensure_ascii=False,indent=2))
