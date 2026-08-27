import FreeCAD as App, Part
# PX-1 Rev.BF manual parallelogram camera lift kinematic skeleton
# Geometry is a manufacturable candidate for link lengths/pivots, but camera-head envelope remains HOLD.
doc=App.newDocument('PX1_Camera_Lift_Kinematics_RevBF')

# Coordinate system: X crawler length, Y width, Z height from body bottom.
BASE_X1=34.0
BASE_X2=76.0
BASE_Z=76.0
LINK_L=68.0
LINK_W=12.0
LINK_T=5.0
PIVOT_D=6.0
TOP_BAR_SPACING=42.0

# Three manual detent angles chosen to create useful discrete heights.
POSITIONS={
    'LOW': 8.0,
    'DN150_SAFE': 28.0,
    'HIGH': 48.0,
}

def pin(name,x,y,z):
    o=doc.addObject('Part::Feature',name)
    o.Shape=Part.makeCylinder(PIVOT_D/2,18,App.Vector(x,y-9,z),App.Vector(0,1,0))
    return o

def link_between(name,x0,z0,x1,z1,y):
    import math
    dx=x1-x0; dz=z1-z0
    L=(dx*dx+dz*dz)**0.5
    box=Part.makeBox(L,LINK_T,LINK_W)
    ang=math.degrees(math.atan2(dz,dx))
    box.rotate(App.Vector(0,0,0),App.Vector(0,1,0),-ang)
    box.translate(App.Vector(x0,y,z0-LINK_W/2))
    o=doc.addObject('Part::Feature',name)
    o.Shape=box
    return o

# Base pivot rail reference
rail=doc.addObject('Part::Feature','Lift_Base_Rail')
rail.Shape=Part.makeBox(88,42,8,App.Vector(18,26,76))
rail.addProperty('App::PropertyString','Interface').Interface='Bolts to Rev.BE front/lift interface; 4x M5 target'

for state,theta in POSITIONS.items():
    import math
    a=math.radians(theta)
    dx=LINK_L*math.cos(a)
    dz=LINK_L*math.sin(a)
    tx1=BASE_X1+dx; tx2=BASE_X2+dx
    tz=BASE_Z+dz
    grp=doc.addObject('App::DocumentObjectGroup',state)
    objs=[]
    for side,y in [('L',31.0),('R',63.0)]:
        p1=pin(f'{state}_{side}_BaseFront',BASE_X1,y,BASE_Z)
        p2=pin(f'{state}_{side}_BaseRear',BASE_X2,y,BASE_Z)
        l1=link_between(f'{state}_{side}_LinkFront',BASE_X1,BASE_Z,tx1,tz,y-2.5)
        l2=link_between(f'{state}_{side}_LinkRear',BASE_X2,BASE_Z,tx2,tz,y-2.5)
        objs += [p1,p2,l1,l2]
    top=doc.addObject('Part::Feature',f'{state}_Camera_Carrier')
    top.Shape=Part.makeBox(TOP_BAR_SPACING+30,42,8,App.Vector(tx1-15,26,tz-4))
    top.addProperty('App::PropertyLength','CameraCenterZ').CameraCenterZ=tz+24.0
    top.addProperty('App::PropertyString','State').State=state
    objs.append(top)
    grp.addObjects(objs)

rules=doc.addObject('App::FeaturePython','LiftRules')
rules.addProperty('App::PropertyLength','LinkLength').LinkLength=LINK_L
rules.addProperty('App::PropertyLength','PivotDiameter').PivotDiameter=PIVOT_D
rules.addProperty('App::PropertyString','PivotHardware').PivotHardware='M6 shoulder bolt or Ø6 stainless pin + polymer/bronze bush; exact purchased part HOLD'
rules.addProperty('App::PropertyString','Locking').Locking='Positive manual detent/locking pin required at LOW, DN150_SAFE, HIGH'
rules.addProperty('App::PropertyString','OneHand').OneHand='Target one-hand lift operation with positive lock; spring assist optional after measured camera mass'
rules.addProperty('App::PropertyString','Status').Status='KINEMATIC CANDIDATE; camera envelope and DN150 circular clearance must be verified before RELEASE'

doc.recompute()
doc.saveAs('PX1_Camera_Lift_Kinematics_RevBF.FCStd')
