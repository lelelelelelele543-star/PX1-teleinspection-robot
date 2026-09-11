import cadquery as cq
import math, json, os

# PX-1 Rev.B WB20 — integrated correction after WB19 full-crawler audit.
# Engineering validation only; NOT machining release.
OUT=os.path.abspath('build_wb20'); os.makedirs(OUT,exist_ok=True)

PIPE_R=75.0; PIPE_Z=52.0480547
BODY_L=307.0; BODY_W=92.0; HALF_OUT=46.0; HALF_IN=34.0; Z0=8.0; ZTOP=90.0; REAR_END=358.0
WHEEL_X=(50.0,150.0,250.0); GEAR_X=(50.0,100.0,150.0,200.0,250.0)
WHEEL_Z=45.0; WHEEL_CENTER_Y=59.0; WHEEL_OD=90.0; WHEEL_W=16.0
GEAR_Y=42.0; GEAR_OD=52.0; GEAR_FACE=3.75; GEAR_INNER_FACE=GEAR_Y-GEAR_FACE/2.0
ROOF_PTS=[(0.0,22.0),(140.0,26.0),(200.0,77.0),(220.0,90.0)]; DECK_HALF_W=38.0; ROOF_T=5.0
CAM_X=83.557; CAM_Z=75.0; HEAD_R=26.0; HEAD_L=78.0; TILT_MIN=-105; TILT_MAX=105; TILT_STEP=1
BOSS_OUTER_Y=34.0; YOKE_GAP=0.5; YOKE_T=3.0
YOKE_INNER_Y=BOSS_OUTER_Y+YOKE_GAP; YOKE_OUTER_Y=YOKE_INNER_Y+YOKE_T; YOKE_CENTER_Y=(YOKE_INNER_Y+YOKE_OUTER_Y)/2.0
YOKE_R=29.0; YOKE_INNER_R=10.75; TILT_POD_OD=18.0; TILT_POD_X=56.0; TILT_WHEEL_Y=-16.75; WORM_CD=14.5
BODY_PIVOT_X=200.0; PIVOT_Z_LOW=92.0; PIVOT_Z_HIGH=112.0; LINK_L=120.0; CAM_AXIS_OFFSET_Z=2.0
CAM_ZS={'LOW':75.0,'MID':130.0,'HIGH':205.0}
GAS_ARTICLE='ACE GS-12-20-V4A'; GAS_FORCE_N=150.0; GAS_BODY_OD=12.0; GAS_ROD_OD=4.0; GAS_STROKE=20.0; GAS_EXTENDED=72.0
GAS_BASE=(194.0,82.9); GAS_ATTACH_FROM_LOWER_PIVOT=63.0; GAS_CENTER_Y=16.0

wp=lambda s:cq.Workplane('XY').newObject([s])
def box0(x0,y0,z0,dx,dy,dz): return wp(cq.Solid.makeBox(dx,dy,dz,cq.Vector(x0,y0,z0)))
def boxc(x,y,z,dx,dy,dz): return cq.Workplane('XY').box(dx,dy,dz,centered=(True,True,True)).translate((x,y,z))
def cyl_x_center(x,y,z,r,l): return wp(cq.Solid.makeCylinder(r,l,cq.Vector(x-l/2,y,z),cq.Vector(1,0,0)))
def cyl_y(x,y0,z,r,l,sgn): return wp(cq.Solid.makeCylinder(r,l,cq.Vector(x,y0,z),cq.Vector(0,sgn,0)))
def cyl_y_center(x,y,z,r,l): return wp(cq.Solid.makeCylinder(r,l,cq.Vector(x,y-l/2,z),cq.Vector(0,1,0)))
def cyl_z(x,y,z0,r,l): return wp(cq.Solid.makeCylinder(r,l,cq.Vector(x,y,z0),cq.Vector(0,0,1)))
def cut(a,b): return wp(a.val().cut(b.val()))
def fuse(a,b): return wp(a.val().fuse(b.val()))
def outside(a,b): return a.val().cut(b.val()).Volume()
def inter(a,b): return a.val().intersect(b.val()).Volume()
def prism_x(x0,pts,length): return cq.Workplane('YZ',origin=(x0,0,0)).polyline(pts).close().extrude(length)
def ring_y_center(x,y,z,ro,ri,l):
    o=cyl_y_center(x,y,z,ro,l); i=cyl_y_center(x,y,z,ri,l+0.2); return wp(o.val().cut(i.val()))
def fuse_all(parts):
    s=parts[0].val()
    for p in parts[1:]: s=s.fuse(p.val())
    return wp(s)
def roof_top(x):
    if x<=ROOF_PTS[0][0]: return ROOF_PTS[0][1]
    for (x0,z0),(x1,z1) in zip(ROOF_PTS,ROOF_PTS[1:]):
        if x<=x1: return z0+(z1-z0)*(x-x0)/(x1-x0)
    return ROOF_PTS[-1][1]

# Corrected pressure body: front dry roof follows 5 mm below lowered wet deck.
body=box0(0,-HALF_OUT,Z0,BODY_L,BODY_W,ZTOP-Z0)
inner_pts=[(8.0,14.0),(299.0,14.0),(299.0,85.0),(220.0,85.0),(200.0,72.0),(140.0,21.0),(8.0,roof_top(8.0)-ROOF_T)]
inner=cq.Workplane('XZ',origin=(0,HALF_IN,0)).polyline(inner_pts).close().extrude(2*HALF_IN); body=cut(body,inner)
wet_poly=ROOF_PTS+[(220.0,115.0),(0.0,115.0)]
wet=cq.Workplane('XZ',origin=(0,-DECK_HALF_W,0)).polyline(wet_poly).close().extrude(2*DECK_HALF_W); body=cut(body,wet)
body=cut(body,box0(10.5,HALF_IN,6.0,286.0,HALF_OUT-HALF_IN,80.0)); body=cut(body,box0(10.5,-HALF_OUT,6.0,286.0,HALF_OUT-HALF_IN,80.0))
rear_outer=box0(242.0,-40.0,22.0,REAR_END-242.0,80.0,46.0); body=fuse(body,rear_outer)
rear_cav=box0(246.0,-36.0,26.0,REAR_END-252.0,72.0,38.0); body=cut(body,rear_cav)
pod_outer_pts=[(-39,90),(39,90),(39,104),(34,110),(-34,110),(-39,104)]; pod_outer=prism_x(218,pod_outer_pts,89); body=fuse(body,pod_outer)
pod_inner_pts=[(-35.5,92),(35.5,92),(35.5,104.5),(32.5,106),(-32.5,106),(-35.5,104.5)]; pod_cav=prism_x(221,pod_inner_pts,83); body=cut(body,pod_cav)
throat=box0(224,-33,84,76,66,10); body=cut(body,throat)
cavity=wp(inner.val().fuse(rear_cav.val()).fuse(pod_cav.val()).fuse(throat.val()))
body_vertices,_=body.val().tessellate(0.5); body_clear=PIPE_R-max(math.hypot(v.y,v.z-PIPE_Z) for v in body_vertices)

wheels=[(s,x,cyl_y_center(x,s*WHEEL_CENTER_Y,WHEEL_Z,WHEEL_OD/2,WHEEL_W)) for s in (-1,1) for x in WHEEL_X]
gears=[(s,x,cyl_y_center(x,s*GEAR_Y,WHEEL_Z,GEAR_OD/2,GEAR_FACE)) for s in (-1,1) for x in GEAR_X]
assert len(wheels)==6 and len(gears)==10

shell=cyl_x_center(CAM_X,0,CAM_Z,HEAD_R,HEAD_L)
boss_pos=cyl_y(CAM_X,HEAD_R,CAM_Z,10.0,BOSS_OUTER_Y-HEAD_R,1); boss_neg=cyl_y(CAM_X,-HEAD_R,CAM_Z,10.0,BOSS_OUTER_Y-HEAD_R,-1)
tilt_pod=cyl_x_center(CAM_X+12.0,TILT_WHEEL_Y,CAM_Z+WORM_CD,TILT_POD_OD/2,TILT_POD_X)
moving=fuse_all([shell,boss_pos,boss_neg,tilt_pod])
yoke_pos=ring_y_center(CAM_X,+YOKE_CENTER_Y,CAM_Z,YOKE_R,YOKE_INNER_R,YOKE_T); yoke_neg=ring_y_center(CAM_X,-YOKE_CENTER_Y,CAM_Z,YOKE_R,YOKE_INNER_R,YOKE_T)
bridge=boxc(CAM_X+58.0,0,CAM_Z+20.0,8.0,2*YOKE_OUTER_Y,8.0); fixed=fuse_all([yoke_pos,yoke_neg,bridge])

# Full 1-degree sweep using one detailed mesh rotated mathematically.
verts,_=moving.val().tessellate(0.18); V=[(v.x-CAM_X,v.y,v.z-CAM_Z) for v in verts]
fverts,_=fixed.val().tessellate(0.18); FV=[(v.x,v.y,v.z) for v in fverts]
def rotated(dx,y,dz,deg):
    a=math.radians(deg); c=math.cos(a); s=math.sin(a); return CAM_X+dx*c+dz*s,y,CAM_Z-dx*s+dz*c
min_pipe=1e9; min_floor=1e9; worst_pipe=None; worst_floor=None; worst_pipe_xyz=None; worst_floor_xyz=None
for deg in range(TILT_MIN,TILT_MAX+1,TILT_STEP):
    mp=1e9; mf=1e9
    for dx,y,dz in V:
        x,yy,z=rotated(dx,y,dz,deg); pc=PIPE_R-math.hypot(yy,z-PIPE_Z); fc=z-roof_top(x)
        if pc<mp: mp=pc; mp_xyz=(x,yy,z)
        if fc<mf: mf=fc; mf_xyz=(x,yy,z)
    if mp<min_pipe: min_pipe=mp; worst_pipe=deg; worst_pipe_xyz=mp_xyz
    if mf<min_floor: min_floor=mf; worst_floor=deg; worst_floor_xyz=mf_xyz
fixed_pipe=min(PIPE_R-math.hypot(y,z-PIPE_Z) for x,y,z in FV); fixed_floor=min(z-roof_top(x) for x,y,z in FV)
fixed_max_y=max(abs(y) for x,y,z in FV); moving_max_y=max(abs(y) for dx,y,dz in V)
fixed_gear_gap=GEAR_INNER_FACE-fixed_max_y; moving_gear_gap=GEAR_INNER_FACE-moving_max_y
fixed_deck_gap=DECK_HALF_W-fixed_max_y; moving_deck_gap=DECK_HALF_W-moving_max_y

# Repack active commercial articles/reserves into remaining dry volume.
parts={
 'TRACTION_DRIVER_L_RESERVE':boxc(167,+16,22,34,22,14),
 'TRACTION_DRIVER_R_RESERVE':boxc(167,-16,22,34,22,14),
 'DELTA_TR1D_P2':boxc(205,-22,42,43,16,15),
 'NICHICON_UCS2D221MHD1TN':cyl_x_center(205,+24,30,9,25),
 'INPUT_PROTECTION_RESERVE':boxc(215,0,60,24,48,18),
 'CINCON_CQB150W110S24_CARRIER_RESERVE':boxc(260,0,70,65,45,16),
 'PRESSURE_SENSOR_RESERVE':cyl_z(280,0,35,12.2,25),
 'NUCLEO_F446RE_LOWPROFILE':boxc(262.25,0,98,82.5,70,12),
}
part_out={k:outside(v,cavity) for k,v in parts.items()}; part_intersections={}; keys=list(parts)
for i,a in enumerate(keys):
    for b in keys[i+1:]:
        iv=inter(parts[a],parts[b])
        if iv>1e-4: part_intersections[a+'__'+b]=iv

# ACE GS-12-20-V4A gas spring screen.
def lift_theta(zcam): return math.asin((zcam-CAM_AXIS_OFFSET_Z-(PIVOT_Z_LOW+PIVOT_Z_HIGH)/2.0)/LINK_L)
def gas_metrics(zcam):
    th=lift_theta(zcam); ax=BODY_PIVOT_X-GAS_ATTACH_FROM_LOWER_PIVOT*math.cos(th); az=PIVOT_Z_LOW+GAS_ATTACH_FROM_LOWER_PIVOT*math.sin(th); bx,bz=GAS_BASE
    L=math.hypot(ax-bx,az-bz); fx=GAS_FORCE_N*(ax-bx)/L; fz=GAS_FORCE_N*(az-bz)/L
    assist=(fx*GAS_ATTACH_FROM_LOWER_PIVOT*math.sin(th)+fz*GAS_ATTACH_FROM_LOWER_PIVOT*math.cos(th))/1000.0
    floor_clear=1e9; pipe_clear=1e9
    for i in range(101):
        t=i/100.0; x=bx+(ax-bx)*t; z=bz+(az-bz)*t
        floor_clear=min(floor_clear,z-roof_top(x)-GAS_BODY_OD/2.0)
        pipe_clear=min(pipe_clear,PIPE_R-(math.hypot(GAS_CENTER_Y,z-PIPE_Z)+GAS_BODY_OD/2.0))
    return {'length_mm':L,'assist_torque_Nm_at_150N':assist,'moving_pin_xz_mm':[ax,az],'floor_clearance_for_OD12_mm':floor_clear,'ideal_DN150_clearance_for_OD12_mm':pipe_clear}
gas={name:gas_metrics(z) for name,z in CAM_ZS.items()}; gas_lengths=[v['length_mm'] for v in gas.values()]
gas_used=max(gas_lengths)-min(gas_lengths); gas_retracted=GAS_EXTENDED-GAS_STROKE
gas_low_margin=min(gas_lengths)-gas_retracted; gas_high_margin=GAS_EXTENDED-max(gas_lengths)

kinematic_ok=(min_pipe>=3.0 and min_floor>=3.0 and fixed_pipe>=3.0 and fixed_floor>=3.0 and fixed_gear_gap>=2.0 and moving_gear_gap>=2.0 and fixed_deck_gap>=0.25 and moving_deck_gap>=0.25)
pack_ok=(body.val().isValid() and body_clear>0 and all(v<1e-4 for v in part_out.values()) and not part_intersections)
gas_ok=(gas_low_margin>=3.0 and gas_high_margin>=3.0 and min(v['floor_clearance_for_OD12_mm'] for v in gas.values())>=3.0 and gas['LOW']['ideal_DN150_clearance_for_OD12_mm']>=5.0 and min(v['assist_torque_Nm_at_150N'] for v in gas.values())>1.0)
status='PASS_SCREEN / MANUFACTURING_HOLD' if kinematic_ok and pack_ok and gas_ok else 'FAIL_SCREEN'

checks={
 'status':status,
 'architecture':{'wheel_stations_x_mm':list(WHEEL_X),'wheels_total':len(wheels),'z50_positions_x_mm':list(GEAR_X),'z50_total':len(gears),'rear_drive_x_mm':250.0,'rule':'3 AXLES / 6 WHEELS HARD LOCK'},
 'correction_reason':{'WB19_gap':'WB18/WB19 validated camera/yoke internally and against DN150 but not complete fixed-yoke vs Rev.PR body/side-gear integration.','WB20_action':'lower front wet deck and narrow/recess TILT stack before any further harness freeze.'},
 'body':{'wet_deck_floor_points_xz_mm':ROOF_PTS,'wet_deck_half_width_mm':DECK_HALF_W,'pressure_roof_nominal_mm':ROOF_T,'body_valid':body.val().isValid(),'body_min_ideal_DN150_clearance_mm':body_clear},
 'tilt_stack':{'bearing':'618/8 8x16x4 recessed into P3, y22..26 each side','seal':'8x16x7 FKM, y26..33 each side','boss_outer_abs_y_mm':BOSS_OUTER_Y,'yoke_inner_abs_y_mm':YOKE_INNER_Y,'yoke_outer_abs_y_mm':YOKE_OUTER_Y,'gear_inner_face_abs_y_mm':GEAR_INNER_FACE,'yoke_to_Z50_lateral_gap_mm':GEAR_INNER_FACE-YOKE_OUTER_Y,'yoke_to_wetdeck_side_gap_mm':DECK_HALF_W-YOKE_OUTER_Y},
 'tilt_sweep':{'range_deg':[TILT_MIN,TILT_MAX],'step_deg':TILT_STEP,'moving_min_ideal_DN150_clearance_mm':min_pipe,'moving_worst_pipe_deg':worst_pipe,'moving_worst_pipe_xyz_mm':worst_pipe_xyz,'moving_min_floor_clearance_mm':min_floor,'moving_worst_floor_deg':worst_floor,'moving_worst_floor_xyz_mm':worst_floor_xyz,'fixed_min_ideal_DN150_clearance_mm':fixed_pipe,'fixed_min_floor_clearance_mm':fixed_floor,'moving_lateral_gap_to_Z50_mm':moving_gear_gap,'fixed_lateral_gap_to_Z50_mm':fixed_gear_gap},
 'electronics_pack':{'component_outside_dry_volume_mm3':part_out,'component_intersections_mm3':part_intersections,'placements':{'Cincon CQB150W-110S24 + carrier reserve':'65x45x16 @ X260 Y0 Z70','Delta TR-1D*P2':'43x16x15 @ X205 Y-22 Z42','Nichicon UCS2D221MHD1TN':'OD18x25 horizontal @ X205 Y+24 Z30','NUCLEO F446RE':'82.5x70x12 @ X262.25 Y0 Z98'}},
 'gas_spring':{'selected_prototype_family':GAS_ARTICLE,'force_N':GAS_FORCE_N,'manufacturer_geometry':{'body_OD_mm':GAS_BODY_OD,'rod_OD_mm':GAS_ROD_OD,'stroke_mm':GAS_STROKE,'extended_L_mm':GAS_EXTENDED},'source_url':'https://www.ace-ace.com/com/products/motion-control/industrial-gas-springs-push-type/gs-8-v4a-to-gs-40-va/gs-12-v4a/gs-12-20-v4a.html','fixed_pin_xz_mm':list(GAS_BASE),'moving_pin_distance_from_lower_body_pivot_mm':GAS_ATTACH_FROM_LOWER_PIVOT,'spring_center_y_screen_mm':GAS_CENTER_Y,'positions':gas,'used_length_span_mm':gas_used,'nominal_retracted_L_mm':gas_retracted,'compression_end_margin_mm':gas_low_margin,'extension_end_margin_mm':gas_high_margin,'note':'150 N starting force preserves CRP-class intent; final force and end fittings require physical balance/cycle test.'},
 'release_holds':['physical DN150 tube test with ovality/debris allowance; 3.04 mm camera hard clearance is only ideal geometry','pressure FEA/proof of lowered front roof and transition ramp','exact machined yoke/retainer fastener detail and stiffness','actual 618/8 and 8x16x7 sample tolerances/fits','ROLL N20 output-shaft useful length after recessed bearing integration','ACE gas spring exact 150 N configuration and chosen end-fitting pin-to-pin length checked on purchased sample','gas-spring body/moving brackets detailed and fatigue/corrosion tested','constant camera-harness length/routing re-solved after WB20 geometry; WB19 harness coordinates are superseded for manufacturing','all existing WB18 camera electrical/CVBS/pressure physical-sample gates remain active'],
 'execution':{'engine':'CadQuery 2.8.0','model':'WB20','method':'solid body/packaging + single-mesh analytical 1deg TILT sweep'}
}
with open(os.path.join(OUT,'REV_B_WB20_VALIDATION.json'),'w') as f: json.dump(checks,f,indent=2)
assy=cq.Assembly(name='PX1_WB20_INTEGRATED_CORRECTION'); assy.add(body,name='PressureBody_WB20'); assy.add(moving,name='CameraMoving_TILT0'); assy.add(fixed,name='NarrowFixedYoke')
for s,x,w in wheels: assy.add(w,name=f'Wheel_S{s:+d}_X{int(x)}')
for s,x,g in gears: assy.add(g,name=f'Z50_S{s:+d}_X{int(x)}')
for n,p in parts.items(): assy.add(p,name=n)
assy.save(os.path.join(OUT,'PX1_WB20_INTEGRATED_CORRECTION.step')); cq.exporters.export(body,os.path.join(OUT,'PX1_WB20_PRESSURE_BODY.step'))
print(json.dumps(checks,indent=2))
if status.startswith('FAIL'): raise SystemExit(2)
