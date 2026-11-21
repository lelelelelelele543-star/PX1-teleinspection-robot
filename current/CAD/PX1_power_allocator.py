#!/usr/bin/env python3
"""PX1 integrated 24V tether current allocator. DESIGN SCREEN, not firmware.
Run: python current/CAD/PX1_power_allocator.py
No hardware IO. All motor and auxiliary currents are design assumptions.
"""
from pathlib import Path
import json, math
L_M=40.0
CORE_MM2=1.5
RHO=0.0175
ALPHA=0.00393
SUPPLY_V=24.0
MIN_BUS_V=20.0
AUX_A=0.8
MOTOR_RUN_A=2.0
MOTOR_START_A=4.0
def loop_ohm(temp_c):
    return 2*L_M*RHO/CORE_MM2*(1+ALPHA*(temp_c-20))
def max_total_current(temp_c):
    return max(0.0,(SUPPLY_V-MIN_BUS_V)/loop_ohm(temp_c))
def allocate(left_request_a,right_request_a,temp_c,aux_a=AUX_A):
    assert left_request_a>=0 and right_request_a>=0 and aux_a>=0
    limit=max_total_current(temp_c)
    motor_budget=max(0.0,limit-aux_a)
    requested=left_request_a+right_request_a
    factor=0.0 if aux_a>limit else (min(1.0,motor_budget/requested) if requested else 1.0)
    left=left_request_a*factor
    right=right_request_a*factor
    total=aux_a+left+right
    v=SUPPLY_V-total*loop_ohm(temp_c)
    fault = aux_a>limit or v<MIN_BUS_V-1e-8
    return dict(temp_C=temp_c,requested_left_A=left_request_a,requested_right_A=right_request_a,
                allowed_left_A=round(left,4),allowed_right_A=round(right,4),
                motor_scale=round(factor,4),total_A=round(total,4),bus_V=round(v,4),
                status="FAIL_AUX_LOAD" if fault else "PASS_DESIGN_SCREEN",
                protection="AUX_OVER_BUDGET" if aux_a>limit else "LIMITED" if factor<1 else "UNLIMITED")
def main():
    cases=[allocate(l,r,t) for t in (20,60) for l,r in
           ((0,0),(2,0),(2,2),(4,2),(4,4))]
    assert math.isclose(loop_ohm(20),0.9333333333333333)
    assert all(c["bus_V"]>=MIN_BUS_V-1e-4 for c in cases)
    assert allocate(2,2,60)["motor_scale"]<1
    assert allocate(2,0,60)["motor_scale"]==1
    assert allocate(4,4,60)["allowed_left_A"]<2
    assert allocate(0,0,60,aux_a=5)["protection"]=="AUX_OVER_BUDGET"
    assert allocate(4,4,60,aux_a=5)["allowed_left_A"]==0
    assert allocate(4,4,60,aux_a=5)["status"]=="FAIL_AUX_LOAD"
    assert allocate(4,4,60,aux_a=5)["bus_V"]<MIN_BUS_V
    assert allocate(2,2,60)["status"]=="PASS_DESIGN_SCREEN"
    report={
      "release":False,"model":"DESIGN_ASSUMPTIONS_ONLY",
      "power_wiring":"2 copper cores power, 2 RS485, 2 balanced CVBS; no coax, no twisted pairs",
      "design":{"supply_V":SUPPLY_V,"minimum_bus_V_assumed":MIN_BUS_V,
        "tether_m":L_M,"copper_mm2_each_power_core":CORE_MM2,
        "auxiliary_current_A_assumed":AUX_A,
        "running_current_A_each_motor_assumed":MOTOR_RUN_A,
        "startup_current_A_each_motor_assumed":MOTOR_START_A},
      "control_requirements":[
        "Measure bus voltage and BOTH motor currents at robot; current requests alone cannot enforce current limits.",
        "Hardware overcurrent protection independent of STM32 and BTS7960 PWM.",
        "Software allocate() is a steady-state design bound, not a transient control algorithm.",
        "AUX_OVER_BUDGET is a FAULT: force motor request to zero; auxiliary load must be shed by independent hardware or supply redesign.",
        "Add filtered undervoltage fault, hysteresis, motor shutdown and operator telemetry.",
        "Verify voltage at robot, source tolerance, connector resistance, temperature, RS485 and CVBS signal quality."],
      "checks":{"arithmetic":"PASS","assumed_bus_limit":"PASS_DESIGN_SCREEN",
        "motor_current_feedback":"NOT_RUN","motor_stall":"NOT_RUN",
        "driver_thermal":"NOT_RUN","video_and_rs485":"NOT_RUN",
        "cable_thermal":"PHYSICAL_CHECK","pressure_feedthrough":"PHYSICAL_CHECK"},
      "cases":cases}
    p=Path(__file__).resolve().parent
    (p/"PX1_power_allocator.json").write_text(json.dumps(report,indent=2,ensure_ascii=False)+"\n")
    print(json.dumps({"checks":report["checks"],"both_running_60C":allocate(2,2,60)},ensure_ascii=False))
if __name__=="__main__":
    main()
