import FreeCAD as App, Part
# PX-1 Rev.BJ camera-head internal packaging study
# Purchased items are envelopes; exact supplier CAD/drawings govern release.
doc=App.newDocument('PX1_Camera_Head_Internal_RevBJ')

HEAD_OD=52.0; HEAD_L=72.0
shell=doc.addObject('Part::Feature','HeadEnvelope')
shell.Shape=Part.makeCylinder(HEAD_OD/2,HEAD_L)
shell.addProperty('App::PropertyString','Status').Status='MAXIMUM PACKAGING ENVELOPE, NOT RELEASE GEOMETRY'

# RunCam Phoenix 2 nominal envelope 19x19x20
cam=doc.addObject('Part::Feature','Camera_19x19x20')
cam.Shape=Part.makeBox(19,19,20,App.Vector(-9.5,-9.5,5))

# Two 6803 bearing envelopes, coaxial with roll axis
for i,z in enumerate((31.0,58.0),1):
    b=doc.addObject('Part::Feature',f'RollBearing_6803_{i}')
    b.Shape=Part.makeCylinder(13,5,App.Vector(0,0,z)).cut(Part.makeCylinder(8.5,5,App.Vector(0,0,z)))
    b.addProperty('App::PropertyString','Envelope').Envelope='6803-2RS 17x26x5'

# Central rotary-transfer keepout; Ø12.5 prototype slip-ring envelope
sr=doc.addObject('Part::Feature','RotaryTransferKeepout')
sr.Shape=Part.makeCylinder(6.25,24,App.Vector(0,0,34))
sr.addProperty('App::PropertyString','Status').Status='KEEP-OUT ONLY; final video-capable 75-ohm rotary transfer HOLD'

# N20 gearmotor envelopes; orientation/gear coupling still to be finalized
for name,x,y,z in [('TiltMotor',-6,-20,24),('RollMotor',-6,8,44)]:
    m=doc.addObject('Part::Feature',name)
    m.Shape=Part.makeBox(12,10,26,App.Vector(x,y,z))
    m.addProperty('App::PropertyString','Envelope').Envelope='GM12-N20 class; verify exact purchased motor drawing'

# Gear design targets, not tooth-solid models yet
rules=doc.addObject('App::FeaturePython','DriveTargets')
rules.addProperty('App::PropertyString','Tilt').Tilt='N20 30-60 rpm + spur reduction target 2:1 to 3:1; self-lock/holding to be verified'
rules.addProperty('App::PropertyString','Roll').Roll='N20 30-60 rpm + spur reduction target ~2:1; continuous rotation'
rules.addProperty('App::PropertyString','GearModule').GearModule='m=0.5 candidate, 20deg pressure angle; metal/POM decision after torque test'
rules.addProperty('App::PropertyString','Clearance').Clearance='>=1.0 mm purchased-envelope to shell nominal; >=0.5 mm between non-contacting internal parts'
rules.addProperty('App::PropertyString','Release').Release='NO RELEASE until exact motors + rotary transfer + lens/window geometry verified'

doc.recompute()
doc.saveAs('PX1_Camera_Head_Internal_RevBJ.FCStd')
