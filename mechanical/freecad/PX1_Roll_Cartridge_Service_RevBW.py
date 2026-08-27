import FreeCAD as App, Part
# PX-1 Rev.BW ROLL cartridge service architecture
# Concept model: dimensions requiring measured fits remain HOLD.
doc=App.newDocument('PX1_Roll_Cartridge_Service_RevBW')

# Fixed head inner envelope: shell OD52, wall2.5 => ID47
housing=doc.addObject('Part::Feature','FixedHeadInnerEnvelope')
housing.Shape=Part.makeCylinder(23.5,54)

# Rotating cartridge OD30 / through passage Ø17
cart=doc.addObject('Part::Feature','RollCartridge')
cart.Shape=Part.makeCylinder(15,46,App.Vector(0,0,4)).cut(Part.makeCylinder(8.5,46,App.Vector(0,0,4)))

# Bearings
for name,z in [('Front6803',8),('Rear6803',39)]:
    b=doc.addObject('Part::Feature',name)
    b.Shape=Part.makeCylinder(13,5,App.Vector(0,0,z)).cut(Part.makeCylinder(8.5,5,App.Vector(0,0,z)))

# Rear service retaining ring envelope
ring=doc.addObject('Part::Feature','RearBearingServiceRing')
ring.Shape=Part.makeCylinder(16.5,4,App.Vector(0,0,45)).cut(Part.makeCylinder(13,4,App.Vector(0,0,45)))
ring.addProperty('App::PropertyString','Thread').Thread='THREAD HOLD — select after housing wall/tolerance review'

# Roll gear z51 envelope
gear=doc.addObject('Part::Feature','RollGear_z51')
gear.Shape=Part.makeCylinder(13.25,3,App.Vector(0,0,32)).cut(Part.makeCylinder(8.5,3,App.Vector(0,0,32)))

# Motor bracket travel envelope showing ±0.75 mm center-distance adjustment
slot=doc.addObject('Part::Feature','RollMotor_AdjustmentEnvelope')
slot.Shape=Part.makeBox(13.5,12,28,App.Vector(12.25,-6,21))
slot.addProperty('App::PropertyString','Adjustment').Adjustment='+/-0.75 mm along gear center-distance axis; nominal CD 17.0 mm'

# TILT harness passage/keepout
harness=doc.addObject('Part::Feature','TiltHarnessKeepout')
harness.Shape=Part.makeCylinder(3.0,18,App.Vector(-20,0,24),App.Vector(1,0,0))
harness.addProperty('App::PropertyString','Rule').Rule='Protected passage + controlled service loop; verify -105..+105 deg sweep'

rules=doc.addObject('App::FeaturePython','AssemblyRules')
rules.addProperty('App::PropertyString','BearingRetention').BearingRetention='Shoulder + removable rear service ring; no adhesive as primary retention'
rules.addProperty('App::PropertyString','Backlash').Backlash='Set free-running backlash; verify full 360 deg and thermal condition'
rules.addProperty('App::PropertyString','RollWiring').RollWiring='Continuous ROLL conductors only through rotary transfer'
rules.addProperty('App::PropertyString','Release').Release='NO RELEASE until fits, thread, rotary transfer and leak test are closed'

doc.recompute()
doc.saveAs('PX1_Roll_Cartridge_Service_RevBW.FCStd')
