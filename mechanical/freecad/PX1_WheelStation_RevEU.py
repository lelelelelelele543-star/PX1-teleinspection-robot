import FreeCAD as App, Part

# PX-1 Rev.EU — one machinable six-wheel station candidate.
# Axis is Y. This file models a left-side station; right side is mirrored in assembly.

doc = App.newDocument('PX1_WheelStation_RevEU')

AXIS_X = 50.0
AXIS_Z = 45.0

# axial Y datums from body centerline toward left exterior
Y_INNER0 = 30.0
Y_BRG1_0 = 31.0
Y_GEAR_0 = 36.0
Y_BRG2_0 = 44.0
Y_STEP = 49.0
Y_FLANGE_FACE = 46.0
Y_BRG3_0 = 50.0
Y_SEAL_0 = 57.0
Y_LAB_0 = 64.0
Y_WHEEL_0 = 69.0

D_INNER = 12.0
D_OUTER = 17.0
B61801_OD = 21.0
B61801_W = 5.0
B61903_OD = 30.0
B61903_W = 7.0
GEAR_OD = 52.0
GEAR_W = 8.0
FLANGE_OD = 50.0
FLANGE_T = 9.0
SEAL_OD = 30.0
SEAL_W = 7.0
LAB_OD = 27.0
WHEEL_OD = 90.0
WHEEL_W = 16.0
WHEEL_OUTER_OD = 44.0


def cyl_y(d, length, y0):
    return Part.makeCylinder(d/2.0, length,
                             App.Vector(AXIS_X, y0, AXIS_Z),
                             App.Vector(0,1,0))

# Shaft: Ø12 inner journal + Ø17 outer journal.
shaft_inner = cyl_y(D_INNER, Y_STEP-Y_INNER0, Y_INNER0)
shaft_outer = cyl_y(D_OUTER, (Y_WHEEL_0+WHEEL_W+4.0)-Y_STEP, Y_STEP)
shaft_shape = shaft_inner.fuse(shaft_outer)

# Internal M6 retaining thread represented by drill envelope only.
retainer_drill = Part.makeCylinder(2.5, 12.0,
                                   App.Vector(AXIS_X,Y_WHEEL_0+WHEEL_W+4.0,AXIS_Z),
                                   App.Vector(0,-1,0))
shaft_shape = shaft_shape.cut(retainer_drill)

shaft = doc.addObject('Part::Feature','WheelShaft_PX1_431_6W')
shaft.Shape = shaft_shape
shaft.addProperty('App::PropertyString','Material').Material = '40X13/AISI420-class candidate; seal journal hardened/polished'
shaft.addProperty('App::PropertyString','Fits').Fits = 'Ø12 h6 candidate; Ø17 h6 candidate; final supplier/measurement gate'
shaft.addProperty('App::PropertyString','SealSurface').SealSurface = 'Ø17 no key/thread; Ra<=0.4 um target'

# Bearings and Z50 envelope.
for name, y0 in [('B61801_IN',Y_BRG1_0),('B61801_OUT',Y_BRG2_0)]:
    b = doc.addObject('Part::Feature',name)
    b.Shape = cyl_y(B61801_OD,B61801_W,y0)
    b.addProperty('App::PropertyString','Spec').Spec = '61801 12x21x5'

gear = doc.addObject('Part::Feature','WheelGear_Z50')
gear.Shape = cyl_y(GEAR_OD,GEAR_W,Y_GEAR_0)
gear.addProperty('App::PropertyString','Spec').Spec = 'm1 Z50 OD52 face8, keyed Ø12 hub; tooth detail omitted'

# Key envelope, positioned on shaft away from dynamic seal.
key = doc.addObject('Part::Feature','Key_4x4')
key.Shape = Part.makeBox(4.0,10.0,4.0,
                         App.Vector(AXIS_X-D_INNER/2.0,Y_GEAR_0-1.0,AXIS_Z+D_INNER/2.0-2.0))
key.addProperty('App::PropertyString','Note').Note = 'parallel key envelope only; exact keyway orientation/dimensions on shaft drawing'

# Removable flange with bearing and seal bores.
flange = Part.makeCylinder(FLANGE_OD/2.0,FLANGE_T,
                           App.Vector(AXIS_X,Y_FLANGE_FACE,AXIS_Z),App.Vector(0,1,0))
# bore for shaft/bearing path
flange = flange.cut(Part.makeCylinder(B61903_OD/2.0,FLANGE_T+2.0,
                                      App.Vector(AXIS_X,Y_FLANGE_FACE-1.0,AXIS_Z),App.Vector(0,1,0)))
fl = doc.addObject('Part::Feature','AxleFlange')
fl.Shape = flange
fl.addProperty('App::PropertyString','StaticSeal').StaticSeal = 'local FKM O-ring around flange; exact article/groove HOLD'
fl.addProperty('App::PropertyString','Fasteners').Fasteners = '3x or 4x M4 outside local O-ring; jacking holes preferred'

b3 = doc.addObject('Part::Feature','B61903_OUTER')
b3.Shape = cyl_y(B61903_OD,B61903_W,Y_BRG3_0)
b3.addProperty('App::PropertyString','Spec').Spec = '61903 17x30x7 main wheel-load bearing'

seal = doc.addObject('Part::Feature','DynamicSeal_Envelope')
seal.Shape = cyl_y(SEAL_OD,SEAL_W,Y_SEAL_0)
seal.addProperty('App::PropertyString','Spec').Spec = 'FKM 17 mm ID compact double-lip candidate; exact OD/width HOLD'

lab = doc.addObject('Part::Feature','Labyrinth_Excluder')
lab.Shape = cyl_y(LAB_OD,4.0,Y_LAB_0)
lab.addProperty('App::PropertyString','Note').Note = 'non-contact dirt/water excluder ahead of primary dynamic seal'

# Tapered wheel envelope: full Ø90 traction crown narrowing toward outside.
wheel_crown = Part.makeCylinder(WHEEL_OD/2.0,7.0,
                                App.Vector(AXIS_X,Y_WHEEL_0,AXIS_Z),App.Vector(0,1,0))
wheel_taper = Part.makeCone(WHEEL_OD/2.0,WHEEL_OUTER_OD/2.0,WHEEL_W-7.0,
                            App.Vector(AXIS_X,Y_WHEEL_0+7.0,AXIS_Z),App.Vector(0,1,0))
wheel = doc.addObject('Part::Feature','Wheel_Profiled_90')
wheel.Shape = wheel_crown.fuse(wheel_taper)
wheel.addProperty('App::PropertyString','Mount').Mount = 'keyed hub + independent M6 axial retaining washer'

ret = doc.addObject('Part::Feature','WheelRetainingWasher')
ret.Shape = Part.makeCylinder(14.0,2.5,
                              App.Vector(AXIS_X,Y_WHEEL_0+WHEEL_W,AXIS_Z),App.Vector(0,1,0))
ret.addProperty('App::PropertyString','Fastener').Fastener = 'M6 socket screw into shaft end; lock method after cycle test'

rules = doc.addObject('App::FeaturePython','RevEU_Rules')
rules.addProperty('App::PropertyString','Pressure').Pressure = 'entire wheel station belongs to P1/P2; does not penetrate P0'
rules.addProperty('App::PropertyString','Service').Service = 'outer flange/seal/bearing removable without opening P0'
rules.addProperty('App::PropertyString','Release').Release = 'prototype solid; exact seal, spacer and wheel hub dimensions remain physical-part gates'

doc.recompute()
doc.saveAs('PX1_WheelStation_RevEU.FCStd')
