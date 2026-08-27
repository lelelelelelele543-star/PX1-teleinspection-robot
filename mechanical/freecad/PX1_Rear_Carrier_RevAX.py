import FreeCAD as App, Part
# PX-1 Rev.AX rear bearing/seal carrier — drawing-candidate geometry
# Static body O-ring groove intentionally NOT finalized until exact O-ring is selected.

doc=App.newDocument('PX1_Rear_Carrier_RevAX')

L=28.0
FLANGE_OD=56.0
FLANGE_T=5.0
SPIGOT_OD=38.0
SHAFT_CLEAR=12.0
BEARING_OD=26.0
BEARING_DEPTH=8.2
SEAL_OD=22.0
SEAL_DEPTH=7.2
BOLT_PCD=48.0
BOLT_D=4.5

# flange + locating spigot
flange=Part.makeCylinder(FLANGE_OD/2,FLANGE_T)
spigot=Part.makeCylinder(SPIGOT_OD/2,L-FLANGE_T,App.Vector(0,0,FLANGE_T))
shape=flange.fuse(spigot)

# through shaft clearance
shape=shape.cut(Part.makeCylinder(SHAFT_CLEAR/2,L))
# bearing seat from inner side
shape=shape.cut(Part.makeCylinder(BEARING_OD/2,BEARING_DEPTH,App.Vector(0,0,0)))
# seal seat from outer side
shape=shape.cut(Part.makeCylinder(SEAL_OD/2,SEAL_DEPTH,App.Vector(0,0,L-SEAL_DEPTH)))

# 4x M4 clearance holes on 48 PCD
import math
for a in (45,135,225,315):
    r=BOLT_PCD/2
    x=r*math.cos(math.radians(a)); y=r*math.sin(math.radians(a))
    shape=shape.cut(Part.makeCylinder(BOLT_D/2,FLANGE_T,App.Vector(x,y,0)))

carrier=doc.addObject('Part::Feature','Rear_Carrier')
carrier.Shape=shape
carrier.addProperty('App::PropertyString','Material').Material='EN AW-6082 T6 hard-anodized prototype; stainless alternative for wet interface'
carrier.addProperty('App::PropertyString','BodyLocation').BodyLocation='Ø38 h7/g6-style locating spigot candidate; mating body bore to be frozen with body drawing'
carrier.addProperty('App::PropertyString','BearingSeat').BearingSeat='Ø26 H7, depth 8.2 mm; 6000-2RS'
carrier.addProperty('App::PropertyString','SealSeat').SealSeat='Ø22 H8, depth 7.2 mm; 10x22x7 FKM radial seal'
carrier.addProperty('App::PropertyString','ShaftClearance').ShaftClearance='Ø12 through; no contact with Ø10 shaft'
carrier.addProperty('App::PropertyString','Fasteners').Fasteners='4x M4 clearance Ø4.5 on PCD 48; captive/thread strategy in body TBD'
carrier.addProperty('App::PropertyString','Concentricity').Concentricity='bearing seat to seal seat <=0.03 mm target'
carrier.addProperty('App::PropertyString','StaticSeal').StaticSeal='HOLD: exact flange/body O-ring and groove not released yet'
carrier.addProperty('App::PropertyString','Status').Status='DRAWING-CANDIDATE except static body seal interface'

doc.recompute()
doc.saveAs('PX1_Rear_Carrier_RevAX.FCStd')
