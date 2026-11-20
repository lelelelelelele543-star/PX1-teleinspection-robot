"""PX1 m1 Z50 parametric involute gear, assumed geometry. FreeCAD solid + pure Python profile.
No root fillet, backlash, bore, key, heat treatment or strength validation.
"""
import math

def profile(z=50, module=1.0, pressure_angle_deg=20.0, samples=8):
    if z < 17 or module <= 0 or samples < 3:
        raise ValueError("invalid gear")
    rp=module*z/2
    rb=rp*math.cos(math.radians(pressure_angle_deg))
    ra=rp+module
    rf=rp-1.25*module
    def inv(r):
        t=math.sqrt(max(0.0,(r/rb)**2-1.0))
        return t-math.atan(t)
    half=math.pi/(2*z)
    pitch_inv=inv(rp)
    pts=[]
    def put(r,a):
        pts.append((r*math.cos(a),r*math.sin(a)))
    for k in range(z):
        c=2*math.pi*k/z
        put(rf,c-half-pitch_inv+inv(rf))
        for i in range(samples+1):
            r=max(rb,rf)+(ra-max(rb,rf))*i/samples
            put(r,c-half-pitch_inv+inv(r))
        a1=c-half-pitch_inv+inv(ra)
        a2=c+half+pitch_inv-inv(ra)
        for j in range(1,5):
            put(ra,a1+(a2-a1)*j/4)
        for i in range(samples,-1,-1):
            r=max(rb,rf)+(ra-max(rb,rf))*i/samples
            put(r,c+half+pitch_inv-inv(r))
        put(rf,c+half+pitch_inv-inv(rf))
        nxt=c+2*math.pi/z-half-pitch_inv+inv(rf)
        a=c+half+pitch_inv-inv(rf)
        for j in range(1,4):
            put(rf,a+(nxt-a)*j/4)
    return pts

def solid(Part,V,z=50,module=1.0,thickness=6.0,center=(0,0,0),phase_deg=0.0):
    xy=profile(z,module)
    a=math.radians(phase_deg)
    xy=[(x*math.cos(a)-y*math.sin(a),x*math.sin(a)+y*math.cos(a)) for x,y in xy]
    wire=Part.makePolygon([V(x,y,0) for x,y in xy]+[V(xy[0][0],xy[0][1],0)])
    shape=Part.Face(wire).extrude(V(0,0,thickness))
    shape.rotate(V(0,0,0),V(1,0,0),90)
    shape.translate(V(center[0],center[1]+thickness/2,center[2]))
    return shape

if __name__=="__main__":
    p=profile()
    rr=[math.hypot(x,y) for x,y in p]
    assert len(p)==1350 and abs(max(rr)-26)<1e-8 and abs(min(rr)-23.75)<1e-8
    try:
        from shapely.geometry import Polygon
        from shapely.affinity import translate,rotate
        g=Polygon(p)
        assert g.is_valid
        adjacent=translate(rotate(g,3.6,origin=(0,0)),xoff=50)
        assert g.intersection(adjacent).area < 1e-6
        print("PASS: 1350 vertices, valid polygon, zero static overlap at 50 mm centers / 3.6 deg phase")
    except ImportError:
        print("SKIPPED: shapely polygon/mesh test")
    print("NOT_RUN: FreeCAD extrusion, full rotation mesh, backlash, stress, root fillets")
