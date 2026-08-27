import FreeCAD as App, Part

# PX-1 Rev.AN rear shaft stack
# This assembly supersedes the earlier 54 mm shaft prototype envelope.
# Reason: 54 mm was too short to package bearing + spacer + seal + gear + 18 mm wheel + serviceable external retention.

DOC='PX1_Rear_Stack_RevAN'
doc=App.newDocument(DOC)

SHAFT_D=10.0
SHAFT_L=62.0
BEARING_OD=26.0
BEARING_W=8.0
SEAL_OD=22.0
SEAL_W=7.0
WHEEL_W=18.0

# Axial stack from dry side (Z=0) toward water/wheel side
Z_MAGNET=0.0
Z_BEARING=4.0
Z_SPACER=12.0
SPACER_W=3.0
Z_SEAL=15.0
Z_LAB=22.0
LAB_W=3.0
Z_GEAR=25.0
GEAR_W=8.0
Z_WHEEL=33.0
Z_THREAD=52.0
THREAD_L=10.0

# Shaft
shaft=doc.addObject('Part::Feature','Rear_Output_Shaft_RevAN')
shape=Part.makeCylinder(SHAFT_D/2,SHAFT_L)
shape=shape.cut(Part.makeCylinder(3.05,3.2)) # AS5600 magnet pocket
shaft.Shape=shape
for name,val in [
    ('Material','AISI316 / 40X13'),
    ('SealJournal','Ø10 h6, Ra<=0.4'),
    ('BearingJournal','Ø10 h6'),
    ('ExternalDrive','3x3 keyway only in external gear/wheel zone'),
    ('Retention','M8 external thread, 10 mm long; all-metal locknut'),
    ('Status','PROTOTYPE GEOMETRY - VERIFY AFTER FIRST ASSEMBLY')]:
    shaft.addProperty('App::PropertyString',name); setattr(shaft,name,val)

# Bearing 6000-2RS envelope
bearing=doc.addObject('Part::Feature','Bearing_6000_2RS')
bearing.Shape=Part.makeCylinder(BEARING_OD/2,BEARING_W,App.Vector(0,0,Z_BEARING)).cut(
    Part.makeCylinder(SHAFT_D/2,BEARING_W,App.Vector(0,0,Z_BEARING)))

# Spacer
sp=doc.addObject('Part::Feature','Spacer')
sp.Shape=Part.makeCylinder(8.0,SPACER_W,App.Vector(0,0,Z_SPACER)).cut(
    Part.makeCylinder(5.05,SPACER_W,App.Vector(0,0,Z_SPACER)))

# Seal envelope
seal=doc.addObject('Part::Feature','Radial_Seal_10x22x7')
seal.Shape=Part.makeCylinder(SEAL_OD/2,SEAL_W,App.Vector(0,0,Z_SEAL)).cut(
    Part.makeCylinder(SHAFT_D/2,SEAL_W,App.Vector(0,0,Z_SEAL)))
seal.addProperty('App::PropertyString','PreferredMaterial').PreferredMaterial='FKM'

# Labyrinth/grease cavity marker
lab=doc.addObject('Part::Feature','Grease_Labyrinth_Zone')
lab.Shape=Part.makeCylinder(13.0,LAB_W,App.Vector(0,0,Z_LAB)).cut(
    Part.makeCylinder(6.0,LAB_W,App.Vector(0,0,Z_LAB)))

# Compound gear envelope z30/z40; exact teeth generated separately
gear=doc.addObject('Part::Feature','Compound_Gear_Envelope')
gear.Shape=Part.makeCylinder(21.0,GEAR_W,App.Vector(0,0,Z_GEAR)).cut(
    Part.makeCylinder(5.0,GEAR_W,App.Vector(0,0,Z_GEAR)))
gear.addProperty('App::PropertyString','Definition').Definition='m1 z30/z40 compound; exact involute from Rev.AL generator'

# Wheel hub envelope
wheel=doc.addObject('Part::Feature','Wheel_Hub_Envelope')
wheel.Shape=Part.makeCylinder(45.0,WHEEL_W,App.Vector(0,0,Z_WHEEL)).cut(
    Part.makeCylinder(5.0,WHEEL_W,App.Vector(0,0,Z_WHEEL)))

# Locknut envelope
nut=doc.addObject('Part::Feature','M8_AllMetal_Locknut_Envelope')
nut.Shape=Part.makeCylinder(6.5,7.0,App.Vector(0,0,54.0)).cut(
    Part.makeCylinder(4.0,7.0,App.Vector(0,0,54.0)))

# AS5600 magnet envelope
mag=doc.addObject('Part::Feature','AS5600_Magnet_6x2_5')
mag.Shape=Part.makeCylinder(3.0,2.5,App.Vector(0,0,0))

# Engineering notes object
notes=doc.addObject('App::FeaturePython','Engineering_Notes')
for n,v in [
    ('AxialStack','bearing 4-12 / spacer 12-15 / seal 15-22 / labyrinth 22-25 / gear 25-33 / wheel 33-51 / retention 52-62 mm'),
    ('SealRule','No thread, keyway or D-flat under seal lip'),
    ('KeyRule','3x3 keyway limited to external gear/wheel drive zone only'),
    ('ServiceRule','Wheel and external gear removable without opening pressure body'),
    ('Supersedes','Previous 54 mm rear shaft envelope')]:
    notes.addProperty('App::PropertyString',n); setattr(notes,n,v)

doc.recompute()
doc.saveAs('PX1_Rear_Stack_RevAN.FCStd')
