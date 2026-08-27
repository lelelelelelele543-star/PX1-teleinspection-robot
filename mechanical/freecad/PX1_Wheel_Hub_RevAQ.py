import FreeCAD as App, Part
# PX-1 Rev.AQ wheel hub / prototype manufacturable geometry
# Common hub for front/rear wheel wherever possible.
doc=App.newDocument('PX1_Wheel_Hub_RevAQ')

HUB_OD=28.0
HUB_L=18.0
BORE=10.0
KEY_W=3.0
KEY_D=1.8

hub=doc.addObject('Part::Feature','Wheel_Hub')
shape=Part.makeCylinder(HUB_OD/2,HUB_L)
shape=shape.cut(Part.makeCylinder(BORE/2,HUB_L))
# external face recess for M8 washer/nut/socket access
shape=shape.cut(Part.makeCylinder(8.5,4.0,App.Vector(0,0,HUB_L-4.0)))
# simplified keyway cut in hub only; shaft keyway stays outside seal journal
key=Part.makeBox(KEY_W,KEY_D,HUB_L,App.Vector(-KEY_W/2,BORE/2-KEY_D,0))
shape=shape.cut(key)
hub.Shape=shape
hub.addProperty('App::PropertyString','BoreFit').BoreFit='Ø10 H7 prototype'
hub.addProperty('App::PropertyString','Key').Key='3x3 DIN 6885-style; verify purchased key stock'
hub.addProperty('App::PropertyString','Retention').Retention='M8 external nut + washer; prototype'
hub.addProperty('App::PropertyString','ServiceTool').ServiceTool='13 mm socket target; verify actual selected nut standard'
hub.addProperty('App::PropertyString','Status').Status='PROTOTYPE - verify wheel material/interface before release'
doc.recompute()
doc.saveAs('PX1_Wheel_Hub_RevAQ.FCStd')
