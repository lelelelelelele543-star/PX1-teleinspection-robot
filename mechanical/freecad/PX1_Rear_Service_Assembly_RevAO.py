import FreeCAD as App, Part

# PX-1 Rev.AO - rear service assembly, one side
# Goal: validate field teardown without opening sealed body.

doc=App.newDocument('PX1_Rear_Service_Assembly_RevAO')

# Axial stack, dry side -> outside
# z-axis used as shaft axis for clarity.
shaft_len=62.0
shaft_d=10.0
bearing_od=26.0
bearing_w=8.0
seal_od=22.0
seal_w=7.0
spacer_w=2.0
labyrinth_w=4.0
gear_w=8.0
wheel_w=18.0

z0=0.0

# shaft
shaft=doc.addObject('Part::Feature','Shaft')
shaft.Shape=Part.makeCylinder(shaft_d/2,shaft_len)
shaft.addProperty('App::PropertyString','Note').Note='Rev.AN shaft 62 mm; seal journal free of thread/keyway'

# purchased bearing envelope
bearing=doc.addObject('Part::Feature','Bearing_6000_2RS')
bearing.Shape=Part.makeCylinder(bearing_od/2,bearing_w,App.Vector(0,0,4)).cut(Part.makeCylinder(5.0,bearing_w,App.Vector(0,0,4)))
bearing.addProperty('App::PropertyString','Status').Status='PURCHASED ENVELOPE 10x26x8'

# spacer
sp=doc.addObject('Part::Feature','Spacer')
sp.Shape=Part.makeCylinder(8.0,spacer_w,App.Vector(0,0,12)).cut(Part.makeCylinder(5.05,spacer_w,App.Vector(0,0,12)))

# seal envelope
seal=doc.addObject('Part::Feature','Seal_10x22x7')
seal.Shape=Part.makeCylinder(seal_od/2,seal_w,App.Vector(0,0,14)).cut(Part.makeCylinder(5.0,seal_w,App.Vector(0,0,14)))
seal.addProperty('App::PropertyString','Status').Status='PURCHASED ENVELOPE FKM preferred'

# grease/labyrinth zone
lab=doc.addObject('Part::Feature','Grease_Labyrinth_Zone')
lab.Shape=Part.makeCylinder(12.5,labyrinth_w,App.Vector(0,0,21)).cut(Part.makeCylinder(5.2,labyrinth_w,App.Vector(0,0,21)))

# compound gear envelope z30/z40 external
gear=doc.addObject('Part::Feature','Compound_Gear_z30_z40')
gear.Shape=Part.makeCylinder(21.0,gear_w,App.Vector(0,0,25)).cut(Part.makeCylinder(5.0,gear_w,App.Vector(0,0,25)))
gear.addProperty('App::PropertyString','Status').Status='GEAR ENVELOPE; involute profile controlled separately'

# wheel
wheel=doc.addObject('Part::Feature','Wheel_90x18')
wheel.Shape=Part.makeCylinder(45.0,wheel_w,App.Vector(0,0,33)).cut(Part.makeCylinder(5.0,wheel_w,App.Vector(0,0,33)))

# retaining nut zone
nut=doc.addObject('Part::Feature','Retaining_Nut_Zone')
nut.Shape=Part.makeCylinder(8.0,8.0,App.Vector(0,0,51)).cut(Part.makeCylinder(4.0,8.0,App.Vector(0,0,51)))
nut.addProperty('App::PropertyString','Locking').Locking='Mechanical lock required; threadlocker alone not sufficient'

# service sequence as properties
asm=doc.addObject('App::FeaturePython','Service_Sequence')
asm.addProperty('App::PropertyStringList','Remove').Remove=[
    '1 Disconnect power and unload tether',
    '2 Remove side gear cover',
    '3 Remove mechanical wheel retainer',
    '4 Remove wheel',
    '5 Remove compound z30/z40 gear',
    '6 Remove outer labyrinth/grease protector',
    '7 Withdraw shaft only if internal AS5600 magnet clearance is confirmed',
    '8 Bearing and seal service requires rear carrier removal, not full body strip'
]
asm.addProperty('App::PropertyStringList','DoNot').DoNot=[
    'Do not lever against seal lip',
    'Do not drag thread/keyway through seal lip',
    'Do not reuse damaged FKM seal',
    'Do not open electronics tray for routine wheel/gear service'
]

doc.recompute()
doc.saveAs('PX1_Rear_Service_Assembly_RevAO.FCStd')
