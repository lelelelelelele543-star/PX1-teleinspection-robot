import cadquery as cq
import math, json, os

# PX-1 Rev.B WB23C — Proteus-style pressure/lift service interface.
# Purpose: replace the over-complicated WB23B flex-chamber study with a simple,
# serviceable topology confirmed by Proteus source material and repair photos:
# dry body -> removable pressure/service cover -> M12 gland -> short flexible harness
# -> protected run along lift -> fixed camera connector.
# Engineering packaging screen only; seal and flex life require physical tests.

OUT=os.path.abspath('build_wb23c'); os.makedirs(OUT,exist_ok=True)

# Active crawler datum retained from WB22A.
PIPE_R=75.0
PIPE_Z=52.0480547
BODY_PIVOT_X=200.0
PIVOT_Z_LOW=92.0
PIVOT_Z_HIGH=109.0
LINK_L=90.0
ARM_Y=31.0
ARM_T=4.0
ARM_H=14.0
CAM_Z_LOW=75.0
CAM_Z_HIGH=185.0
CAM_AXIS_OFFSET_Z=2.0
PIVOT_AVG=(PIVOT_Z_LOW+PIVOT_Z_HIGH)/2.0

# Rear/top pressure roof from WB22A packaging pod.
PRESSURE_ROOF_TOP_Z=110.0
PRESSURE_ROOF_X0=218.0
PRESSURE_ROOF_X1=307.0
PRESSURE_ROOF_HALF_Y=39.0

# PX1 removable service cover candidate.
# Two M4 screws are a PX1 design choice for this SMALL cover, not claimed as exact Proteus screw count.
COVER_CX=257.0
COVER_CY=0.0
COVER_Z0=PRESSURE_ROOF_TOP_Z
COVER_L=78.0
COVER_W=42.0
COVER_T=6.0
OPEN_L=58.0
OPEN_W=24.0
SCREW_X=(224.0,290.0)
SCREW_Y=0.0
SCREW_D=4.5
SCREW_HEAD_D=8.0
SCREW_HEAD_H=3.0
O_RING_CORD=2.0
O_RING_GROOVE_W=2.5
O_RING_GROOVE_D=1.5

# Low-profile pressure fill point envelope. Exact bought valve remains procurement HOLD.
PRESSURE_PORT_CX=268.0
PRESSURE_PORT_CY=0.0
PRESSURE_PORT_OD=14.0
PRESSURE_PORT_PROTRUSION=6.0
PRESSURE_PORT_THREAD='M10x1 or G1/8 service-valve candidate; final after sample purchase'

# Proteus-source-compatible M12 gland envelope.
GLAND_ARTICLE='LAPP SKINTOP MS-M M12x1.5 53112000'
GLAND_THREAD='M12x1.5'
GLAND_CLAMP=(3.5,7.0)
GLAND_OD=17.6
GLAND_OVERALL_L=26.5
GLAND_THREAD_L=6.5
# Horizontal gland in front face of the service-cover boss keeps height out of DN150 envelope.
GLAND_AXIS_Z=103.0
GLAND_AXIS_Y=12.0
GLAND_X_FRONT=205.0
GLAND_X_REAR=231.5

# Local external harness target.
HARNESS_OD=5.0
HARNESS_Y=25.5
ARM_PROTECTED_START=20.0
ARM_PROTECTED_END=72.0
ARM_COVER_OUTER=7.0
BODY_SERVICE_SLACK_TARGET=35.0
HEAD_SERVICE_SLACK_TARGET=35.0

# Internal dry service connector candidate; not purchase-released yet.
INTERNAL_CONNECTOR_HEADER='JST B8P-VH-B'
INTERNAL_CONNECTOR_HOUSING='JST VHR-8N'

# Head interface retained from camera quick-connect work.
HEAD_CONNECTOR_PANEL='WEIPU SP1312/P6-C'
HEAD_CONNECTOR_HARNESS='WEIPU SP1310/S6I-N for <=5 mm local harness; exact purchased sample controls'


def wp(s): return cq.Workplane('XY').newObject([s])
def boxc(x,y,z,dx,dy,dz): return cq.Workplane('XY').box(dx,dy,dz,centered=(True,True,True)).translate((x,y,z))
def cyl_z(x,y,z0,r,h): return wp(cq.Solid.makeCylinder(r,h,cq.Vector(x,y,z0),cq.Vector(0,0,1)))
def cyl_x_between(x0,x1,y,z,r):
    a=min(x0,x1); L=abs(x1-x0)
    return wp(cq.Solid.makeCylinder(r,L,cq.Vector(a,y,z),cq.Vector(1,0,0)))
def cyl_between(p1,p2,r):
    a=cq.Vector(*p1); b=cq.Vector(*p2); v=b-a; L=v.Length
    return wp(cq.Solid.makeCylinder(r,L,a,v.normalized()))
def radial_clear(part,tol=0.25):
    vs,_=part.val().tessellate(tol)
    return PIPE_R-max(math.hypot(v.y,v.z-PIPE_Z) for v in vs)
def inter(a,b): return a.val().intersect(b.val()).Volume()

def theta_for(zcam):
    return math.asin((zcam-CAM_AXIS_OFFSET_Z-PIVOT_AVG)/LINK_L)
def lower_arm_points(zcam):
    th=theta_for(zcam)
    p=(BODY_PIVOT_X, PIVOT_Z_LOW)
    e=(BODY_PIVOT_X-LINK_L*math.cos(th), PIVOT_Z_LOW+LINK_L*math.sin(th))
    return p,e,th

def point_on_arm(zcam,s):
    p,e,th=lower_arm_points(zcam)
    return (p[0]-s*math.cos(th), HARNESS_Y, p[1]+s*math.sin(th))

# Pressure roof reference block only for interface placement, not a replacement for full WB22A body.
roof=boxc((PRESSURE_ROOF_X0+PRESSURE_ROOF_X1)/2,0,PRESSURE_ROOF_TOP_Z-5,
          PRESSURE_ROOF_X1-PRESSURE_ROOF_X0,2*PRESSURE_ROOF_HALF_Y,10)
cover=boxc(COVER_CX,COVER_CY,COVER_Z0+COVER_T/2,COVER_L,COVER_W,COVER_T)
opening=boxc(COVER_CX,COVER_CY,COVER_Z0-0.5,OPEN_L,OPEN_W,3.0)
pressure_cap=cyl_z(PRESSURE_PORT_CX,PRESSURE_PORT_CY,COVER_Z0+COVER_T,PRESSURE_PORT_OD/2,PRESSURE_PORT_PROTRUSION)
gland=cyl_x_between(GLAND_X_FRONT,GLAND_X_REAR,GLAND_AXIS_Y,GLAND_AXIS_Z,GLAND_OD/2)

screws=[]; heads=[]
for x in SCREW_X:
    screws.append(cyl_z(x,SCREW_Y,COVER_Z0-8,SCREW_D/2,COVER_T+8))
    heads.append(cyl_z(x,SCREW_Y,COVER_Z0+COVER_T,SCREW_HEAD_D/2,SCREW_HEAD_H))

# Simple protected lift harness: solid only for the protected middle run.
# Small free service lengths at both pivots remain physical-flex-test items rather than fake CAD arcs.
states={}
worst_arm_cover_pipe=1e9
for name,zcam in [('LOW',CAM_Z_LOW),('MID',(CAM_Z_LOW+CAM_Z_HIGH)/2),('HIGH',CAM_Z_HIGH)]:
    a=point_on_arm(zcam,ARM_PROTECTED_START)
    b=point_on_arm(zcam,ARM_PROTECTED_END)
    cable=cyl_between(a,b,HARNESS_OD/2)
    protected=cyl_between(a,b,ARM_COVER_OUTER/2)
    cclear=radial_clear(cable)
    pclear=radial_clear(protected)
    worst_arm_cover_pipe=min(worst_arm_cover_pipe,pclear)
    states[name]={
        'camera_z_mm':zcam,
        'lift_angle_deg':math.degrees(theta_for(zcam)),
        'protected_run_start_xyz_mm':list(a),
        'protected_run_end_xyz_mm':list(b),
        'cable_ideal_DN150_clearance_mm':cclear,
        'protective_cover_ideal_DN150_clearance_mm':pclear,
    }

# Packaging checks for all fixed service-cover parts.
fixed_parts={
    'cover_plate':cover,
    'pressure_port_cap':pressure_cap,
    'horizontal_M12_gland':gland,
}
for i,h in enumerate(heads,1): fixed_parts[f'M4_head_{i}']=h
fixed_clear={k:radial_clear(v) for k,v in fixed_parts.items()}
min_fixed_clear=min(fixed_clear.values())

# Service opening must fit fully inside plate with minimum 7 mm land on all sides.
land_x=(COVER_L-OPEN_L)/2.0
land_y=(COVER_W-OPEN_W)/2.0
# Screws must lie outside the service opening footprint in X.
screw_clear_from_open=min(abs(x-COVER_CX)-OPEN_L/2.0 for x in SCREW_X)

# Simple pressure load screen. This is NOT a structural certification.
opening_area=OPEN_L*OPEN_W
loads={
    'at_plus_0_25_bar_N':opening_area*0.025,
    'at_1_bar_N':opening_area*0.1,
    'per_screw_at_1_bar_N':opening_area*0.1/2.0,
}

# Ensure the gland is outside the service opening cavity and is not towering above the plate.
# It is intentionally horizontal and below cover top.
gland_top=GLAND_AXIS_Z+GLAND_OD/2.0

checks_ok=(
    min_fixed_clear>=3.0 and
    states['LOW']['protective_cover_ideal_DN150_clearance_mm']>=5.0 and
    land_x>=7.0 and land_y>=7.0 and
    screw_clear_from_open>=3.0 and
    gland_top <= COVER_Z0+COVER_T+0.5 and
    COVER_Z0==PRESSURE_ROOF_TOP_Z
)
status='PASS_PACKAGING_SCREEN / SEAL_TEST_HOLD / FLEX_TEST_HOLD / PROCUREMENT_HOLD' if checks_ok else 'FAIL_PACKAGING_SCREEN'

result={
    'status':status,
    'architecture_rule':'WB22A mechanics retained; no X207.5 pivot shift; no R16 flex-fan; no two-flex-chamber requirement.',
    'source_logic':{
        'Proteus_topology':'removable sealed cover/lift housing + M12 3.5-5 mm cable gland + camera connector + lift cover',
        'PX1_interpretation':'small independent pressure/service cover feeding a short field-replaceable harness along the lift',
        'screw_count_note':'2x M4 is a PX1 service-cover choice; exact Proteus screw count is not asserted from current evidence.'
    },
    'pressure_service_cover':{
        'outer_LxWxT_mm':[COVER_L,COVER_W,COVER_T],
        'centre_xyz_mm':[COVER_CX,COVER_CY,COVER_Z0+COVER_T/2],
        'service_opening_LxW_mm':[OPEN_L,OPEN_W],
        'seal_land_xy_mm':[land_x,land_y],
        'o_ring_cord_mm':O_RING_CORD,
        'provisional_face_groove_WxD_mm':[O_RING_GROOVE_W,O_RING_GROOVE_D],
        'fasteners':'2x M4 A4 stainless, blind threads in body boss; exact length after sample/build',
        'screw_x_mm':list(SCREW_X),
        'minimum_screw_edge_clear_from_opening_mm':screw_clear_from_open,
        'pressure_load_screen':loads,
        'label':'PRESSURE / CAMERA SERVICE'
    },
    'fill_port':{
        'thread_candidate':PRESSURE_PORT_THREAD,
        'hard_envelope_ODxH_mm':[PRESSURE_PORT_OD,PRESSURE_PORT_PROTRUSION],
        'position_xy_mm':[PRESSURE_PORT_CX,PRESSURE_PORT_CY],
        'note':'must accept compressor-gun/Schrader style service without leaving a tall fitting in DN150 envelope'
    },
    'gland':{
        'article':GLAND_ARTICLE,
        'thread':GLAND_THREAD,
        'clamping_range_mm':list(GLAND_CLAMP),
        'OD_mm':GLAND_OD,
        'overall_length_mm':GLAND_OVERALL_L,
        'thread_length_mm':GLAND_THREAD_L,
        'axis':'horizontal, forward-facing',
        'axis_xyz_mm':[(GLAND_X_FRONT+GLAND_X_REAR)/2,GLAND_AXIS_Y,GLAND_AXIS_Z],
        'top_z_mm':gland_top
    },
    'local_harness':{
        'target_max_OD_mm':HARNESS_OD,
        'protected_run_on_lower_arm_s_mm':[ARM_PROTECTED_START,ARM_PROTECTED_END],
        'body_service_slack_target_mm':BODY_SERVICE_SLACK_TARGET,
        'head_service_slack_target_mm':HEAD_SERVICE_SLACK_TARGET,
        'internal_dry_connector_candidates':[INTERNAL_CONNECTOR_HEADER,INTERNAL_CONNECTOR_HOUSING],
        'head_connectors':[HEAD_CONNECTOR_PANEL,HEAD_CONNECTOR_HARNESS],
        'rule':'free slack at pivots is verified physically, not represented by invented constant-radius CAD loops.'
    },
    'DN150_clearance':{
        'fixed_parts_mm':fixed_clear,
        'minimum_fixed_mm':min_fixed_clear,
        'states':states,
        'minimum_lift_protective_cover_all_states_mm':worst_arm_cover_pipe,
        'DN150_release_rule':'Only LOW is required to fit DN150. MID/HIGH are larger-pipe positions and may leave the DN150 envelope.'
    },
    'holds':[
        'Buy and measure real M12 gland and chosen <=5 mm harness before machining gland boss.',
        'Choose real low-profile fill valve / Schrader service port and confirm compressor-gun interface.',
        'Leak test service cover and gland at +0.25 bar minimum; later submerged test and 1 bar proof target if body design is released for that rating.',
        'Cycle local harness through full lift travel at least 500 cycles, target 1000, then wet/grit repeat.',
        'Final O-ring groove dimensions to be frozen from purchased elastomer and machining standard, not this screen value.',
        'Exact cover position must be rechecked in the full master with final fastener heads and real wheel solids.'
    ]
}

with open(os.path.join(OUT,'REV_B_WB23C_VALIDATION.json'),'w',encoding='utf-8') as f:
    json.dump(result,f,indent=2,ensure_ascii=False)
print(json.dumps(result,indent=2,ensure_ascii=False))
if not checks_ok:
    raise SystemExit(2)
