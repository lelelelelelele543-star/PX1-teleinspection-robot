"""PX1 M1 wheel/shaft seal packaging gate; Python 3 standard library only.
DESIGN ASSUMPTIONS, NOT manufacturer dimensions or verified seal selection.
Outputs reproducible SVG and JSON beside this file. Run: python M1_seal_packaging_gate.py
"""
import math, json, pathlib
ROOT=pathlib.Path(__file__).resolve().parent
P=dict(pipe_radius=75.,wheel_radius=39.,wheel_y_inner=43.,wheel_width=18.,
       body_half_width=39.,wall=5.,bearing_y_inner=34.,bearing_width=7.,
       seal_axial_target=4.,seal_clearance_target=1.)
outer_y=P["wheel_y_inner"]+P["wheel_width"]
wheel_corner=math.hypot(outer_y,P["wheel_radius"])
max_outer_y=math.sqrt(P["pipe_radius"]**2-P["wheel_radius"]**2)
axial_gap=P["wheel_y_inner"]-(P["bearing_y_inner"]+P["bearing_width"])
needed=P["seal_axial_target"]+P["seal_clearance_target"]
radial_budget=max_outer_y-outer_y
checks={"wheel_circular_envelope":"PASS" if wheel_corner<=75 else "FAIL",
        "seal_cartridge_axial_fit":"PASS" if axial_gap>=needed else "FAIL",
        "outboard_shift_to_fit":"PASS" if radial_budget>=needed-axial_gap else "FAIL",
        "pressure_rating":"PHYSICAL_CHECK","dynamic_seal_vendor_geometry":"NOT_RUN",
        "bearing_pressure_isolation":"FAIL"}
report={"assumptions_mm":P,"calculated_mm":{"wheel_outer_corner_radius":round(wheel_corner,3),
"max_wheel_outer_y":round(max_outer_y,3),"available_outboard_shift":round(radial_budget,3),
"bearing_to_wheel_gap":axial_gap,"target_seal_package":needed,
"required_outboard_shift":needed-axial_gap},"checks":checks,
"note":"Static envelope only. Shaft bearing is exposed to pressure; do not assume bearing is a dynamic pressure seal.",
"next":"Repackage axle seal inside dry body or redesign bearing cartridge without exceeding DN150; validate actual seal datasheet and FreeCAD booleans."}
assert round(axial_gap,6)==2 and checks["seal_cartridge_axial_fit"]=="FAIL"
assert checks["wheel_circular_envelope"]=="PASS"
(ROOT/"M1_seal_packaging_gate.json").write_text(json.dumps(report,indent=2,ensure_ascii=False)+"\n",encoding="utf-8")
# SVG uses the exact numerical coordinates of this gate, not a CAD render.
scale=5
def X(y):return 170+y*scale
def Z(z):return 270-z*scale
def rect(y1,y2,z1,z2,color,opacity=1):
 return f'<rect x="{X(y1):.1f}" y="{Z(z2):.1f}" width="{(y2-y1)*scale:.1f}" height="{(z2-z1)*scale:.1f}" fill="{color}" opacity="{opacity}"/>'
svg=['<svg xmlns="http://www.w3.org/2000/svg" width="900" height="580" viewBox="0 0 900 580">',
'<rect width="900" height="580" fill="#fff"/>','<text x="28" y="38" font-size="23" font-family="sans-serif">PX1 M1 — seal packaging gate (DESIGN ASSUMPTIONS)</text>',
'<text x="28" y="65" font-size="15" font-family="sans-serif">Right-hand YZ section at wheel station. Units mm. NOT FreeCAD.</text>']
svg.append(f'<circle cx="{X(0)}" cy="{Z(0)}" r="{75*scale}" fill="none" stroke="#4d87bd" stroke-width="2" stroke-dasharray="7 5"/>')
svg.append(rect(34,39,-35,35,"#b9c1ca"))
svg.append(rect(34,41,-11,11,"#e3aa46"))
svg.append(rect(34,41,-5,5,"#f7f7f7"))
svg.append(rect(41,43,-14,14,"#f7d17c",0.65))
svg.append(rect(43,61,-39,39,"#303b49"))
svg.append(rect(29,61,-5,5,"#abb9c6"))
svg.append('<text x="575" y="135" font-size="16" font-family="sans-serif">Wheel: Y 43–61, R39</text>')
svg.append('<text x="575" y="165" font-size="16" font-family="sans-serif">Bearing: Y 34–41, 10×22×7 proxy</text>')
svg.append('<text x="575" y="195" font-size="16" font-family="sans-serif">Free axial gap: 2 mm</text>')
svg.append('<text x="575" y="225" font-size="16" font-family="sans-serif">Seal target: 4 + 1 mm clearance</text>')
svg.append(f'<text x="575" y="255" font-size="16" font-family="sans-serif">Outboard shift budget: {radial_budget:.2f} mm</text>')
svg.append('<text x="575" y="295" font-size="18" fill="#b02b2b" font-family="sans-serif">FAIL: seal does not fit outside bearing</text>')
svg.append('<text x="575" y="325" font-size="16" font-family="sans-serif">No pressure qualification claimed</text>')
svg.append('<text x="28" y="550" font-size="14" font-family="sans-serif">Blue dashed: DN150 envelope. Orange: bearing proxy. Dark: wheel. Grey: body wall and axle.</text>')
svg.append('</svg>')
(ROOT/"M1_seal_packaging_gate.svg").write_text("\n".join(svg),encoding="utf-8")
print(json.dumps(report["checks"],ensure_ascii=False))
