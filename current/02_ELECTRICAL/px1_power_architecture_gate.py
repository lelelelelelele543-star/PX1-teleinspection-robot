#!/usr/bin/env python3
"""PX1 tether supply integrated power budget: constant-current and constant-power feasibility.
Run: python3 current/02_ELECTRICAL/px1_power_architecture_gate.py
All current, efficiency, minimum voltage, and conductor dimensions are DESIGN ASSUMPTIONS.
"""
from pathlib import Path
import math,json
LENGTH_M=40.0
RHO20=0.0175
ALPHA=0.00393
HOT_C=60.0
SUPPLY_V=24.0
MIN_ROBOT_V=20.0 # design target, NOT a vendor minimum
AREAS=(0.5,0.75,1.0,1.5)
LOAD_W=(48.0,96.0) # illustrative input powers, NOT measured
def loop_r(area, temp=HOT_C):
    return 2*LENGTH_M*RHO20*(1+ALPHA*(temp-20))/area
def constant_current(area, amps):
    r=loop_r(area)
    return {"area_mm2":area,"current_A":amps,"robot_V":round(SUPPLY_V-amps*r,3),"cable_loss_W":round(amps*amps*r,3)}
def constant_power(area, watts):
    r=loop_r(area)
    disc=SUPPLY_V**2-4*r*watts
    if disc<0:
        return {"area_mm2":area,"load_W":watts,"status":"FAIL_NO_DC_EQUILIBRIUM"}
    v=(SUPPLY_V+math.sqrt(disc))/2
    i=watts/v
    return {"area_mm2":area,"load_W":watts,"robot_V":round(v,3),"current_A":round(i,3),"cable_loss_W":round(i*i*r,3),"status":"PASS_SCREEN" if v>=MIN_ROBOT_V else "FAIL_MIN_V_SCREEN"}
cc=[constant_current(a,i) for a in AREAS for i in (2.0,4.0)]
cp=[constant_power(a,p) for a in AREAS for p in LOAD_W]
assert math.isclose(loop_r(.5,20),2.8)
assert math.isclose(loop_r(1.5),1.08004,rel_tol=.001)
assert constant_current(1.5,4)["robot_V"]<20
assert all(x["status"]!="PASS_SCREEN" or x["robot_V"]>=20 for x in cp)
data={"project":"PX1","status":"CALCULATED_ONLY","assumptions":{"supply_V":SUPPLY_V,"hot_C":HOT_C,"minimum_robot_V":MIN_ROBOT_V,"input_power_W":LOAD_W,"copper_mm2":AREAS,"copper_rho20_ohm_mm2_m":RHO20},"constant_current":cc,"constant_power":cp,"max_current_A_at_20V":[{"area_mm2":a,"max_A":round((SUPPLY_V-MIN_ROBOT_V)/loop_r(a),3)} for a in AREAS],"checks":{"math":"PASS","driver_voltage_compatibility":"NOT_RUN","startup_current":"PHYSICAL_CHECK","thermal_ampacity":"PHYSICAL_CHECK","CVBS_40m":"PHYSICAL_CHECK","RS485_40m":"PHYSICAL_CHECK","sealing":"PHYSICAL_CHECK"},"engineering_decision":"Do not release 24V tether design for 4A peak; verify actual load and evaluate local bulk capacitance or a qualified higher-voltage tether supply plus robot DC/DC; do not connect 36/48V directly to 24V drivers."}
out=Path(__file__).resolve().parent
(out/"px1_power_architecture_gate.json").write_text(json.dumps(data,indent=2)+"\n")
print(json.dumps({"constant_power":cp,"max_current":data["max_current_A_at_20V"]},indent=2))
