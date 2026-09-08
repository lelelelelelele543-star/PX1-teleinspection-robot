"""Reproducible scenario calculations; not measurements of the user's cable."""
import json,math
from pathlib import Path
root=Path(__file__).resolve().parents[1]
h=json.loads((root/'firmware/crawler/r12/hardware_profile.json').read_text())
pins=[p.split('/')[0] for ps in h['pins'].values() for p in ps]
assert len(pins)==len(set(pins))
assert not set(pins)&{p.split('/')[0] for p in h['reserved']}
assert len(set(h['i2c_addresses'].values()))==len(h['i2c_addresses'])
lo,typ,hi=59000/101000,64000/100000,69000/99000
assert hi<3*.25
def torque(i):return (i-.1)/(3-.1)*39*.0980665
assert torque(hi)<10*.0980665
def cable(length,temp=20,source=110,power=56,area=.5):
 r=2*.0175*(1+.00393*(temp-20))*length/area
 disc=source**2-4*power*r
 if disc<0:return {'length_m':length,'temperature_C':temp,'source_V':source,'status':'NO_CONSTANT_POWER_DC_SOLUTION','R_loop_ohm':r}
 vr=(source+math.sqrt(disc))/2
 return {'length_m':length,'temperature_C':temp,'source_V':source,'R_loop_ohm':r,'load_V':vr,'loss_W':(power/vr)**2*r}
# Use the44mm CAD crown radius as an ideal rolling reference; loaded contact is unmeasured.
report={'status':'PASS_SCENARIO_ARITHMETIC_NOT_HARDWARE',
 'assumptions':{'rolling_radius_m':.044,'robot_mass_kg':6,'wet_friction':.35,'cable_mass_kg_m':.055,'cable_drag_friction':.4,'copper_area_mm2':.5,'power_W':56},
 'traction_current_A':[lo,typ,hi],'camera_current_typ_A':64000/390000,
 'traction_torque_typ_Nm':torque(typ),'electromagnetic_force_typ_N':2*torque(typ)*2.5*.8/.044,
 'speed_no_load_m_min':100/2.5*2*math.pi*.044,
 'assumed_wet_grip_N':6*9.80665*.35,
 'assumed_cable_drag_N':{str(l):l*.055*9.80665*.4 for l in (40,150)},
 'motor_copper_heat_partial_W':2*.64**2*(24/3),
 'cable_cases':[cable(40),cable(150),cable(150,70),cable(40,source=24),cable(150,source=24)],
 'limitations':['TI limit spread was characterized near1A; 0.64/0.164A settings need actual calibration.',
 'Linear torque-current interpolation is an estimate, not a validated load curve.',
 'No measured traction, gear efficiency, winding resistance, thermal resistance or actual cable parameters.',
 '6kg mass is assumed. Rolling radius44mm is an ideal CAD reference; loaded contact is unmeasured.',
 'A pass in an ideal straight DN150 cylinder does not demonstrate bends or towing150m.']}
out=root/'build_r12';out.mkdir(exist_ok=True)
(out/'engineering_validation.json').write_text(json.dumps(report,indent=2))
print(json.dumps(report,indent=2))

