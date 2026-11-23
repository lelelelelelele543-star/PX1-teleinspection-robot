#!/usr/bin/env python3
"""PX1 tether power feasibility; design assumptions only. Python stdlib."""
from pathlib import Path
import json, math
L=40.0
RHO20=0.0175
ALPHA=0.00393
V=24.0
AREAS=(0.5,0.75,1.0,1.5)
CURRENTS=(1.0,2.0,3.0,4.0)
TMAX=60.0
V_MIN=20.0 # DESIGN TARGET, not confirmed input limit of robot electronics
def loop_r(area, temp=20.0):
    return 2*L*RHO20*(1+ALPHA*(temp-20))/area
def evaluate(area, amps, temp=20.0):
    r=loop_r(area,temp)
    return dict(area_mm2=area, current_A=amps, conductor_temp_C=temp,
                loop_ohm=round(r,4), drop_V=round(amps*r,3),
                robot_V=round(V-amps*r,3), loss_W=round(amps*amps*r,3),
                meets_assumed_20V=V-amps*r>=V_MIN)
rows=[evaluate(a,i,t) for t in (20.,TMAX) for a in AREAS for i in CURRENTS]
assert abs(loop_r(.5)-2.8)<1e-10
assert evaluate(.5,2)['drop_V']==5.6
assert evaluate(.5,2,60)['robot_V']<evaluate(.5,2)['robot_V']
assert evaluate(1.5,2,60)['meets_assumed_20V']
result={'status':'CALCULATED_ONLY','length_m':L,'six_core_assignment':
        ['24V+','power return','RS485 A','RS485 B','CVBS signal','CVBS return'],
        'assumptions':{'copper_rho20_ohm_mm2_per_m':RHO20,
          'copper_alpha_per_C':ALPHA,'supply_V':V,'minimum_robot_voltage_V':V_MIN,
          'conductor_hot_case_C':TMAX,'cross_sections_mm2':AREAS},
        'cases':rows,'physical_checks':['thermal ampacity of actual six-core cable',
          'motor starting/stall current and undervoltage behavior',
          'RS485 and CVBS signal integrity on untwisted, noncoax 40m cable',
          'connector losses, cable flex and shielding/EMC'],
        'note':'Do not treat V_MIN=20V as a verified DC/DC or motor limit.'}
p=Path(__file__).resolve().parent
(p/'px1_tether40_power_budget.json').write_text(json.dumps(result,indent=2,ensure_ascii=False)+'\n')
print('PASS: 32 calculated voltage-drop cases; PHYSICAL_CHECK: cable, EMC, video and peak load')
