import cadquery as cq
import os, json, math

# PX-1 Rev.FI — X200 bevel shaft/bearing/seal production candidate
# Source-aligned architecture: 61801-supported pinion shaft, 61800 + 18x30x7 sealed output shaft.
# KHK 18/45 bevel pair remains purchased-part gate. Prototype only.

PIN_MOTOR_D=6.0
PIN_GEAR_D=8.0
PIN_BRG_D=12.0
PIN_MOTOR_L=12.0
PIN_GEAR_L=14.0
PIN_SHOULDER_L=2.0
PIN_BRG_L=5.0
PIN_END_L=6.0

OUT_GEAR_D=10.0
OUT_BRG_D=10.0
OUT_SEAL_D=18.0
OUT_COUPLING_D=12.0
OUT_GEAR_L=16.0
OUT_BRG_L=5.0
OUT_SPACER_L=2.0
OUT_SEAL_L=7.0
OUT_COUPLING_L=12.0

BRG61800_OD=19.0
SEAL_OD=30.0
BOSS_OD=38.0
BOSS_L=15.0

pin=(cq.Workplane('XY').circle(PIN_MOTOR_D/2).extrude(PIN_MOTOR_L)
     .faces('>Z').workplane().circle(PIN_GEAR_D/2).extrude(PIN_GEAR_L)
     .faces('>Z').workplane().circle(6.0).extrude(PIN_SHOULDER_L)
     .faces('>Z').workplane().circle(PIN_BRG_D/2).extrude(PIN_BRG_L)
     .faces('>Z').workplane().circle(5.0/2).extrude(PIN_END_L))
pin=pin.faces('>Z').workplane().hole(4.2, depth=PIN_END_L)

out=(cq.Workplane('XY').circle(OUT_GEAR_D/2).extrude(OUT_GEAR_L)
     .faces('>Z').workplane().circle(OUT_BRG_D/2).extrude(OUT_BRG_L)
     .faces('>Z').workplane().circle(7.0).extrude(OUT_SPACER_L)
     .faces('>Z').workplane().circle(OUT_SEAL_D/2).extrude(OUT_SEAL_L)
     .faces('>Z').workplane().circle(OUT_COUPLING_D/2).extrude(OUT_COUPLING_L))
out=out.faces('<Z').workplane().hole(4.2, depth=8.0)
out_total=OUT_GEAR_L+OUT_BRG_L+OUT_SPACER_L+OUT_SEAL_L+OUT_COUPLING_L
flat=(cq.Workplane('XY').box(20,20,10,centered=(True,True,False)).translate((0,8,out_total-10)))
out=out.cut(flat)

boss=cq.Workplane('XY').circle(BOSS_OD/2).extrude(BOSS_L)
boss=boss.faces('<Z').workplane().hole(BRG61800_OD, depth=5.0)
boss=boss.faces('>Z').workplane().hole(SEAL_OD, depth=7.0)
boss=boss.faces('>Z').workplane().hole(OUT_SEAL_D+0.4, depth=BOSS_L)

build=os.path.abspath('build_revfi')
os.makedirs(build,exist_ok=True)
for name,part in [('PX1_PinionShaft_RevFI',pin),('PX1_OutputShaft_RevFI',out),('PX1_X200_Boss_RevFI',boss)]:
    cq.exporters.export(part, os.path.join(build,name+'.step'))

T_pin=1.5*1000.0
T_out=1.5*2.5*0.9*1000.0
tau_pin=16*T_pin/(math.pi*PIN_GEAR_D**3)
tau_out10=16*T_out/(math.pi*OUT_GEAR_D**3)
tau_out12=16*T_out/(math.pi*OUT_COUPLING_D**3)
metrics={
 'pinion_total_length_mm':PIN_MOTOR_L+PIN_GEAR_L+PIN_SHOULDER_L+PIN_BRG_L+PIN_END_L,
 'output_total_length_mm':out_total,
 'boss_bbox_mm':[BOSS_OD,BOSS_OD,BOSS_L],
 'pinion_tau_MPa_at_d8_T1p5Nm':tau_pin,
 'output_tau_MPa_at_d10_T3p375Nm':tau_out10,
 'output_tau_MPa_at_d12_T3p375Nm':tau_out12,
 'bearing_source_architecture':'61801 pinion / 61800 output',
 'seal_source_architecture':'18x30x7 output shaft seal',
 'status':'prototype candidate; KHK mounting distance/backlash remains physical setup gate'
}
with open(os.path.join(build,'REV_FI_VALIDATION.json'),'w') as f:
    json.dump(metrics,f,indent=2)
print(json.dumps(metrics,indent=2))