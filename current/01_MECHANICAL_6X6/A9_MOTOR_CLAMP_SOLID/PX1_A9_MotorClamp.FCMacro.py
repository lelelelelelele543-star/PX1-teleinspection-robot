# PX1 A9 parametric motor clamp (assumed geometry). Run inside FreeCAD Python console.
import FreeCAD as App
import Part
from FreeCAD import Vector
P = dict(base_width=44.0, base_length=44.0, base_thickness=3.0,
         motor_diameter=24.0, strap_inner_diameter=25.0, strap_outer_diameter=31.0,
         motor_axis_z=17.0, strap_length=20.0, bolt_x=19.0,
         bolt_y=16.0, hole_diameter=3.2, leg_width=3.0)
doc = App.newDocument("PX1_A9_MotorClamp")
w=P["base_width"]; L=P["base_length"]; t=P["base_thickness"]
base=Part.makeBox(w,L,t,Vector(-w/2,-L/2,0))
# Two bolt stations per side: four clearance bores through base.
for x in (-P["bolt_x"],P["bolt_x"]):
    for y in (-P["bolt_y"],P["bolt_y"]):
        base=base.cut(Part.makeCylinder(P["hole_diameter"]/2,t+2,Vector(x,y,-1)))
axis=Vector(0,1,0); z=P["motor_axis_z"]; sl=P["strap_length"]
outer=Part.makeCylinder(P["strap_outer_diameter"]/2,sl,Vector(0,-sl/2,z),axis)
inner=Part.makeCylinder(P["strap_inner_diameter"]/2,sl+2,Vector(0,-sl/2-1,z),axis)
ring=outer.cut(inner)
# Upper semicircular strap: remove all material below motor centreline.
upper=Part.makeBox(50,sl+2,25,Vector(-25,-sl/2-1,z))
ring=ring.common(upper)
# Vertical bolt tabs; bridge from ring edge to tabs at centreline.
for sign in (-1,1):
    x0=17.5 if sign>0 else -20.5
    leg=Part.makeBox(3,sl,17,Vector(x0,-sl/2,3))
    bridge=Part.makeBox(5.5,sl,3,Vector(15 if sign>0 else -20.5,-sl/2,17))
    ring=ring.fuse(leg).fuse(bridge)
    for y in (-P["bolt_y"],P["bolt_y"]):
        # Bolt y positions are OUTSIDE 20 mm strap length: tabs need longitudinal ears.
        pass
# Longitudinal bolt ears on both sides, integrated with legs.
for x in (-19,19):
    ear=Part.makeBox(5,38,3,Vector(x-2.5,-19,3))
    ring=ring.fuse(ear)
    for y in (-16,16):
        ring=ring.cut(Part.makeCylinder(1.6,6,Vector(x,y,2)))
base_obj=doc.addObject("PartDesign::Feature","Base");base_obj.Shape=base
clamp_obj=doc.addObject("PartDesign::Feature","Clamp");clamp_obj.Shape=ring.removeSplitter()
base_obj.ViewObject.ShapeColor=(0.62,0.68,0.74)
clamp_obj.ViewObject.ShapeColor=(0.88,0.42,0.22)
doc.recompute()
print("A9 BASE valid",base_obj.Shape.isValid(),"CLAMP valid",clamp_obj.Shape.isValid())
print("A9 volumes",base_obj.Shape.Volume,clamp_obj.Shape.Volume)
# Outputs are preliminary and require FreeCAD execution and clash checking.
Part.export([base_obj,clamp_obj],"PX1_A9_motor_clamp.step")
doc.saveAs("PX1_A9_motor_clamp.FCStd")
