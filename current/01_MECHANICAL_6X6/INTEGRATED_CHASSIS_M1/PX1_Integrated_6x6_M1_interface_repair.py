"""PX1 integrated 6x6 chassis, design-target only. Run in FreeCAD Python / FreeCADCmd.
Generated parts are simplified solids. Gear teeth, bevel teeth, O-ring grooves and dynamic seals are NOT validated.
Axes: X along crawler, Y lateral, Z up. Units mm.
"""
import FreeCAD as App, Part, math, os
from FreeCAD import Vector as V
ROOT=os.path.dirname(os.path.abspath(__file__))
D=App.newDocument("PX1_Integrated_6x6_M1")
P=dict(body_L=307.,body_W=78.,body_H=70.,wall=5.,wheel_D=78.,wheel_W=18.,
       stations=(-110.,0.,110.),gear_x=(-110.,-55.,0.,55.,110.),
       gear_m=1.1,gear_z=0.,gear_y=30.,gear_thick=6.,axle_D=10.,
       motor_D=22.,motor_L=42.,motor_z=10.,motor_y=14.,
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
lid_opening=Part.makeBox(170,60,12,V(-85,-30,29))
# Six through-wall shaft passages and bearing counterbores (design targets).
for xx in P["stations"]:
    for sign in (-1,1):
        outer=outer.cut(cyl(5.5,12,(xx,sign*34,0),(0,sign,0)))
        outer=outer.cut(cyl(11,3,(xx,sign*35,0),(0,sign,0)))
add("Body_hollow_ASSUMED",outer.cut(inner).cut(lid_opening),(0.64,0.69,0.73))
# Separate lid is a design envelope; cut aperture into top before production release.
add("Lid_ASSUMED",Part.makeBox(178,68,4,V(-89,-34,36)),(0.18,0.4,0.62))
gasket=Part.makeBox(174,64,1,V(-87,-32,35)).cut(Part.makeBox(166,56,1,V(-83,-28,35)))
add("Lid_gasket_PROXY",gasket,(0.18,0.64,0.35))
for side,s in (("L",-1),("R",1)):
    # Motors face rear wheel station; avoid center axle at X=0 by raising motor axes.
    add("Motor_"+side+"_ENVELOPE",cyl(P["motor_D"]/2,P["motor_L"],(35,s*14,10),(1,0,0)),(0.22,0.32,0.4))
    add("Motor_shaft_"+side,cyl(4,32,(77,s*14,10),(1,0,0)),(0.8,0.7,0.3))
    # Five Z50 stations per side. m=1.1 design assumption -> 55 mm pitch diameter and 55 mm centers.
    for j,x in enumerate(P["gear_x"]):
        gy=s*P["gear_y"]
        # Pitch solids are intentionally NOT teeth or manufactured gears.
        add("Z50_pitch_PROXY_"+side+"_"+str(j+1),cyl(27.5,6,(x,gy-3,P["gear_z"]),(0,1,0)),(0.75,0.42,0.19))
        if j%2==0:
            add("Wheel_axle_"+side+"_"+str(j//2+1),cyl(5,34,(x,s*29,P["gear_z"]),(0,s,0)),(0.77,0.78,0.79))
            # Bearing 10x22x7: geometry proxy, not manufacturer verification.
            bp=(x,s*34,P["gear_z"])
            add("Bearing_PROXY_"+side+"_"+str(j//2+1),
                cyl(11,7,bp,(0,s,0)).cut(cyl(5,7,bp,(0,s,0))),(0.92,0.72,0.28))
            add("Wheel_"+side+"_"+str(j//2+1),cyl(P['wheel_D']/2,18,(x,s*43,P["gear_z"]),(0,s,0)),(0.11,0.14,0.18))
        else:
            add("Idler_stub_"+side+"_"+str(j),cyl(5,13,(x,s*25,P["gear_z"]),(0,s,0)),(0.7,0.73,0.76))
    # Bevel input at rear X=100: proxy solids only, orientation requires contact validation.
    add("Bevel_Z16_PROXY_"+side,cyl(12,8,(101,s*14,10),(1,0,0)),(0.85,0.5,0.18))
    add("Bevel_Z40_PROXY_"+side,cyl(30,8,(110,s*19,P["gear_z"]),(0,s,0)),(0.85,0.5,0.18))
# Analytical envelope checks; not a substitute for FreeCAD Boolean collision tests.
wheel_gap=(P["stations"][1]-P["stations"][0])-P["wheel_D"]
gear_pitch=P["gear_m"]*50
gear_gap=(P["gear_x"][1]-P["gear_x"][0])-gear_pitch
motor_top=P["motor_z"]+P["motor_D"]/2
assert wheel_gap>=0, "Adjacent wheels overlap"
# Conservative wheel bounding rectangle in YZ, DN150, including full rim width.
wheel_outer_y=43+P["wheel_W"]
wheel_z_extent=max(abs(P["gear_z"]-P["wheel_D"]/2),abs(P["gear_z"]+P["wheel_D"]/2))
wheel_radial_envelope=math.hypot(wheel_outer_y,wheel_z_extent)
body_radial_envelope=math.hypot(P["body_W"]/2,P["body_H"]/2)
assert wheel_radial_envelope<=75, "Wheel violates DN150 circular envelope"
assert body_radial_envelope<=75, "Body violates DN150 circular envelope"
assert abs(gear_gap)<1e-8, "Z50 pitch mismatch"
assert motor_top <= P["body_H"]/2-P["wall"], "Motor above inner roof"
motor_to_spur_y_clearance = P["gear_y"]-P["gear_thick"]/2-(P["motor_y"]+P["motor_D"]/2)
motor_pair_y_clearance = 2*P["motor_y"]-P["motor_D"]
assert motor_to_spur_y_clearance >= 2, "Motor intersects Z50 spur envelope"
assert motor_pair_y_clearance >= 2, "Traction motors collide across centerline"
# Integrated static clearance gates; conservative envelopes, not 3D Boolean validation.
wheel_body_side_gap = 43 - P["body_W"]/2
gear_inner_wall_gap = P["body_W"]/2 - P["wall"] - (P["gear_y"] + P["gear_thick"]/2)
gear_bottom_gap = P["gear_z"] - P["gear_m"]*50/2 - (-P["body_H"]/2+P["wall"])
assert wheel_body_side_gap >= 1, "Wheel touches outer shell"
assert gear_inner_wall_gap >= 1, "Z50 proxy touches inner wall"
assert gear_bottom_gap >= 1, "Z50 proxy cuts bottom wall"
# Lid perimeter: 4 mm nominal flange outside 170x60 opening; gasket lands on top face.
assert (178-170)/2 >= 4 and (68-60)/2 >= 4, "Lid flange below design target"
assert 68 <= P["body_W"] and 64 <= P["body_W"], "Lid/gasket overhang body"
assert 35 == P["body_H"]/2, "Gasket does not sit on top of shell"
print("PASS nominal static clearances wheel/body",wheel_body_side_gap,"gear/inner-wall",gear_inner_wall_gap,"gear/bottom",gear_bottom_gap,"mm")
print("PASS motor/spur Y clearance", motor_to_spur_y_clearance,
      "mm; left/right motor clearance", motor_pair_y_clearance, "mm")
bearing_wheel_axial_clearance=43-(34+7)
assert bearing_wheel_axial_clearance>=2, "Bearing-to-wheel axial clearance below target"
assert P["motor_D"]==22, "Motor CAD diameter mismatch"
print("PASS design envelope: motor Ø",P["motor_D"],"bearing-to-wheel axial gap",bearing_wheel_axial_clearance,"mm")
assert 80-(35+P["motor_L"])>=3, "Motor rear-end intersects bevel proxy X envelope"\nprint("PASS rear motor/bevel X envelope gap",80-(35+P["motor_L"]),"mm; assumed motor L",P["motor_L"],"mm")\nprint("NOT_RUN bearing bore-to-seat fits, bevel-to-motor actual teeth, lid seal, complete 3D booleans")
assert len([o for o in parts if o.Name.startswith("Wheel_L_") or o.Name.startswith("Wheel_R_")])==6
print("PASS wheel clearance",wheel_gap,"mm; Z50 pitch",gear_pitch,"mm; motor top",motor_top,"mm; DN150 radial wheel",wheel_radial_envelope,"mm; body",body_radial_envelope,"mm")
print("NOT_RUN bevel contact, real teeth, bearing fits, pressure seals, volumetric interference")
D.recompute()
D.saveAs(os.path.join(ROOT,"PX1_Integrated_6x6_M1.FCStd"))
Part.export(parts,os.path.join(ROOT,"PX1_Integrated_6x6_M1.step"))
print("NOT_RUN STEP reopen / Boolean checks; PHYSICAL_CHECK bearing seating, shaft seals, pressure")
print("DESIGN PROXY ONLY: generated FCStd/STEP; check interference, gear mesh, pressure seals before manufacturing")
