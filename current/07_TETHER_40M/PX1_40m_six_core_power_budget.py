"""PX1 six-core 40 m tether: preliminary electrical feasibility, not a cable qualification.
Run: python PX1_40m_six_core_power_budget.py
All cross sections, currents and resistivity are DESIGN ASSUMPTIONS.
"""
import json, math
from pathlib import Path
L_M=40.0
RHO_OHM_MM2_PER_M=0.0175 # assumed copper at ~20 C, not a cable datasheet
V_SOURCE=24.0
MIN_V_LOAD_ASSUMED=20.0
SECTIONS_MM2=(0.5,0.75,1.0)
CURRENTS_A=(0.5,1.0,1.5,2.0,3.0)
allocation={
 "core_1":"24 V supply +",
 "core_2":"24 V power return",
 "core_3":"RS485 A",
 "core_4":"RS485 B",
 "core_5":"CVBS video signal",
 "core_6":"CVBS video return"}
assert len(allocation)==6 and len(set(allocation))==6
rows=[]
for area in SECTIONS_MM2:
 loop_r=2*L_M*RHO_OHM_MM2_PER_M/area
 max_i=(V_SOURCE-MIN_V_LOAD_ASSUMED)/loop_r
 for current in CURRENTS_A:
  drop=current*loop_r
  rows.append({"cross_section_mm2_ASSUMED":area,"current_A_ASSUMED":current,
               "loop_resistance_ohm":round(loop_r,3),
               "drop_V":round(drop,3),
               "load_V":round(V_SOURCE-drop,3),
               "cable_heat_W":round(current*current*loop_r,3),
               "voltage_gate":"PASS" if V_SOURCE-drop>=MIN_V_LOAD_ASSUMED else "FAIL"})
 print(f"{area:.2f} mm2: Rloop={loop_r:.3f} ohm, max current at 20 V target={max_i:.2f} A")
report={
 "scope":"40 m, six separate copper conductors, no coax/twisted pair/fiber",
 "assumptions":{"length_m":L_M,"copper_resistivity_ohm_mm2_per_m":RHO_OHM_MM2_PER_M,
                "supply_V":V_SOURCE,"minimum_load_voltage_V_ASSUMED":MIN_V_LOAD_ASSUMED},
 "allocation":allocation,"power_rows":rows,
 "checks":{
  "six_core_allocation":{"status":"PASS","detail":"logical allocation only"},
  "power_voltage":{"status":"CONDITIONAL","detail":"PASS/FAIL per current and area in rows; no real motor load profile"},
  "RS485_40m_no_twist":{"status":"NOT_RUN","detail":"bitrate, impedance, termination, common-mode, EMC and BER testing required"},
  "CVBS_40m_no_coax":{"status":"NOT_RUN","detail":"75-ohm source/load, attenuation, reflection, crosstalk and picture test required; do not claim usable video"},
  "thermal_cable":{"status":"PHYSICAL_CHECK","detail":"actual cable temperature, insulation rating, reel winding and derating"},
  "cable_vendor":{"status":"NOT_RUN","detail":"cross-section, copper resistance, capacitance and shield specification not verified"}
 },
 "note":"24 V at source does not guarantee 24 V at robot. This is NOT proof that six-core CVBS works."}
out=Path(__file__).with_suffix(".json")
out.write_text(json.dumps(report,ensure_ascii=False,indent=2),encoding="utf-8")
print(json.dumps(report["checks"],ensure_ascii=False,indent=2))
