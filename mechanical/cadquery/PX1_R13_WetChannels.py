"""R13 integration study: separate wet lift channels, original 100 W supply.

All units mm. NOT manufacturing release. R12 remains an immutable baseline.
Run with --motor-step for the vendor traction motor. Local BREP cache is derived.
Pressure walls are explicitly constructed; a packing PASS is not a pressure test.
"""
from pathlib import Path
import argparse, hashlib, itertools, json, math
import cadquery as cq
import PX1_R12_SelectedParts as r12
from PX1_R12_SelectedParts import box,cyl,ann,ring,volume,bounds,SEAT

ROOT=Path(__file__).resolve().parents[2]
PX, LO, HI, LINK = 105.,116.,136.,120.
ARM_YS, ARM_T = {'lower':24.25,'upper':27.25},2.5
LOW_Z,HIGH_Z=100.,235.

def solids(p):
    return [cq.Workplane('XY').newObject([s]) for s in p.solids().vals()]

def hit(a,b):
    # Check every solid; Workplane boolean on an assembly can select one solid.
    aa,bb=a.val().BoundingBox(),b.val().BoundingBox()
    if any(getattr(aa,k+'max')<=getattr(bb,k+'min') or getattr(bb,k+'max')<=getattr(aa,k+'min') for k in 'xyz'):return 0.
    return sum(r12.intersect(p,q) for p in solids(a) for q in solids(b))

def outvol(a,b):
    return sum(max(0.,volume(p.cut(b))) for p in solids(a))

def baseline(out,path):
    cache=out/'r12_cache'; cache.mkdir(parents=True,exist_ok=True)
    digest=hashlib.sha256(Path(r12.__file__).read_bytes()+(path.read_bytes() if path else b'ABSTRACT')).hexdigest()
    meta=cache/'index.json'
    if meta.exists():
        d=json.loads(meta.read_text())
        if d.get('digest')==digest:
            return {n:cq.Workplane('XY').newObject([cq.Shape.importBrep(str(cache/f))]) for n,f in d['files'].items()},d['groups']
    parts,groups,_=r12.build(out/'baseline_validation',path)
    files={n:f'{i:03}.brep' for i,n in enumerate(parts)}
    for n,p in parts.items():p.val().exportBrep(str(cache/files[n]))
    meta.write_text(json.dumps({'digest':digest,'files':files,'groups':groups},indent=2))
    return parts,groups

def pressure_body():
    # R12 side transmission datum and bearing features, without obsolete shelves.
    sh=box(412,86,107,206,0,77.5).union(box(412,96,9,206,0,126.5))
    sh=sh.cut(box(396,78,102,206,0,75))
    sh=sh.union(box(188,96,2,318,0,132))
    sh=sh.cut(box(180,78,3,314,0,126.5))
    sh=sh.union(box(412,98,8,206,0,28))
    sh=sh.cut(box(396,78,12,206,0,26))
    for s in (-1,1):
        sh=sh.union(box(258,6.5,64,150,s*42.75,75))
        sh=sh.cut(box(250,17,58,150,s*37.5,75))
        for x in r12.WHEELS:
            sh=sh.union(cyl(40,10,(x,s*40.65,75),'y'))
            sh=sh.union(box(16,7.75,17,x,s*39.525,51.5))
            for d,t,y in ((18.25,25,39),(30.05,7.2,39.15),(40.15,2.7,44.75)):
                sh=sh.cut(cyl(d,t,(x,s*y,75),'y'))
        for x in (38,75,112,150,188,225,262):
            for z in (48,102):sh=sh.cut(cyl(2.5,5.5,(x,s*43.25,z),'y'))
    # Lower front central roof. Closed vertical walls separate the two wet
    # grooves from converter and gears. Wet clearance is Y22.5..29 each side.
    sh=sh.cut(box(222,62,100,110,0,149))
    sh=sh.union(box(222,41,4,111,0,101)) # dry roof underside99, outside103
    for s in (-1,1):
        sh=sh.union(box(222,10.5,4,111,s*25.75,68)) # groove floor66..70
        sh=sh.union(box(222,2,37,111,s*21.5,84.5))
        sh=sh.union(box(222,2,65,111,s*30,98.5))
        sh=sh.cut(box(220,6.5,100,108,s*25.75,120)) # open wet groove; retains4mm floor
    sh=sh.union(box(4,62,65,220,0,98.5)) # sealed rear step ends222
    # Removable lift brackets land on external bosses; blind taps stop above
    # the pressure roof, so lift servicing does not open the dry volume.
    for s in (-1,1):
        sh=sh.union(box(50,10,6,PX,s*15.5,106))
        for x in (PX-18,PX+18):sh=sh.cut(cyl(3.3,5,(x,s*15.5,106.5)))
        # Hanging bearing bridge + rear electronics shelf connect to sidewalls.
        for x in (240,296):
            sh=sh.union(box(12,8,4,x,s*39,106))
            sh=sh.cut(cyl(2.5,3,(x,s*37,106.5)))
        for x in (340,380):
            sh=sh.union(box(12,10,6,x,s*35,103))
            sh=sh.cut(cyl(2.5,4,(x,s*34,104)))
    sh=sh.cut(cyl(14.5,10,(408,0,45),'x'))
    sh=sh.cut(cyl(8.8,10,(4,0,65),'x'))
    sh=sh.cut(cyl(8.8,9,(408,23,104),'x'))
    # Bottom service lid, same continuous 290x2 O-ring candidate as R12.
    lid=cq.Workplane('YZ').polyline([(-46,20),(46,20),(49,23),(49,24),(-49,24),(-49,23)]).close().extrude(412)
    lid=lid.cut(ring(390,84,8,2.8,1.5,(206,0,23.25)))
    bolts=[(x,y) for x in (28,78,128,178,228,278,328,378) for y in (-46,46)]
    bolts += [(x,y) for x in (6,406) for y in (-28,0,28)]
    for x,y in bolts:
        sh=sh.cut(cyl(2.5,7,(x,y,27.5)))
        lid=lid.cut(cyl(3.4,6,(x,y,22)))
    for s in (-1,1):
        sy=s*19.5
        lid=lid.union(box(20,38,7,335,sy,27.5))
        for x in (329,341):
            for y in (sy-15.4,sy+15.4):lid=lid.cut(cyl(2.5,5,(x,y,28.5)))
    return sh.clean(),lid.clean()

def link(p,q,y):
    dx,dz=q[0]-p[0],q[1]-p[1]
    length=math.hypot(dx,dz);ang=-math.degrees(math.atan2(dz,dx))
    sh=box(length,ARM_T,18,0,0,0).rotate((0,0,0),(0,1,0),ang).translate(((p[0]+q[0])/2,y,(p[1]+q[1])/2))
    for x,z in (p,q):sh=sh.union(cyl(18,ARM_T,(x,y,z),'y')).cut(cyl(8.1,6,(x,y,z),'y'))
    return sh

def lift_bracket(s):
    br=box(50,10,3,PX,s*15.5,110.5)
    br=br.union(box(20,8,27,PX,s*18.5,122.5))
    for z in (LO,HI):br=br.union(cyl(20,8,(PX,s*18.5,z),'y'))
    br=br.cut(box(70,20,20,PX,s*18.5,99)) # flat seating plane109
    for z in (LO,HI):br=br.cut(cyl(8.02,12,(PX,s*18.5,z),'y'))
    for x in (PX-18,PX+18):br=br.cut(cyl(4.4,6,(x,s*15.5,110.5)))
    return br.clean()

def between(p,q,d):
    vec=cq.Vector(*[q[i]-p[i] for i in range(3)])
    return cq.Workplane('XY').newObject([cq.Solid.makeCylinder(d/2,vec.Length,cq.Vector(*p),vec.normalized())])

def pose(z,camera):
    th=math.asin((z-128)/LINK); dx,dz=-LINK*math.cos(th),LINK*math.sin(th)
    qx=PX+dx; q1,q2=(qx,LO+dz),(qx,HI+dz)
    ps={f'{a}_{s}':link((PX,p),q,s*ARM_YS[a]) for s in (-1,1) for a,p,q in [('lower',LO,q1),('upper',HI,q2)]}
    # Clamp sits on fixed rear housing. Rearcap ends22mm ahead of lift pivots.
    cradle=ann(90.2,100,30,(qx-33,0,z),'x').union(ann(50,100,4,(qx-18,0,z),'x'))
    for s in (-1,1):
        cheek=box(18,4,38,qx-9,s*20,z-2)
        for zz in (z-12,z+8):cheek=cheek.union(cyl(18,4,(qx,s*20,zz),'y')).cut(cyl(8.1,6,(qx,s*20,zz),'y'))
        cradle=cradle.union(cheek)
    cradle=cradle.union(box(6,40,6,qx,0,z+13))
    ps['Camera_cradle_REFERENCE']=cradle.clean()
    ps['Camera']=camera.translate((qx-198,0,z))
    # 150N spring keeps its base beneath the upper pivot. Positive dL/dtheta
    # means an EXTENSION spring assists raising (old RevFN force sign differed).
    base=(PX,0,112.); attach=(qx,0,z+13)
    ps['Gas150N_INSTALLATION_RESERVE']=between(base,attach,15)
    length=math.dist(base,attach)
    dL=(LINK*((PX-base[0])*math.sin(th)+(HI+5-base[2])*math.cos(th)))/length
    return ps,{'camera_axis_Z_mm':z,'front_pivot_X_mm':qx,'angle_deg':math.degrees(th),
      'gas_pin_distance_mm':length,'gas_assist_Nm_for_150N':150*dL/1000,
      'camera_full_bounds_mm':bounds(ps['Camera'])}

def build(out,path=None,step_deg=5):
    out.mkdir(parents=True,exist_ok=True)
    parts,groups=baseline(out,path)
    print('R13: loaded baseline',flush=True)
    remove=['BODY_6061','LID_5mm','Front_tray','RSD_thermal_angle']
    remove += [n for n,g in groups.items() if g=='route' or n.startswith(('Pinion_support_','Rear_inner_support_'))]
    for n in remove:parts.pop(n,None);groups.pop(n,None)
    def add(n,p,g):parts[n]=p;groups[n]=g
    main,lid=pressure_body();add('BODY_R13',main,'housing');add('BOTTOM_LID_R13',lid,'housing')
    print('R13: built pressure body',flush=True)
    # Keep original100W converter. A3mm thermal angle leaves2mm nominal room
    # on the other side; vendor drawing carries a +/-1mm dimension tolerance.
    for n in list(parts):
        if n=='RSD100D24' or n.startswith('RSD_terminals_'):parts[n]=parts[n].translate((0,.5,0))
    heat=box(167,3,74,108.5,-19,61).union(box(167,14,4,108.5,-13.5,26))
    add('RSD_thermal_angle',heat,'mount')
    replacements={
      'NUCLEO_F446RE':(82.5,70,18,246.25,0,37),
      'Pololu_2855_12V':(17.8,17.8,8,311,20,39),
      'RECOM_5V_carrier_ALLOWANCE':(22,20,20,306,-10,42),
      'MPRLS_3965':(17.8,16.7,7.5,223,20,51.75),
      'TMP117_4821':(25.5,4.6,17.7,160,-25,35),
      'SEBOKS_SU1P':(50,42,18,372,0,45),
      'Waveshare_RS485_C':(42.8,15.2,4.75,250,-20,51),
      'DRV8871_left':(24.4,20.4,9.7,256,-19,115.85),
      '24V_distribution_RESERVE':(46,30,20,373,-18,117),
    }
    for n,d in replacements.items():parts[n]=box(*d)
    plate=box(76,76,2,270,0,109)
    for x in (240,296):
        for y in (-37,37):plate=plate.cut(cyl(3.4,4,(x,y,109)))
    add('Hanging_bearing_bridge',plate,'mount')
    parts['Rear_tray']=parts['Rear_tray'].cut(box(48,32,6,373,-18,107))
    for s in (-1,1):
        a='L' if s==1 else 'R';sy=s*19.5
        parts['Motor_mount_'+a]=parts['Motor_mount_'+a].intersect(box(30,38,80,335,sy,65))
        for x in (50.,150.):
            n='Axle_'+a+str(x)
            # End the new front/middle shaft in the dry gear volume. Do not
            # drill a passage from the wet lift groove into the gear case.
            parts[n]=parts[n].cut(box(20,3,20,x,s*30,75))
        br=None
        for x in (278.5,295.5):
            p=box(5,27,46.5,x,sy,84.75).cut(cyl(21.02,7,(x,sy,75),'x'))
            br=p if br is None else br.union(p)
        br=br.union(box(25,27,3,287,sy,106.5))
        add('Pinion_hanging_support_'+a,br,'mount')
        br=box(24,5,42.5,250,s*12,86.75).cut(cyl(19.02,7,(250,s*12,75),'y'))
        add('Rear_inner_hanging_support_'+a,br,'mount')
        add('Lift_bracket_'+a,lift_bracket(s),'lift_mount')
    add('NUCLEO_insulation_tray_RESERVE',box(90,74,1,246.25,0,25.5),'board_mount_reserve')
    add('HV_route_RESERVE',box(375,5,7,210,-36,116),'route')
    add('LV_route_RESERVE',box(260,5,7,159,36,116),'route')
    camera=cq.importers.importStep(str(ROOT/'build_r12/PX1_R12_CAMERA_CANDIDATE.step'))
    report={'revision':'R13','manufacturing_release':False,'physical_test':False,'status':'UNTESTED',
      'motor_model':'vendor_STEP' if path else 'documented_dimension_abstraction',
      'changed_parts':replacements,'housing_solid_count':len(main.solids().vals()),
      'housing_bounds_mm':bounds(main),'seated_drop_mm':SEAT,
      'nominal_wet_channel_Y_mm':[22.5,29.0],'arm_thickness_mm':ARM_T,'arm_planes_abs_Y_mm':ARM_YS,
      'groove_floor_thickness_mm':4,'groove_wall_thickness_mm':2,
      'solid_validity':{n:all(s.isValid() for s in p.solids().vals()) for n,p in parts.items()},
      'part_bounds_mm':{n:bounds(p) for n,p in parts.items()},
      'static_collisions':{},'routing_collisions':{},'mount_contacts':{},'lift_positions':{},'low_pipe_outside':{},
      'limitations':['Discrete sweep, not tolerance or deflection verification.',
       'Gear references have no manufacturing teeth, axial locks or torque proof.',
       'Camera cradle is a clearance reference; split clamp, fastening and harness unfinished.',
       'Spring150N OD15 is an installation reserve, not a validated purchasable spring.',
       'Bearing bridge and board mounts need complete fasteners and assembly access.',
       'Bottom seal candidate transferred fromR12; pressure/FEA/retention not tested.',
       'Lift arms:316L sheet2.5mm in separate planes; strength and wear qualification pending.',
       'Only neutral camera with lift sweep; combined PAN/ROTATE plus lift is not certified.']}
    # Explicit categories: manufactured gear envelopes intentionally overlap.
    active={'component','mount','housing','bearing','drive','gear_envelope','seal_holder','lift_mount','board_mount_reserve'}
    print('R13: static collision checks',flush=True)
    for (n,p),(m,q) in itertools.combinations(parts.items(),2):
        a,b=groups[n],groups[m]
        check=(a=='component' and b in active) or (b=='component' and a in active)
        check |= (a in {'mount','lift_mount','board_mount_reserve'} and b in {'housing','drive','bearing','gear_envelope'}) or (b in {'mount','lift_mount','board_mount_reserve'} and a in {'housing','drive','bearing','gear_envelope'})
        check |= (a=='housing' and b in {'drive','bearing','gear_envelope'}) or (b=='housing' and a in {'drive','bearing','gear_envelope'})
        if check:
            v=hit(p,q)
            if v>1e-3:report['static_collisions'][n+'__'+m]=v
        if (a=='route' and b in active) or (b=='route' and a in active):
            v=hit(p,q)
            if v>1e-3:report['routing_collisions'][n+'__'+m]=v
    mounting=[p for n,p in parts.items() if groups[n] in ('housing','mount','lift_mount')]
    for n,p in parts.items():
        if groups[n] in ('mount','lift_mount'):
            report['mount_contacts'][n]=min(p.val().distance(q.val()) for q in mounting if q is not p)
    supports={n:p for n,p in parts.items() if groups[n] in ('housing','mount','lift_mount')}
    reachable={n for n in supports if groups[n]=='housing'}
    while True:
        attached={n for n,p in supports.items() if n not in reachable and any(p.val().distance(supports[m].val())<=1e-5 for m in reachable)}
        if not attached:break
        reachable.update(attached)
    report['supports_without_contact_path_to_housing']=sorted(set(supports)-reachable)
    print('R13: DN150 containment checks',flush=True)
    pipe=cyl(150,1600,(100,0,75),'x')
    low,low_metrics=pose(LOW_Z,camera)
    for n,p in (parts|low).items():
        v=outvol(p.translate((0,0,-SEAT)),pipe)
        if v>1e-3:report['low_pipe_outside'][n]=v
    angles=list(range(math.ceil(math.degrees(math.asin((LOW_Z-128)/120))),math.floor(math.degrees(math.asin((HIGH_Z-128)/120)))+1,step_deg))
    levels=sorted(set([LOW_Z,HIGH_Z,160.]+[128+120*math.sin(math.radians(a)) for a in angles]))
    for z in levels:
        print(f'R13: lift Z={z:.3f}',flush=True)
        moving,metrics=pose(z,camera);hits={}
        for n,p in moving.items():
            for m,q in parts.items():
                if groups[m] not in ('route','external_reserve'):
                    v=hit(p,q)
                    if v>1e-3:hits[n+'__'+m]=v
        # Arms and cradle may connect at holes, but solid overlap is not exempt.
        for (n,p),(m,q) in itertools.combinations(moving.items(),2):
            if {n,m}=={'Gas150N_INSTALLATION_RESERVE','Camera_cradle_REFERENCE'}:continue # intentional endpoint; clevis detail pending
            v=hit(p,q)
            if v>1e-3:hits[n+'__'+m]=v
        metrics['collisions']=hits
        report['lift_positions'][f'{z:.6f}']=metrics
    bad=report['static_collisions'] or report['routing_collisions'] or report['low_pipe_outside'] or report['supports_without_contact_path_to_housing'] or report['housing_solid_count']!=1 or not all(report['solid_validity'].values()) or any(p['collisions'] for p in report['lift_positions'].values())
    report['status']='FAIL_INTEGRATION_STUDY' if bad else 'PASS_SCOPED_R13_PACKING_AND_LIFT_SWEEP'
    report['gas_pin_distance_range_mm']=[min(p['gas_pin_distance_mm'] for p in report['lift_positions'].values()),max(p['gas_pin_distance_mm'] for p in report['lift_positions'].values())]
    report['gas_assist_range_Nm']=[min(p['gas_assist_Nm_for_150N'] for p in report['lift_positions'].values()),max(p['gas_assist_Nm_for_150N'] for p in report['lift_positions'].values())]
    report['body_and_lid_aluminum_mass_kg']=(volume(main)+volume(lid))*2.7e-6
    report['sweep_step_deg']=step_deg
    report['sweep_pose_count']=len(levels)
    report['source_sha256']=hashlib.sha256(Path(__file__).read_bytes()).hexdigest()
    report['camera_step_sha256']=hashlib.sha256((ROOT/'build_r12/PX1_R12_CAMERA_CANDIDATE.step').read_bytes()).hexdigest()
    report['spring_cradle_endpoint_exclusion']='Only spring vs its cradle end attachment is excluded; all other spring collisions are checked.'
    report['LOW_assembly_bounds_mm']=[
      [min(bounds(p)[0][i] for p in (parts|low).values()) for i in range(3)],
      [max(bounds(p)[1][i] for p in (parts|low).values()) for i in range(3)]]
    ass=cq.Assembly(name='PX1_R13_INTEGRATION_STUDY')
    colors={'housing':(.5,.55,.58,.4),'component':(.12,.5,.3),'gear_envelope':(.85,.65,.2),'wheel':(.12,.12,.12),'route':(.9,.2,.1,.3)}
    for n,p in (parts|low).items():ass.add(p,name=n.replace('.','_').replace('-','minus'),color=cq.Color(*colors.get(groups.get(n),(.65,.65,.67))))
    ass.export(str(out/'PX1_R13_INTEGRATION_STUDY.step'))
    cq.exporters.export(main,str(out/'PX1_R13_BODY.step'))
    cq.exporters.export(lid,str(out/'PX1_R13_BOTTOM_LID.step'))
    (out/'validation.json').write_text(json.dumps(report,indent=2))
    print(json.dumps({k:v for k,v in report.items() if k not in ('solid_validity','part_bounds_mm','limitations','changed_parts','lift_positions')},indent=2))
    print('Lift collisions:',json.dumps({z:p['collisions'] for z,p in report['lift_positions'].items() if p['collisions']},indent=2))
    return parts,groups,report

if __name__=='__main__':
    ap=argparse.ArgumentParser();ap.add_argument('--out',type=Path,default=ROOT/'build_r13');ap.add_argument('--motor-step',type=Path);ap.add_argument('--step-deg',type=int,default=5)
    a=ap.parse_args();build(a.out,a.motor_step,a.step_deg)
