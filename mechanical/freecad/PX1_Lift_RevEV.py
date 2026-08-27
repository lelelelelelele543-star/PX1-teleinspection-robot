import FreeCAD as App, Part, math

# PX-1 Rev.EV — plate-arm manual lift prototype solid.
# Kinematics derived from current project baseline. Prototype only.

doc = App.newDocument('PX1_Lift_RevEV')

PIVOT_X = 200.0
PIVOT_Z = 94.0
LINK_L = 120.0
ARM_W = 22.0
ARM_T = 4.0
ARM_Y = 24.0
PIN_D = 8.0
CAM_Z_LOW = 75.0
CAM_Z_MID = 130.0
CAM_Z_HIGH = 205.0
CAM_OFFSET_Z = 10.0
YOKE_W = 54.0
YOKE_T = 5.0
CAM_R = 26.0
CAM_L = 72.0


def pose(cam_z):
    s = (cam_z-(PIVOT_Z+CAM_OFFSET_Z))/LINK_L
    if abs(s) > 1.0:
        raise ValueError('target outside linkage reach')
    th = math.asin(s)
    ux = PIVOT_X - LINK_L*math.cos(th)
    uz = PIVOT_Z + LINK_L*math.sin(th)
    return th, ux, uz


def plate_between(x1,z1,x2,z2,y0,t,w):
    dx=x2-x1
    dz=z2-z1
    L=math.hypot(dx,dz)
    a=math.degrees(math.atan2(dz,dx))
    plate=Part.makeBox(L,t,w,App.Vector(x1,y0,z1-w/2.0))
    plate.rotate(App.Vector(x1,y0,z1),App.Vector(0,1,0),-a)
    return plate

th, ux, uz = pose(CAM_Z_LOW)

# left/right plate arms at LOW position
for side, y in [('L',ARM_Y),('R',-ARM_Y-ARM_T)]:
    arm = doc.addObject('Part::Feature',f'LiftArm_{side}_LOW')
    arm.Shape = plate_between(PIVOT_X,PIVOT_Z,ux,uz,y,ARM_T,ARM_W)
    arm.addProperty('App::PropertyString','Material').Material='4 mm stainless candidate'
    arm.addProperty('App::PropertyString','Pivot').Pivot='Ø8 bushed pivots'

# lower structural bosses
for side,yc in [('L',ARM_Y+ARM_T/2.0),('R',-ARM_Y-ARM_T/2.0)]:
    boss=doc.addObject('Part::Feature',f'LowerPivotBoss_{side}')
    boss.Shape=Part.makeCylinder(10.0,12.0,App.Vector(PIVOT_X,yc-6.0,PIVOT_Z),App.Vector(0,1,0))
    boss.Shape=boss.Shape.cut(Part.makeCylinder(PIN_D/2.0,14.0,App.Vector(PIVOT_X,yc-7.0,PIVOT_Z),App.Vector(0,1,0)))
    boss.addProperty('App::PropertyString','Mount').Mount='integral/body-mounted structural boss; not on service cover'

# camera yoke crossmember at upper pivot
cross=doc.addObject('Part::Feature','CameraYokeCrossmember')
cross.Shape=Part.makeBox(18.0,YOKE_W,YOKE_T,App.Vector(ux-9.0,-YOKE_W/2.0,uz-YOKE_T/2.0))
cross.addProperty('App::PropertyString','Function').Function='ties left/right arms; supports camera tilt yoke and quick release'

# camera LOW envelope
cam=doc.addObject('Part::Feature','CameraHead_LOW_Envelope')
cam.Shape=Part.makeCylinder(CAM_R,CAM_L,App.Vector(ux-CAM_L/2.0,0,CAM_Z_LOW),App.Vector(1,0,0))
cam.addProperty('App::PropertyString','Motion').Motion='TILT +/-105 deg, ROLL continuous; envelope only'

# DN150 stop pin candidate near left boss
stop=doc.addObject('Part::Feature','DN150_StopPin_Envelope')
stop.Shape=Part.makeCylinder(4.0,18.0,App.Vector(PIVOT_X-18.0,-9.0,PIVOT_Z-7.0),App.Vector(0,1,0))
stop.addProperty('App::PropertyString','Function').Function='captive/removable hard stop blocks lift above DN150-safe range'

# clamp stack envelope on right pivot
clamp=doc.addObject('Part::Feature','M8_ClampStack_Envelope')
clamp.Shape=Part.makeCylinder(11.0,24.0,App.Vector(PIVOT_X,-36.0,PIVOT_Z),App.Vector(0,1,0))
clamp.addProperty('App::PropertyString','Stack').Stack='M8 adjustable lever + Belleville washers + thrust/friction washers'

# gas spring candidate envelope between lower body point and moving arm point
# Exact endpoints remain tuning variables.
GS_FIXED=(230.0,0.0,68.0)
GS_MOVING=(ux+32.0,0.0,uz+5.0)
v=App.Vector(GS_MOVING[0]-GS_FIXED[0],0,GS_MOVING[2]-GS_FIXED[2])
gs=doc.addObject('Part::Feature','GasSpring_150N_Envelope')
gs.Shape=Part.makeCylinder(6.0,v.Length,App.Vector(*GS_FIXED),v)
gs.addProperty('App::PropertyString','Status').Status='150 N class only; endpoints/stroke/article not frozen'

rules=doc.addObject('App::FeaturePython','RevEV_Rules')
rules.addProperty('App::PropertyString','Low').Low=f'LOW camera Z={CAM_Z_LOW}; upper pivot X={ux:.2f}/Z={uz:.2f}'
rules.addProperty('App::PropertyString','MidHigh').MidHigh=f'MID Z={CAM_Z_MID}; HIGH Z={CAM_Z_HIGH}; full solids not shown simultaneously'
rules.addProperty('App::PropertyString','DN150').DN150='mechanical stop mandatory; LOW only until full physical sweep'
rules.addProperty('App::PropertyString','Release').Release='prototype plate-arm solid, not manufacturing release'

doc.recompute()
doc.saveAs('PX1_Lift_RevEV.FCStd')
