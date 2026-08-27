import FreeCAD as App, Part
# PX-1 Rev.AR visual/boolean service-clearance checker.
# Run after loading/creating the drivetrain assembly or standalone for envelope review.
doc=App.newDocument('PX1_Service_Clearance_Check_RevAR')

BODY_L=250.0; BODY_W=94.0; BODY_H=76.0
FRONT_X=45.0; REAR_X=205.0; AXLE_Z=37.0
WHEEL_D=90.0; WHEEL_W=18.0

body=doc.addObject('Part::Feature','BodyEnvelope')
body.Shape=Part.makeBox(BODY_L,BODY_W,BODY_H)

# Socket envelopes around four wheel-retention axes: Ø20, 32 mm approach length.
for side,y,axis in [('L',-32.0,App.Vector(0,1,0)),('R',BODY_W+32.0,App.Vector(0,-1,0))]:
    for pos,x in [('F',FRONT_X),('R',REAR_X)]:
        obj=doc.addObject('Part::Feature',f'SocketEnvelope_{side}_{pos}')
        obj.Shape=Part.makeCylinder(10.0,32.0,App.Vector(x,y,AXLE_Z),axis)
        obj.addProperty('App::PropertyString','Requirement').Requirement='Ø20 mm minimum socket envelope'

# Nominal wheel envelopes.
for side,y,axis in [('L',-18.0,App.Vector(0,1,0)),('R',BODY_W,App.Vector(0,1,0))]:
    for pos,x in [('F',FRONT_X),('R',REAR_X)]:
        w=doc.addObject('Part::Feature',f'WheelEnvelope_{side}_{pos}')
        w.Shape=Part.makeCylinder(WHEEL_D/2,WHEEL_W,App.Vector(x,y,AXLE_Z),axis)

# Side cover service slabs, intentionally offset from body; final position depends on drivetrain thickness.
for side,y in [('L',-8.0),('R',BODY_W+5.0)]:
    c=doc.addObject('Part::Feature',f'CoverEnvelope_{side}')
    c.Shape=Part.makeBox(214.0,3.0,66.0,App.Vector(18.0,y,5.0))
    c.addProperty('App::PropertyString','ClearanceRule').ClearanceRule='>=2 mm nominal to rotating wheel/gear geometry'

note=doc.addObject('App::FeaturePython','VerificationRules')
note.addProperty('App::PropertyString','RotatingToCover').RotatingToCover='>=2.0 mm nominal'
note.addProperty('App::PropertyString','GearToBody').GearToBody='>=1.5 mm nominal'
note.addProperty('App::PropertyString','ToolClearance').ToolClearance='>=1.0 mm nominal'
note.addProperty('App::PropertyString','Status').Status='VISUAL/BOOLEAN CHECK ONLY; physical mock-up required before release'

doc.recompute()
doc.saveAs('PX1_Service_Clearance_Check_RevAR.FCStd')
