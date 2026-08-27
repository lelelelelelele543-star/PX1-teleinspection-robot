import FreeCAD as App, Part
# PX-1 Rev.BV internal ROLL cartridge
# Outer camera-head shell remains fixed/sealed; this cartridge rotates inside.
doc=App.newDocument('PX1_Roll_Cartridge_RevBV')

CARTRIDGE_OD=30.0
CARTRIDGE_L=46.0
BORE=17.0

cart=doc.addObject('Part::Feature','Roll_Cartridge')
shape=Part.makeCylinder(CARTRIDGE_OD/2,CARTRIDGE_L)
shape=shape.cut(Part.makeCylinder(BORE/2,CARTRIDGE_L))
cart.Shape=shape
cart.addProperty('App::PropertyString','Material').Material='EN AW-6082 T6 / POM prototype alternative'
cart.addProperty('App::PropertyString','Function').Function='Rotating internal camera/optics carrier inside fixed sealed shell'

# Bearing seats / envelopes
for i,z in enumerate((2.0,39.0),1):
    seat=doc.addObject('Part::Feature',f'BearingSeat_6803_{i}')
    seat.Shape=Part.makeCylinder(13.05,5.2,App.Vector(0,0,z)).cut(Part.makeCylinder(8.5,5.2,App.Vector(0,0,z)))
    seat.addProperty('App::PropertyString','FitTarget').FitTarget='6803-2RS 17x26x5; housing fit to be frozen after material decision'

# Driven gear envelope around cartridge
gear=doc.addObject('Part::Feature','RollDrivenGear_z51_Envelope')
gear.Shape=Part.makeCylinder(13.25,3.0,App.Vector(0,0,31.0)).cut(Part.makeCylinder(8.5,3.0,App.Vector(0,0,31.0)))
gear.addProperty('App::PropertyString','Geometry').Geometry='m0.5 z51, pitch Ø25.5, OD ~26.5, face 3 mm candidate'

# Central video rotary-transfer keepout
rt=doc.addObject('Part::Feature','RotaryTransfer_Keepout')
rt.Shape=Part.makeCylinder(6.25,24.0,App.Vector(0,0,11.0))
rt.addProperty('App::PropertyString','Status').Status='HOLD: final 75-ohm video-capable rotary transfer not selected'

# Camera mount plate envelope
plate=doc.addObject('Part::Feature','Camera_Mount_Plate')
plate.Shape=Part.makeBox(22,22,2.5,App.Vector(-11,-11,5.0))
plate.addProperty('App::PropertyString','Camera').Camera='RunCam Phoenix 2 class, 19x19x20 mm'

rules=doc.addObject('App::FeaturePython','Rules')
rules.addProperty('App::PropertyString','OuterShell').OuterShell='Fixed sealed shell Ø52; no large rotating external pressure boundary'
rules.addProperty('App::PropertyString','BearingSupport').BearingSupport='2x 6803-2RS support cartridge only; bearings are not water seals'
rules.addProperty('App::PropertyString','RadialClearance').RadialClearance='target >=1.5 mm cartridge/inner-shell rotating clearance before wires'
rules.addProperty('App::PropertyString','AxialClearance').AxialClearance='target 0.2–0.5 mm after bearing retention is frozen'
rules.addProperty('App::PropertyString','Service').Service='cartridge removable from rear of head after quick-release module removal'
rules.addProperty('App::PropertyString','Release').Release='NO RELEASE until rotary transfer, bearing fits and camera mount are exact'

doc.recompute()
doc.saveAs('PX1_Roll_Cartridge_RevBV.FCStd')
