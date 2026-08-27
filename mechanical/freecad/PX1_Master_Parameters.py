import FreeCAD as App

DOC_NAME = 'PX1_MASTER'

def q(mm):
    return App.Units.Quantity(f'{mm} mm')

doc = App.ActiveDocument or App.newDocument(DOC_NAME)
params = doc.getObject('PX1_Parameters') or doc.addObject('App::FeaturePython','PX1_Parameters')
params.Label = 'PX-1 Master Parameters'

# Envelope
for name,label,val in [
    ('BodyLength','Body length',250.0),
    ('BodyWidth','Body width',94.0),
    ('BodyHeight','Body height',76.0),
    ('WallSide','Side wall',8.0),
    ('WallFrontRear','Front/rear wall',12.0),
    ('WallFloorRoof','Floor/roof wall',7.0),
    ('Wheelbase','Wheelbase',160.0),
    ('WheelDiameter','Nominal wheel diameter',90.0),
    ('WheelWidth','Nominal wheel width',18.0),
    ('RearAxleX','Rear axle station X',205.0),
    ('FrontAxleX','Front axle station X',45.0),
    ('AxleZ','Wheel axle Z',37.0),
    ('RearCarrierBore','Rear carrier body bore',38.0),
    ('RearShaftDiameter','Rear output shaft',10.0),
    ('BearingOD','6000 bearing OD',26.0),
    ('BearingWidth','6000 bearing width',8.0),
    ('SealOD','Radial seal OD',22.0),
    ('SealWidth','Radial seal width',7.0),
    ('TailThreadMajor','LEMO tail nominal thread major',45.0),
    ('MotorEnvelopeL','Max motor envelope length',95.0),
    ('MotorEnvelopeW','Max motor envelope width',42.0),
    ('MotorEnvelopeH','Max motor envelope height',42.0),
]:
    if not hasattr(params,name):
        params.addProperty('App::PropertyLength',name,'PX1',label)
    setattr(params,name,q(val))

# Non-length engineering constants
for name,label,val in [
    ('SideGearModule','Side gear module',1.0),
    ('SideGearTeeth','Side gear teeth',40),
    ('MotorPinionTeeth','Motor pinion teeth',18),
    ('ReductionGearTeeth','Reduction gear teeth',30),
]:
    if not hasattr(params,name):
        typ='App::PropertyInteger' if isinstance(val,int) else 'App::PropertyFloat'
        params.addProperty(typ,name,'PX1',label)
    setattr(params,name,val)

# Status strings
for name,label,val in [
    ('Revision','Mechanical master revision','Rev.AK'),
    ('ManufacturingStatus','Status','PROTOTYPE - NOT SERIAL RELEASE'),
    ('MaterialBody','Body material','EN AW-6082 T6 / prototype'),
]:
    if not hasattr(params,name):
        params.addProperty('App::PropertyString',name,'PX1',label)
    setattr(params,name,val)

doc.recompute()
