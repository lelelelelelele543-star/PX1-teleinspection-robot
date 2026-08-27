import FreeCAD as App, Part
# PX-1 Rev.BU camera-head shell / window / LED / quick-release packaging candidate
# Not production release; rotating seal and final video rotary transfer are still HOLD.

doc=App.newDocument('PX1_Camera_Head_Shell_RevBU')

OD=52.0
L=78.0
WALL=2.5
FRONT_RING_L=8.0
REAR_QR_L=10.0
WINDOW_OD=28.0
WINDOW_T=3.0

outer=Part.makeCylinder(OD/2,L)
inner=Part.makeCylinder((OD-2*WALL)/2,L-FRONT_RING_L-REAR_QR_L,App.Vector(0,0,FRONT_RING_L))
shell_shape=outer.cut(inner)

shell=doc.addObject('Part::Feature','Head_Shell')
shell.Shape=shell_shape
shell.addProperty('App::PropertyString','Material').Material='EN AW-6082 T6 candidate'
shell.addProperty('App::PropertyString','Wall').Wall='2.5 mm nominal prototype'
shell.addProperty('App::PropertyString','Status').Status='DRAWING-CANDIDATE ENVELOPE; sealing details not released'

# Front optical window envelope
window=doc.addObject('Part::Feature','Optical_Window')
window.Shape=Part.makeCylinder(WINDOW_OD/2,WINDOW_T,App.Vector(0,0,1.5))
window.addProperty('App::PropertyString','Material').Material='Tempered mineral glass or sapphire candidate'
window.addProperty('App::PropertyString','Seal').Seal='Static face O-ring groove HOLD until exact window supplier/tolerance selected'

# LED annulus envelope
led=doc.addObject('Part::Feature','LED_Ring_Envelope')
led.Shape=Part.makeCylinder(21.5,3.0,App.Vector(0,0,5.0)).cut(Part.makeCylinder(15.0,3.0,App.Vector(0,0,5.0)))
led.addProperty('App::PropertyString','Role').Role='Illumination annulus; PCB/LED carrier geometry to follow actual LED selection'

# Rear quick-release spigot envelope
qr=doc.addObject('Part::Feature','Quick_Release_Spigot')
qr.Shape=Part.makeCylinder(18.0,REAR_QR_L,App.Vector(0,0,L-REAR_QR_L))
qr.addProperty('App::PropertyString','Concept').Concept='One retained radial latch + anti-rotation key + axial O-ring'
qr.addProperty('App::PropertyString','Service').Service='Disconnect electrical interface, release one latch, withdraw head without opening crawler body'

# Anti-rotation key envelope
key=doc.addObject('Part::Feature','Anti_Rotation_Key')
key.Shape=Part.makeBox(4.0,3.0,8.0,App.Vector(18.0,-1.5,L-9.0))

rules=doc.addObject('App::FeaturePython','RevBU_Rules')
rules.addProperty('App::PropertyString','HeadEnvelope').HeadEnvelope='Ø52 x 78 mm target'
rules.addProperty('App::PropertyString','Window').Window='Ø28 x 3 mm candidate; pressure/impact proof test required'
rules.addProperty('App::PropertyString','QuickRelease').QuickRelease='Single retained latch + key; no loose parts in field'
rules.addProperty('App::PropertyString','RollBoundary').RollBoundary='Waterproof continuous ROLL seal architecture still HOLD'
rules.addProperty('App::PropertyString','DN150').DN150='Re-run swept clearance after real front ring / latch geometry is merged'
rules.addProperty('App::PropertyString','Release').Release='NO RELEASE until rotary seal, window seal and video rotary transfer are frozen'

doc.recompute()
doc.saveAs('PX1_Camera_Head_Shell_RevBU.FCStd')
