import FreeCAD as App, Part

doc=App.newDocument('PX1_Rear_Output_Shaft')
shaft=doc.addObject('Part::Feature','Rear_Output_Shaft')
main=Part.makeCylinder(5.0,54.0)
shoulder=Part.makeCylinder(6.0,8.0,App.Vector(0,0,46))
shape=main.fuse(shoulder)
shape=shape.cut(Part.makeCylinder(3.05,3.2))
shaft.Shape=shape
shaft.addProperty('App::PropertyString','Material').Material='AISI316 / 40X13'
shaft.addProperty('App::PropertyString','SealJournal').SealJournal='Ø10 h6, Ra<=0.4'
shaft.addProperty('App::PropertyString','BearingJournal').BearingJournal='Ø10 h6'
shaft.addProperty('App::PropertyString','Runout').Runout='<=0.02 mm'
doc.recompute()
doc.saveAs('PX1_Rear_Output_Shaft.FCStd')
