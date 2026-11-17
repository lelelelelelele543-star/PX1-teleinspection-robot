"""A56: parameterized 3D *proxy* straight-bevel tooth lofts.
Run with FreeCAD Python (FreeCADCmd or GUI macro): python a56_freecad.py
No conjugacy/contact verification. No manufacturing release.
All dimensions ESTIMATED, not measured on Proteus.
"""
import math, os
import FreeCAD as App, Part
from FreeCAD import Vector
M=1.5
ALPHA_DEG=20.0
FACE=8.0
Z=(16,40)
CONE=M*math.hypot(*Z)/2
assert FACE<CONE/3
doc=App.newDocument("PX1_A56_CONICAL_TOOTH_PROXY")
def profile(z, other, rcone, tooth_index, axis="z"):
    delta=math.atan2(z,other)
    pitch_r=rcone*math.sin(delta)
    scale=rcone/CONE
    # Approximate radial sector; NOT a generated involute bevel tooth.
    root_r=(M*z/2-1.25*M)*scale
    tip_r=(M*z/2+M)*scale
    theta=2*math.pi*tooth_index/z
    half=math.pi/(2*z)
    pts=[]
    for r,a in [(root_r,theta-half),(tip_r,theta-half*0.72),
                (tip_r,theta+half*0.72),(root_r,theta+half)]:
        x,y=r*math.cos(a),r*math.sin(a)
        # common apex at z=0, increasing cone distance outward
        p=Vector(x,y,rcone*math.cos(delta))
        pts.append(p)
    pts.append(pts[0])
    return Part.makePolygon(pts)
def build(z,other,name):
    # Each tooth is a ruled shell between two cone-distance sections.
    # The two sections lie on the pitch-cone direction, with radial addendum offsets.
    solids=[]
    for i in range(z):
        inner=Part.Wire(profile(z,other,CONE-FACE,i).Edges)
        outer=Part.Wire(profile(z,other,CONE,i).Edges)
        solids.append(Part.makeLoft([inner,outer],True,True))
    obj=doc.addObject("PartDesign::Feature",name)
    obj.Shape=Part.makeCompound(solids)
    obj.addProperty("App::PropertyString","GeometryStatus")
    obj.GeometryStatus="NON_CONJUGATE_TOOTH_PROXY_NO_CONTACT_VALIDATION"
    obj.addProperty("App::PropertyInteger","Teeth")
    obj.Teeth=z
    return obj
small=build(16,40,"Z16_PROXY")
large=build(40,16,"Z40_PROXY")
# Both gear axes shown coincident for individual shape inspection only.
# They are NOT assembled at 90 degrees here.
doc.recompute()
out=os.path.dirname(os.path.abspath(__file__))
doc.saveAs(os.path.join(out,"a56_proxy.FCStd"))
Part.export([small,large],os.path.join(out,"a56_proxy_unassembled.step"))
print("A56 exported proxy solids, NOT validated meshing gears")
