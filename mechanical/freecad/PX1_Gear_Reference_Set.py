import FreeCAD as App, Part

doc=App.newDocument('PX1_Gear_Reference_Set')
GEAR_MODULE=1.0

def add_ref(name,z,bore,face):
    pitch_d=z*GEAR_MODULE
    od=(z+2)*GEAR_MODULE
    obj=doc.addObject('Part::Feature',name)
    obj.Shape=Part.makeCylinder(od/2,face).cut(Part.makeCylinder(bore/2,face))
    obj.addProperty('App::PropertyInteger','Teeth').Teeth=z
    obj.addProperty('App::PropertyLength','Module').Module=GEAR_MODULE
    obj.addProperty('App::PropertyLength','PitchDiameter').PitchDiameter=pitch_d
    obj.addProperty('App::PropertyLength','OutsideDiameter').OutsideDiameter=od
    obj.addProperty('App::PropertyString','PressureAngle').PressureAngle='20 deg'
    obj.addProperty('App::PropertyString','Status').Status='REFERENCE ENVELOPE ONLY — not manufacturing tooth geometry'
    return obj

add_ref('Pinion_Z18',18,6.0,8.0)
add_ref('Reduction_Z30',30,10.0,8.0)
add_ref('Side_Z40',40,10.0,8.0)
doc.recompute()
doc.saveAs('PX1_Gear_Reference_Set.FCStd')
