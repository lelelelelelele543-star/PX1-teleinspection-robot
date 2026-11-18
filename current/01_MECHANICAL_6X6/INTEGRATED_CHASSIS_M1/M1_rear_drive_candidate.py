"""PX1 M1: integrated rear drivetrain layout alternative, pure Python 3.
All values DESIGN ASSUMPTIONS, not production gear geometry.
Produces SVG and JSON. Tests exact interval clearances, not tooth contact.
Run: python M1_rear_drive_candidate.py
"""
import json
from pathlib import Path

OUT=Path(__file__).parent
# Rear axle X=110. Both sides are symmetric. Y values are magnitudes.
# Candidate: bevel Z40 inboard of spur Z50, and bearing outboard.
# Motor must NOT occupy rear gear X envelope. Shorter motor is hypothetical.
P=dict(axle_x=110., spur_y0=27., spur_y1=33.,
       bevel_y0=19., bevel_y1=27., bearing_y0=34., bearing_y1=41.,
       wheel_y0=43., wheel_y1=61., body_halfwidth=39.,
       motor_x0=35., motor_x1=77., motor_y0=3., motor_y1=25.,
       bevel_x0=80., bevel_x1=140., wheel_r=39., tube_r=75.)
def overlap(a,b,c,d): return max(0.,min(b,d)-max(a,c))
checks={}
checks["spur_bevel_axial_gap_mm"]=P["spur_y0"]-P["bevel_y1"]
checks["spur_bearing_axial_gap_mm"]=P["bearing_y0"]-P["spur_y1"]
checks["bearing_wheel_axial_gap_mm"]=P["wheel_y0"]-P["bearing_y1"]
checks["wheel_body_axial_gap_mm"]=P["wheel_y0"]-P["body_halfwidth"]
checks["motor_bevel_x_gap_mm"]=P["bevel_x0"]-P["motor_x1"]
checks["wheel_dn150_radial_margin_mm"]=P["tube_r"]-(P["wheel_y1"]**2+P["wheel_r"]**2)**0.5
# Conservative motor cylinder versus bevel envelope: x intervals disjoint.
checks["motor_bevel_proxy_overlap_x_mm"]=overlap(P["motor_x0"],P["motor_x1"],P["bevel_x0"],P["bevel_x1"])
passed=all(v>=0 for k,v in checks.items() if k!="motor_bevel_proxy_overlap_x_mm") and checks["motor_bevel_proxy_overlap_x_mm"]==0
# Bevel and spur touch in Y but DO NOT share solid volume. Gear mesh and
# bearing seat still need modeling. Motor shaft must be lengthened from X77
# to Z16 at X101, unsupported without deflection calculation.
report=dict(status="PASS_PROXY_ONLY" if passed else "FAIL",assumptions=P,checks=checks,
            blockers=["42 mm motor envelope requires real supplier verification",
                      "longer motor shaft/coupling and support bearings not designed",
                      "Z16-Z40 bevel mesh axes and tooth contact NOT_RUN",
                      "bevel Z40 and spur Z50 axial coupling/hub NOT_RUN",
                      "pressure shaft seals PHYSICAL_CHECK",
                      "FreeCAD solid collisions and STEP NOT_RUN"])
(OUT/"M1_rear_drive_candidate.json").write_text(json.dumps(report,indent=2),encoding="utf-8")
# Parametric YZ section; axis Y horizontal, Z vertical. Both sides.
scale=4.; origin=400.
def rect(y0,y1,z0,z1,color,label):
    x=origin+scale*y0; yy=240-scale*z1
    return f'<rect x="{x:.1f}" y="{yy:.1f}" width="{scale*(y1-y0):.1f}" height="{scale*(z1-z0):.1f}" fill="{color}" fill-opacity=".45" stroke="{color}" stroke-width="1.5"/><text x="{x+3:.1f}" y="{yy+16:.1f}" font-size="12">{label}</text>'
svg=['<svg xmlns="http://www.w3.org/2000/svg" width="920" height="490" viewBox="0 0 920 490">',
'<rect width="920" height="490" fill="#f8fafc"/>',
'<text x="28" y="35" font-family="sans-serif" font-size="21" font-weight="bold">PX1 M1 — rear axle YZ candidate (design assumptions)</text>',
'<text x="28" y="57" font-family="sans-serif" font-size="13">NOT a FreeCAD render; rectangles are radial/axial envelopes, not actual teeth or seals</text>',
'<g font-family="sans-serif">']
for s in [-1,1]:
    def rr(a,b,z0,z1,color,label):
        return rect(s*b,s*a,z0,z1,color,label) if s<0 else rect(a,b,z0,z1,color,label)
    svg.extend([rr(19,27,-30,30,"#db7c2b","Z40 bevel"),
                rr(27,33,-27.5,27.5,"#e0b342","Z50 spur"),
                rr(34,41,-11,11,"#319b7c","bearing"),
                rr(43,61,-39,39,"#4b648c","wheel")])
svg.append('<line x1="100" y1="240" x2="700" y2="240" stroke="#111827" stroke-dasharray="6 4"/>')
svg.append('<text x="28" y="425" font-size="15">Axial: Z40 [19,27] | Z50 [27,33] | bearing [34,41] | wheel [43,61] mm (mirrored)</text>')
svg.append('<text x="28" y="450" font-size="13">Motor X 35..77; bevel X 80..140: 3 mm proxy gap. Real motor / coupling unverified.</text>')
svg.append('</g></svg>')
(OUT/"M1_rear_drive_candidate.svg").write_text("".join(svg),encoding="utf-8")
print(json.dumps(report,indent=2))
if not passed: raise SystemExit(1)
