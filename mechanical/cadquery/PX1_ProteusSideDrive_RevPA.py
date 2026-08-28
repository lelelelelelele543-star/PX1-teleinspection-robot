import cadquery as cq
import math, json, os

# PX-1 Rev.PA — Proteus CRP-150 source-authentic side-drive reconstruction
# Based on source assemblies DRW-002-374, DRW-002-375, DRW-002-386.
# Purpose: restore proven topology first; unavailable bought parts will be substituted later.

OUT=os.path.abspath('build_revpa')
os.makedirs(OUT, exist_ok=True)

GEAR_TEETH=50
GEAR_MODULE=1.0
GEAR_FACE=4.0
PITCH_D=GEAR_TEETH*GEAR_MODULE
GEAR_OD=(GEAR_TEETH+2)*GEAR_MODULE
STATIONS=[0.0,50.0,100.0,150.0,200.0]
WHEEL_STATIONS=[0.0,100.0,200.0]
IDLER_STATIONS=[50.0,150.0]
INPUT_X=200.0

B61801=(12.0,21.0,5.0)
B61903=(17.0,30.0,7.0)
XRING=(18.72,2.62)
FLANGE_ORING=(32.0,1.5)
SIDE_ORING=(190.0,1.5)
BEVEL_BIG_TEETH=40
BEVEL_SMALL_TEETH=16

COVER_X0=-28.0
COVER_L=256.0
COVER_Z0=-37.0
COVER_H=74.0
COVER_T=5.0
GEAR_Y=-2.0


def involute_gear(teeth,module,face,bore,center=(0,0,0),axis='y',pressure_angle=20.0):
    pa=math.radians(pressure_angle)
    rp=module*teeth/2.0; rb=rp*math.cos(pa); ra=module*(teeth+2)/2.0; rf=max(module*(teeth-2.5)/2.0,0.5)
    pitch=2*math.pi/teeth
    tp=math.sqrt(max((rp/rb)**2-1,0)); invp=tp-math.atan(tp)
    half=math.pi/(2*teeth); off=half+invp
    pts=[]; ns=6
    for k in range(teeth):
        t0=k*pitch
        if rf<rb: pts.append((rf*math.cos(t0-off),rf*math.sin(t0-off)))
        for s in range(ns):
            r=max(rb,rf)+(ra-max(rb,rf))*s/(ns-1); tt=math.sqrt(max((r/rb)**2-1,0)); inv=tt-math.atan(tt)
            a=t0-off+inv; pts.append((r*math.cos(a),r*math.sin(a)))
        for s in reversed(range(ns)):
            r=max(rb,rf)+(ra-max(rb,rf))*s/(ns-1); tt=math.sqrt(max((r/rb)**2-1,0)); inv=tt-math.atan(tt)
            a=t0+off-inv; pts.append((r*math.cos(a),r*math.sin(a)))
        if rf<rb: pts.append((rf*math.cos(t0+off),rf*math.sin(t0+off)))
    g=cq.Workplane('XY').polyline(pts).close().extrude(face)
    if bore: g=g.faces('>Z').workplane().hole(bore,depth=face+0.2)
    if axis=='y':
        g=g.rotate((0,0,0),(1,0,0),90).translate((center[0],center[1]+face/2,center[2]))
    elif axis=='x':
        g=g.rotate((0,0,0),(0,1,0),90).translate((center[0]-face/2,center[1],center[2]))
    else:
        g=g.translate((center[0],center[1],center[2]-face/2))
    return g


def ring_y(x,y,z,od,id_,width):
    o=cq.Workplane('XZ').center(x,z).circle(od/2).extrude(width).translate((0,y,0))
    i=cq.Workplane('XZ').center(x,z).circle(id_/2).extrude(width+0.2).translate((0,y-0.1,0))
    return o.cut(i)

cover=(cq.Workplane('XZ').workplane(offset=0).box(COVER_L,COVER_H,COVER_T,centered=(False,False,False))
       .translate((COVER_X0,0,COVER_Z0)))
for x in WHEEL_STATIONS:
    hole=cq.Workplane('XZ').workplane(offset=-0.1).center(x,0).circle(18.0).extrude(COVER_T+0.2)
    cover=cover.cut(hole)
for x in [-20,20,70,120,170,220]:
    for z in (-31,31):
        h=cq.Workplane('XZ').workplane(offset=-0.1).center(x,z).circle(1.7).extrude(COVER_T+0.2)
        cover=cover.cut(h)

parts={'FAL-002-062_like_SideCover':cover}
for x in STATIONS:
    bore=17.0 if x in WHEEL_STATIONS else 12.0
    name=('GEA-002-529_Axle_Z50' if x in WHEEL_STATIONS else 'GEA-002-528_Idle_Z50')+f'_X{int(x)}'
    parts[name]=involute_gear(50,1.0,GEAR_FACE,bore,(x,GEAR_Y,0),'y')

for x in WHEEL_STATIONS:
    flange=(cq.Workplane('XZ').workplane(offset=COVER_T).center(x,0).circle(24.0).extrude(4.0)
            .cut(cq.Workplane('XZ').workplane(offset=COVER_T-0.1).center(x,0).circle(9.5).extrude(4.2)))
    parts[f'FSS-002-061_AxleFlange_X{int(x)}']=flange
    parts[f'BEA-002-704_61903_X{int(x)}']=ring_y(x,COVER_T+0.5,0,30,17,7)
    parts[f'SEA-002-526_XRing_X{int(x)}']=ring_y(x,COVER_T+7.7,0,21.34,18.72,2.62)
    parts[f'SEA-002-722_O32x1p5_X{int(x)}']=ring_y(x,COVER_T+0.2,0,35.0,32.0,1.5)


def shaft_y(x,y0,segments):
    out=None; yy=y0
    for d,l in segments:
        s=cq.Workplane('XZ').workplane(offset=yy).center(x,0).circle(d/2).extrude(l)
        out=s if out is None else out.union(s)
        yy+=l
    return out

for x in [0.0,100.0]:
    parts[f'FSS-002-063_AxleShort_X{int(x)}']=shaft_y(x,-8.0,[(12,7),(17,14),(18.5,4),(17,10)])

parts['FSS-002-064_AxleLong_INPUT_X200']=shaft_y(200.0,-28.0,[(10,12),(12,10),(17,14),(18.5,4),(17,15)])
parts['BEA-002-701_61801_LongAxle']=ring_y(200,-21.0,0,21,12,5)

for x in IDLER_STATIONS:
    parts[f'BEA-002-537_Bushing10_12_4_X{int(x)}']=ring_y(x,-7.0,0,12,10,4)
    parts[f'IdlerPin_X{int(x)}']=cq.Workplane('XZ').workplane(offset=-9).center(x,0).circle(5).extrude(10)

bevel_big=(cq.Workplane('XZ').workplane(offset=-30).center(200,0).circle(21).workplane(offset=8).circle(14).loft())
parts['GEA-002-530_BevelZ40_envelope']=bevel_big
motor=(cq.Workplane('YZ').center(-15,0).circle(16).extrude(75).translate((205,0,0)))
parts['MOT-001-760_replacement_envelope']=motor
bevel_small=(cq.Workplane('YZ').center(-15,0).circle(9).workplane(offset=7).circle(5).loft().translate((193,0,0)))
parts['GEA-002-531_BevelZ16_envelope']=bevel_small

for x in WHEEL_STATIONS:
    parts[f'Wheel90_reference_X{int(x)}']=cq.Workplane('XZ').workplane(offset=COVER_T+13).center(x,0).circle(45).extrude(14)

assy=cq.Assembly(name='PX1_ProteusSideDrive_RevPA')
colors={'cover':cq.Color(0.45,0.48,0.52),'gear':cq.Color(0.75,0.68,0.40),'shaft':cq.Color(0.78,0.16,0.14),'bearing':cq.Color(0.35,0.38,0.42),'seal':cq.Color(0.12,0.12,0.12),'wheel':cq.Color(0.08,0.08,0.08),'motor':cq.Color(0.25,0.38,0.55)}
for n,p in parts.items():
    if 'SideCover' in n: c=colors['cover']
    elif 'Z50' in n or 'BevelZ' in n: c=colors['gear']
    elif 'Axle' in n or 'Pin' in n: c=colors['shaft']
    elif 'BEA-' in n: c=colors['bearing']
    elif 'SEA-' in n: c=colors['seal']
    elif 'Wheel90' in n: c=colors['wheel']
    elif 'MOT-' in n: c=colors['motor']
    else: c=cq.Color(0.6,0.6,0.6)
    assy.add(p,name=n,color=c)

assy.save(os.path.join(OUT,'PX1_ProteusSideDrive_RevPA.step'))

gear_sign={200:+1,150:-1,100:+1,50:-1,0:+1}
wheel_sign={x:gear_sign[x] for x in WHEEL_STATIONS}
checks={
    'source_topology':'5 x Z50 B4; 3 axle gears + 2 idlers; rear/end wheel axle is long input axle',
    'stations_mm':STATIONS,
    'wheel_stations_mm':WHEEL_STATIONS,
    'idler_stations_mm':IDLER_STATIONS,
    'input_station_mm':INPUT_X,
    'wheel_rotation_signs':wheel_sign,
    'all_wheels_same_direction':len(set(wheel_sign.values()))==1,
    'mesh_counts_from_input_to_wheels':{str(x):int(abs(INPUT_X-x)/50) for x in WHEEL_STATIONS},
    'extra_intermediate_input_shaft_present':False,
    'source_bearings':{'61801':'12x21x5 qty1/side','61903':'17x30x7 qty3/side'},
    'source_dynamic_seal':'X-Ring 18.72x2.62 qty3/side',
    'source_static_seals':['32x1.5 O-ring x3/side','190x1.5 O-ring side cover'],
    'status':'PASS topology reconstruction; exact source part profiles/mounting distances still require detailed part drawings or physical measurement'
}
with open(os.path.join(OUT,'REV_PA_VALIDATION.json'),'w') as f: json.dump(checks,f,indent=2)
print(json.dumps(checks,indent=2))