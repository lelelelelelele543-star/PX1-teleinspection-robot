import FreeCAD as App, Part

# PX-1 Rev.AM service-access and keep-out visualization.
# Goal: verify drivetrain can be serviced externally without opening pressure body.

doc=App.newDocument('PX1_Service_Access_RevAM')

BODY_L=250.0; BODY_W=94.0; BODY_H=76.0

body=doc.addObject('Part::Feature','PressureBody')
body.Shape=Part.makeBox(BODY_L,BODY_W,BODY_H)

# External side cover keep-out volumes.
for side,y in [('L',-24.0),('R',94.0)]:
    k=doc.addObject('Part::Feature',f'SideCoverKeepout_{side}')
    k.Shape=Part.makeBox(214.0,24.0,70.0,App.Vector(18.0,y,3.0))
    k.addProperty('App::PropertyString','Requirement').Requirement='Must be removable without opening sealed body'

# Tool-access cylinders around idler fasteners.
for side,y in [('L',-20.0),('R',114.0)]:
    for i,x in enumerate([85.0,125.0,165.0]):
        a=doc.addObject('Part::Feature',f'ToolAccess_{side}_{i}')
        a.Shape=Part.makeCylinder(8.0,30.0,App.Vector(x,y,37.0),App.Vector(0,1,0))
        a.addProperty('App::PropertyString','Requirement').Requirement='Ø16 tool/socket access keep-out'

# Wheel-removal axial access keep-outs.
for side,y in [('L',-45.0),('R',94.0)]:
    for pos,x in [('F',45.0),('R',205.0)]:
        a=doc.addObject('Part::Feature',f'WheelRemoval_{side}_{pos}')
        a.Shape=Part.makeCylinder(16.0,45.0,App.Vector(x,y,37.0),App.Vector(0,1,0))
        a.addProperty('App::PropertyString','Requirement').Requirement='Wheel retention must be reachable with side cover removed'

notes=doc.addObject('App::FeaturePython','ServiceRules')
notes.addProperty('App::PropertyString','R1').R1='Side cover removable without wheel removal where practical'
notes.addProperty('App::PropertyString','R2').R2='Idler gears/axles replaceable without opening dry body'
notes.addProperty('App::PropertyString','R3').R3='Front axle is external and independently replaceable'
notes.addProperty('App::PropertyString','R4').R4='Rear shaft seal requires body service, but external gear/wheel do not'
notes.addProperty('App::PropertyString','R5').R5='No hidden permanent adhesive joints in drivetrain service path'

doc.recompute()
doc.saveAs('PX1_Service_Access_Check_RevAM.FCStd')
