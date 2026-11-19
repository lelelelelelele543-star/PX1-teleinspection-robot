"""PX1 integrated 6x6 chassis, design-target only. Run in FreeCAD Python / FreeCADCmd.
Generated parts are simplified solids. Gear teeth, bevel teeth, O-ring grooves and dynamic seals are NOT validated.
Axes: X along crawler, Y lateral, Z up. Units mm.
"""
import FreeCAD as App, Part, math, os
from FreeCAD import Vector as V
ROOT=os.path.dirname(os.path.abspath(__file__))
D=App.newDocument("PX1_Integrated_6x6_M1")
P=dict(body_L=307.,body_W=78.,body_H=70.,wall=5.,wheel_D=78.,wheel_W=14.,
       stations=(-100.,0.,100.),gear_x=(-100.,-50.,0.,50.,100.),
       gear_m=1.0,gear_z=0.,gear_y=30.,gear_thick=6.,axle_D=10.,
       motor_D=22.,motor_L=42.,motor_z=18.,motor_y=14.,motor_x=-30.,
       pressure_bar_min=0.4,pressure_bar_max=0.7,
       lid_gasket_nominal=1.0,lid_gasket_compression=0.3)
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
# Only six wheel through-wall shaft passages; four idlers remain internal.
for xx in P["stations"]:
    for sign in (-1,1):
        outer=outer.cut(cyl(5.5,12,(xx,sign*34,0),(0,sign,0)))
        # Bearing 10x22x7 occupies Y=34..41; cut full 5 mm shell wall (34..39).
        # Previous Y=35..38 pocket left 2 mm of rigid shell/bearing interference.
        outer=outer.cut(cyl(11,5,(xx,sign*34,0),(0,sign,0)))
# Eight blind M3 pilot holes on the existing solid lid land, never through the pressure boundary.
# These are ESTIMATED locations; no thread, torque, gasket stress or pressure proof is implied.
lid_bolts=[(x,y) for x in (-90.,0.,90.) for y in (-34.5,34.5)]
lid_bolts += [(-90.,0.),(90.,0.)]
assert len(lid_bolts)==8 and len(set(lid_bolts))==8
for bx,by in lid_bolts:
    outer=outer.cut(cyl(1.25,4,(bx,by,31),(0,0,1)))
add("Body_hollow_ASSUMED",outer.cut(inner).cut(lid_opening),(0.64,0.69,0.73))
# 190 x 78 lid provides a nominal 10 mm x-land and 9 mm y-land around aperture.
# Existing gasket stays 174 x 64; holes are outside its nominal footprint.
lid_bottom=35+P["lid_gasket_nominal"]-P["lid_gasket_compression"]
lid_shape=Part.makeBox(190,78,4,V(-95,-39,lid_bottom))
for bx,by in lid_bolts:
    lid_shape=lid_shape.cut(cyl(1.7,4,(bx,by,lid_bottom),(0,0,1)))
add("Lid_ASSUMED",lid_shape,(0.18,0.4,0.62))
for i,(bx,by) in enumerate(lid_bolts,1):
    # Screw is a proxy only; no thread engagement, washer or preload model.
    shank=cyl(1.5,7.7,(bx,by,32),(0,0,1))
    head=cyl(2.8,2.5,(bx,by,lid_bottom+4),(0,0,1))
    add("Lid_M3_fastener_PROXY_"+str(i),shank.fuse(head),(0.65,0.65,0.68))
gasket=Part.makeBox(174,64,1,V(-87,-32,35)).cut(Part.makeBox(166,56,1,V(-83,-28,35)))
add("Lid_gasket_PROXY",gasket,(0.18,0.64,0.35))
for side,s in (("L",-1),("R",1)):
    # Relocated motors: X=-30..12, raised Z=18. Assumed envelopes, not mounting design.
    add("Motor_"+side+"_ENVELOPE",cyl(P["motor_D"]/2,P["motor_L"],(P["motor_x"],s*14,P["motor_z"]),(1,0,0)),(0.22,0.32,0.4))
    add("Motor_shaft_"+side,cyl(4,93,(P["motor_x"]+P["motor_L"],s*14,P["motor_z"]),(1,0,0)),(0.8,0.7,0.3))
    # Five Z50 stations per side. m=1.0 design assumption -> 50 mm pitch diameter and 50 mm centers.
    for j,x in enumerate(P["gear_x"]):
        gy=s*P["gear_y"]
        # Pitch solids are intentionally NOT teeth or manufactured gears.
        add("Z50_pitch_PROXY_"+side+"_"+str(j+1),cyl(P["gear_m"]*50/2,6,(x,gy-3,P["gear_z"]),(0,1,0)),(0.75,0.42,0.19))
        if j%2==0:
            add("Wheel_axle_"+side+"_"+str(j//2+1),cyl(5,30,(x,s*29,P["gear_z"]),(0,s,0)),(0.77,0.78,0.79))
            # Bearing 10x22x7: geometry proxy, not manufacturer verification.
            bp=(x,s*34,P["gear_z"])
            add("Bearing_PROXY_"+side+"_"+str(j//2+1),
                cyl(11,7,bp,(0,s,0)).cut(cyl(5,7,bp,(0,s,0))),(0.92,0.72,0.28))
            # External shaft seal cartridge between bearing outer face (Y=41) and wheel inner face (Y=46).
            # Annular solids are packaging proxies only; seal type/pressure rating UNVERIFIED.
            sp=(x,s*41,P["gear_z"])
            add("Shaft_seal_CARTRIDGE_PROXY_"+side+"_"+str(j//2+1),
                cyl(11.5,4,sp,(0,s,0)).cut(cyl(5,4,sp,(0,s,0))),(0.18,0.56,0.48))
            add("Wheel_"+side+"_"+str(j//2+1),cyl(P['wheel_D']/2,P["wheel_W"],(x,s*46,P["gear_z"]),(0,s,0)),(0.11,0.14,0.18))
        else:
            # Idler support shares the 10x22x7 nominal envelope with wheel bearings.
            # Idlers use blind internal carriers, not wall penetrations.
            # Axle and bearing are simplified envelopes, not verified fits or load ratings.
            # Blind internal idler: NO through-wall hole. Carrier attachment is NOT_RUN.
            add("Idler_stub_"+side+"_"+str(j),cyl(5,15,(x,s*19,P["gear_z"]),(0,s,0)),(0.7,0.73,0.76))
            ip=(x,s*19,P["gear_z"])
            add("Idler_bearing_PROXY_"+side+"_"+str(j),
                cyl(11,7,ip,(0,s,0)).cut(cyl(5,7,ip,(0,s,0))),(0.88,0.68,0.25))
            cp=(x,s*18,P["gear_z"])
            add("Idler_carrier_PROXY_"+side+"_"+str(j),
                cyl(12,9,cp,(0,s,0)).cut(cyl(11,9,cp,(0,s,0))),(0.44,0.54,0.62))
    # Rear Z40 bevel pitch proxy is coaxial with rear Z50 at X=100 (was X=110: disconnected torque path).
    # These are still pitch cylinders, NOT conjugate bevel teeth or a validated keyed hub.
    assert P["gear_x"][-1] == 100., "Rear gear coordinate changed"
    # Bevel input at rear X=100: proxy solids only, orientation requires contact validation.
    add("Bevel_Z16_PROXY_"+side,cyl(12,8,(101,s*14,P["motor_z"]),(1,0,0)),(0.85,0.5,0.18))
    add("Bevel_Z40_PROXY_"+side,cyl(30,8,(100,s*19,P["gear_z"]),(0,s,0)),(0.85,0.5,0.18))
    # Drive shaft X=12..105 enters Z16 X=101..109 by 4 mm; interference is intentional for a nominal hub.
    # This is NOT a torque-rated key, press fit, or validated bevel mesh.
    assert P["motor_x"]+P["motor_L"]+93 >= 105 and P["motor_x"]+P["motor_L"]+93-101 >= 4
    print("PASS nominal motor-shaft/Z16 overlap 4 mm; NOT_RUN torque joint and actual fits",side)
# Explicit rear coaxiality gate: this checks the modeled bevel Z40 axis, not tooth engagement.
for side_label in ("L","R"):
    z40=next(o for o in parts if o.Name=="Bevel_Z40_PROXY_"+side_label)
    rear=next(o for o in parts if o.Name=="Z50_pitch_PROXY_"+side_label+"_5")
    assert abs(z40.Shape.BoundBox.XCenter-rear.Shape.BoundBox.XCenter)<1e-6, "Rear bevel/spur axes offset in X"
print("PASS rear Z40/Z50 pitch-solid coaxiality in X; NOT_RUN hub joint and bevel tooth contact")
# Analytical envelope checks; not a substitute for FreeCAD Boolean collision tests.
wheel_gap=(P["stations"][1]-P["stations"][0])-P["wheel_D"]
gear_pitch=P["gear_m"]*50
gear_gap=(P["gear_x"][1]-P["gear_x"][0])-gear_pitch
assert P["stations"] == (P["gear_x"][0],P["gear_x"][2],P["gear_x"][4]), "Wheel stations disagree with gear chain"
assert P["gear_x"] == tuple(-100.+50.*i for i in range(5)), "AGENTS.md X50..X250 local-coordinate mapping failed"
motor_top=P["motor_z"]+P["motor_D"]/2
assert wheel_gap>=0, "Adjacent wheels overlap"
# Conservative wheel bounding rectangle in YZ, DN150, including full rim width.
wheel_outer_y=46+P["wheel_W"]
wheel_z_extent=max(abs(P["gear_z"]-P["wheel_D"]/2),abs(P["gear_z"]+P["wheel_D"]/2))
wheel_radial_envelope=math.hypot(wheel_outer_y,wheel_z_extent)
# Reserve a real design clearance instead of accepting the previous 0.047 mm nominal margin.
minimum_pipe_clearance=2.0
body_radial_envelope=math.hypot(P["body_W"]/2,P["body_H"]/2)
assert wheel_radial_envelope<=75-minimum_pipe_clearance, "Wheel DN150 clearance below 2 mm design target"
assert body_radial_envelope<=75, "Body violates DN150 circular envelope"
assert abs(gear_gap)<1e-8, "Z50 pitch mismatch"
assert motor_top <= P["body_H"]/2-P["wall"], "Motor above inner roof"
motor_to_spur_y_clearance = P["gear_y"]-P["gear_thick"]/2-(P["motor_y"]+P["motor_D"]/2)
motor_pair_y_clearance = 2*P["motor_y"]-P["motor_D"]
assert motor_to_spur_y_clearance >= 2, "Motor intersects Z50 spur envelope"
assert motor_pair_y_clearance >= 2, "Traction motors collide across centerline"
# Motor/idler and longitudinal drive-shaft/idler clearance, conservative radial envelope.
# Idler bearing: Y=19..26, Z radius 11; shaft radius 4 at Y=14,Z=18.
# Shaft overlaps idler stations X=+-50, so cross-sectional separation is required.
idler_to_shaft=math.hypot(P["motor_y"]-19.,P["motor_z"]-P["gear_z"])
assert idler_to_shaft >= 11.+4.+1., "Drive shaft intersects idler bearing envelope"
# Motor X interval must not reach the X=+-50 idler bearing radius (11 mm).
assert P["motor_x"] >= -50.+11.+1. and P["motor_x"]+P["motor_L"] <= 50.-11.-1., "Motor X envelope intersects idler station"
print("PASS motor/idler axial separation and drive-shaft/idler radial clearance",round(idler_to_shaft-15.,3),"mm (assumed envelopes)")
# Integrated static clearance gates; conservative envelopes, not 3D Boolean validation.
wheel_body_side_gap = 46 - P["body_W"]/2
gear_inner_wall_gap = P["body_W"]/2 - P["wall"] - (P["gear_y"] + P["gear_thick"]/2)
gear_bottom_gap = P["gear_z"] - P["gear_m"]*50/2 - (-P["body_H"]/2+P["wall"])
assert wheel_body_side_gap >= 1, "Wheel touches outer shell"
assert gear_inner_wall_gap >= 1, "Z50 proxy touches inner wall"
assert gear_bottom_gap >= 1, "Z50 proxy cuts bottom wall"
# Lid perimeter: 4 mm nominal flange outside 170x60 opening; gasket lands on top face.
assert (190-170)/2 >= 9 and (78-60)/2 >= 9, "Lid flange below design target"
assert 78 <= P["body_W"] and 64 <= P["body_W"], "Lid/gasket overhang body"
assert 35 == P["body_H"]/2, "Gasket does not sit on top of shell"
# Design-target gasket compression by lid placement; no fasteners or material stiffness yet.
lid_z=35+P["lid_gasket_nominal"]-P["lid_gasket_compression"]
assert 0 < P["lid_gasket_compression"] < P["lid_gasket_nominal"]
assert abs(lid_z-35.7)<1e-8
print("PASS nominal lid/gasket overlap",P["lid_gasket_compression"],"mm; 8 blind M3 pilot holes, 8 fastener proxies; NOT_RUN clamp load, gasket extrusion and threads")
print("PASS nominal static clearances wheel/body",wheel_body_side_gap,"gear/inner-wall",gear_inner_wall_gap,"gear/bottom",gear_bottom_gap,"mm")
print("PASS motor/spur Y clearance", motor_to_spur_y_clearance,
      "mm; left/right motor clearance", motor_pair_y_clearance, "mm")
# Bearing seat coverage: full shell thickness, not merely a shallow counterbore.
bearing_start=34.0
bearing_length=7.0
shell_outer=P["body_W"]/2
shell_inner=shell_outer-P["wall"]
seat_start=34.0
seat_depth=5.0
assert seat_start <= shell_inner and seat_start+seat_depth >= shell_outer, "Bearing shell interference: incomplete counterbore"
assert bearing_start <= shell_inner and bearing_start+bearing_length >= shell_outer, "Bearing does not span wall"
print("PASS nominal bearing counterbore covers full sidewall; 2 mm bearing protrusion is intentional")
bearing_wheel_axial_clearance=46-(34+7)
assert bearing_wheel_axial_clearance>=5, "Bearing-to-wheel axial clearance below seal cartridge target"
assert 4+1 <= bearing_wheel_axial_clearance, "Seal cartridge + axial service clearance does not fit"
assert math.hypot(46+P["wheel_W"],P["wheel_D"]/2) <= 75-minimum_pipe_clearance, "External seal packaging leaves under 2 mm DN150 radial margin"
assert P["motor_D"]==22, "Motor CAD diameter mismatch"
print("PASS DN150 nominal radial clearance",round(75-wheel_radial_envelope,3),"mm; wheel width",P["wheel_W"],"mm; ASSUMED, verify traction/contact")
print("PASS design envelope: motor Ø",P["motor_D"],"bearing-to-wheel axial gap",bearing_wheel_axial_clearance,"mm")
# Axial motor-to-bevel spacing; long drive shaft is an unverified single-piece proxy.
assert 100-(P["motor_x"]+P["motor_L"])>=80, "Relocated motor has insufficient drive run"
print("PASS motor relocated X",P["motor_x"],"to",P["motor_x"]+P["motor_L"],"mm; rear run",100-(P["motor_x"]+P["motor_L"]),"mm")
print("PASS nominal shaft-seal axial packaging: 4 mm cartridge + 1 mm wheel clearance; PHYSICAL_CHECK pressure rating and shaft runout")
print("NOT_RUN bearing bore-to-seat fits, bevel-to-motor actual teeth, lid seal, complete 3D booleans")
# Integrated actual-solid geometry assertions (not merely parameters).
for side_label in ("L","R"):
    wheels=[o for o in parts if o.Name.startswith("Wheel_"+side_label+"_")]
    assert len(wheels)==3
    for wheel in wheels:
        assert abs(wheel.Shape.BoundBox.YLength-P["wheel_W"])<1e-6, "Wheel CAD width differs from wheel_W"
        assert abs(wheel.Shape.BoundBox.ZLength-P["wheel_D"])<1e-6, "Wheel CAD diameter differs from wheel_D"
print("PASS actual FreeCAD wheel solid widths and diameters")
# Wheel axle tip must remain recessed relative to the wheel outside face on BOTH sides.
# Previously 29+36=65 exceeded the wheel outer face 46+14=60 by 5 mm.
axle_tip=29+30
wheel_outer_face=46+P["wheel_W"]
assert axle_tip<=wheel_outer_face-1, "Wheel axle protrudes beyond wheel face"
for side_label in ("L","R"):
    axles=[o for o in parts if o.Name.startswith("Wheel_axle_"+side_label+"_")]
    assert len(axles)==3
    for axle in axles:
        assert abs(axle.Shape.BoundBox.YLength-30)<1e-6, "Actual axle length mismatch"
print("PASS six axle tips recessed",wheel_outer_face-axle_tip,"mm; ASSUMED wheel fastening still NOT_RUN")

# Verify integrated support inventory, nominal idler bore coverage and shaft support.
assert len([o for o in parts if o.Name.startswith("Idler_bearing_PROXY_")])==4
assert len([o for o in parts if o.Name.startswith("Idler_stub_")])==4
assert set(P["gear_x"])-set(P["stations"])=={-50.,50.}
assert seat_start<=shell_inner and seat_start+seat_depth>=shell_outer
assert len([o for o in parts if o.Name.startswith("Idler_carrier_PROXY_")])==4
print("PASS 6 wheel wall passages and 4 internal idler carrier proxies; mounting NOT_RUN")
print("NOT_RUN actual bearing fits, idler loads and volumetric Boolean collision tests")
assert len([o for o in parts if o.Name.startswith("Wheel_L_") or o.Name.startswith("Wheel_R_")])==6
print("PASS wheel clearance",wheel_gap,"mm; Z50 pitch",gear_pitch,"mm; motor top",motor_top,"mm; DN150 radial wheel",wheel_radial_envelope,"mm; body",body_radial_envelope,"mm")
print("NOT_RUN bevel contact, real teeth, bearing fits, pressure seals, volumetric interference")
# Validate fastener inventory and lid hole placement against aperture and gasket.
assert len([o for o in parts if o.Name.startswith("Lid_M3_fastener_PROXY_")])==8
for bx,by in lid_bolts:
    assert (abs(bx)>=90 or abs(by)>=34.5)
    assert abs(bx)<=95-2.8 and abs(by)<=39-2.8, "M3 head exceeds lid boundary"
    assert abs(bx)>87 or abs(by)>32, "M3 screw intrudes into gasket footprint"
print("PASS 8 lid fastener proxy positions and blind pilot depths; PHYSICAL_CHECK thread engagement and pressure preload")
D.recompute()
D.saveAs(os.path.join(ROOT,"PX1_Integrated_6x6_M1.FCStd"))
Part.export(parts,os.path.join(ROOT,"PX1_Integrated_6x6_M1.step"))
# Export is a proxy assembly only, not validated involute gears or pressure seals.
print("NOT_RUN STEP reopen / Boolean checks; PHYSICAL_CHECK bearing seating, shaft seals, pressure")
print("DESIGN PROXY ONLY: generated FCStd/STEP; check interference, gear mesh, pressure seals before manufacturing")


# M1 integrated STEP round-trip gate. Runs in FreeCADCmd, no GUI required.
# This is a topology/export verification, NOT a pressure or manufacturability certification.
step_path=os.path.join(ROOT,"PX1_Integrated_6x6_M1.step")
if not os.path.isfile(step_path) or os.path.getsize(step_path)<1024:
    raise RuntimeError("FAIL STEP missing/implausibly small")
check_doc=App.newDocument("PX1_M1_STEP_Roundtrip")
try:
    imported=Part.read(step_path)
    if imported.isNull():
        raise RuntimeError("FAIL STEP imported null shape")
    expected=Part.makeCompound([o.Shape for o in parts])
    if expected.isNull() or expected.Volume<=0 or imported.Volume<=0:
        raise RuntimeError("FAIL invalid original/imported assembly volume")
    # STEP compound may reorder solids; compare aggregate envelopes and volume, not topology indices.
    b1,b2=expected.BoundBox,imported.BoundBox
    for axis in ("XLength","YLength","ZLength"):
        if abs(getattr(b1,axis)-getattr(b2,axis))>0.05:
            raise RuntimeError("FAIL STEP envelope "+axis)
    volume_error=abs(expected.Volume-imported.Volume)/expected.Volume
    if volume_error>1e-4:
        raise RuntimeError("FAIL STEP round-trip volume error "+str(volume_error))
    print("PASS STEP round-trip: envelope within 0.05 mm, relative volume error",volume_error)
finally:
    App.closeDocument(check_doc.Name)
print("NOT_RUN true involute mesh, physical shaft-seal pressure, fastener preload and motion collision sweep")
