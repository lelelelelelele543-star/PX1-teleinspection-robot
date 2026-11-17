"""PX1 integrated 6x6 chassis, design-target only. Run in FreeCAD Python / FreeCADCmd.
Generated parts are simplified solids. Gear teeth, bevel teeth, O-ring grooves and dynamic seals are NOT validated.
Axes: X along crawler, Y lateral, Z up. Units mm.
"""
import FreeCAD as App, Part, math, os
from FreeCAD import Vector as V
ROOT=os.path.dirname(os.path.abspath(__file__))
D=App.newDocument("PX1_Integrated_6x6_M1")
P=dict(body_L=307.,body_W=92.,body_H=70.,wall=5.,wheel_D=105.,wheel_W=18.,
       stations=(-110.,0.,110.),gear_x=(-110.,-55.,0.,55.,110.),
       gear_m=1.1,gear_z=-5.,gear_y=32.,gear_thick=6.,axle_D=10.,
       motor_D=24.,motor_L=62.,motor_z=10.,motor_y=18.,
       pressure_bar_min=0.4,pressure_bar_max=0.7)
parts=[]
def add(name,shape,color):
    if shape.isNull(): raise RuntimeError(name+" null shape")
    o=D.addObject("PartDesign::Feature",name);o.Shape=shape
    o.ViewObject.ShapeColor=color;parts.append(o);return o
def cyl(r,h,p,d): return Part.makeCylinder(r,h,V(*p),V(*d))
L,W,H=P["body_L"],P["body_W"],P["body_H"]
outer=Part.makeBox(L,W,H,V(-L/2,-W/2,-H/2))
inner=Part.makeBox(L-10,W-10,H-10,V(-L/2+5,-W/2+5,-H/2+5))
lid_opening=Part.makeBox(170,75,12,V(-85,-37.5,29))
add("Body_hollow_ASSUMED",outer.cut(inner).cut(lid_opening),(0.64,0.69,0.73))
# Separate lid is a design envelope; cut aperture into top before production release.
add("Lid_ASSUMED",Part.makeBox(170,75,4,V(-85,-37.5,35)),(0.18,0.4,0.62))
gasket=Part.makeBox(174,79,2,V(-87,-39.5,34)).cut(Part.makeBox(168,73,2,V(-84,-36.5,34)))
add("Lid_gasket_PROXY",gasket,(0.18,0.64,0.35))
for side,s in (("L",-1),("R",1)):
    # Motors face rear wheel station; avoid center axle at X=0 by raising motor axes.
    add("Motor_"+side+"_ENVELOPE",cyl(12,62,(35,s*18,10),(1,0,0)),(0.22,0.32,0.4))
    add("Motor_shaft_"+side,cyl(4,16,(97,s*18,10),(1,0,0)),(0.8,0.7,0.3))
    # Five Z50 stations per side. m=1.1 design assumption -> 55 mm pitch diameter and 55 mm centers.
    for j,x in enumerate(P["gear_x"]):
        gy=s*32
        # Pitch solids are intentionally NOT teeth or manufactured gears.
        add("Z50_pitch_PROXY_"+side+"_"+str(j+1),cyl(27.5,6,(x,gy-3,-5),(0,1,0)),(0.75,0.42,0.19))
        if j%2==0:
            add("Wheel_axle_"+side+"_"+str(j//2+1),cyl(5,43,(x,s*29,-5),(0,s,0)),(0.77,0.78,0.79))
            # Bearing 10x22x7: geometry proxy, not manufacturer verification.
            bp=(x,s*43,-5)
            add("Bearing_PROXY_"+side+"_"+str(j//2+1),
                cyl(11,7,bp,(0,s,0)).cut(cyl(5,7,bp,(0,s,0))),(0.92,0.72,0.28))
            add("Wheel_"+side+"_"+str(j//2+1),cyl(52.5,18,(x,s*60,-5),(0,s,0)),(0.11,0.14,0.18))
        else:
            add("Idler_stub_"+side+"_"+str(j),cyl(5,13,(x,s*25,-5),(0,s,0)),(0.7,0.73,0.76))
    # Bevel input at rear X=100: proxy solids only, orientation requires contact validation.
    add("Bevel_Z16_PROXY_"+side,cyl(12,8,(101,s*18,10),(1,0,0)),(0.85,0.5,0.18))
    add("Bevel_Z40_PROXY_"+side,cyl(30,8,(110,s*24,-5),(0,s,0)),(0.85,0.5,0.18))
# Analytical envelope checks; not a substitute for FreeCAD Boolean collision tests.
wheel_gap=(P["stations"][1]-P["stations"][0])-P["wheel_D"]
gear_pitch=P["gear_m"]*50
gear_gap=(P["gear_x"][1]-P["gear_x"][0])-gear_pitch
motor_top=P["motor_z"]+P["motor_D"]/2
assert wheel_gap>=0, "Adjacent wheels overlap"
assert abs(gear_gap)<1e-8, "Z50 pitch mismatch"
assert motor_top <= P["body_H"]/2-P["wall"], "Motor above inner roof"
assert len([o for o in parts if o.Name.startswith("Wheel_L_") or o.Name.startswith("Wheel_R_")])==6
print("PASS wheel clearance",wheel_gap,"mm; Z50 pitch",gear_pitch,"mm; motor top",motor_top,"mm")
print("NOT_RUN bevel contact, real teeth, bearing fits, pressure seals, volumetric interference")
D.recompute()
D.saveAs(os.path.join(ROOT,"PX1_Integrated_6x6_M1.FCStd"))
Part.export(parts,os.path.join(ROOT,"PX1_Integrated_6x6_M1.step"))
print("DESIGN PROXY ONLY: generated FCStd/STEP; check interference, gear mesh, pressure seals before manufacturing")
