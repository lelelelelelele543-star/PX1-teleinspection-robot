import FreeCAD as App, Part, math
# PX-1 Rev.AZ rear bearing/seal carrier with static O-ring groove
# Drawing-candidate geometry; verify physical first article before RELEASE.

doc=App.newDocument('PX1_Rear_Carrier_RevAZ')

L=28.0
BODY_OD=42.0
FLANGE_OD=60.0
FLANGE_T=5.0
PILOT_OD=38.0
PILOT_L=4.0
SHAFT_CLEAR=12.0
BEARING_OD=26.0
BEARING_DEPTH=8.2
SEAL_OD=22.0
SEAL_DEPTH=7.2
PCD=54.0
M4_CLEAR=4.5

# O-ring 40x2 face-seal groove candidate
GROOVE_ID=39.0
GROOVE_OD=44.0
GROOVE_DEPTH=1.50
GROOVE_WIDTH=(GROOVE_OD-GROOVE_ID)/2.0

body=Part.makeCylinder(BODY_OD/2,L)
flange=Part.makeCylinder(FLANGE_OD/2,FLANGE_T)
pilot=Part.makeCylinder(PILOT_OD/2,PILOT_L,App.Vector(0,0,FLANGE_T))
shape=body.fuse(flange).fuse(pilot)

# Through shaft passage
shape=shape.cut(Part.makeCylinder(SHAFT_CLEAR/2,L))
# Bearing pocket from inner side
shape=shape.cut(Part.makeCylinder(BEARING_OD/2,BEARING_DEPTH,App.Vector(0,0,L-BEARING_DEPTH)))
# Seal pocket from outer/front side behind flange region
shape=shape.cut(Part.makeCylinder(SEAL_OD/2,SEAL_DEPTH,App.Vector(0,0,FLANGE_T+PILOT_L)))

# Face O-ring annular groove on flange mounting face z=0
outer=Part.makeCylinder(GROOVE_OD/2,GROOVE_DEPTH)
inner=Part.makeCylinder(GROOVE_ID/2,GROOVE_DEPTH)
shape=shape.cut(outer.cut(inner))

# 4x M4 clearance holes on PCD54
for i in range(4):
    a=math.radians(45+90*i)
    x=(PCD/2)*math.cos(a); y=(PCD/2)*math.sin(a)
    shape=shape.cut(Part.makeCylinder(M4_CLEAR/2,FLANGE_T,App.Vector(x,y,0)))

obj=doc.addObject('Part::Feature','Rear_Carrier')
obj.Shape=shape
obj.addProperty('App::PropertyString','Material').Material='EN AW-6082 T6 or 7075-T6 prototype; anodize after machining if selected'
obj.addProperty('App::PropertyString','BearingSeat').BearingSeat='Ø26 H7 x 8.2 deep; 6000-2RS'
obj.addProperty('App::PropertyString','SealSeat').SealSeat='Ø22 H8 x 7.2 deep; FKM 10x22x7'
obj.addProperty('App::PropertyString','Pilot').Pilot='Ø38 h7 candidate x 4 mm'
obj.addProperty('App::PropertyString','Mount').Mount='4x Ø4.5 on PCD54'
obj.addProperty('App::PropertyString','StaticSeal').StaticSeal='O-ring 40x2 FKM face seal; groove ID39 / OD44 / depth1.50'
obj.addProperty('App::PropertyString','Concentricity').Concentricity='bearing seat to seal seat <=0.03 mm target'
obj.addProperty('App::PropertyString','FaceRunout').FaceRunout='mounting face to bearing axis <=0.03 mm target'
obj.addProperty('App::PropertyString','Status').Status='DRAWING-CANDIDATE — first article and leak test required'

doc.recompute()
doc.saveAs('PX1_Rear_Carrier_RevAZ.FCStd')
