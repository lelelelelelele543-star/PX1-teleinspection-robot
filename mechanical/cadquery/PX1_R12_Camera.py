"""PX1 R12 camera: engineering envelope with selected modules, not released tooling.
Dimensions mm; X points rearward. PAN about Y through (30,0,0).
No tooth geometry, bearing retainers, pressure rating or complete harness release.
"""
from pathlib import Path
import argparse,itertools,json,math
import cadquery as cq
from PX1_R12_SelectedParts import box,cyl,ann,volume,intersect,outside,bounds

ROOT=Path(__file__).resolve().parents[2]
def sphere(r,p):return cq.Workplane('XY').sphere(r).translate(p)
def cone(r1,r2,length,p):
    return cq.Workplane('XY').newObject([cq.Solid.makeCone(r1,r2,length,cq.Vector(*p),cq.Vector(1,0,0))])
def bevel_reference(axis,sign):
    # Equal 20/20, m0.5, face2.5; no invented apex-length hub.
    lo=(math.sqrt(50)-2.5)/math.sqrt(2)
    sh=cq.Workplane('XY').workplane(offset=lo).circle(5.5*(math.sqrt(50)-2.5)/math.sqrt(50)).workplane(offset=5-lo).circle(5.5).loft()
    sh=sh.cut(cyl(3.05 if axis=='x' else 6.05,9,(0,0,4.5)))
    sh=sh.rotate((0,0,0),(0,1,0),90) if axis=='x' else sh.rotate((0,0,0),(1,0,0),90)
    return sh.translate((30,-34.5,0))
def micro(face,y):
    return box(29.5,10,12,face+14.75,y,0).union(cyl(3,9,(face-4.5,y,0),'x'))

def build(out):
    out.mkdir(parents=True,exist_ok=True)
    parts,groups={},{}
    def add(n,p,g):parts[n]=p;groups[n]=g;return p
    clip=box(100,100,100,62,0,0) # X12..112
    head=sphere(26,(30,0,0)).intersect(clip)
    cavity=sphere(24,(30,0,0)).intersect(box(80,100,100,58,0,0)) # X18+
    head=head.cut(cavity).cut(cyl(28,12,(12,0,0),'x')).cut(cyl(32.2,3.5,(13.75,0,0),'x'))
    head=head.cut(ann(28.6,31.4,.75,(15.875,0,0),'x'))
    for y,z in ((16.5,0),(-16.5,0),(0,16.5),(0,-16.5)):
        head=head.cut(cyl(1.25,4,(14.5,y,z),'x'))
    add('PAN_head_6061',head,'pan_housing')
    bezel=ann(30,35,1.5,(11.75,0,0),'x')
    for y,z in ((16.5,0),(-16.5,0),(0,16.5),(0,-16.5)):
        bezel=bezel.cut(cyl(1.8,2,(11.75,y,z),'x'))
    add('Window_bezel',bezel,'pan_housing')
    add('Glass_32x3_RESERVE',cyl(32,3,(14,0,0),'x'),'pan_window')
    add('RunCam_Phoenix2SEV2',box(22,19,19,27,0,0),'pan_component')
    # Tapered rear housing keeps the +/-135-degree optical AXIS clear.
    fore=cone(31,45,14,(64,0,0)).union(cyl(60,40,(98,0,0),'x'))
    fore=fore.cut(cyl(56,52,(93,0,0),'x')) # internal X67..119
    for s in (-1,1):
        pod=box(56,16,24,50,s*35,0)
        # Blind dry cheeks; hardware fixing/cover details remain open.
        pod=pod.cut(box(10,13,14,34,s*35.5,0))
        pod=pod.cut(cyl(6.2,19,(30,s*35,0),'y'))
        pod=pod.cut(cyl(12,4,(30,s*29,0),'y'))
        pod=pod.cut(cyl(13.02,3.5,(30,s*32.75,0),'y'))
        if s==-1:
            pod=pod.cut(box(33,10.4,12.4,55.5,-34.5,0))
            pod=pod.cut(cyl(3.2,4,(39,-34.5,0),'x'))
            pod=pod.cut(cyl(4,12,(69,-28,0),'y'))
        fore=fore.union(pod)
    add('Rotating_fore_housing',fore.clean(),'rotating_housing')
    for s in (-1,1):
        add('PAN_686_'+str(s),ann(6,13,3.5,(30,s*32.75,0),'y'),'bearing')
        add('PAN_TC6x12x4_'+str(s),ann(6,12,4,(30,s*29,0),'y'),'seal')
        # Axles deliberately join the head shell; attachment not released.
        add('PAN_hollow_axle_'+str(s),ann(3,6,16,(30,s*32,0),'y'),'pan_drive')
    add('Pololu3046_PAN',micro(40,-34.5),'rotating_component')
    add('PAN_Z20_driver_REFERENCE',bevel_reference('x',-1),'gear_reference')
    add('PAN_Z20_driven_REFERENCE',bevel_reference('y',-1),'gear_reference')
    pack={
      'RP2040_Zero':(23.5,18,4,80,10,-16),
      'DRV8871_PAN':(24.4,20.4,9.7,80,10,3),
      'RECOM_R78C5V':(11.6,8.5,10.4,80,-14,-13),
      'MPRLS_3965':(17.8,16.7,7.5,82,4,20),
      'LDD300L':(22.6,9.9,8.9,80,-13,14)
    }
    for n,d in pack.items():add(n,box(*d),'rotating_component')
    # RECOM lead/service space is kept separate from actual body dimensions.
    add('RECOM_LEADS_ALLOWANCE',box(12,9,4.1,80,-14,-20.25),'service')
    rear=cyl(90,88,(122,0,0),'x').cut(cyl(60.2,38,(97,0,0),'x'))
    rear=rear.cut(cyl(80,7,(81.5,0,0),'x'))
    for x in (91,109):rear=rear.cut(cyl(78.02,10,(x,0,0),'x'))
    rear=rear.cut(cyl(84,40,(136,0,0),'x')).cut(cyl(70,12,(162,0,0),'x'))
    rear=rear.cut(ann(73.2,78.8,1.5,(165.25,0,0),'x'))
    cap=cyl(90,4,(168,0,0),'x')
    for a in range(0,360,60):
        y,z=42*math.cos(math.radians(a)),42*math.sin(math.radians(a))
        rear=rear.cut(cyl(2.5,8,(162,y,z),'x'))
        cap=cap.cut(cyl(3.4,5,(168,y,z),'x'))
    cap=cap.cut(cyl(8.8,6,(168,0,0),'x')) # M10 ending pilot, not a sealed ending
    add('Fixed_rear_housing',rear,'fixed_housing')
    add('Rear_cap',cap,'fixed_housing')
    add('ROTATE_TC60x80x7',ann(60,80,7,(81.5,0,0),'x'),'seal')
    for x in (91,109):add('ROTATE_61812_'+str(x),ann(60,78,10,(x,0,0),'x'),'bearing')
    add('ROTATE_Z160_m04_REFERENCE',ann(60.05,64.8,3,(116.5,0,0),'x'),'gear_reference')
    add('ROTATE_Z20_m04_REFERENCE',ann(3.05,8.8,3,(116.5,36,0),'x'),'gear_reference')
    add('Pololu3046_ROTATE',micro(120,36),'fixed_component')
    add('Senring_M125_06',cyl(12.5,13.5,(126.75,0,0),'x'),'fixed_component')
    comps={n:p for n,p in parts.items() if groups[n].endswith('component')}
    housings={n:p for n,p in parts.items() if groups[n].endswith('housing')}
    checks={'revision':'R12','manufacturing_release':False,'camera_axial_extent_max_mm':[4,170],
      'outer_diameter_candidate_mm':90,'body_length_zero_pan_mm':159,
      'component_pairs':{},'component_vs_housing':{},'solid_validity':{n:p.val().isValid() for n,p in parts.items()},
      'housing_solid_counts':{n:len(p.solids().vals()) for n,p in housings.items()},
      'pan_sweep_collisions':{},'pan_optical_axis_collisions':{},
      'module_bounds_mm':{n:bounds(p) for n,p in comps.items()},
      'limitations':['Candidate is larger than CAM026 and is not a drop-in replacement.',
       'No pressure-depth certification, completed bearing retention, fit tolerances or tooth geometry.',
       'Only optical axis is checked; full RunCam field of view and refraction NOT validated.',
       'LED boards/windows and PAN/ROTATE angle feedback remain unresolved.',
       'Internal module holders, opening/service sequence and flexible harness remain unresolved.',
       'PAN axle-to-head static seals and external cable ending are unfinished.',
       'Full body/lift assembly and pipe bends are not certified by this check.',
       'Main tether has six cores. Short body-camera harness also needs fixed ROTATE and feedback circuits.']}
    for (n,p),(m,q) in itertools.combinations(comps.items(),2):
        v=intersect(p,q)
        if v>1e-3:checks['component_pairs'][n+'__'+m]=v
    for n,p in comps.items():
        for m,q in housings.items():
            v=intersect(p,q)
            if v>1e-3:checks['component_vs_housing'][n+'__'+m]=v
    rotating_targets={n:p for n,p in parts.items() if groups[n] in ('rotating_housing','fixed_housing','rotating_component','fixed_component')}
    moving={n:p for n,p in parts.items() if groups[n] in ('pan_housing','pan_window','pan_component')}
    for a in range(-135,136,5):
        for n,p in moving.items():
            p=p.rotate((30,0,0),(30,1,0),a)
            for m,q in rotating_targets.items():
                v=intersect(p,q)
                if v>1e-3:checks['pan_sweep_collisions'][str(a)+'__'+n+'__'+m]=v
        r=math.radians(a);v=cq.Vector(-math.cos(r),0,math.sin(r))
        ray=cq.Workplane('XY').newObject([cq.Solid.makeCylinder(.25,240,cq.Vector(30,0,0)+v*27,v)])
        for n,p in rotating_targets.items():
            iv=intersect(ray,p)
            if iv>1e-3:checks['pan_optical_axis_collisions'][str(a)+'__'+n]=iv
    fail=any(checks[k] for k in ('component_pairs','component_vs_housing','pan_sweep_collisions','pan_optical_axis_collisions')) or not all(checks['solid_validity'].values())
    checks['status']='FAIL' if fail else 'PASS_SCOPED_CAMERA_PACKING_AND_AXIS_SWEEP'
    (out/'camera_validation.json').write_text(json.dumps(checks,indent=2))
    ass=cq.Assembly(name='PX1_R12_CAMERA_CANDIDATE')
    for n,p in parts.items():
        c=(.5,.53,.56) if groups[n].endswith('housing') else (.1,.5,.3) if groups[n].endswith('component') else (.75,.55,.16)
        ass.add(p,name=n.replace('-','minus'),color=cq.Color(*c))
    ass.export(str(out/'PX1_R12_CAMERA_CANDIDATE.step'))
    print(json.dumps({k:v for k,v in checks.items() if k not in ('solid_validity','module_bounds_mm','limitations')},indent=2))
    return parts,groups,checks
if __name__=='__main__':
    p=argparse.ArgumentParser();p.add_argument('--out',type=Path,default=ROOT/'build_r12');a=p.parse_args();build(a.out)
