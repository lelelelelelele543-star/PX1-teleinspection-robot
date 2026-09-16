from pathlib import Path
import math, json, os
import cadquery as cq
from cadquery import exporters

OUT=Path(os.environ.get('PX1_A1_OUT', str(Path(__file__).resolve().parent/'generated'))); OUT.mkdir(parents=True,exist_ok=True)

# PX1 Rev.A A1: rolling 6x6 prototype chassis.
# Purpose: flat-floor/bench drivetrain and steering proof before pressure-body release.
# Frozen source-derived longitudinal topology from CRP150 reconstruction.
WHEEL_X=(50.0,150.0,250.0)
GEAR_X=(50.0,100.0,150.0,200.0,250.0)
Z=45.0
GEAR_Y=31.8
WHEEL_Y=54.5
Z50_N=50; MOD=1.0; FACE=4.0
SHAFT_D=12.0
BEARING_ID=12.0; BEARING_OD=28.0; BEARING_W=8.0 # bench-only 6001
PLATE_T=6.0
INNER_Y=25.5
OUTER_Y=38.1
PLATE_X0=20.0; PLATE_L=260.0; PLATE_Z0=8.0; PLATE_H=74.0
PIPE_R=75.0; PIPE_CZ=52.0480547


def wp(s): return cq.Workplane('XY').newObject([s])
def boxc(x,y,z,dx,dy,dz): return cq.Workplane('XY').box(dx,dy,dz,centered=(True,True,True)).translate((x,y,z))
def cyl_x(x,y,z,r,l,dir=1): return wp(cq.Solid.makeCylinder(r,l,cq.Vector(x,y,z),cq.Vector(dir,0,0)))
def cyl_y(x,y,z,r,l,dir=1): return wp(cq.Solid.makeCylinder(r,l,cq.Vector(x,y,z),cq.Vector(0,dir,0)))
def cut(a,b): return wp(a.val().cut(b.val()))
def fuse(parts):
    s=parts[0].val()
    for p in parts[1:]: s=s.fuse(p.val())
    return wp(s)

def make_spur(teeth=50,module=1.0,face=4.0,bore=12.0,pa=20.0):
    rp=module*teeth/2; ra=rp+module; rf=max(0.2*module,rp-1.25*module)
    alpha=math.radians(pa); rb=rp*math.cos(alpha)
    def invol(r):
        if r<=rb: return 0.0
        q=math.sqrt(max(0,(r/rb)**2-1))
        return q-math.acos(min(1,rb/r))
    half=math.pi/(2*teeth)+math.tan(alpha)-alpha
    pts=[]; r0=max(rf,rb); radii=[r0+(ra-r0)*i/8 for i in range(9)]
    for k in range(teeth):
        a=k*2*math.pi/teeth
        pts.append((rf*math.cos(a-half),rf*math.sin(a-half)))
        for r in radii:
            t=a-half+invol(r); pts.append((r*math.cos(t),r*math.sin(t)))
        for r in reversed(radii):
            t=a+half-invol(r); pts.append((r*math.cos(t),r*math.sin(t)))
        pts.append((rf*math.cos(a+half),rf*math.sin(a+half)))
    clean=[]
    for p in pts:
        if not clean or math.dist(p,clean[-1])>1e-7: clean.append(p)
    g=cq.Workplane('XZ').polyline(clean).close().extrude(face/2,both=True)
    return g.cut(cq.Workplane('XZ').circle(bore/2).extrude(face,both=True))

def bearing_y(x,y,z):
    return cq.Workplane('XZ').circle(BEARING_OD/2).circle(BEARING_ID/2).extrude(BEARING_W/2,both=True).translate((x,y,z))

def side_plate(y):
    p=boxc(150,y,45,PLATE_L,PLATE_T,PLATE_H)
    for x in (75,125,175,225):
        p=cut(p,boxc(x,y,45,30,PLATE_T+1,36))
    for x in GEAR_X:
        p=cut(p,cyl_y(x,y-PLATE_T/2-0.1,Z,BEARING_OD/2+0.08,PLATE_T+0.2))
        for dx,dz in ((-17,-17),(-17,17),(17,-17),(17,17)):
            p=cut(p,cyl_y(x+dx,y-PLATE_T/2-0.1,Z+dz,2.1,PLATE_T+0.2))
    for x in (30,270):
        for z in (15,75): p=cut(p,cyl_y(x,y-PLATE_T/2-0.1,z,2.6,PLATE_T+0.2))
    return p

def wheel_photo_screen(side,x):
    # Photo/reconstruction screen from current master. NOT final QRW90SR/150 profile.
    pts=[(26,-12),(32,-12),(42,-8),(45,0),(42,8),(32,12),(8,12),(8,-2),(26,-2)]
    if side<0: pts=[(r,-yy) for r,yy in pts]
    w=cq.Workplane('XY').polyline(pts).close().revolve(360,(0,0),(0,1)).translate((x,side*WHEEL_Y,Z))
    w=cut(w,cyl_y(x,side*(WHEEL_Y-16),Z,6.1,32,dir=side))
    return w

def crossbar(x,z):
    length=2*(INNER_Y-PLATE_T/2)
    b=boxc(x,0,z,14,length,12)
    for side in (-1,1):
        b=cut(b,cyl_y(x,side*(length/2+0.1),z,2.6,10,dir=-side))
    return b

parts=[]
def add(name,shape,kind): parts.append((name,shape,kind)); return shape

for side in (-1,1):
    yi=side*INNER_Y; yo=side*OUTER_Y
    add(f'A1_INNER_PLATE_{side:+d}',side_plate(yi),'print')
    add(f'A1_OUTER_PLATE_{side:+d}',side_plate(yo),'print')
    for j,x in enumerate(GEAR_X):
        gear=make_spur(Z50_N,MOD,FACE,SHAFT_D,20).translate((x,side*GEAR_Y,Z))
        if j%2: gear=gear.rotate((x,side*GEAR_Y,Z),(x,side*GEAR_Y+1,Z),3.6)
        add(f'A1_Z50_TEST_{side:+d}_{int(x)}',gear,'test_gear')
        add(f'A1_SHAFT_{side:+d}_{int(x)}',cyl_y(x,side*(INNER_Y-8),Z,SHAFT_D/2,2*(OUTER_Y-INNER_Y+8),dir=side),'bench_shaft')
        add(f'A1_BEAR_IN_{side:+d}_{int(x)}',bearing_y(x,yi,Z),'bearing')
        add(f'A1_BEAR_OUT_{side:+d}_{int(x)}',bearing_y(x,yo,Z),'bearing')
    for x in WHEEL_X:
        add(f'A1_QRW90_SCREEN_{side:+d}_{int(x)}',wheel_photo_screen(side,x),'wheel_screen')
    y0=side*(GEAR_Y+2); y1=side*5.0
    ln=abs(y0-y1)
    add(f'A1_REAR_LONG_AXLE_{side:+d}',cyl_y(250,min(y0,y1),Z,SHAFT_D/2,ln,dir=1),'bench_shaft')

for x,z in ((35,20),(135,70),(235,20)):
    add(f'A1_CROSSBAR_{int(x)}',crossbar(x,z),'print')

for side in (-1,1):
    add(f'A1_Z40_ENVELOPE_{side:+d}', wp(cq.Solid.makeCone(20.37,14.3,2.41,cq.Vector(250,side*5.5,Z),cq.Vector(0,side,0))), 'bevel_screen')

compound=cq.Compound.makeCompound([s.val() for _,s,_ in parts])
exporters.export(compound,str(OUT/'PX1_A1_Rolling_6x6_Assembly.step'))

# Export print/tooling parts in local coordinates suitable for slicers.
def localize(shape):
    bb=shape.val().BoundingBox()
    return shape.translate((-(bb.xmin+bb.xmax)/2, -(bb.ymin+bb.ymax)/2, -bb.zmin))
master_plate=localize(side_plate(0))
exporters.export(master_plate,str(OUT/'PX1_A1_SidePlate.step'))
exporters.export(master_plate,str(OUT/'PX1_A1_SidePlate.stl'),tolerance=0.10,angularTolerance=0.18)
for i,(x,z) in enumerate(((35,20),(135,70),(235,20)),1):
    b=localize(crossbar(x,z))
    exporters.export(b,str(OUT/f'PX1_A1_Crossbar_{i}.step'))
    exporters.export(b,str(OUT/f'PX1_A1_Crossbar_{i}.stl'),tolerance=0.10,angularTolerance=0.18)
wheel=localize(wheel_photo_screen(1,0))
exporters.export(wheel,str(OUT/'PX1_A1_QRW90_SCREEN_ONLY.stl'),tolerance=0.10,angularTolerance=0.18)
gear=make_spur(Z50_N,MOD,FACE,SHAFT_D,20)
exporters.export(gear,str(OUT/'PX1_A1_Z50_m1_PA20_TEST.stl'),tolerance=0.06,angularTolerance=0.12)

pipe=cyl_x(0,0,PIPE_CZ,PIPE_R,300)
checks={}
for name,shape,kind in parts:
    if kind not in ('wheel_screen','print','bevel_screen'): continue
    v=shape.val().Volume(); inside=shape.val().intersect(pipe.val()).Volume(); outside=max(0.0,v-inside)
    checks[name]={'volume_mm3':v,'outside_DN150_mm3':outside,'outside_fraction':outside/v if v else 0.0}
maxfrac=max((d['outside_fraction'] for d in checks.values()),default=0)
bb=compound.BoundingBox()
validation={
  'status':'A1_ROLLING_FIXTURE_GENERATED__NOT_PRESSURE_BODY__NOT_PRODUCTION_RELEASE',
  'source_trace':{
    'DRW-002-374':'3 wheel stations/side, Z50 axle and idle gears, source bearings/seals',
    'DRW-002-375':'Z40 big bevel, 61800 support in housing',
    'DRW-002-386':'Z16 motor unit topology with two motors and 61801 supports'
  },
  'frozen':{'wheel_x_mm':WHEEL_X,'gear_x_mm':GEAR_X,'gear_plane_y_mm':[-GEAR_Y,GEAR_Y],'z_axis_mm':Z},
  'bench_substitutions':{'shaft_d_mm':SHAFT_D,'bearing':'6001-2RS 12x28x8','reason':'rapid A1 floor-running fixture; production axial stack remains H02/H04'},
  'wheel_status':'QRW90SR/150 photo-screen only; exact tire/quick-lock remains H01',
  'bbox_mm':{'xmin':bb.xmin,'xmax':bb.xmax,'ymin':bb.ymin,'ymax':bb.ymax,'zmin':bb.zmin,'zmax':bb.zmax},
  'dn150_screen':{'pipe_radius_mm':PIPE_R,'pipe_center_z_mm':PIPE_CZ,'max_component_outside_fraction':maxfrac,'note':'screen only, not acceptance; physical pipe jig still required'},
  'parts':len(parts),
  'next_interface':'rear x250 long axle -> matched Z40/Z16 -> two motor pack'
}
(OUT/'PX1_A1_Validation.json').write_text(json.dumps(validation,indent=2,ensure_ascii=False),encoding='utf-8')
print(json.dumps(validation,indent=2,ensure_ascii=False))
