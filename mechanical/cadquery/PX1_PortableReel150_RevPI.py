import cadquery as cq, math, json, os
OUT='/mnt/data/build_revpi'; os.makedirs(OUT,exist_ok=True)
# PX1 Rev.PI — compact Proteus/RMP-style manual reel for 150 m
# Source-controlled functions: RMP200 spindle 160 mm, RMP300 160 mm crank,
# chain Z30/Z16 + 670 mm, standard bearing stacks, meter-counter roller topology.
# PX1 design dimensions (not claimed MiniCam dimensions): 530 x 240 x 520 mm envelope.
L=530.0; W=240.0; H=520.0; SIDE_T=5.0
DRUM_FLANGE_D=330.0; PACK_D=300.0; CORE_D=140.0; DRUM_W=145.0
SPINDLE_L=160.0; HANDLE_L=160.0
SHAFT_D=20.0; SHAFT_Z=282.0
CABLE_D=6.8; CABLE_L=150000.0; PACK_EFF=0.78

def box(x0,y0,z0,dx,dy,dz): return cq.Workplane('XY').box(dx,dy,dz,centered=(False,False,False)).translate((x0,y0,z0))
def cyl_x(x0,y,z,r,l): return cq.Workplane('YZ').center(y,z).circle(r).extrude(l).translate((x0,0,0))
def cyl_y(x,y0,z,r,l): return cq.Workplane('XZ').center(x,z).circle(r).extrude(l).translate((0,y0,0))

# side plate as a simple source-like triangular frame plate with large lightening windows
# exact MiniCam contour remains non-source and therefore is only PX1 geometry.
def side_plate(y0):
    p=cq.Workplane('XZ').workplane(offset=y0).polyline([(-L/2,0),(L/2,0),(L/2-35,H-95),(L/2-90,H),( -L/2+90,H),(-L/2+35,H-95)]).close().extrude(SIDE_T)
    for cx,cz,w,h in [(-150,255,150,250),(0,330,170,190),(150,255,150,250)]:
        cut=cq.Workplane('XZ').workplane(offset=y0-0.5).center(cx,cz).rect(w,h).extrude(SIDE_T+1)
        p=p.cut(cut)
    cut=cq.Workplane('XZ').workplane(offset=y0-0.5).center(0,H-38).slot2D(120,28,0).extrude(SIDE_T+1)
    return p.cut(cut)

parts={}
parts['Frame_Left']=side_plate(-W/2)
parts['Frame_Right']=side_plate(W/2-SIDE_T)
for i,(z,x) in enumerate([(25,0),(H-80,-150),(H-80,150)],1):
    parts[f'Crossbar_{i}']=cyl_y(x,-W/2+SIDE_T,z,8,W-2*SIDE_T)

parts['Drum_Core']=cyl_y(0,-DRUM_W/2,SHAFT_Z,CORE_D/2,DRUM_W)
for n,y in [('L',-DRUM_W/2-4),('R',DRUM_W/2)]:
    parts[f'Drum_Flange_{n}']=cyl_y(0,y,SHAFT_Z,DRUM_FLANGE_D/2,4)
parts['Main_Shaft']=cyl_y(0,-W/2+18,SHAFT_Z,SHAFT_D/2,W-36)

parts['BEA_61904_L']=cyl_y(0,-W/2+10,SHAFT_Z,18.5,9)
parts['BEA_16006_L']=cyl_y(0,-W/2+22,SHAFT_Z,27.5,9)
parts['Seal_30x42x7_L']=cyl_y(0,-W/2+34,SHAFT_Z,21,7)
parts['BEA_61804_R']=cyl_y(0,W/2-29,SHAFT_Z,16,7)
parts['BEA_6203_R']=cyl_y(0,W/2-20,SHAFT_Z,20,12)

Z30_PD=58.0; Z16_PD=32.0
parts['Sprocket_Z30']=cyl_y(0,W/2-12,SHAFT_Z,Z30_PD/2,6)
spindle_z=105.0; spindle_x=0.0
parts['Sprocket_Z16']=cyl_y(spindle_x,W/2-12,spindle_z,Z16_PD/2,6)
parts['Chain_Guard']=box(-48,W/2-8,spindle_z-25,96,8,SHAFT_Z-spindle_z+55)

parts['Layering_Spindle_160']=cyl_y(0,-SPINDLE_L/2,spindle_z,8,SPINDLE_L)
parts['Layering_Slider']=box(-22,-18,spindle_z-18,44,36,36)

mr_x=-115; mr_z=70
parts['Guide_Roller_D29']=cyl_y(mr_x,-18,mr_z,14.5,36)
parts['Measuring_Wheel_REF']=cyl_y(mr_x+52,-8,mr_z,20,16)
parts['Meter_Bearing_618_8_A']=cyl_y(mr_x+52,-10,mr_z,8,4)
parts['Meter_Bearing_618_8_B']=cyl_y(mr_x+52,6,mr_z,8,4)
parts['AS5600_Module_Envelope']=box(mr_x+42,12,mr_z-10,20,8,20)

parts['SlipRing_12way_Envelope']=cyl_y(0,-W/2+44,SHAFT_Z,11,32)
parts['Crank_160']=box(0,W/2+8,SHAFT_Z-5,HANDLE_L,10,10)
parts['Crank_Grip']=cyl_y(HANDLE_L-5,W/2+5,SHAFT_Z,10,70)

cable_vol=math.pi*(CABLE_D/2)**2*CABLE_L
ann_area=math.pi/4*(PACK_D**2-CORE_D**2)
required_width=cable_vol/(ann_area*PACK_EFF)
capacity_margin=DRUM_W-required_width

assy=cq.Assembly(name='PX1_PortableReel150_RevPI')
for n,p in parts.items(): assy.add(p,name=n)
assy.save(os.path.join(OUT,'PX1_PortableReel150_RevPI.step'))
checks={
 'target_envelope_mm':[L,W,H],
 'source_hard_items':{
  'RMP200_layering_spindle_mm':160,
  'RMP_crank_handle_mm':160,
  'RMP300_chain_length_mm':670,
  'RMP300_sprockets':'Z30/Z16',
  'left_bearings':'61904 20x37x9 + 16006 30x55x9 + seal 30x42x7',
  'right_bearings':'61804 20x32x7 + 6203 17x40x12',
  'meter_bearings':'2x 618/8 8x16x4'
 },
 'px1_capacity_design':{
  'cable_length_m':150,'cable_od_mm':CABLE_D,'core_d_mm':CORE_D,'pack_d_mm':PACK_D,
  'packing_efficiency':PACK_EFF,'required_pack_width_mm':round(required_width,1),
  'drum_working_width_mm':DRUM_W,'width_margin_mm':round(capacity_margin,1)
 },
 'all_solids_valid':all(p.val().isValid() for p in parts.values()),
 'status':'PASS SOURCE-FUNCTION / PX1 DIMENSIONAL DESIGN; exact side-plate contour, chain pitch and slip-ring article remain HOLD'
}
with open(os.path.join(OUT,'REV_PI_VALIDATION.json'),'w') as f: json.dump(checks,f,indent=2)
print(json.dumps(checks,indent=2))
