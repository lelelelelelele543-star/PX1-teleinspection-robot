#!/usr/bin/env python3
"""PX1 40 m six-core tether: electrical first-pass calculation and SVG schematic.
All cable geometry and signal quality are DESIGN ASSUMPTIONS, not measurements.
Run: python3 current/02_ELECTRICAL/px1_tether40_integration.py
"""
from pathlib import Path
import json, math
L_M=40.0
RHO_CU=0.0175 # ohm*mm2/m at 20 C, engineering approximation
AREA_MM2=0.5 # ASSUMED conductor cross-section, six equal cores
CURRENT_A=(1.0,2.0,3.0,4.0)
SUPPLY_V=24.0
RS485_RATE_BPS=19200 # initial target; not verified on cable
VIDEO_Z0_OHM=75.0 # termination target, NOT characteristic impedance of cable
VIDEO_LOAD_OHM=75.0
out=Path(__file__).resolve().parent
res={"length_m":L_M,"cores":6,"core_area_mm2_assumed":AREA_MM2,
"power_pair_loop_ohm_at20C":2*L_M*RHO_CU/AREA_MM2,
"voltage_drop":[{"load_A":i,"drop_V":round(i*2*L_M*RHO_CU/AREA_MM2,3),
"crawler_V":round(SUPPLY_V-i*2*L_M*RHO_CU/AREA_MM2,3),
"copper_loss_W":round(i*i*2*L_M*RHO_CU/AREA_MM2,3)} for i in CURRENT_A],
"assignments":{"1":"24V+","2":"24V return","3":"RS485 A","4":"RS485 B","5":"CVBS signal","6":"CVBS return"},
"assumptions":["0.5mm2 copper per conductor; actual cable unspecified",
"20C copper resistivity, not hot operating limit",
"RS485 A/B use separate untwisted conductors, validate eye diagram/EMC",
"CVBS over non-coax pair is unqualified; verify impedance, amplitude, sync and noise over 40m",
"no common conductor shared between video and power returns",
"no galvanic isolation or surge protection verified in this model"],
"status":{"wire_assignment":"PASS","ohmic_math":"PASS",
"thermal_ampacity":"NOT_RUN","RS485_40m":"PHYSICAL_CHECK",
"CVBS_40m":"PHYSICAL_CHECK","power_load_budget":"NOT_RUN"}}
assert len(res["assignments"])==6
assert abs(res["power_pair_loop_ohm_at20C"]-2.8)<1e-9
assert res["voltage_drop"][2]["crawler_V"]==15.6
(out/"px1_tether40_calculation.json").write_text(json.dumps(res,ensure_ascii=False,indent=2)+"\n",encoding="utf-8")
print(json.dumps(res,ensure_ascii=False,indent=2))
