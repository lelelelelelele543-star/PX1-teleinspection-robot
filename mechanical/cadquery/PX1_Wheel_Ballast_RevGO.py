import cadquery as cq
import math, json, os

# PX-1 Rev.GO — interchangeable tread candidates + removable belly ballast
# Prototype geometry only; NOT machining release.

OUT=os.path.abspath('build_revgo')
os.makedirs(OUT, exist_ok=True)

PIPE_R=75.0
PIPE_Z=52.0480547
BODY_Z0=8.0
BODY_HALF_W=46.0
SIDE_COVER_OUT=51.0

# Active Rev.GF wheel outer profile, converted to local axial coordinates.
GLOBAL_Y=[51.25,53.00,55.00,58.00,61.00,64.00,67.00,70.00,71.00]
OUTER_R=[45.00,45.00,43.80,40.38,36.45,31.90,26.50,18.00,15.50]
Y0=GLOBAL_Y[0]
AX=[y-Y0 for y in GLOBAL_Y]
TIRE_RADIAL=4.0
INNER_R=[max(10.5,r-TIRE_RADIAL) for r in OUTER_R]
BORE_R=8.5 # Ø17 wheel seat


def revolve_shell(ax, outer_r, inner_r):
    pts=[(x,r) for x,r in zip(ax,outer_r)] + [(x,r) for x,r in reversed(list(zip(ax,inner_r)))]
    return cq.Workplane('XY').polyline(pts).close().revolve(360,(0,0),(1,0)).rotate((0,0,0),(0,0,1),90)


def revolve_core(ax, inner_r, bore_r):
    # Metal core follows tire inner profile and closes to the keyed Ø17 bore.
    pts=[(x,r) for x,r in zip(ax,inner_r)] + [(ax[-1],bore_r),(ax[0],bore_r)]
    core=cq.Workplane('XY').polyline(pts).close().revolve(360,(0,0),(1,0)).rotate((0,0,0),(0,0,1),90)
    # Keyway only on the 7 mm wheel-seat span. 4 mm wide, 2 mm radial depth in hub.
    key_y0=(62.15-Y0)
    key_len=7.0
    key=(cq.Workplane('XY').box(4.0,key_len,4.0,centered=(True,False,False))
         .translate((0,key_y0,BORE_R-0.2)))
    return core.cut(key)


def high_grip_slots(tire):
    # Geometry-only tread candidate: 18 transverse slots, cut inward so outer envelope never grows.
    out=tire
    axial_center=3.0
    axial_span=6.0
    tangential_w=1.4
    radial_depth=1.8
    for a in range(0,360,20):
        slot=(cq.Workplane('XY').box(tangential_w,axial_span,radial_depth,centered=(True,True,True))
              .translate((0,axial_center,44.1)))
        slot=slot.rotate((0,0,0),(0,1,0),a)
        out=out.cut(slot)
    return out

sr_tire=revolve_shell(AX,OUTER_R,INNER_R)
hg_tire=high_grip_slots(sr_tire)
core=revolve_core(AX,INNER_R,BORE_R)

# Belly ballast: same planform for 1/2/3 x 5 mm stainless plates.
BALLAST_X0=30.0
BALLAST_L=250.0
BALLAST_W=50.0
PLATE_T=5.0
CORNER_R=6.0

# Rounded 2D rectangle extruded downward from the body belly plane.
plate2d=(cq.Workplane('XY').rect(BALLAST_L-2*CORNER_R,BALLAST_W).extrude(PLATE_T)
         .union(cq.Workplane('XY').rect(BALLAST_L,BALLAST_W-2*CORNER_R).extrude(PLATE_T)))
for sx in (-1,1):
    for sy in (-1,1):
        c=cq.Workplane('XY').center(sx*(BALLAST_L/2-CORNER_R),sy*(BALLAST_W/2-CORNER_R)).circle(CORNER_R).extrude(PLATE_T)
        plate2d=plate2d.union(c)
plate=plate2d.translate((BALLAST_X0+BALLAST_L/2,0,BODY_Z0-PLATE_T))

# Four M5 clearance references; body side uses blind local bosses, never through P0.
HOLES=[(65,-18),(65,18),(245,-18),(245,18)]
for x,y in HOLES:
    hole=(cq.Workplane('XY').center(x,y).circle(2.75).extrude(PLATE_T+1).translate((0,0,BODY_Z0-PLATE_T-0.5)))
    plate=plate.cut(hole)

# Maximum 3-plate stack envelope.
ballast_stack=plate
for i in (1,2):
    ballast_stack=ballast_stack.union(plate.translate((0,0,-i*PLATE_T)))

# DN150 radial sanity check on relevant fixed cross-section envelopes.
def radial(y,z): return math.hypot(y,z-PIPE_Z)
ballast_corners=[(BALLAST_W/2,BODY_Z0),(-BALLAST_W/2,BODY_Z0),(BALLAST_W/2,BODY_Z0-3*PLATE_T),(-BALLAST_W/2,BODY_Z0-3*PLATE_T)]
ballast_max=max(radial(y,z) for y,z in ballast_corners)
ballast_margin=PIPE_R-ballast_max
sidecover_lower=PIPE_R-radial(SIDE_COVER_OUT,6.0)

# Weight / CG screen for stainless 7.85 g/cc.
rho=7.85e-6 # kg/mm3
plate_mass=BALLAST_L*BALLAST_W*PLATE_T*rho # conservative ignores corner rounding/holes
base_mass=7.0
base_cg=(153.0,0.0,48.0)
plate_cg=(BALLAST_X0+BALLAST_L/2,0.0,BODY_Z0-1.5*PLATE_T/2) # center of 3-plate stack
stack_mass=3*plate_mass
combined_cgx=(base_mass*base_cg[0]+stack_mass*plate_cg[0])/(base_mass+stack_mass)
combined_cgz=(base_mass*base_cg[2]+stack_mass*plate_cg[2])/(base_mass+stack_mass)

metrics={
    'wheel_outer_width_mm':AX[-1]-AX[0],
    'wheel_tire_valid':sr_tire.val().isValid(),
    'wheel_hg_valid':hg_tire.val().isValid(),
    'wheel_core_valid':core.val().isValid(),
    'tread_variants':['SR smooth/compliant candidate','HG 18-slot candidate; same outer envelope'],
    'ballast_plate_plan_mm':[BALLAST_L,BALLAST_W,PLATE_T],
    'ballast_single_plate_mass_screen_kg':plate_mass,
    'ballast_three_plate_mass_screen_kg':stack_mass,
    'ballast_max_stack_dn150_margin_mm':ballast_margin,
    'existing_sidecover_lower_corner_margin_mm':sidecover_lower,
    'base_nominal_cg_xz_mm':[base_cg[0],base_cg[2]],
    'with_three_plate_cg_xz_mm':[combined_cgx,combined_cgz],
    'body_attachment':'4 x M5 blind local thickened floor bosses; no through-hole into P0',
    'status':'PASS geometry screen; exact tread material and ballast fastener bosses remain prototype gates'
}

cq.exporters.export(sr_tire,os.path.join(OUT,'PX1_Wheel90_SR_RevGO.step'))
cq.exporters.export(hg_tire,os.path.join(OUT,'PX1_Wheel90_HG_RevGO.step'))
cq.exporters.export(core,os.path.join(OUT,'PX1_Wheel90_Core_RevGO.step'))
cq.exporters.export(ballast_stack,os.path.join(OUT,'PX1_Ballast_3x5mm_RevGO.step'))
with open(os.path.join(OUT,'REV_GO_VALIDATION.json'),'w') as f: json.dump(metrics,f,indent=2)
print(json.dumps(metrics,indent=2))
