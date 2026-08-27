import FreeCAD as App, Part
# PX-1 Rev.BQ combined camera head packaging: camera + TILT + ROLL
# Purchased components are envelope models only.
doc=App.newDocument('PX1_Camera_Head_Combined_RevBQ')

HEAD_OD=52.0
HEAD_L=78.0  # revised from 72 after combined packaging

shell=doc.addObject('Part::Feature','Head_Max_Envelope')
shell.Shape=Part.makeCylinder(HEAD_OD/2,HEAD_L)
shell.addProperty('App::PropertyString','Status').Status='PACKAGING LIMIT; target OD <=52 mm'

# Front camera envelope 19x19x20
cam=doc.addObject('Part::Feature','RunCam_Phoenix2_Envelope')
cam.Shape=Part.makeBox(19,19,20,App.Vector(-9.5,-9.5,5))

# Roll bearings 6803-2RS
for i,z in enumerate((34.0,65.0),1):
    b=doc.addObject('Part::Feature',f'RollBearing_6803_{i}')
    b.Shape=Part.makeCylinder(13,5,App.Vector(0,0,z)).cut(Part.makeCylinder(8.5,5,App.Vector(0,0,z)))

# Rotary transfer keepout through roll axis
rot=doc.addObject('Part::Feature','Video_Rotary_Transfer_Keepout')
rot.Shape=Part.makeCylinder(6.25,27,App.Vector(0,0,38))
rot.addProperty('App::PropertyString','Status').Status='FINAL 75-ohm CVBS-capable part still HOLD'

# Roll driven gear envelope m0.5 z51: pitch Ø25.5, OD Ø26.5
rg=doc.addObject('Part::Feature','Roll_Gear_z51_Envelope')
rg.Shape=Part.makeCylinder(13.25,3,App.Vector(0,0,58)).cut(Part.makeCylinder(8.5,3,App.Vector(0,0,58)))

# Roll motor envelope placed radially
rm=doc.addObject('Part::Feature','Roll_N20_Envelope')
rm.Shape=Part.makeBox(12,10,26,App.Vector(13,-5,34))

# Tilt worm module envelope placed behind camera, transverse packaging reservation
tm=doc.addObject('Part::Feature','Tilt_Module_Envelope')
tm.Shape=Part.makeBox(28,16,24,App.Vector(-14,-8,26))
tm.addProperty('App::PropertyString','Includes').Includes='N20 interface, coupling, Ø3 worm shaft, 2x693, worm/wheel, HOME and stops'

rules=doc.addObject('App::FeaturePython','PackagingRules')
rules.addProperty('App::PropertyString','OD').OD='<=52 mm hard target'
rules.addProperty('App::PropertyString','Length').Length='78 mm current combined target; previous 72 mm target exceeded'
rules.addProperty('App::PropertyString','TiltRange').TiltRange='-105..+105 deg commanded; mechanical stops approx +/-108 deg'
rules.addProperty('App::PropertyString','Roll').Roll='continuous 360 deg; no cable wind-up'
rules.addProperty('App::PropertyString','DN150').DN150='Must be rechecked with Rev.BQ 78 mm head and lift solids'
rules.addProperty('App::PropertyString','Release').Release='NO RELEASE: rotary video transfer and collision sweep unresolved'

doc.recompute()
doc.saveAs('PX1_Camera_Head_Combined_RevBQ.FCStd')
