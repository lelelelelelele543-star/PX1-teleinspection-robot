import cadquery as cq
import math, json, os

# PX-1 Rev.B WB24A — Proteus-like low-profile PRESSURE valve packaging screen.
# Validation only. NOT valve-detail or machining release.
OUT=os.path.abspath('build_wb24a'); os.makedirs(OUT, exist_ok=True)

PIPE_R=75.0; PIPE_Z=52.0480547

# WB23E service-cover baseline
COVER_CX=261.0; COVER_CY=0.0; COVER_Z0=110.0
COVER_L=86.0; COVER_W=44.0; COVER_T=6.0
OPEN_L=48.0; OPEN_W=22.0
SCREW_X=(226.0,296.0); SCREW_HEAD_D=8.0; SCREW_HEAD_H=3.0
GLAND_OD=17.6; GLAND_AXIS_Y=12.0; GLAND_AXIS_Z=103.0
GLAND_X_FRONT=205.0; GLAND_X_REAR=231.5

# WB24A independent PX1 prototype envelope; source topology only, not source dimensions.
VALVE_X=273.0; VALVE_Y=0.0
CAP_OD=12.0; CAP_EXPOSED_H=1.5
SERVICE_THREAD='M8x1 candidate'
CARTRIDGE_OD=10.0; CARTRIDGE_DEPTH=18.0
CARTRIDGE_Z1=COVER_Z0+COVER_T
CARTRIDGE_Z0=CARTRIDGE_Z1-CARTRIDGE_DEPTH

# WB23G six-way dry connector packaging screen on the opposite side of the service opening.
DRY_CONN_CX=247.0; DRY_CONN_CY=0.0; DRY_CONN_CZ=101.5
DRY_CONN_L=14.0; DRY_CONN_W=12.0; DRY_CONN_H=7.0
RETAINER_OD=8.0; RETAINER_H=3.0

def wp(s): return cq.Workplane('XY').newObject([s])
def boxc(x,y,z,dx,dy,dz): return cq.Workplane('XY').box(dx,dy,dz,centered=(True,True,True)).translate((x,y,z))
def cyl_z(x,y,z0,r,h): return wp(cq.Solid.makeCylinder(r,h,cq.Vector(x,y,z0),cq.Vector(0,0,1)))
def cyl_x_between(x0,x1,y,z,r):
    a=min(x0,x1); L=abs(x1-x0)
    return wp(cq.Solid.makeCylinder(r,L,cq.Vector(a,y,z),cq.Vector(1,0,0)))
def inter(a,b): return a.val().intersect(b.val()).Volume()
def radial_clear(part,tol=0.15):
    vv,_=part.val().tessellate(tol)
    return PIPE_R-max(math.hypot(v.y,v.z-PIPE_Z) for v in vv)

cover=boxc(COVER_CX,COVER_CY,COVER_Z0+COVER_T/2,COVER_L,COVER_W,COVER_T)
heads=[cyl_z(x,0,COVER_Z0+COVER_T,SCREW_HEAD_D/2,SCREW_HEAD_H) for x in SCREW_X]
gland=cyl_x_between(GLAND_X_FRONT,GLAND_X_REAR,GLAND_AXIS_Y,GLAND_AXIS_Z,GLAND_OD/2)
cap=cyl_z(VALVE_X,VALVE_Y,COVER_Z0+COVER_T,CAP_OD/2,CAP_EXPOSED_H)
cartridge=cyl_z(VALVE_X,VALVE_Y,CARTRIDGE_Z0,CARTRIDGE_OD/2,CARTRIDGE_DEPTH)
retainer=cyl_z(VALVE_X,VALVE_Y,CARTRIDGE_Z0,RETAINER_OD/2,RETAINER_H)
dry_conn=boxc(DRY_CONN_CX,DRY_CONN_CY,DRY_CONN_CZ,DRY_CONN_L,DRY_CONN_W,DRY_CONN_H)

internal={
    'cartridge_vs_dry_connector_mm3': inter(cartridge,dry_conn),
    'cartridge_vs_gland_mm3': inter(cartridge,gland),
    'retainer_vs_dry_connector_mm3': inter(retainer,dry_conn),
}

def inside_opening_xy(part):
    bb=part.val().BoundingBox()
    return (bb.xmin >= COVER_CX-OPEN_L/2 and bb.xmax <= COVER_CX+OPEN_L/2 and
            bb.ymin >= -OPEN_W/2 and bb.ymax <= OPEN_W/2)

packaging={
    'cartridge_inside_service_opening_xy': inside_opening_xy(cartridge),
    'dry_connector_inside_service_opening_xy': inside_opening_xy(dry_conn),
    'cartridge_to_connector_x_gap_mm': (VALVE_X-CARTRIDGE_OD/2) - (DRY_CONN_CX+DRY_CONN_L/2),
    'cartridge_depth_below_cover_top_mm': CARTRIDGE_DEPTH,
}

fixed_dn150={
    'WB23E_cover_mm': radial_clear(cover),
    'WB24A_flush_cap_mm': radial_clear(cap),
    'M4_head_1_mm': radial_clear(heads[0]),
    'M4_head_2_mm': radial_clear(heads[1]),
    'horizontal_M12_gland_mm': radial_clear(gland),
}

cap_sensitivity={}
for h in (1.0,1.5,2.0,2.5,3.0,4.0,5.0):
    p=cyl_z(VALVE_X,VALVE_Y,COVER_Z0+COVER_T,CAP_OD/2,h)
    cap_sensitivity[f'{h:.1f}mm']=radial_clear(p)

checks_ok=(
    all(v < 1e-5 for v in internal.values()) and
    all(packaging[k] for k in ('cartridge_inside_service_opening_xy','dry_connector_inside_service_opening_xy')) and
    packaging['cartridge_to_connector_x_gap_mm'] >= 5.0 and
    fixed_dn150['WB24A_flush_cap_mm'] >= 5.0 and
    fixed_dn150['WB23E_cover_mm'] >= 5.0
)
status='PASS_FLUSH_VALVE_PACKAGING_SCREEN / VALVE_DETAIL_HOLD / LEAK_TEST_HOLD / MACHINING_HOLD' if checks_ok else 'FAIL_FLUSH_VALVE_PACKAGING_SCREEN'

result={
    'status':status,
    'pressure_port':{
        'xy_mm':[VALVE_X,VALVE_Y],
        'service_thread_candidate':SERVICE_THREAD,
        'protection_cap_OD_mm':CAP_OD,
        'protection_cap_exposed_height_mm':CAP_EXPOSED_H,
        'internal_cartridge_OD_mm':CARTRIDGE_OD,
        'internal_cartridge_depth_mm':CARTRIDGE_DEPTH,
        'source_inspiration':'MiniCam guided valve/check topology; PX1 dimensions independent',
    },
    'internal_packaging':packaging,
    'unintended_intersections_mm3':internal,
    'ideal_DN150_fixed_clearance_mm':fixed_dn150,
    'cap_height_sensitivity_OD12_mm':cap_sensitivity,
    'result_note':'With a <=OD12 x 1.5 mm driving cap, the pressure port is no longer the limiting top feature; the WB23E cover itself is lower-clearance. Fill adaptor is a service tool and is excluded from driving envelope.',
    'holds':[
        'valve seat/poppet/shaft detail dimensions not released',
        'M8x1 thread is prototype candidate only',
        'spring preload/rate not released',
        'real FKM seat and O-ring gland dimensions not released',
        '+0.25 bar decay/submersion and contamination test mandatory',
    ]
}
with open(os.path.join(OUT,'REV_B_WB24A_VALIDATION.json'),'w',encoding='utf-8') as f: json.dump(result,f,indent=2)
print(json.dumps(result,indent=2))
if not checks_ok: raise SystemExit(2)
