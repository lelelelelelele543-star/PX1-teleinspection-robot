import FreeCAD as App, Part
# PX-1 Rev.BB main dry pressure body — machining candidate envelope
# Rectangular monocoque concept, inspired by serviceability requirements, not a copy of vendor geometry.
doc=App.newDocument('PX1_Main_Pressure_Body_RevBB')

L=250.0; W=94.0; H=76.0
WALL_SIDE=6.0; WALL_TOP=6.0; WALL_BOTTOM=8.0
END_LAND=12.0

outer=Part.makeBox(L,W,H)
inner=Part.makeBox(L-2*END_LAND,W-2*WALL_SIDE,H-WALL_TOP-WALL_BOTTOM,
                   App.Vector(END_LAND,WALL_SIDE,WALL_BOTTOM))
shape=outer.cut(inner)
body=doc.addObject('Part::Feature','Main_Pressure_Body')
body.Shape=shape
body.addProperty('App::PropertyString','Material').Material='EN AW-6082 T6 preferred prototype; 6061-T6 acceptable alternate'
body.addProperty('App::PropertyString','Envelope').Envelope='250 x 94 x 76 mm'
body.addProperty('App::PropertyString','Wall').Wall='side/top 6 mm; bottom 8 mm prototype'
body.addProperty('App::PropertyString','EndLand').EndLand='12 mm each end for cover pilot/seal/fasteners'
body.addProperty('App::PropertyString','RearModules').RearModules='2x PX1-DR-002 carriers at rear axle station; exact wall bores added after assembly interference check'
body.addProperty('App::PropertyString','Pressure').Pressure='Prototype target <=0.5 bar gauge; final rating only after analysis + proof test'
body.addProperty('App::PropertyString','Status').Status='DRAWING-CANDIDATE ENVELOPE — end-cover and carrier interfaces not yet RELEASED'

doc.recompute()
doc.saveAs('PX1_Main_Pressure_Body_RevBB.FCStd')
