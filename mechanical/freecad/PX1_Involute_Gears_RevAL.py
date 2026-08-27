import FreeCAD as App, Part
import math
from PX1_Master_Parameters import *

# Standard external spur gears, ISO-style basic rack approximation:
# module 1.0, pressure angle 20 deg, addendum 1.0m, dedendum 1.25m.
# Involute flanks are generated analytically. Root transition is a simple radial connection,
# so this file is suitable for prototype gears / interference checks. For production-cut gears,
# root trochoid and cutter data must be confirmed by the gear supplier.

ALPHA = math.radians(20.0)
FACE = 8.0


def involute_point(rb, t, rot):
    x = rb * (math.cos(t) + t * math.sin(t))
    y = rb * (math.sin(t) - t * math.cos(t))
    c, s = math.cos(rot), math.sin(rot)
    return App.Vector(x*c-y*s, x*s+y*c, 0)


def gear_wire(z, m=1.0, bore=10.0, samples=10):
    rp = m*z/2.0
    rb = rp*math.cos(ALPHA)
    ra = rp + m
    rf = rp - 1.25*m
    tp = math.sqrt((rp/rb)**2 - 1.0)
    invp = tp - math.atan(tp)
    half_tooth = math.pi/(2.0*z)
    base_rot = half_tooth - invp

    tmax = math.sqrt((ra/rb)**2 - 1.0)
    flank = [involute_point(rb, tmax*i/samples, base_rot) for i in range(samples+1)]
    flank_m = [App.Vector(p.x,-p.y,0) for p in flank]

    # one tooth: root-right -> involute-right -> tip arc -> involute-left -> root-left
    ang_root_r = math.atan2(flank[0].y, flank[0].x)
    ang_root_l = -ang_root_r
    rr = App.Vector(rf*math.cos(ang_root_r), rf*math.sin(ang_root_r), 0)
    rl = App.Vector(rf*math.cos(ang_root_l), rf*math.sin(ang_root_l), 0)

    edges=[]
    edges.append(Part.makeLine(rr, flank[0]))
    edges.append(Part.makePolygon(flank))
    tip_r = flank[-1]
    tip_l = flank_m[-1]
    midang = 0.0
    mid = App.Vector(ra,0,0)
    edges.append(Part.Arc(tip_r,mid,tip_l).toShape())
    edges.append(Part.makePolygon(list(reversed(flank_m))))
    edges.append(Part.makeLine(flank_m[0], rl))

    tooth_wire = Part.Wire([e if isinstance(e,Part.Edge) else e for e in edges])
    tooth_face = Part.Face(tooth_wire)

    # root disk + replicated teeth
    shape = Part.makeCylinder(rf, FACE)
    tooth = tooth_face.extrude(App.Vector(0,0,FACE))
    for i in range(z):
        cp = tooth.copy()
        cp.rotate(App.Vector(0,0,0),App.Vector(0,0,1),360.0*i/z)
        shape = shape.fuse(cp)
    shape = shape.cut(Part.makeCylinder(bore/2.0, FACE))
    return shape, rp, rb, ra, rf


def add_gear(doc,name,z,bore):
    obj=doc.addObject('Part::Feature',name)
    shape,rp,rb,ra,rf=gear_wire(z,GEAR_MODULE,bore)
    obj.Shape=shape
    for prop,val in [('Teeth',z)]:
        obj.addProperty('App::PropertyInteger',prop,'Gear'); setattr(obj,prop,val)
    for prop,val in [('Module',GEAR_MODULE),('PitchDiameter',2*rp),('BaseDiameter',2*rb),('OutsideDiameter',2*ra),('RootDiameter',2*rf)]:
        obj.addProperty('App::PropertyLength',prop,'Gear'); setattr(obj,prop,val)
    obj.addProperty('App::PropertyString','PressureAngle','Gear').PressureAngle='20 deg'
    obj.addProperty('App::PropertyString','RootStatus','Gear').RootStatus='Prototype radial root transition; production cutter trochoid TBD'
    return obj


doc=App.newDocument('PX1_Involute_Gears_RevAL')
add_gear(doc,'Pinion_Z18',PINION_Z,6.0)
add_gear(doc,'Reduction_Z30',REDUCTION_Z,10.0)
add_gear(doc,'Side_Z40',SIDE_Z,10.0)
doc.recompute()
doc.saveAs('PX1_Involute_Gears_RevAL.FCStd')
