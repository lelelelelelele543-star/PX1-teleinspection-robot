from pathlib import Path
import json, math, os
import cadquery as cq
from cadquery import exporters

OUT=Path(os.environ.get('PX1_A3_OUT', str(Path(__file__).resolve().parent/'generated')))
OUT.mkdir(parents=True,exist_ok=True)

# PX1 Rev.A A3.0 open camera/light test fixture.
# It intentionally does NOT model a pressure-rated head.
# X is optical axis, front at X=0, rear toward +X.

CAM=(19.0,19.0,20.0)  # Phoenix 2 body class; fixture pocket has clearance
CAM_POCKET=19.4
FRONT_OD=60.0
FRONT_T=5.0
HEAT_T=2.0
LENS_CLEAR_D=18.0
LED_MCPCB_D=8.0
LED_LOC_D=8.3
LED_RING_R=21.0
LED_COUNT=6
CAGE_L=72.0
BASE_L=105.0
BASE_W=70.0
BASE_T=4.0
CAM_FRONT_X=12.0
CAM_CENTER_Z=34.0
HARNESS_OD_SCREEN=5.4


def wp(s): return cq.Workplane('XY').newObject([s])
def boxc(x,y,z,dx,dy,dz):
    return cq.Workplane('XY').box(dx,dy,dz,centered=(True,True,True)).translate((x,y,z))
def cyl_x(x,y,z,r,l,dir=1):
    return wp(cq.Solid.makeCylinder(r,l,cq.Vector(x,y,z),cq.Vector(dir,0,0)))
def cut(a,b): return wp(a.val().cut(b.val()))
def fuse(parts):
    s=parts[0].val()
    for p in parts[1:]: s=s.fuse(p.val())
    return wp(s)
def localize(shape):
    bb=shape.val().BoundingBox()
    return shape.translate((-(bb.xmin+bb.xmax)/2, -(bb.ymin+bb.ymax)/2, -bb.zmin))


def front_carrier():
    # Printed structural ring behind the aluminium heat spreader.
    ring=cyl_x(0,0,CAM_CENTER_Z,FRONT_OD/2,FRONT_T)
    ring=cut(ring,cyl_x(-0.1,0,CAM_CENTER_Z,LENS_CLEAR_D/2,FRONT_T+0.2))
    # Vent/service windows between LED sectors: fixture is intentionally open.
    for a in range(0,360,60):
        ang=math.radians(a+30)
        y=17.5*math.cos(ang); z=CAM_CENTER_Z+17.5*math.sin(ang)
        ring=cut(ring,cyl_x(-0.1,y,z,3.2,FRONT_T+0.2))
    # M3 holes holding heat spreader to printed carrier.
    for a in (0,120,240):
        ang=math.radians(a)
        y=26.0*math.cos(ang); z=CAM_CENTER_Z+26.0*math.sin(ang)
        ring=cut(ring,cyl_x(-0.1,y,z,1.65,FRONT_T+0.2))
    return ring


def heat_spreader():
    disc=cyl_x(-HEAT_T,0,CAM_CENTER_Z,FRONT_OD/2,HEAT_T)
    disc=cut(disc,cyl_x(-HEAT_T-0.1,0,CAM_CENTER_Z,LENS_CLEAR_D/2,HEAT_T+0.2))
    for a in (0,120,240):
        ang=math.radians(a)
        y=26.0*math.cos(ang); z=CAM_CENTER_Z+26.0*math.sin(ang)
        disc=cut(disc,cyl_x(-HEAT_T-0.1,y,z,1.65,HEAT_T+0.2))
    # 0.25 mm locating recesses for six Ø8 MCPCB carriers. They are not through-holes.
    for i in range(LED_COUNT):
        a=2*math.pi*i/LED_COUNT
        y=LED_RING_R*math.cos(a); z=CAM_CENTER_Z+LED_RING_R*math.sin(a)
        recess=cyl_x(-HEAT_T-0.01,y,z,LED_LOC_D/2,0.26)
        disc=cut(disc,recess)
    return disc


def camera_cradle():
    # Sleeve around 19 mm camera. No assumed M2 hole pitch is required.
    outer=boxc(CAM_FRONT_X+CAM[2]/2,0,CAM_CENTER_Z,CAM[2]+6,28,28)
    pocket=boxc(CAM_FRONT_X+CAM[2]/2,0,CAM_CENTER_Z,CAM[2]+0.4,CAM_POCKET,CAM_POCKET)
    sleeve=cut(outer,pocket)
    # Open top and both side windows for service/heat access.
    sleeve=cut(sleeve,boxc(CAM_FRONT_X+CAM[2]/2,0,CAM_CENTER_Z+10,CAM[2]-2,16,12))
    sleeve=cut(sleeve,boxc(CAM_FRONT_X+CAM[2]/2,13,CAM_CENTER_Z,CAM[2]-2,12,15))
    sleeve=cut(sleeve,boxc(CAM_FRONT_X+CAM[2]/2,-13,CAM_CENTER_Z,CAM[2]-2,12,15))
    # Flexible printed clamp bridge, M3 service screw.
    clamp=boxc(CAM_FRONT_X+CAM[2]/2,0,CAM_CENTER_Z+13,CAM[2]+6,8,3)
    clamp=cut(clamp,cyl_x(CAM_FRONT_X+CAM[2]/2-14,0,CAM_CENTER_Z+13,1.65,CAM[2]+28))
    return fuse([sleeve,clamp])


def bench_base():
    b=boxc(BASE_L/2-8,0,BASE_T/2,BASE_L,BASE_W,BASE_T)
    for x in (5,BASE_L-21):
        for y in (-28,28):
            b=cut(b,cq.Workplane('XY').circle(2.6).extrude(BASE_T+0.2).translate((x,y,-0.1)))
    # Two upright ribs supporting front carrier and camera cradle.
    rib1=boxc(2,0,CAM_CENTER_Z/2,6,54,CAM_CENTER_Z)
    rib1=cut(rib1,boxc(2,0,CAM_CENTER_Z/2,8,38,CAM_CENTER_Z-8))
    rib2=boxc(CAM_FRONT_X+CAM[2]+6,0,CAM_CENTER_Z/2,5,36,CAM_CENTER_Z)
    rib2=cut(rib2,boxc(CAM_FRONT_X+CAM[2]+6,0,CAM_CENTER_Z/2,7,22,CAM_CENTER_Z-8))
    # Rear harness guide with 5.4 mm screen + clearance.
    guide=boxc(58,0,15,10,18,22)
    guide=cut(guide,cyl_x(52.9,0,17,(HARNESS_OD_SCREEN+0.8)/2,10.2))
    return fuse([b,rib1,rib2,guide])


parts=[]
def add(name,shape,kind): parts.append((name,shape,kind)); return shape

carrier=add('A3_PRINT_FRONT_CARRIER',front_carrier(),'print')
spreader=add('A3_ALUMINIUM_LED_HEAT_SPREADER_2MM',heat_spreader(),'metal')
cradle=add('A3_PRINT_CAMERA_CRADLE',camera_cradle(),'print')
base=add('A3_PRINT_BENCH_BASE',bench_base(),'print')

# Camera reference block and lens envelope.
cam=boxc(CAM_FRONT_X+CAM[2]/2,0,CAM_CENTER_Z,CAM[2],CAM[0],CAM[1])
add('RUNCAM_PHOENIX2_19x19x20_SCREEN',cam,'purchased_screen')
add('M12_LENS_SCREEN',cyl_x(2.5,0,CAM_CENTER_Z,7.0,10),'purchased_screen')

# LED MCPCB screens on the aluminium face.
for i in range(LED_COUNT):
    a=2*math.pi*i/LED_COUNT
    y=LED_RING_R*math.cos(a); z=CAM_CENTER_Z+LED_RING_R*math.sin(a)
    add(f'XP_G_MCPCB_SCREEN_{i+1}',cyl_x(-2.25,y,z,LED_MCPCB_D/2,1.0),'led_screen')

# Two PT4115-module packaging placeholders behind the camera fixture, not final head positions.
for y in (-11,11):
    add(f'PT4115_MODULE_SCREEN_{y:+g}',boxc(62,y,23,29.3,15.1,9),'electronics_screen')

# Six-core local harness route screen from rear service area.
add('LOCAL_6CORE_HARNESS_OD5p4_SCREEN',cyl_x(45,0,17,HARNESS_OD_SCREEN/2,45),'cable_screen')

assembly=cq.Compound.makeCompound([p.val() for _,p,_ in parts])
exporters.export(assembly,str(OUT/'PX1_A3_Camera_Light_Bench.step'))

for filename,shape in (
    ('PX1_A3_FrontCarrier',carrier),
    ('PX1_A3_CameraCradle',cradle),
    ('PX1_A3_BenchBase',base),
):
    s=localize(shape)
    exporters.export(s,str(OUT/f'{filename}.step'))
    exporters.export(s,str(OUT/f'{filename}.stl'),tolerance=0.10,angularTolerance=0.18)

hs=localize(spreader)
exporters.export(hs,str(OUT/'PX1_A3_LED_HeatSpreader_2mm.step'))

bb=assembly.BoundingBox()
validation={
  'status':'A3_CAMERA_LIGHT_BENCH_GENERATED__NOT_PRESSURE_RATED',
  'source_architecture':{
    'ASM000':'separate camera housing / side frame / bearing housing; source overall axial dimension 132 mm',
    'ASM001':'camera module + pan gear + focus mechanism + rear cover + O-rings + light ring',
    'ASM004':'rotate motor + rotate bearing housing + axle/connector/gears + seals',
    'ASM006':'LED PCB + sapphire lens glass + lock ring + O-rings'
  },
  'bench_camera':{'family':'RunCam Phoenix 2','screen_mm':[19,19,20],'supply_v':[5,36],'signal':'CVBS'},
  'lighting':{'led_count':6,'strings':2,'leds_per_string':3,'initial_current_ma_per_string':350,'heat_spreader':'60mm OD x 2mm aluminium screen'},
  'local_harness':['+12V_HEAD','GND_HEAD','UART_TX_CRAWLER_TO_HEAD','UART_RX_HEAD_TO_CRAWLER','CVBS_SIGNAL','CVBS_RETURN'],
  'bbox_mm':{'xmin':bb.xmin,'xmax':bb.xmax,'ymin':bb.ymin,'ymax':bb.ymax,'zmin':bb.zmin,'zmax':bb.zmax},
  'pressure_release':False,
  'next_gate':'video/lighting/thermal/EMI bench -> then pan/rotate motor and sealed housing release'
}
(OUT/'PX1_A3_Validation.json').write_text(json.dumps(validation,indent=2,ensure_ascii=False),encoding='utf-8')
print(json.dumps(validation,indent=2,ensure_ascii=False))
