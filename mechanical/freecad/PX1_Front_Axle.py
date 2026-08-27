import FreeCAD as App, Part

doc=App.newDocument('PX1_Front_Axle')
ax=doc.addObject('Part::Feature','Front_Stationary_Axle')
ax.Shape=Part.makeCylinder(5.0,32.0).fuse(Part.makeCylinder(9.0,5.0))
ax.addProperty('App::PropertyString','Material').Material='AISI316'
ax.addProperty('App::PropertyString','Function').Function='External stationary axle; no pressure-body penetration'
doc.recompute()
doc.saveAs('PX1_Front_Axle.FCStd')
