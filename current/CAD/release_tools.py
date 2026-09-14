"""Exports and reproducible geometric checks for the single PX1 current master.

No manufacturing PASS is inferred from envelopes, a skipped pair, or a CAD exception.
"""
from pathlib import Path
import json, math, hashlib, csv, itertools, os
import cadquery as cq
from cadquery import exporters

def shape(p):
    vals=p.vals() if isinstance(p,cq.Workplane) else [p]
    return vals[0] if len(vals)==1 else cq.Compound.makeCompound(vals)

def box(s):
    b=s.BoundingBox()
    return [b.xmin,b.ymin,b.zmin,b.xmax,b.ymax,b.zmax]

def possible(a,b,tol=1e-6):
    return all(min(a[i+3],b[i+3])-max(a[i],b[i])>tol for i in range(3))

def finish_build(g):
    root=g['ROOT'];cad=g['CAD'];metal=g['METAL'];prints=g['PRINT']
    components=g['components']; shapes={n:shape(p) for n,p,c in components}
    # Remove only previous generated exports, so removed geometry cannot survive in the package.
    for old in metal.glob('*.step'): old.unlink()
    colors={'body':(.45,.5,.55),'metal':(.6,.66,.7),'shaft':(.7,.73,.75),'gear':(.84,.61,.19),
        'bevel':(.92,.45,.12),'bearing':(.4,.65,.85),'seal':(.15,.15,.18),'wheel':(.11,.11,.12),
        'lift':(.65,.68,.7),'camera':(.3,.36,.4),'connector':(.2,.22,.24),'purchased':(.22,.5,.68),
        'electronics':(.16,.47,.3),'electronics_hold':(.3,.55,.3),'wire':(.82,.27,.2),'print':(.2,.68,.77),'valve':(.7,.66,.3),'cable':(.1,.11,.1)}
    assembly=cq.Assembly(name='PX1_Current_Master')
    invalid=[];registry=[]; categories={}
    for n,p,c in components:
        s=shapes[n];categories[n]=c
        if not s.isValid() or s.Volume()<=0: invalid.append(n)
        assembly.add(s,name=n,color=cq.Color(*colors.get(c,(.65,.65,.65))))
        b=box(s)
        registry.append({'id':n,'category':c,'geometry_state':('MANUFACTURER_STEP' if 'MANUFACTURER_STEP' in n else 'HOLD' if 'HOLD' in n else 'BOUNDARY_ENVELOPE_OR_DESIGN'),
            'bbox_mm':[round(v,5) for v in b],'dimensions_mm':[round(b[i+3]-b[i],5) for i in range(3)],'volume_mm3':round(s.Volume(),5),'solids':len(s.Solids())})
    step=cad/'PX1_Current_Master.step';assembly.export(str(step),'STEP')
    # Every exported custom part is the exact assembly solid, not a separately redrawn surrogate.
    export_map={};used=set()
    for n,p,c in components:
        if c not in ('metal','shaft','lift','camera','body'):continue
        # Left/right quantities are retained in BOM, identical solids need only one part export.
        stem=n.replace('_-1_','_SIDE_').replace('_1_','_SIDE_')
        if stem in used:continue
        used.add(stem);fn=metal/(n+'.step');exporters.export(shapes[n],str(fn));export_map[n]=str(fn.relative_to(root))
    # Non-pressure print outputs are also made from the active assembly geometry.
    print_map={
      'PX1_Lift_Harness_Guard_PROTOTYPE.stl':shape(g['hguard']),
      'PX1_Motor_Holder_FitCheck_ONLY.stl':shape(g['motor_holder']),
      'PX1_PRESSURE_Cover_FitCheck_ONLY.stl':shape(g['cover']),
      'PX1_Side_Cover_FitCheck_ONLY.stl':shape(g['side_covers'][1][1]),
    }
    print_validation=[]
    for fn,s in print_map.items():
        b=box(s);center=((b[0]+b[3])/2,(b[1]+b[4])/2,b[2])
        s=s.translate(tuple(-v for v in center))
        if 'Motor' in fn:s=s.rotate((0,0,0),(0,1,0),90)
        if 'Side' in fn:s=s.rotate((0,0,0),(1,0,0),90)
        b=box(s);s=s.translate((0,0,-b[2]));b=box(s)
        dims=[b[i+3]-b[i] for i in range(3)]
        exporters.export(s,str(prints/fn),tolerance=.06,angularTolerance=.12)
        print_validation.append({'file':fn,'dimensions_mm':dims,'fits_chiron_400x400x450':all(x<=lim for x,lim in zip(dims,(400,400,450))),
            'solid_valid':s.isValid(),'use':'FIT CHECK ONLY; no pressure or traction structural release'})
    counts={
        'wheel':sum('_QRW90SR150_WHEEL_' in n for n in shapes),
        'Z50':sum(n.startswith('HOLD_Z50_') for n in shapes),
        'Z40':sum(n.startswith('HOLD_Z40_BEVEL_') for n in shapes),
        'Z16':sum(n.startswith('HOLD_Z16_BEVEL_') for n in shapes),
        'traction_motor':sum(n.startswith('POLOLU_5707_MOTOR_') for n in shapes),
        '61801_side':sum(n.startswith('61801_SIDE_') for n in shapes),
        '61801_pinion':sum(n.startswith('61801_Z16_') for n in shapes),
        '61903':sum(n.startswith('61903_SIDE_') for n in shapes),
        '61800':sum(n.startswith('61800_Z40_') for n in shapes),
        'idler_bush':sum(n.startswith('IDLE_BUSH_') for n in shapes),
        'camera_harness_cores':sum(n.startswith('CAMERA_HARNESS_CORE_') for n in shapes),
    }
    expected={'wheel':6,'Z50':10,'Z40':2,'Z16':2,'traction_motor':2,'61801_side':2,'61801_pinion':2,'61903':6,'61800':2,'idler_bush':4,'camera_harness_cores':6}
    boxes={n:box(s) for n,s in shapes.items()};pairs=[];errors=[];tested=0
    allpairs=len(shapes)*(len(shapes)-1)//2
    for a,b in itertools.combinations(shapes,2):
        if not possible(boxes[a],boxes[b]):continue
        tested+=1
        try:v=shapes[a].intersect(shapes[b]).Volume()
        except Exception as exc:errors.append({'a':a,'b':b,'error':str(exc)});continue
        if v>1e-4:
            # These categories are reported, not silently ignored. All rigid clashes are FAIL/HOLD.
            ca,cb=categories[a],categories[b]
            typ='RIGID_INTERFERENCE'
            if 'seal' in (ca,cb):typ='SEAL_CONTACT_REQUIRES_GLAND_CHECK'
            if 'wheel' in (ca,cb):typ='WHEEL_PROFILE_HOLD_INTERFERENCE'
            if ca in ('gear','bevel') and cb in ('gear','bevel'):typ='TOOTH_CONTACT_HOLD'
            if ('WHEEL_RETENTION_M6' in a and 'WHEEL_SHAFT' in b) or ('WHEEL_RETENTION_M6' in b and 'WHEEL_SHAFT' in a):typ='THREAD_ENGAGEMENT_HOLD_NO_HELICAL_GEOMETRY'
            if ('WHEEL_RETENTION_M5' in a and 'WHEEL_SHAFT' in b) or ('WHEEL_RETENTION_M5' in b and 'WHEEL_SHAFT' in a):typ='THREAD_ENGAGEMENT_HOLD_NO_HELICAL_GEOMETRY'
            if 'valve' == ca == cb:typ='VALVE_INTERNAL_ENVELOPE_HOLD'
            pairs.append({'a':a,'b':b,'volume_mm3':round(v,6),'classification':typ})
    # Radial containment tests ALL solids, including wheels, levers, covers and connectors.
    radial=[];pipeZ=g['PIPE_CENTER_Z'];rpipe=75
    for n,s in shapes.items():
        vv,tt=s.tessellate(.12,.08)
        clearance=rpipe-max(math.hypot(v.y,v.z-pipeZ) for v in vv)
        radial.append({'id':n,'clearance_mm':round(clearance,4),'status':'INTERFERENCE' if clearance<-.12 else 'SCREEN_ONLY',
            'tessellation_tolerance_mm':.12})
    # No assumed camera/tyre state can produce a global clearance PASS.
    # Actual service-tool cylinders against all stationary geometry; only the target cover is exempt.
    def sweep_check(moving_names,delta,removed_names=(),steps=12):
        result=[];error=[]
        obstacle=[n for n in shapes if n not in moving_names and n not in removed_names]
        for k in range(1,steps+1):
            t=k/steps
            for n in moving_names:
                s=shapes[n].translate(tuple(v*t for v in delta));bb=box(s)
                for other in obstacle:
                    if not possible(bb,boxes[other]):continue
                    try:vol=s.intersect(shapes[other]).Volume()
                    except Exception as exc:error.append(str(exc));continue
                    if vol>.1:result.append({'moving':n,'obstacle':other,'fraction':t,'volume_mm3':round(vol,3)})
        return {'status':'BLOCKED' if result else ('ERROR' if error else 'NO_COLLISION_IN_DISCRETE_SCREEN'),
            'motion_mm':delta,'samples':steps,'collisions':result,'errors':error,'release':'HOLD: discrete envelope screen is not a certified service path'}
    body_names=[n for n in shapes if 'PRESSURE_BODY' in n]
    motor_names=[n for n in shapes if 'POLOLU_5707_MOTOR' in n]
    rear_names=[n for n in shapes if n.startswith('HOLD_REAR_') or 'REAR_SERVICE_COVER' in n or 'REAR_PANEL' in n or 'MAIN_TETHER' in n]
    motor_removed=[n for n in shapes if any(k in n for k in ('PRESSURE_ELECTRONICS_COVER','LIFT_','HARNESS','ACE_','NBK_','PAIRED_MOTOR_HOLDER','SPLIT_ADAPTER')) or categories[n] in ('electronics','electronics_hold')]
    motor_sweep=sweep_check(motor_names,(0,0,80),motor_removed,8)
    motor_sweep['removed_before_screen']=motor_removed
    cam_names=[n for n in shapes if categories[n]=='camera' or 'CAM026_REFERENCE' in n]
    cam_sweep=sweep_check(cam_names,(-80,0,0),[n for n in shapes if 'SP13' in n or 'CAMERA_HARNESS' in n],8)
    tools=[]
    for x,y in itertools.product(g['SERVICE_SCREW_X'],(-19,19)):
        probe=cq.Solid.makeCylinder(3,60,cq.Vector(x,y,82.1),cq.Vector(0,0,1));hits=[]
        for n,s in shapes.items():
            if possible(box(probe),boxes[n]):
                try:v=probe.intersect(s).Volume()
                except Exception as exc:errors.append({'tool':x,'part':n,'error':str(exc)});continue
                if v>.01:hits.append({'id':n,'volume_mm3':v})
        tools.append({'screw_x_mm':x,'screw_y_mm':y,'tool_diameter_mm':6,'approach_mm':60,'collisions':hits,'release':'HOLD: screw/groove/mating dimensions unresolved'})
    gas_sweep=[]
    for deg in range(0,71,2):
        t=math.radians(deg);m=(g['PIVOT_X']-g['gas_move_s']*math.cos(t),16,g['PIVOT_Z_LOW']+g['gas_move_s']*math.sin(t))
        L=math.dist(g['body_pt'],m);gas_sweep.append({'angle_deg':deg,'distance_mm':L,'within_bare_112_to_192':112<=L<=192})
    val={'revision':'Rev.C 2026-09-14','master':'CAD/PX1_Current_Master.step','source_sha256':hashlib.sha256(Path(g['__file__']).read_bytes()).hexdigest(),
        'status':'HOLD_NOT_MANUFACTURING_RELEASE','source_reference':'Proteus CRP150 DRW-002-374/375/386/744/745/752',
        'counts':counts,'expected_counts':expected,'counts_match':counts==expected,'component_count':len(components),'invalid_shapes':invalid,
        'collision_method':{'all_pairs':allpairs,'boolean_pairs_after_AABB':tested,'excluded_pairs':0,'errors':errors,'volume_threshold_mm3':1e-4},
        'interferences':pairs,'dn150':{'diameter_mm':150,'assumed_pipe_center_z_mm':pipeZ,'pose':'LOW, inherited wheel-ground pose H01',
            'all_component_results':radial,'global_status':'HOLD; reference protrusions are reported, real tyre/contact pose unknown'},
        'service':{'motor_vertical_extraction':motor_sweep,'camera_forward_removal':cam_sweep,'service_screw_tools':tools,
            'wheel_removal':'HOLD H01: source quick-lock unknown; proxy cannot certify wheel removal',
            'harness_removal':'HOLD H07: SP13 cable end must be reterminated if larger than gland throat; replacement sequence in documentation'},
        'gas_spring':{'assembled_distance_mm':g['gas_length'],'bare_limits_mm':[112,192],'sampled_angle_checks':gas_sweep,'release':'HOLD H06: end fittings, actual limit angles and physical 150 N balancing'},
        'pressure':{'status':'HOLD H03 H07','cad_is_leak_test':False,'side_cover_window_error_fixed':True,'common_pressure_communication':'requires physical/section verification'},
        'print_outputs':print_validation,'metal_release':False,'part_exports':export_map,
        'unmodelled_required_items':['complete camera PAN/TILT/lighting/control internals','side-cover static seal installed contour','lift pivot bushings and seals','pressure valve spring and seat detail','SP13 panel half and contact inserts','SP17 cable half and seals','internal six-way service connector','board standoffs and all power terminal insulation','INA226 ready-made modules and branch capacitors/TVS/fuses','circlips, internal gear keys and complete fastening hardware'],
        'holds':json.loads((root/'HOLD_REGISTER.json').read_text())}
    (root/'PX1_Current_Validation.json').write_text(json.dumps(val,ensure_ascii=False,indent=2))
    (root/'component_registry.json').write_text(json.dumps(registry,ensure_ascii=False,indent=2))
    # Persist the exact assembly mesh for deterministic drawing generation, without another master model.
    meshes=[]
    for n,p,c in components:
        vv,tt=shapes[n].tessellate(.25,.15)
        meshes.append({'id':n,'category':c,'color':colors.get(c,(.6,.6,.6)),'vertices':[v.toTuple() for v in vv],'triangles':tt})
    import gzip
    with gzip.open(root/'images'/'assembly_mesh.json.gz','wt') as f:json.dump(meshes,f)
    print(json.dumps({'components':len(components),'counts':counts,'invalid':invalid,'interference_count':len(pairs),
        'rigid_interferences':sum(x['classification']=='RIGID_INTERFERENCE' for x in pairs),
        'dn150_protrusions':[(x['id'],x['clearance_mm']) for x in radial if x['clearance_mm']<-.12],
        'motor_sweep':motor_sweep['status'],'camera_sweep':cam_sweep['status']},ensure_ascii=False,indent=2),flush=True)
