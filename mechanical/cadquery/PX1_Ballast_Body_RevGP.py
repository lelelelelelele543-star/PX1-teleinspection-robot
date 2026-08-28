import cadquery as cq
import math, json, os

# PX-1 Rev.GP — blind-boss ballast integration into active pressure body
# Prototype geometry only; NOT machining release.

OUT=os.path.abspath('build_revgp_ballast')
os.makedirs(OUT,exist_ok=True)

# Active Rev.GJ/GL body envelopes.
MAIN_L=307.0
BODY_W=92.0
Z0=8.0
ZTOP=90.0
P0_HALF_OUT=46.0
P0_HALF_IN=34.0
POD_X0=299.0
TOTAL_L=340.0
POD_HALF_W=38.0
POD_Z0=23.0
POD_Z1=67.0


def wp(s): return cq.Workplane('XY').newObject([s])
def box(x0,y0,z0,dx,dy,dz): return wp(cq.Solid.makeBox(dx,dy,dz,cq.Vector(x0,y0,z0)))
def cyl_z(x,y,z0,r,h): return wp(cq.Solid.makeCylinder(r,h,cq.Vector(x,y,z0),cq.Vector(0,0,1)))
def fuse(a,b): return wp(a.val().fuse(b.val()))
def cut(a,b): return wp(a.val().cut(b.val()))
def inter(a,b): return a.val().intersect(b.val()).Volume()

main_outer=box(0,-P0_HALF_OUT,Z0,MAIN_L,BODY_W,ZTOP-Z0)
pod_outer=box(POD_X0,-POD_HALF_W,POD_Z0,TOTAL_L-POD_X0,2*POD_HALF_W,POD_Z1-POD_Z0)
outer=fuse(main_outer,pod_outer)
main_inner=box(8,-P0_HALF_IN,14,MAIN_L-8,68,71)
pod_inner=box(POD_X0,-P0_HALF_IN,27,(TOTAL_L-8)-POD_X0,68,36)
inner=fuse(main_inner,pod_inner)
body=cut(outer,inner)

# Rev.GP refines Rev.GO to 4 mm plates so standard screw lengths maintain
# constant 8 mm thread engagement: M5x12 / M5x16 / M5x20 for 1/2/3 plates.
PLATE_X0=55.0
PLATE_L=225.0
PLATE_W=50.0
PLATE_T=4.0
N_PLATES=3
BOSS_R=6.5
BOSS_H=5.0
BOSS_Z0=14.0
TAP_D=4.2
BLIND_DEPTH=9.0
HOLES=[(105,-18),(105,18),(245,-18),(245,18)]

# Add local internal bosses; they are pressure-body material, not separate penetrators.
for x,y in HOLES:
    body=fuse(body,cyl_z(x,y,BOSS_Z0,BOSS_R,BOSS_H))

# Blind M5 tap drill begins at external belly face Z=8 and stops at Z=17.
for x,y in HOLES:
    body=cut(body,cyl_z(x,y,Z0,TAP_D/2,BLIND_DEPTH))

# Smooth rounded plate approximation; three identical plates stack externally.
def rounded_plate(z_top):
    base=(cq.Workplane('XY').rect(PLATE_L-12,PLATE_W).extrude(PLATE_T)
          .union(cq.Workplane('XY').rect(PLATE_L,PLATE_W-12).extrude(PLATE_T)))
    for sx in (-1,1):
        for sy in (-1,1):
            c=(cq.Workplane('XY').center(sx*(PLATE_L/2-6),sy*(PLATE_W/2-6)).circle(6).extrude(PLATE_T))
            base=base.union(c)
    base=base.translate((PLATE_X0+PLATE_L/2,0,z_top-PLATE_T))
    for x,y in HOLES:
        h=cyl_z(x,y,z_top-PLATE_T-0.5,2.75,PLATE_T+1)
        base=base.cut(h)
    return base

plates=[]
for i in range(N_PLATES):
    plates.append(rounded_plate(Z0-i*PLATE_T))
stack=plates[0]
for p in plates[1:]: stack=fuse(stack,p)

PIPE_R=75.0
PIPE_Z=52.0480547
def rad(y,z): return math.hypot(y,z-PIPE_Z)
ballast_bottom=Z0-N_PLATES*PLATE_T
ballast_margin=PIPE_R-max(rad(PLATE_W/2,ballast_bottom),rad(-PLATE_W/2,ballast_bottom))

MOTOR_L=wp(cq.Solid.makeCylinder(16,92,cq.Vector(237,16.5,45),cq.Vector(1,0,0)))
MOTOR_R=wp(cq.Solid.makeCylinder(16,92,cq.Vector(237,-16.5,45),cq.Vector(1,0,0)))

metrics={
    'body_valid':body.val().isValid(),
    'ballast_stack_valid':stack.val().isValid(),
    'plate_mm':[PLATE_L,PLATE_W,PLATE_T],
    'plate_count_max_initial':N_PLATES,
    'blind_boss_OD_mm':2*BOSS_R,
    'boss_height_into_P0_mm':BOSS_H,
    'M5_tap_drill_mm':TAP_D,
    'blind_hole_depth_mm':BLIND_DEPTH,
    'remaining_boss_cap_above_blind_hole_mm':(BOSS_Z0+BOSS_H)-(Z0+BLIND_DEPTH),
    'standard_screw_lengths_mm':{'1_plate':12,'2_plates':16,'3_plates':20},
    'thread_engagement_each_case_mm':8.0,
    'max_stack_bottom_Z_mm':ballast_bottom,
    'max_stack_DN150_margin_mm':ballast_margin,
    'boss_motor_intersections_mm3':{},
    'front_boss_to_nucleo_axial_gap_mm':105.0-97.5,
}
for i,(x,y) in enumerate(HOLES,1):
    boss=cyl_z(x,y,BOSS_Z0,BOSS_R,BOSS_H)
    metrics['boss_motor_intersections_mm3'][str(i)]=round(inter(boss,MOTOR_L)+inter(boss,MOTOR_R),6)

rho=7.85e-6
plate_mass=PLATE_L*PLATE_W*PLATE_T*rho
stack_mass=N_PLATES*plate_mass
metrics['single_plate_mass_screen_kg']=plate_mass
metrics['max_stack_mass_screen_kg']=stack_mass
base_mass=7.0
base_cgx=153.0; base_cgz=48.0
px=PLATE_X0+PLATE_L/2
pz=Z0-N_PLATES*PLATE_T/2
metrics['combined_nominal_CG_X_mm']=(base_mass*base_cgx+stack_mass*px)/(base_mass+stack_mass)
metrics['combined_nominal_CG_Z_mm']=(base_mass*base_cgz+stack_mass*pz)/(base_mass+stack_mass)

pass_all=(metrics['body_valid'] and metrics['ballast_stack_valid'] and
          metrics['remaining_boss_cap_above_blind_hole_mm']>=2.0 and
          metrics['max_stack_DN150_margin_mm']>=8.0 and
          all(v<1e-5 for v in metrics['boss_motor_intersections_mm3'].values()) and
          metrics['front_boss_to_nucleo_axial_gap_mm']>=5.0)
metrics['status']='PASS' if pass_all else 'FAIL'
metrics['note']='Blind thread is captured entirely in local pressure-body boss; no ballast hole penetrates P0.'

cq.exporters.export(body,os.path.join(OUT,'PX1_PressureBody_BallastBoss_RevGP.step'))
cq.exporters.export(stack,os.path.join(OUT,'PX1_BallastStack_RevGP.step'))
with open(os.path.join(OUT,'REV_GP_BALLAST_VALIDATION.json'),'w') as f: json.dump(metrics,f,indent=2)
print(json.dumps(metrics,indent=2))
if metrics['status']!='PASS': raise SystemExit(2)
