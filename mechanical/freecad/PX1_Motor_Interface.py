import FreeCAD as App, Part

doc=App.newDocument('PX1_Motor_Interface')
base=doc.addObject('Part::Feature','Universal_Cradle')
base.Shape=Part.makeBox(104,58,5)
base.addProperty('App::PropertyString','Role').Role='Permanent chassis interface'
adapter=doc.addObject('Part::Feature','Replaceable_37mm_Adapter')
adapter.Shape=Part.makeBox(58,48,4).cut(Part.makeCylinder(19,4,App.Vector(29,24,0)))
adapter.addProperty('App::PropertyString','Role').Role='Supplier-specific replaceable plate'
adapter.addProperty('App::PropertyString','MotorEnvelope').MotorEnvelope='<=95x42x42 mm excluding shaft'
adapter.addProperty('App::PropertyString','TargetMeshCenter').TargetMeshCenter='24.0 mm z18/z30'
doc.recompute()
doc.saveAs('PX1_Motor_Interface.FCStd')
