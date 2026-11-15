#!/usr/bin/env python3
"""PX1 A10 Z16/Z40 standard external spur mesh, analytical geometry only.
No tooth solid, shaft keyway, backlash or physical load validation claimed.
"""
import json, math, pathlib, sys
P = dict(module_mm=1.5, pinion_teeth=16, wheel_teeth=40, pressure_angle_deg=20.0,
         addendum_coefficient=1.0, dedendum_coefficient=1.25,
         center_distance_design_mm=42.0, face_width_assumed_mm=8.0)
def calculate(p=P):
    m=p["module_mm"]; z1=p["pinion_teeth"]; z2=p["wheel_teeth"]
    alpha=math.radians(p["pressure_angle_deg"])
    rp1=m*z1/2; rp2=m*z2/2
    a=m*(z1+z2)/2
    ra1=rp1+m*p["addendum_coefficient"]; ra2=rp2+m*p["addendum_coefficient"]
    rf1=rp1-m*p["dedendum_coefficient"]; rf2=rp2-m*p["dedendum_coefficient"]
    rb1=rp1*math.cos(alpha); rb2=rp2*math.cos(alpha)
    # Standard full-depth involute transverse contact ratio, no profile shift.
    path=math.sqrt(ra1**2-rb1**2)+math.sqrt(ra2**2-rb2**2)-a*math.sin(alpha)
    base_pitch=math.pi*m*math.cos(alpha)
    eps=path/base_pitch
    clearance=(1.25-1.0)*m
    return dict(center_distance_mm=a, pinion_pitch_diameter_mm=2*rp1,
                wheel_pitch_diameter_mm=2*rp2, pinion_tip_diameter_mm=2*ra1,
                wheel_tip_diameter_mm=2*ra2, pinion_root_diameter_mm=2*rf1,
                wheel_root_diameter_mm=2*rf2, contact_ratio_nominal=eps,
                theoretical_radial_clearance_mm=clearance,
                reduction_ratio=z2/z1, output_speed_fraction=z1/z2,
                design_center_error_mm=p["center_distance_design_mm"]-a)
def validate(p=P):
    r=calculate(p)
    assert p["pinion_teeth"]>=12 and p["wheel_teeth"]>=12
    assert r["pinion_root_diameter_mm"]>0
    assert abs(r["design_center_error_mm"])<1e-9
    assert r["contact_ratio_nominal"]>1.0
    assert abs(r["center_distance_mm"]-42)<1e-9
    assert abs(r["reduction_ratio"]-2.5)<1e-9
    return r
def svg(p=P):
    r=validate(p); s=7; x1=160; x2=x1+r["center_distance_mm"]*s; y=260
    def circle(x,rad,color,dash=""):
        return f'<circle cx="{x:.3f}" cy="{y}" r="{rad*s:.3f}" fill="none" stroke="{color}" stroke-width="1.7" {dash}/>'
    out=['<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 700 540">',
         '<rect width="700" height="540" fill="#fff"/>',
         '<text x="24" y="35" font-family="sans-serif" font-size="19">PX1 A10 | Z16 / Z40 | m1.5 | 20 deg</text>',
         '<text x="24" y="59" font-family="sans-serif" font-size="12">Analytical pitch, tip and root circles; teeth and housings NOT modeled</text>']
    for x,z in [(x1,p["pinion_teeth"]),(x2,p["wheel_teeth"])]:
        rp=p["module_mm"]*z/2
        out.extend([circle(x,rp,"#1b70ae",'stroke-dasharray="6 4"'),
                    circle(x,rp+p["module_mm"],"#dc6036"),
                    circle(x,rp-1.25*p["module_mm"],"#64748b"),
                    f'<circle cx="{x}" cy="{y}" r="3" fill="#222"/>',
                    f'<text x="{x-20}" y="{y+20}" font-family="sans-serif" font-size="14">Z{z}</text>'])
    out.extend([f'<line x1="{x1}" y1="95" x2="{x2}" y2="95" stroke="#333"/>',
                f'<line x1="{x1}" y1="87" x2="{x1}" y2="103" stroke="#333"/>',
                f'<line x1="{x2}" y1="87" x2="{x2}" y2="103" stroke="#333"/>',
                f'<text x="275" y="85" font-family="sans-serif" font-size="15">a = 42.00 mm</text>',
                '<text x="24" y="482" font-family="sans-serif" font-size="13">Blue dashed: pitch | Orange: tip | Grey: root</text>',
                f'<text x="24" y="505" font-family="sans-serif" font-size="13">Nominal contact ratio = {r["contact_ratio_nominal"]:.3f}; reduction 2.50:1; assumed face width 8 mm</text>',
                '<text x="24" y="525" font-family="sans-serif" font-size="12">No tooth contact, backlash, torque, bearing or collision test performed</text>','</svg>'])
    return "\n".join(out)+"\n"
if __name__=="__main__":
    result=validate()
    dest=pathlib.Path(sys.argv[1]) if len(sys.argv)>1 else pathlib.Path(".")
    dest.mkdir(parents=True,exist_ok=True)
    (dest/"px1_a10_mesh_preview.svg").write_text(svg(),encoding="utf-8")
    (dest/"px1_a10_mesh_metrics.json").write_text(json.dumps({"assumptions":P,"derived":result},indent=2)+"\n",encoding="utf-8")
    print("PASS analytical mesh:",json.dumps(result))
