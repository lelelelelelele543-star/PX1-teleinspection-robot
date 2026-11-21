#!/usr/bin/env python3
"""PX1 24V / 40m tether integrated load guard. Design assumptions, NOT hardware approval.
Run: python current/CAD/PX1_power_budget_guard.py
"""
from pathlib import Path
import json, math
P=Path(__file__).resolve().parent
L=40.0; A=1.5; RHO=0.0175; ALPHA=0.00393
VS=24.0; VMIN=20.0
# Scenario-only load allocation. No measured motor stall/LED/camera ratings.
LOADS={"left_motor_A":2.0,"right_motor_A":2.0,"camera_lights_control_A":0.8}
def loop_r(t):
    return 2*L*RHO*(1+ALPHA*(t-20))/A
def voltage(i,t):
    return VS-i*loop_r(t)
def budget(t):
    return (VS-VMIN)/loop_r(t)
scenarios={}
for t in (20,60):
    i=sum(LOADS.values())
    scenarios[str(t)]={"load_A":i,"received_V":round(voltage(i,t),3),
       "cable_loss_W":round(i*i*loop_r(t),3),
       "max_current_for_20V_A":round(budget(t),3),
       "status":"PASS" if voltage(i,t)>=VMIN else "FAIL"}
assert math.isclose(loop_r(20),0.9333333333333333)
assert scenarios["20"]["status"]=="FAIL"
assert scenarios["60"]["status"]=="FAIL"
assert budget(60)<budget(20)
# This is a CURRENT BUDGET, not a current limiter design. Driver peak currents must be measured.
report={"release":False,"status":"DESIGN_SCREEN_ONLY",
 "assumptions":{"supply_V":VS,"minimum_robot_V_provisional":VMIN,
 "copper_area_mm2_per_core":A,"length_m":L,"motor_currents_unmeasured":True,
 "load_scenarios_A":LOADS,"no_coax":True,"no_twisted_pair":True},
 "scenarios":scenarios,
 "checks":{"power_math":"PASS","scenario_voltage_margin":"FAIL",
 "actual_motor_start_stall":"NOT_RUN","driver_current_limit":"NOT_RUN",
 "video_and_rs485_EMI":"NOT_RUN","cable_heat":"PHYSICAL_CHECK",
 "feedthrough_pressure":"PHYSICAL_CHECK"},
 "recommendation":"Do not claim 24V delivery at combined 4.8A. Verify motor start/stall, consider staged acceleration and current limiting after driver capability is confirmed; preserve six-core architecture."}
(P/"PX1_power_budget_guard.json").write_text(json.dumps(report,indent=2,ensure_ascii=False)+"\n")
svg=['<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 1050 470">',
'<rect width="1050" height="470" fill="#f8fafc"/>',
'<text x="32" y="43" font-size="25" font-family="sans-serif">PX1 / integrated load budget / 40 m six-core tether</text>',
'<text x="32" y="71" font-size="15" font-family="sans-serif">PARAMETRIC ELECTRICAL 2D / ALL load currents are assumptions, not measured ratings</text>',
'<rect x="35" y="110" width="200" height="180" rx="9" fill="#dbeafe" stroke="#1e40af"/>',
'<text x="55" y="148" font-size="20" font-family="sans-serif">24 V console</text>',
'<text x="55" y="180" font-size="16" font-family="sans-serif">6 copper cores</text>',
'<text x="55" y="208" font-size="16" font-family="sans-serif">2 power + 2 RS485</text>',
'<text x="55" y="234" font-size="16" font-family="sans-serif">+ 2 balanced video</text>',
'<rect x="800" y="110" width="215" height="180" rx="9" fill="#e2e8f0" stroke="#334155"/>',
'<text x="815" y="148" font-size="20" font-family="sans-serif">PX1 robot</text>',
'<text x="815" y="182" font-size="16" font-family="sans-serif">L motor: 2.0 A*</text>',
'<text x="815" y="209" font-size="16" font-family="sans-serif">R motor: 2.0 A*</text>',
'<text x="815" y="236" font-size="16" font-family="sans-serif">Other: 0.8 A*</text>',
'<line x1="235" y1="162" x2="800" y2="162" stroke="#dc2626" stroke-width="5"/>',
'<line x1="235" y1="235" x2="800" y2="235" stroke="#2563eb" stroke-width="5"/>',
'<text x="360" y="145" font-size="18" font-family="sans-serif">40 m supply + return</text>',
'<text x="360" y="260" font-size="16" font-family="sans-serif">RS485 and video cores omitted visually</text>']
for j,t in enumerate((20,60)):
 d=scenarios[str(t)]
 x=35+j*510
 svg.extend([f'<rect x="{x}" y="318" width="490" height="104" rx="8" fill="#fff" stroke="#b91c1c"/>',
 f'<text x="{x+14}" y="346" font-size="18" font-family="sans-serif">{t} C / 4.8 A scenario / FAIL</text>',
 f'<text x="{x+14}" y="376" font-size="17" font-family="sans-serif">Robot: {d["received_V"]:.3f} V (provisional min 20 V)</text>',
 f'<text x="{x+14}" y="402" font-size="16" font-family="sans-serif">Max budget: {d["max_current_for_20V_A"]:.3f} A; heat: {d["cable_loss_W"]:.2f} W</text>'])
svg.append('<text x="35" y="450" font-size="14" font-family="sans-serif">* Assumed only. NOT_RUN: startup/stall, RS485/CVBS. PHYSICAL_CHECK: cable and pressure feedthrough.</text>')
svg.append('</svg>')
(P/"previews").mkdir(exist_ok=True)
(P/"previews/PX1_power_budget_guard.svg").write_text("\n".join(svg)+"\n")
print(json.dumps(report["checks"],ensure_ascii=False))
