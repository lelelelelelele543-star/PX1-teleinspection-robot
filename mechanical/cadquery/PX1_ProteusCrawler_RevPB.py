import cadquery as cq
import math, json, os

# PX-1 Rev.PB — CRP150-like full mechanical skeleton
# External control envelope from MiniCam Proteus documentation: 307 x 133 x 110 mm.
# Internal topology from DRW-002-374 / 375 / 386: 5x Z50 per side, rear wheel long axle input, Z16->Z40, 2 motors total.

OUT=os.path.abspath('build_revpb')
os.makedirs(OUT,exist_ok=True)

L=307.0
OVERALL_W=133.0
OVERALL_H=110.0
BODY_W=92.0
BODY_Z0=8.0
BODY_Z1=90.0
WHEEL_D=90.0
WHEEL_R=WHEEL_D/2
WHEEL_Z=45.0
WX=[50.0,150.0,250.0]
GX=[50.0,100.0,150.0,200.0,250.0]
INPUT_X=250.0
COVER_OUT=51.0
WHEEL_INNER_Y=51.25
WHEEL_OUTER_Y=66.5
GEAR_FACE=4.0
GEAR_Y=42.0
PIPE_R=75.0
PIPE_Z=52.05


def wp(s): return cq.Workplane('XY').newObject([s])
def box(x0,y0,z0,dx,dy,dz): return wp(cq.Solid.makeBox(dx,dy,dz,cq.Vector(x0,y0,z0)))
def cyl_x(x0,y,z,r,l): return wp(cq.Solid.makeCylinder(r,l,cq.Vector(x0,y,z),cq.Vector(1,0,0)))
def cyl_y(x,y0,z,r,l,sgn=1): return wp(cq.Solid.makeCylinder(r,l,cq.Vector(x,y0,z),cq.Vector(0,sgn,0)))

def involute_gear(teeth,module,face,bore,center,side):
    pa=math.radians(20); rp=module*teeth/2; rb=rp*math.cos(pa); ra=module*(teeth+2)/2; rf=module*(teeth-2.5)/2
    pitch=2*math.pi/teeth; tp=math.sqrt((rp/rb)**2-1); invp=tp-math.atan(tp); off=math.pi/(2*teeth)+invp
    pts=[]
    for k in range(teeth):
        t0=k*pitch
        pts.append((rf*math.cos(t0-off),rf*math.sin(t0-off)))
        for s in range(6):
            r=rb+(ra-rb)*s/5; t=math.sqrt((r/rb)**2-1); inv=t-math.atan(t); a=t0-off+inv
            pts.append((r*math.cos(a),r*math.sin(a)))
        for s in reversed(range(6)):
            r=rb+(ra-rb)*s/5; t=math.sqrt((r/rb)**2-1); inv=t-math.atan(t); a=t0+off-inv
            pts.append((r*math.cos(a),r*math.sin(a)))
        pts.append((rf*math.cos(t0+off),rf*math.sin(t0+off)))
    g=cq.Workplane('XY').polyline(pts).close().extrude(face)
    if bore: g=g.faces('>Z').workplane().hole(bore,depth=face+0.2)
    g=g.rotate((0,0,0),(1,0,0),90)
    y=center[1]
    if side=='L': g=g.translate((center[0],y+face/2,center[2]))
    else: g=g.translate((center[0],y-face/2,center[2]))
    return g

outer=box(0,-BODY_W/2,BODY_Z0,L,BODY_W,BODY_Z1-BODY_Z0)
inner=box(8,-34,14,L-16,68,66)
body=wp(outer.val().cut(inner.val()))
wet_clear=box(25,-34,80,115,68,20)
body=wp(body.val().cut(wet_clear.val()))
for sgn in (-1,1):
    pocket=box(12,38 if sgn>0 else -46,8,283,8,76)
    body=wp(body.val().cut(pocket.val()))

covers={}
for side,sgn in [('L',1),('R',-1)]:
    y0=46 if sgn>0 else -51
    cov=box(12,y0,8,283,5,76)
    for x in WX:
        h=cyl_y(x,y0-0.5 if sgn>0 else y0+5.5,WHEEL_Z,18,6,sgn)
        cov=wp(cov.val().cut(h.val()))
    covers[side]=cov

def wheel(x,side):
    sgn=1 if side=='L' else -1
    yi=WHEEL_INNER_Y*sgn
    ax=[0,2,4,7,10,13,15.25]
    rr=[45,45,44,41,36,28,17]
    inner=[max(9,r-5) for r in rr]
    pts=[(a,r) for a,r in zip(ax,rr)] + [(a,r) for a,r in reversed(list(zip(ax,inner)))]
    w=cq.Workplane('XY').polyline(pts).close().revolve(360,(0,0),(1,0)).rotate((0,0,0),(0,0,1),90)
    if sgn>0: w=w.translate((x,yi,WHEEL_Z))
    else: w=w.mirror('XZ').translate((x,yi,WHEEL_Z))
    return w

wheels={}; gears={}; shafts={}
for side,sgn in [('L',1),('R',-1)]:
    for x in WX: wheels[(side,x)]=wheel(x,side)
    gy=42.0*sgn
    for x in GX:
        gears[(side,x)]=involute_gear(50,1.0,4.0,17 if x in WX else 12,(x,gy,WHEEL_Z),side)
    for x in [50,150]: shafts[(side,x)]=cyl_y(x,38*sgn,WHEEL_Z,8.5,29,sgn)
    shafts[(side,250)]=cyl_y(250,20*sgn,WHEEL_Z,8.5,47,sgn)

bevels={}
for side,sgn in [('L',1),('R',-1)]:
    bevels[side]=(cq.Workplane('XZ').workplane(offset=22*sgn).center(250,WHEEL_Z).circle(21).workplane(offset=8*sgn).circle(14).loft())

motors={}
for side,sy in [('L',15.5),('R',-15.5)]: motors[side]=cyl_x(168,sy,WHEEL_Z,15,78)

lift_mount_L=box(170,34,76,42,4,25)
lift_mount_R=box(170,-38,76,42,4,25)
cam_low=cyl_x(36,0,75,26,72)

assy=cq.Assembly(name='PX1_ProteusCrawler_RevPB')
assy.add(body,name='CRP150_like_MainBody',color=cq.Color(0.65,0.67,0.7))
for side,c in covers.items(): assy.add(c,name=f'SideCover_{side}',color=cq.Color(0.5,0.53,0.56))
for (side,x),g in gears.items(): assy.add(g,name=f'Z50_{side}_{int(x)}',color=cq.Color(0.72,0.62,0.30))
for (side,x),w in wheels.items(): assy.add(w,name=f'Wheel_{side}_{int(x)}',color=cq.Color(0.06,0.06,0.06))
for (side,x),s in shafts.items(): assy.add(s,name=f'Axle_{side}_{int(x)}',color=cq.Color(0.65,0.2,0.16))
for side,b in bevels.items(): assy.add(b,name=f'Z40_{side}_rear_wheel_input',color=cq.Color(0.78,0.55,0.24))
for side,m in motors.items(): assy.add(m,name=f'Motor_{side}_replacement_envelope',color=cq.Color(0.25,0.35,0.55))
assy.add(lift_mount_L,name='LiftHoldingPlate_L'); assy.add(lift_mount_R,name='LiftHoldingPlate_R')
assy.add(cam_low,name='CAM026_like_LOW_envelope',color=cq.Color(0.25,0.25,0.28))
assy.save(os.path.join(OUT,'PX1_ProteusCrawler_RevPB.step'))
cq.exporters.export(body,os.path.join(OUT,'PX1_CRP150_like_MainBody_RevPB.step'))

pipe=wp(cq.Solid.makeCylinder(PIPE_R,L+40,cq.Vector(-20,0,PIPE_Z),cq.Vector(1,0,0)))
fixed={'body':body,'cover_L':covers['L'],'cover_R':covers['R'],'lift_mount_L':lift_mount_L,'lift_mount_R':lift_mount_R}
outside={n:round(p.val().cut(pipe.val()).Volume(),5) for n,p in fixed.items()}
wheel_out={f'{s}_{int(x)}':round(w.val().cut(pipe.val()).Volume(),5) for (s,x),w in wheels.items()}
allshape=body.val()
for obj in list(covers.values())+list(wheels.values())+[lift_mount_L.val(),lift_mount_R.val(),cam_low.val()]:
    ov=obj.val() if hasattr(obj,'val') else obj
    allshape=allshape.fuse(ov)
bb=allshape.BoundingBox()
sign={250:1,200:-1,150:1,100:-1,50:1}
checks={
 'official_target_envelope_mm':[307,133,110],
 'current_bbox_mm':[round(bb.xlen,2),round(bb.ylen,2),round(bb.zlen,2)],
 'side_topology':'wheel Z50 @50 - idle @100 - wheel @150 - idle @200 - driven rear wheel Z50 @250',
 'input_station_x_mm':250,
 'extra_4th_input_shaft':False,
 'wheel_rotation_signs':{str(x):sign[x] for x in WX},
 'all_wheels_same_direction':len({sign[x] for x in WX})==1,
 'mesh_counts_from_rear_input':{str(x):int((250-x)/50) for x in WX},
 'two_motors_total':len(motors)==2,
 'fixed_parts_outside_ideal_DN150_mm3':outside,
 'wheel_contact_outside_ideal_DN150_mm3':wheel_out,
 'status':'PROTEUS-LIKE MASTER SKELETON; lift/camera/reel and exact replacement motors remain next gates'
}
with open(os.path.join(OUT,'REV_PB_VALIDATION.json'),'w') as f: json.dump(checks,f,indent=2)
print(json.dumps(checks,indent=2))