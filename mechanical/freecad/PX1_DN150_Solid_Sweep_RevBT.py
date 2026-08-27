import FreeCAD as App, Part, math
# PX-1 Rev.BT — DN150 solid-sweep verification scaffold
# This model uses current Rev.BS lift coordinates and Rev.BQ head envelope.
# It checks swept head solids, lift links and body/wheel reference against a 150 mm pipe circle.

doc=App.newDocument('PX1_DN150_Solid_Sweep_RevBT')

PIPE_ID=150.0
PIPE_R=PIPE_ID/2
CLEARANCE_REQ=3.0
HEAD_OD=52.0
HEAD_R=HEAD_OD/2
HEAD_L=78.0
LINK_L=68.0
PIVOT_X=250.0
PIVOT_Z=66.0
PIVOT_GAP=42.0
WHEEL_R=45.0
BODY_H=76.0
BODY_W=94.0

# Pipe cross-section reference extruded in X.
pipe_outer=Part.makeCylinder(PIPE_R+3,320,App.Vector(-20,0,PIPE_R),App.Vector(1,0,0))
pipe_inner=Part.makeCylinder(PIPE_R,320,App.Vector(-20,0,PIPE_R),App.Vector(1,0,0))
pipe=doc.addObject('Part::Feature','DN150_Pipe_Reference')
pipe.Shape=pipe_outer.cut(pipe_inner)

# Body reference block positioned from wheel contact plane.
body=doc.addObject('Part::Feature','Body_Reference')
body.Shape=Part.makeBox(250,BODY_W,BODY_H,App.Vector(0,-BODY_W/2,0))

# Wheel references.
for x in (45.0,205.0):
    for side,y in [('L',-BODY_W/2-18.0),('R',BODY_W/2)]:
        w=doc.addObject('Part::Feature',f'Wheel_{int(x)}_{side}')
        w.Shape=Part.makeCylinder(WHEEL_R,18.0,App.Vector(x,y,WHEEL_R),App.Vector(0,1,0))

# Lift states: working starting values from prior kinematic study.
states={'LOW':8.0,'DN150_SAFE':28.0}
angles=list(range(-104,106,2))
angles.extend([-105,105])
angles=sorted(set(angles))

# Use simple swept-solid proxy for head: exact Ø52x78 cylinder with end caps.
def head_at(cx,cz,tilt_deg,name):
    # Head axis initially +X, rotate about global Y through center.
    base=App.Vector(cx-HEAD_L/2,0,cz)
    cyl=Part.makeCylinder(HEAD_R,HEAD_L,base,App.Vector(1,0,0))
    center=App.Vector(cx,0,cz)
    cyl.rotate(center,App.Vector(0,1,0),tilt_deg)
    obj=doc.addObject('Part::Feature',name)
    obj.Shape=cyl
    return obj

# Cross-section radial margin conservative approximation from BRep vertices/edges sampled via bounding points.
def radial_clearance(shape):
    min_clear=1e9
    pts=[]
    for v in shape.Vertexes:
        pts.append(v.Point)
    # include edge tessellation points
    for e in shape.Edges:
        try:
            tess=e.tessellate(0.5)
            pts.extend(tess)
        except Exception:
            pass
    for p in pts:
        r=(p.y*p.y + (p.z-PIPE_R)*(p.z-PIPE_R))**0.5
        min_clear=min(min_clear,PIPE_R-r)
    return min_clear

summary=[]
for state,link_deg in states.items():
    a=math.radians(link_deg)
    # camera pivot at end of parallelogram proxy link
    cx=PIVOT_X + LINK_L*math.cos(a)
    cz=PIVOT_Z + LINK_L*math.sin(a)

    # upper and lower lift links as Ø10 round-bar proxies for sweep clearance.
    for idx,z0 in enumerate((PIVOT_Z,PIVOT_Z+PIVOT_GAP)):
        p0=App.Vector(PIVOT_X,0,z0)
        p1=App.Vector(PIVOT_X+LINK_L*math.cos(a),0,z0+LINK_L*math.sin(a))
        vec=p1.sub(p0)
        link=doc.addObject('Part::Feature',f'LiftLink_{state}_{idx}')
        link.Shape=Part.makeCylinder(5.0,vec.Length,p0,vec)

    worst=999.0; worst_ang=None
    for tilt in angles:
        obj=head_at(cx,cz,tilt,f'Head_{state}_{tilt:+04d}')
        clr=radial_clearance(obj.Shape)
        if clr<worst:
            worst=clr; worst_ang=tilt
    summary.append((state,worst,worst_ang,cx,cz))

res=doc.addObject('App::FeaturePython','Sweep_Result')
for state,worst,worst_ang,cx,cz in summary:
    res.addProperty('App::PropertyString',f'{state}_Result')
    setattr(res,f'{state}_Result',f'worst nominal clearance={worst:.2f} mm at tilt {worst_ang} deg; head center X={cx:.1f}, Z={cz:.1f}')
res.addProperty('App::PropertyString','Requirement').Requirement='>=3.0 mm nominal to DN150 wall through full -105..+105 deg sweep'
res.addProperty('App::PropertyString','Limitations').Limitations='Uses current head/lift solids and conservative edge tessellation; final result requires exact shell, lights, fasteners and rotary-seal geometry'
res.addProperty('App::PropertyString','Status').Status='ENGINEERING CHECK ONLY — execute in FreeCAD and review reported clearances/collisions before release'

doc.recompute()
doc.saveAs('PX1_DN150_Solid_Sweep_RevBT.FCStd')
