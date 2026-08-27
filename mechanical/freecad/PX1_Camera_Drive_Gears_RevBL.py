import FreeCAD as App, Part, math
# PX-1 Rev.BL camera-drive gear study
# Spur pair uses analytical involute tooth construction.
# Worm pair is a kinematic/packaging model only; final manufacturable worm geometry remains HOLD.

doc=App.newDocument('PX1_Camera_Drive_Gears_RevBL')

# ---------- common spur involute ----------
def involute_gear(name, module, z, face, bore, pressure_deg=20.0):
    alpha=math.radians(pressure_deg)
    rp=module*z/2.0
    rb=rp*math.cos(alpha)
    ra=module*(z+2)/2.0
    rf=max(module*(z-2.5)/2.0, bore/2+0.5)
    # Tooth flank points from base circle to addendum.
    pts=[]
    for i in range(10):
        r=rb+(ra-rb)*i/9.0
        t=math.sqrt(max((r/rb)**2-1.0,0.0))
        phi=t-math.atan(t)
        x=r*math.cos(phi); y=r*math.sin(phi)
        pts.append(App.Vector(x,y,0))
    # rotate flank so pitch-circle tooth thickness is approximately pi*m/2
    tp=math.sqrt(max((rp/rb)**2-1.0,0.0))
    phip=tp-math.atan(tp)
    half_tooth=math.pi/(2*z)
    rot=half_tooth-phip
    def rotpt(p,a):
        return App.Vector(p.x*math.cos(a)-p.y*math.sin(a),p.x*math.sin(a)+p.y*math.cos(a),0)
    left=[rotpt(p,rot) for p in pts]
    right=[App.Vector(p.x,-p.y,0) for p in left]
    # simple root closure; root fillet not manufacturing-ready
    a1=math.atan2(left[0].y,left[0].x); a2=math.atan2(right[0].y,right[0].x)
    rootL=App.Vector(rf*math.cos(a1),rf*math.sin(a1),0)
    rootR=App.Vector(rf*math.cos(a2),rf*math.sin(a2),0)
    wire=Part.makePolygon([rootL]+left+list(reversed(right))+[rootR,rootL])
    tooth=Part.Face(wire).extrude(App.Vector(0,0,face))
    gear=Part.makeCylinder(rf,face)
    for k in range(z):
        t=tooth.copy(); t.rotate(App.Vector(0,0,0),App.Vector(0,0,1),360.0*k/z)
        gear=gear.fuse(t)
    gear=gear.cut(Part.makeCylinder(bore/2,face))
    obj=doc.addObject('Part::Feature',name); obj.Shape=gear
    obj.addProperty('App::PropertyInteger','Teeth').Teeth=z
    obj.addProperty('App::PropertyLength','Module').Module=module
    obj.addProperty('App::PropertyString','PressureAngle').PressureAngle=f'{pressure_deg} deg'
    obj.addProperty('App::PropertyString','Status').Status='ANALYTICAL INVOLUTE; ROOT FILLET/TOOL GEOMETRY HOLD'
    return obj

# ROLL pair m0.5 z17/z51 = 3:1
roll_p=involute_gear('ROLL_Pinion_z17',0.5,17,5.0,3.0)
roll_g=involute_gear('ROLL_Gear_z51',0.5,51,5.0,17.2)
roll_p.Placement.Base=App.Vector(0,0,0)
roll_g.Placement.Base=App.Vector(17.0,0,0)

# TILT worm packaging target: single-start worm, wheel z20, module-like axial pitch target 0.5
worm=doc.addObject('Part::Feature','TILT_Worm_Packaging')
# core/envelope only; not a tooth surface
worm.Shape=Part.makeCylinder(3.0,16.0)
worm.addProperty('App::PropertyString','RatioTarget').RatioTarget='1-start worm / 20-tooth wheel = 20:1'
worm.addProperty('App::PropertyString','Status').Status='PACKAGING ONLY — FINAL WORM PROFILE MUST MATCH SELECTED WORM/WHEEL STANDARD OR PURCHASED SET'

wheel=involute_gear('TILT_WormWheel_Envelope_z20',0.5,20,5.0,6.0)
wheel.Placement.Base=App.Vector(8.0,0,0)
wheel.addProperty('App::PropertyString','Status2').Status2='SPUR-LIKE ENVELOPE ONLY; NOT A MANUFACTURABLE WORM WHEEL'

check=doc.addObject('App::FeaturePython','DesignChecks')
check.addProperty('App::PropertyString','ROLLCenter').ROLLCenter='17.0 mm for m0.5 z17/z51'
check.addProperty('App::PropertyString','ROLLRatio').ROLLRatio='3.000:1'
check.addProperty('App::PropertyString','TILTRatio').TILTRatio='20:1 target'
check.addProperty('App::PropertyString','HeadLimit').HeadLimit='Must fit within Ø52 x 72 mm camera-head envelope'
check.addProperty('App::PropertyString','Release').Release='ROLL gear root/tooling + all worm geometry require prototype/vendor confirmation before RELEASE'

doc.recompute()
doc.saveAs('PX1_Camera_Drive_Gears_RevBL.FCStd')
