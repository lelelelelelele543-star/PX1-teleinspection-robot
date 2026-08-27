import cadquery as cq
import math, json, os

# PX-1 Rev.FF — CRP150-source-aligned side drive production candidate
# Dimensions mm. Prototype only, not machining release.

# Source-driven architecture
COVER_L=286.0
COVER_H=86.0
COVER_T=5.0
WX=[50.0,150.0,250.0]
WZ=45.0
FLANGE_OD=50.0
FLANGE_T=12.0
FLANGE_PCD=40.0
FLANGE_HOLES=4
COVER_M3_CLR=3.4
FLANGE_M3_CLR=3.4

# Side cover main O-ring: 190 x 1.5 source item.
ORING_ID=190.0
ORING_CS=1.5
# Groove candidate derived from static 20% squeeze and <85% fill.
GROOVE_D=1.20
GROOVE_W=1.90
# Fit a racetrack with same centerline length as nominal O-ring circumference.
# Choose overall centerline height 64 mm to leave useful edge margin.
RT_H=64.0
RT_R=RT_H/2.0
RT_CIRC=math.pi*ORING_ID
RT_STRAIGHT=(RT_CIRC-2*math.pi*RT_R)/2.0
RT_L=RT_STRAIGHT+2*RT_R

# Wheel station shaft / bearings / dynamic seal candidate
D_INNER=12.0
D_BEARING_OUT=17.0
D_XRING_LAND=19.0
D_WHEEL_SEAT=17.0
L_INNER_TOTAL=23.0
L_B61903=7.0
L_XRING=4.0
L_LAB=2.0
L_WHEEL=18.0
XRING_ID=18.72
XRING_CS=2.62
XRING_SQUEEZE=0.12
XRING_GLAND_D=D_XRING_LAND+2*XRING_CS*(1-XRING_SQUEEZE)
XRING_GROOVE_W=3.4

# Cover body, origin x=0..286, y=0..86, z=0..5
cover = cq.Workplane('XY').box(COVER_L,COVER_H,COVER_T, centered=(False,False,False))

# Three flange pilot holes in side cover: pilot for flange register. Candidate Ø36.
for x in WX:
    cover = cover.faces('>Z').workplane().center(x-COVER_L/2, WZ-COVER_H/2).hole(36.0)

# 12 perimeter M3 cover holes; compact source-like pattern, outside seal path.
cover_holes=[
    (8,5),(62,5),(116,5),(170,5),(224,5),(278,5),
    (8,81),(62,81),(116,81),(170,81),(224,81),(278,81),
]
for x,y in cover_holes:
    cover=cover.faces('>Z').workplane().center(x-COVER_L/2,y-COVER_H/2).hole(COVER_M3_CLR)

# Candidate main seal groove as racetrack, centered in plate.
center_x=COVER_L/2
center_y=COVER_H/2
outer_slot=(cq.Workplane('XY').workplane(offset=COVER_T-GROOVE_D)
            .center(center_x,center_y)
            .slot2D(RT_L+GROOVE_W,RT_H+GROOVE_W,0).extrude(GROOVE_D))
inner_slot=(cq.Workplane('XY').workplane(offset=COVER_T-GROOVE_D)
            .center(center_x,center_y)
            .slot2D(RT_L-GROOVE_W,RT_H-GROOVE_W,0).extrude(GROOVE_D))
groove=outer_slot.cut(inner_slot)
cover=cover.cut(groove)

# Flange candidate at local origin; z>0 is external/wheel side.
# Only 3 mm projects beyond the cover face; 9 mm bearing spigot enters the dry side bay.
FLANGE_EXT=3.0
FLANGE_IN=9.0
flange=(cq.Workplane('XY').circle(FLANGE_OD/2).extrude(FLANGE_EXT)
        .union(cq.Workplane('XY').workplane(offset=0).circle(18.0).extrude(-FLANGE_IN)))
flange=flange.faces('>Z').workplane().hole(20.0, depth=FLANGE_EXT+FLANGE_IN)
for a in range(0,360,90):
    r=FLANGE_PCD/2
    px=r*math.cos(math.radians(a)); py=r*math.sin(math.radians(a))
    flange=flange.faces('>Z').workplane().center(px,py).hole(FLANGE_M3_CLR, depth=FLANGE_EXT)
# 61903 pocket from inboard end, Ø30 x 7.
flange=flange.faces('<Z').workplane().hole(30.0, depth=L_B61903)
# Dynamic X-ring gland candidate. Exact gland must follow selected supplier standard.
flange=flange.faces('>Z').workplane().hole(XRING_GLAND_D, depth=XRING_GROOVE_W)

# Wheel shaft candidate, axis Z for standalone part export.
shaft=(cq.Workplane('XY').circle(D_INNER/2).extrude(L_INNER_TOTAL)
       .faces('>Z').workplane().circle(D_BEARING_OUT/2).extrude(L_B61903)
       .faces('>Z').workplane().circle(D_XRING_LAND/2).extrude(L_XRING)
       .faces('>Z').workplane().circle(D_XRING_LAND/2+1.0).extrude(L_LAB)
       .faces('>Z').workplane().circle(D_WHEEL_SEAT/2).extrude(L_WHEEL))
# M6 retaining-thread drill envelope.
shaft=shaft.faces('>Z').workplane().hole(5.0, depth=12.0)
# 4x4x12 keyway envelope on wheel seat, completely outboard of seal land.
total_len=L_INNER_TOTAL+L_B61903+L_XRING+L_LAB+L_WHEEL
key_z=total_len-L_WHEEL+3.0
keybox=(cq.Workplane('XY').box(4.0,4.0,12.0,centered=(True,False,False))
        .translate((0,D_WHEEL_SEAT/2-2.0,key_z+6.0)))
shaft=shaft.cut(keybox)

# Assembly.
assy=cq.Assembly(name='PX1_SideDrive_RevFF')
assy.add(cover,name='SideCover')
for i,x in enumerate(WX):
    assy.add(flange.translate((x,WZ,COVER_T)),name=f'Flange_{i+1}')

out=os.path.abspath('build_revff')
os.makedirs(out, exist_ok=True)
cq.exporters.export(cover, os.path.join(out,'PX1_SideCover_RevFF.step'))
cq.exporters.export(flange, os.path.join(out,'PX1_AxleFlange_RevFF.step'))
cq.exporters.export(shaft, os.path.join(out,'PX1_WheelShaft_RevFF.step'))
assy.save(os.path.join(out,'PX1_SideDrive_RevFF.step'))

ring_area=math.pi*(ORING_CS/2)**2
groove_area=GROOVE_W*GROOVE_D
fill=ring_area/groove_area
xring_stretch=(D_XRING_LAND-XRING_ID)/XRING_ID
metrics={
 'cover_bbox': [cover.val().BoundingBox().xmin,cover.val().BoundingBox().ymin,cover.val().BoundingBox().zmin,cover.val().BoundingBox().xmax,cover.val().BoundingBox().ymax,cover.val().BoundingBox().zmax],
 'cover_volume_mm3': cover.val().Volume(),
 'flange_bbox': [flange.val().BoundingBox().xmin,flange.val().BoundingBox().ymin,flange.val().BoundingBox().zmin,flange.val().BoundingBox().xmax,flange.val().BoundingBox().ymax,flange.val().BoundingBox().zmax],
 'shaft_bbox': [shaft.val().BoundingBox().xmin,shaft.val().BoundingBox().ymin,shaft.val().BoundingBox().zmin,shaft.val().BoundingBox().xmax,shaft.val().BoundingBox().ymax,shaft.val().BoundingBox().zmax],
 'shaft_volume_mm3': shaft.val().Volume(),
 'oring_nominal_circumference_mm': RT_CIRC,
 'racetrack_centerline_overall_L_mm': RT_L,
 'racetrack_centerline_overall_H_mm': RT_H,
 'racetrack_edge_margin_x_mm': (COVER_L-RT_L)/2,
 'racetrack_edge_margin_y_mm': (COVER_H-RT_H)/2,
 'groove_fill_ratio': fill,
 'oring_face_squeeze_ratio': 1-GROOVE_D/ORING_CS,
 'xring_land_stretch_ratio': xring_stretch,
 'xring_gland_bottom_diameter_candidate_mm': XRING_GLAND_D,
 'xring_radial_squeeze_ratio': XRING_SQUEEZE,
 'status':'prototype candidate only'
}
with open(os.path.join(out,'REV_FF_VALIDATION.json'),'w') as f:
    json.dump(metrics,f,indent=2)
print(json.dumps(metrics,indent=2))