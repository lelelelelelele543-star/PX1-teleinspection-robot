import FreeCAD as App, Part

doc=App.newDocument('PX1_Rear_Carrier')
carrier=doc.addObject('Part::Feature','Rear_Carrier')
body=Part.makeCylinder(21.0,28.0)
bearing_bore=Part.makeCylinder(13.0,8.2,App.Vector(0,0,4))
seal_bore=Part.makeCylinder(11.0,7.2,App.Vector(0,0,15))
shaft_clear=Part.makeCylinder(6.0,28.0)
carrier.Shape=body.cut(bearing_bore).cut(seal_bore).cut(shaft_clear)
carrier.addProperty('App::PropertyString','BearingSeat').BearingSeat='Ø26 H7'
carrier.addProperty('App::PropertyString','SealSeat').SealSeat='Ø22 H8'
carrier.addProperty('App::PropertyString','Concentricity').Concentricity='<=0.03 mm'
doc.recompute()
doc.saveAs('PX1_Rear_Carrier.FCStd')
