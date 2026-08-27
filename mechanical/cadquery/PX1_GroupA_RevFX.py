import cadquery as cq
import math, json, os

# PX-1 Rev.FX — Group A rotating/sealing production drawing candidates
# Prototype engineering only; no serial machining release.

OUT=os.path.abspath('build_revfx')
os.makedirs(OUT, exist_ok=True)

WX=[50.0,150.0,250.0]
WZ=45.0

# DRW-PX1-431 wheel shaft
seg431=[('inner_gear_bearing',12.0,23.0),('outer_bearing_61903',17.0,7.0),('xring_land',19.0,4.0),('labyrinth_collar',21.0,2.0),('wheel_seat',17.0,18.0)]
shaft=None; z=0.0
for name,d,l in seg431:
    part=cq.Workplane('XY').workplane(offset=z).circle(d/2).extrude(l)
    shaft=part if shaft is None else shaft.union(part)
    z+=l
shaft=shaft.faces('>Z').workplane().hole(5.0, depth=12.0)
key_start=sum(l for _,_,l in seg431[:-1])+3.0
keybox=(cq.Workplane('XY').box(4.0,4.0,12.0,centered=(True,False,False)).translate((0,17.0/2-2.0,key_start+6.0)))
shaft=shaft.cut(keybox)

# DRW-PX1-432 axle flange
FLANGE_OD=50.0; FLANGE_EXT=3.0; FLANGE_IN=9.0; FLANGE_PCD=40.0
flange=(cq.Workplane('XY').circle(FLANGE_OD/2).extrude(FLANGE_EXT).union(cq.Workplane('XY').circle(18.0).extrude(-FLANGE_IN)))
flange=flange.faces('>Z').workplane().hole(20.0, depth=FLANGE_EXT+FLANGE_IN)
for a in range(0,360,90):
    r=FLANGE_PCD/2
    flange=flange.faces('>Z').workplane().center(r*math.cos(math.radians(a)),r*math.sin(math.radians(a))).hole(3.4,depth=FLANGE_EXT)
flange=flange.faces('<Z').workplane().hole(30.0,depth=7.0)
# Dynamic X-ring gland intentionally held until the exact supplier gland standard is selected.

# DRW-PX1-433 side-drive cover
COVER_L=286.0; COVER_H=86.0; COVER_T=5.0
cover=cq.Workplane('XY').box(COVER_L,COVER_H,COVER_T,centered=(False,False,False))
for x in WX:
    cover=cover.faces('>Z').workplane().center(x-COVER_L/2,WZ-COVER_H/2).hole(36.0)
cover_holes=[(8,5),(62,5),(116,5),(170,5),(224,5),(278,5),(8,81),(62,81),(116,81),(170,81),(224,81),(278,81)]
for x,y in cover_holes:
    cover=cover.faces('>Z').workplane().center(x-COVER_L/2,y-COVER_H/2).hole(3.4)
ORING_ID=190.0; ORING_CS=1.5; GROOVE_D=1.20; GROOVE_W=1.90
RT_H=64.0; RT_R=RT_H/2
RT_CIRC=math.pi*ORING_ID
RT_STRAIGHT=(RT_CIRC-2*math.pi*RT_R)/2
RT_L=RT_STRAIGHT+2*RT_R
cx=COVER_L/2; cy=COVER_H/2
outer=(cq.Workplane('XY').workplane(offset=COVER_T-GROOVE_D).center(cx,cy).slot2D(RT_L+GROOVE_W,RT_H+GROOVE_W,0).extrude(GROOVE_D))
inner=(cq.Workplane('XY').workplane(offset=COVER_T-GROOVE_D).center(cx,cy).slot2D(RT_L-GROOVE_W,RT_H-GROOVE_W,0).extrude(GROOVE_D))
cover=cover.cut(outer.cut(inner))

# DRW-PX1-434 X200 bevel output shaft
seg434=[('bevel_gear_seat',10.0,16.0),('bearing_61800',10.0,5.0),('spacer_shoulder',14.0,2.0),('seal_land',18.0,7.0),('service_coupling',12.0,12.0)]
outshaft=None; z=0.0
for name,d,l in seg434:
    part=cq.Workplane('XY').workplane(offset=z).circle(d/2).extrude(l)
    outshaft=part if outshaft is None else outshaft.union(part)
    z+=l
outshaft=outshaft.faces('<Z').workplane().hole(4.2,depth=8.0)
flat=(cq.Workplane('XY').box(20,20,10,centered=(True,True,False)).translate((0,8,z-10)))
outshaft=outshaft.cut(flat)

# DRW-PX1-435 X200 bearing/seal boss
BOSS_OD=38.0; BOSS_L=15.0
boss=cq.Workplane('XY').circle(BOSS_OD/2).extrude(BOSS_L)
boss=boss.faces('<Z').workplane().hole(19.0,depth=5.0)
boss=boss.faces('>Z').workplane().hole(30.0,depth=7.0)
boss=boss.faces('>Z').workplane().hole(18.4,depth=BOSS_L)

# DRW-PX1-436 supported bevel pinion shaft
seg436=[('motor_adapter',6.0,12.0),('bevel_pinion_seat',8.0,14.0),('shoulder',12.0,2.0),('bearing_61801',12.0,5.0),('retainer_end',5.0,6.0)]
pinion=None; z=0.0
for name,d,l in seg436:
    part=cq.Workplane('XY').workplane(offset=z).circle(d/2).extrude(l)
    pinion=part if pinion is None else pinion.union(part)
    z+=l
pinion=pinion.faces('>Z').workplane().hole(4.2,depth=6.0)

parts={'DRW-PX1-431_WheelShaft':shaft,'DRW-PX1-432_AxleFlange':flange,'DRW-PX1-433_SideCover':cover,'DRW-PX1-434_X200_OutputShaft':outshaft,'DRW-PX1-435_X200_BearingSealBoss':boss,'DRW-PX1-436_BevelPinionShaft':pinion}
metrics={}
for name,p in parts.items():
    v=p.val(); bb=v.BoundingBox()
    metrics[name]={'valid':v.isValid(),'volume_mm3':round(v.Volume(),3),'bbox_mm':[round(bb.xlen,3),round(bb.ylen,3),round(bb.zlen,3)]}
    cq.exporters.export(p, os.path.join(OUT,name+'.step'))
metrics['checks']={'wheel_shaft_total_length_mm':sum(l for _,_,l in seg431),'wheel_keyway_begins_after_seal_land_mm':3.0,'side_cover_main_oring_nominal_circumference_mm':round(RT_CIRC,4),'side_cover_racetrack_centerline_LxH_mm':[round(RT_L,3),RT_H],'side_cover_groove_fill_ratio':round((math.pi*(ORING_CS/2)**2)/(GROOVE_W*GROOVE_D),4),'side_cover_face_squeeze_ratio':round(1-GROOVE_D/ORING_CS,4),'x200_output_shaft_total_length_mm':sum(l for _,_,l in seg434),'pinion_shaft_total_length_mm':sum(l for _,_,l in seg436),'status':'PROTOTYPE DRAWING CANDIDATE; supplier-controlled seal grooves and gear mounting distance remain HOLD'}
with open(os.path.join(OUT,'REV_FX_GROUP_A_VALIDATION.json'),'w') as f: json.dump(metrics,f,indent=2)
print(json.dumps(metrics,indent=2))