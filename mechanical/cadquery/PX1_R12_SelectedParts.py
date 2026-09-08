"""PX1 R12: reproducible selected-parts CAD, mm. NOT manufacturing release.
Run: python mechanical/cadquery/PX1_R12_SelectedParts.py [--motor-step vendor.step]
Vendor STEP is optional and not redistributed. Gears are mesh envelopes.
"""
from pathlib import Path
import argparse, itertools, json, math
import cadquery as cq

ROOT=Path(__file__).resolve().parents[2]
L=412.
SEAT=math.sqrt(75**2-58.8**2)-44
WHEELS=(50.,150.,250.)
GEARS=(50.,100.,150.,200.,250.)
def box(a,b,c,x,y,z):return cq.Workplane('XY').box(a,b,c).translate((x,y,z))
def cyl(d,l,p,axis='z'):
    v={'x':(1,0,0),'y':(0,1,0),'z':(0,0,1)}[axis]
    o=cq.Vector(*[p[i]-v[i]*l/2 for i in range(3)])
    return cq.Workplane('XY').newObject([cq.Solid.makeCylinder(d/2,l,o,cq.Vector(*v))])
def ann(di,do,l,p,axis='z'):return cyl(do,l,p,axis).cut(cyl(di,l+1,p,axis))
def rr(a,b,r,h,p):return box(a,b,h,*p).edges('|Z').fillet(r)
def ring(a,b,r,w,h,p):return rr(a+w,b+w,r+w/2,h,p).cut(rr(a-w,b-w,r-w/2,h+1,p))
def volume(p):return sum(x.Volume() for x in p.solids().vals())
def intersect(a,b):return max(0.,volume(a.intersect(b)))
def outside(a,b):return max(0.,volume(a.cut(b)))
def bounds(p):
    b=p.val().BoundingBox()
    return [[b.xmin,b.ymin,b.zmin],[b.xmax,b.ymax,b.zmax]]

def body():
    sh=cq.Workplane('YZ').polyline([(-39,20),(39,20),(43,24),(43,122),(-43,122),(-43,24)]).close().extrude(L)
    sh=sh.union(box(L,96,4,206,0,124))
    sh=sh.cut(box(L-16,78,98,206,0,73)).cut(box(L-32,76,18,206,0,127))
    for s in (-1,1):
        sh=sh.union(box(258,6.5,64,150,s*42.75,75))
        sh=sh.cut(box(250,17,58,150,s*37.5,75))
        for x in WHEELS:
            sh=sh.union(cyl(40,10.35,(x,s*40.475,75),'y'))
            # Actual connecting webs; a floating bearing ring is not a housing.
            sh=sh.union(box(16,7.75,17,x,s*39.525,51.5))
            for d,t,y in ((18.25,25,39),(30.05,7.2,39.15),(40.15,2.7,44.75)):
                sh=sh.cut(cyl(d,t,(x,s*y,75),'y'))
        for x in (38,75,112,150,188,225,262):
            for z in (48,102):sh=sh.cut(cyl(2.5,5.5,(x,s*43.25,z),'y'))
    sh=sh.cut(ring(390,84,8,2.8,1.5,(206,0,125.25)))
    bolts=[(x,y) for x in (28,78,128,178,228,278,328,378) for y in (-46,46)]
    bolts += [(x,y) for x in (6,406) for y in (-28,0,28)]
    lid=rr(412,96,4,5,(206,0,128.5))
    for x,y in bolts:
        sh=sh.cut(cyl(2.5,7,(x,y,122.5)))
        lid=lid.cut(cyl(3.4,6,(x,y,128.5)))
    # Thread pilot bores only. Final sealed endings are still required.
    sh=sh.cut(cyl(14.5,10,(408,0,45),'x'))
    sh=sh.cut(cyl(8.8,10,(4,0,65),'x'))
    sh=sh.cut(cyl(8.8,9,(408,23,104),'x'))
    return sh.clean(),lid

def side_cover(s):
    sh=rr(258,62,7,4,(0,0,0)).rotate((0,0,0),(1,0,0),90).translate((150,s*48,75))
    for z in (50,100):sh=sh.union(box(244,4,4,150,s*44,z))
    for x in (75,125,175,225):sh=sh.union(box(4,4,46,x,s*44,75))
    for x in WHEELS:sh=sh.cut(cyl(35.05,12,(x,s*47,75),'y'))
    for x in (100,200):
        sh=sh.union(cyl(16,8,(x,s*42,75),'y'))
        sh=sh.cut(cyl(10.05,9.5,(x,s*42.75,75),'y')) # outer wall 2.5
    groove=ring(246,42,17,2.1,1.1,(0,0,0)).rotate((0,0,0),(1,0,0),90).translate((150,s*46.55,75))
    sh=sh.cut(groove)
    for x in (38,75,112,150,188,225,262):
        for z in (48,102):sh=sh.cut(cyl(3.4,7,(x,s*48,z),'y'))
    return sh.clean()

def flange(x,s):
    sh=cyl(40,2.5,(x,s*44.75,75),'y').union(cyl(34.9,4,(x,s*48,75),'y'))
    sh=sh.cut(cyl(18.15,9,(x,s*47,75),'y')).cut(cyl(22.8,2.8,(x,s*48.45,75),'y'))
    return sh.cut(ann(32.85,36.9,2,(x,s*46.95,75),'y'))

def bevel(z,mate,bore):
    m,f=1.25,6.
    R=m/2*math.hypot(z,mate); d=math.atan2(z,mate)
    lo,hi=(R-f)*math.cos(d),R*math.cos(d)
    r1,r2=(m*z/2+m)*(R-f)/R,m*z/2+m
    sh=cq.Workplane('XY').workplane(offset=lo).circle(r1).workplane(offset=hi-lo).circle(r2).loft()
    sh=sh.union(cyl(max(bore+5,m*z*.42),lo,(0,0,lo/2)))
    return sh.cut(cyl(bore,hi+2,(0,0,hi/2)))

def motor(path,s):
    if path:
        sh=cq.importers.importStep(str(path)).translate((-19.925,0,-19.925))
        sh=sh.rotate((0,0,0),(1,0,0),90).rotate((0,0,0),(0,0,1),-90)
    else:
        sh=cyl(36.8,26.5,(13.25,0,0),'x').union(cyl(34,30.7,(41.85,0,0),'x'))
        sh=sh.union(cyl(34.8,15.4,(64.9,0,0),'x')).union(cyl(12,6,(-3,0,-7),'x'))
        sh=sh.union(cyl(6,16,(-14,0,-7),'x')).union(box(10,10,8.5,65,0,-18.4))
    return sh.translate((330,s*19.5,82))

def crown(x,s):
    stations=[(51,31),(55.7,41),(57.2,44),(58.8,44),(60.3,41),(65,31)]
    result=None
    for (y0,r0),(y1,r1) in zip(stations,stations[1:]):
        o,v=cq.Vector(x,s*y0,75),cq.Vector(0,s,0)
        sol=cq.Solid.makeCylinder(r0,y1-y0,o,v) if r0==r1 else cq.Solid.makeCone(r0,r1,y1-y0,o,v)
        sh=cq.Workplane('XY').newObject([sol]);result=sh if result is None else result.union(sh)
    return result.cut(cyl(18.1,18,(x,s*58.5,75),'y'))

COMPONENTS={
 'NUCLEO_F446RE':(82.5,70,18,86.25,0,112),
 'Pololu_2855_12V':(17.8,17.8,8,153,-18,111),
 'RECOM_5V_carrier_ALLOWANCE':(22,20,20,155,16,115),
 'MPRLS_3965':(17.8,16.7,7.5,24,0,111.75),
 'TMP117_4821':(25.5,4.6,17.7,80,-25,75),
 # Video transmitter is now in the BODY to reduce camera bulk.
 'SEBOKS_SU1P':(50,42,18,203,0,116),
 'Waveshare_RS485_C':(42.8,15.2,4.75,264,17,113.375),
 'DRV8871_left':(24.4,20.4,9.7,256,-19,111.85),
 'DRV8871_right':(24.4,20.4,9.7,294,-19,111.85),
 'DRV8871_rotate':(24.4,20.4,9.7,334,-19,113.85),
 'INA260_left_TERMINAL_ALLOWANCE':(22.9,22.8,14,314,19,118),
 'INA260_right_TERMINAL_ALLOWANCE':(22.9,22.8,14,364,19,118),
 '24V_distribution_RESERVE':(46,30,20,345,0,40)
}
SERVICE={
 'NUCLEO_F446RE':(92.5,76,26,86.25,0,113),
 'RECOM_5V_carrier_ALLOWANCE':(28,26,25,155,16,113.5),
 'SEBOKS_SU1P':(60,50,20,203,0,116),
 'Waveshare_RS485_C':(52,22,14,264,17,114),
 'DRV8871_left':(30,27,17,256,-19,113),
 'DRV8871_right':(30,27,17,294,-19,113),
 'DRV8871_rotate':(30,27,17,334,-19,115),
 'INA260_left_TERMINAL_ALLOWANCE':(29,30,20,314,19,116),
 'INA260_right_TERMINAL_ALLOWANCE':(29,30,20,364,19,116)
}

def build(out,path=None):
    out.mkdir(parents=True,exist_ok=True)
    parts,groups={},{}
    def add(n,p,g):parts[n]=p;groups[n]=g;return p
    main,lid=body();add('BODY_6061',main,'housing');add('LID_5mm',lid,'housing')
    add('RSD100D24',box(161,36,68,108.5,0,63),'component')
    for x in (22,195):add('RSD_terminals_'+str(x),box(12,24,44,x,0,63),'component')
    heat=box(167,4,74,108.5,-20,61).union(box(167,14,4,108.5,-15,26))
    for x in (30.5,186.5):
        for z in (35.5,90.5):heat=heat.cut(cyl(2.5,6,(x,-20,z),'y'))
    add('RSD_thermal_angle',heat,'mount')
    for n,d in COMPONENTS.items():add(n,box(*d),'component')
    tray=box(290,60,2,154,0,99)
    for x in (20,136,176,270):
        for y in (-27,27):tray=tray.cut(cyl(3.4,4,(x,y,99)))
    add('Front_tray',tray,'mount')
    add('Rear_tray',box(85,74,2,346,0,107),'mount')
    add('HV_route_RESERVE',box(375,7,7,210,-29,34),'route')
    add('LV_route_RESERVE',box(260,7,7,159,27,34),'route')
    add('signal_front_RESERVE',box(181,8,4,104.5,25,95),'route')
    add('signal_rear_RESERVE',box(110,8,4,262,0,104),'route')
    add('signal_tail_RESERVE',box(84,8,4,360,25,45),'route')
    for s in (-1,1):
        a='L' if s==1 else 'R'; sy=s*19.5
        add('Pololu4695_'+a,motor(path,s),'component')
        br=box(4,38.8,42,328,sy,82).cut(cyl(12.2,6,(328,sy,75),'x'))
        for d in range(0,360,60):
            y,z=sy+15.5*math.cos(math.radians(d)),82+15.5*math.sin(math.radians(d))
            br=br.cut(cyl(3.2,6,(328,y,z),'x'))
        add('Motor_mount_'+a,br,'mount')
        add('Coupler_6_6_'+a,ann(6,18,18,(308,sy,75),'x'),'drive')
        sh=cyl(12,31,(283.5,sy,75),'x').union(cyl(6,9,(303.5,sy,75),'x'))
        add('Pinion_shaft_'+a,sh,'drive')
        for x in (278.5,295.5):
            add('61801_'+a+str(x),ann(12,21,5,(x,sy,75),'x'),'bearing')
            b=box(5,27,42,x,sy,62.5).cut(cyl(21.02,7,(x,sy,75),'x'))
            add('Pinion_support_'+a+str(x),b,'mount')
        add('Z16_ENVELOPE_'+a,bevel(16,40,12.05).rotate((0,0,0),(0,1,0),90).translate((250,sy,75)),'gear_envelope')
        add('Z40_ENVELOPE_'+a,bevel(40,16,10.05).rotate((0,0,0),(1,0,0),-s*90).translate((250,sy,75)),'gear_envelope')
        add('61800_'+a,ann(10,19,5,(250,s*12,75),'y'),'bearing')
        b=box(24,5,41,250,s*12,64.5).cut(cyl(19.02,7,(250,s*12,75),'y'))
        add('Rear_inner_support_'+a,b,'mount')
        add('Side_cover_'+a,side_cover(s),'housing')
        for x in GEARS:
            di=17.1 if x in WHEELS else 18.05
            add('Z50_ENVELOPE_'+a+str(x),ann(di,52,3.75,(x,s*33.5,75),'y'),'gear_envelope')
        for x in (100,200):
            sh=cyl(12,4,(x,s*33.5,75),'y').union(cyl(10,12,(x,s*41.5,75),'y'))
            add('Idler_pin_'+a+str(x),sh,'drive')
            add('6701_'+a+str(x),ann(12,18,4,(x,s*33.5,75),'y'),'bearing')
        for x in WHEELS:
            add('Flange_'+a+str(x),flange(x,s),'seal_holder')
            sh=cyl(17,13.8,(x,s*36.6,75),'y').union(cyl(18,22,(x,s*54.5,75),'y'))
            if x==250:sh=sh.union(cyl(10,22.7,(x,s*18.35,75),'y'))
            add('Axle_'+a+str(x),sh,'drive')
            add('61903_'+a+str(x),ann(17,30,7,(x,s*39.15,75),'y'),'bearing')
            add('Crown_'+a+str(x),crown(x,s),'wheel')
    add('M16_gland_INSTALLATION_RESERVE',ann(8,24,32,(428,0,45),'x'),'external_reserve')
    add('Aramid_anchor_INSTALLATION_RESERVE',ann(8,28,30,(459,0,45),'x'),'external_reserve')
    pipe=cyl(150,800,(150,0,75),'x'); boundary=main.union(lid)
    components={n:p for n,p in parts.items() if groups[n]=='component'}
    checks={'revision':'R12-recovered','manufacturing_release':False,
      'body_envelope_mm':[412,100,111],'motor_model':'vendor_STEP' if path else 'documented_dimension_abstraction',
      'housing_solid_count':len(main.solids().vals()),'seated_drop_mm':SEAT,
      'body_and_lid_outside_DN150_mm3':outside(boundary.translate((0,0,-SEAT)),pipe),
      'wheel_outside_DN150_mm3':{n:outside(p.translate((0,0,-SEAT)),pipe) for n,p in parts.items() if groups[n]=='wheel'},
      'valid':{n:p.val().isValid() for n,p in parts.items()},
      'body_lid_aluminum_mass_kg':(volume(main)+volume(lid))*2.7e-6,
      'component_vs_housing':{},'component_pairs':{},'component_vs_mounts':{},'component_vs_drive':{},
      'service_vs_housing':{},'routing_collisions':{},'bounds_mm':{n:bounds(p) for n,p in parts.items()},
      'limitations':['No full-assembly collision certificate.','Camera is a separate unfinished assembly.',
       'Gear envelopes overlap intentionally; tooth conjugacy and gear/mount contacts not validated.',
       'Some mount attachment details and axial retention remain unresolved.',
       'Connector clearances are allowances, not measurements.',
       'No pressure, thermal, electrical or field test performed.']}
    for n,p in components.items():
        checks['component_vs_housing'][n]=intersect(p,boundary)
        for m,q in parts.items():
            key='component_vs_mounts' if groups[m]=='mount' else 'component_vs_drive' if groups[m] in ('gear_envelope','drive','bearing') else None
            if key:
                v=intersect(p,q)
                if v>1e-4:checks[key][n+'__'+m]=v
    for (n,p),(m,q) in itertools.combinations(components.items(),2):
        v=intersect(p,q)
        if v>1e-4:checks['component_pairs'][n+'__'+m]=v
    for n,d in SERVICE.items():checks['service_vs_housing'][n]=intersect(box(*d),boundary)
    for n,p in parts.items():
        if groups[n]=='route':
            for m,q in parts.items():
                if groups[m] in ('component','housing','drive','bearing','gear_envelope'):
                    v=intersect(p,q)
                    if v>1e-4:checks['routing_collisions'][n+'__'+m]=v
    fail=(checks['housing_solid_count']!=1 or not all(checks['valid'].values()) or
      checks['body_and_lid_outside_DN150_mm3']>1e-4 or
      max(checks['wheel_outside_DN150_mm3'].values(),default=0)>1e-4 or
      max(checks['component_vs_housing'].values(),default=0)>1e-4 or
      max(checks['service_vs_housing'].values(),default=0)>1e-4 or
      any(checks[k] for k in ('component_pairs','component_vs_mounts','component_vs_drive','routing_collisions')))
    checks['status']='FAIL' if fail else 'PASS_SCOPED_COMPONENT_PACKING'
    (out/'validation.json').write_text(json.dumps(checks,indent=2))
    ass=cq.Assembly(name='PX1_R12_COMPONENT_PACKING')
    colors={'housing':(.45,.5,.53),'component':(.15,.48,.32),'gear_envelope':(.82,.62,.2),'wheel':(.15,.15,.15),'route':(.9,.25,.1,.3)}
    for n,p in parts.items():ass.add(p,name=n.replace('.','_'),color=cq.Color(*colors.get(groups[n],(.65,.67,.7))))
    ass.export(str(out/'PX1_R12_COMPONENT_PACKING.step'))
    cq.exporters.export(main,str(out/'PX1_R12_BODY.step'))
    cq.exporters.export(lid,str(out/'PX1_R12_LID.step'))
    print(json.dumps({k:v for k,v in checks.items() if k not in ('valid','bounds_mm','limitations')},indent=2))
    return parts,groups,checks

if __name__=='__main__':
    p=argparse.ArgumentParser();p.add_argument('--out',type=Path,default=ROOT/'build_r12');p.add_argument('--motor-step',type=Path)
    a=p.parse_args();build(a.out,a.motor_step)
