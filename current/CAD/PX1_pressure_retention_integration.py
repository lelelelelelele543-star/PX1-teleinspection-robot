#!/usr/bin/env python3
"""PX1 CURRENT master: integrated cover-pressure/fastener/lift-base load-path screen.
Source of all geometry: PX1_Current_Master.py; uses its actual lobed_seal_face.
Run with installed CadQuery: python current/CAD/PX1_pressure_retention_integration.py
Nominal equilibrium only, NOT FE analysis, preload design, or pressure qualification.
"""
import ast, json, math, sys
from pathlib import Path
import cadquery as cq

HERE=Path(__file__).resolve().parent
MASTER=HERE/"PX1_Current_Master.py"
OUT=HERE/"previews"; OUT.mkdir(exist_ok=True)
source=MASTER.read_text(encoding="utf-8")
tree=ast.parse(source,str(MASTER))
names={t.id:n.value for n in tree.body if isinstance(n,ast.Assign)
       for t in n.targets if isinstance(t,ast.Name)}
def value(name):
    try: return ast.literal_eval(names[name])
    except (KeyError,ValueError,TypeError) as e:
        raise RuntimeError("Cannot read master literal: "+name) from e
keys=("SIDE_SEAL_R SIDE_SEAL_CUSP GEAR_X SIDE_ORING SIDE_COVER_L SIDE_COVER_H "
      "SIDE_COVER_T COVER_SCREW_DX COVER_SCREW_DZ COVER_SCREW_CBORE "
      "SERVICE_PLUG_L SERVICE_OPEN_W SERVICE_PLUG_R SERVICE_OPEN_X0 "
      "SERVICE_PAD_X SERVICE_PAD_HW SERVICE_T COVER_FIX_XY COVER_FIX_L "
      "COVER_FIX_BOSS_R ISO7380_M4 TAP_LEAD LIFT_BASE_L LIFT_BASE_BEHIND_A "
      "LIFT_M4_DRW_PATTERN LIFT_M4_Y_PX1 LIFT_M4_SCREW_L LIFT_M4_CLAMP "
      "LH_REAR_X LH752_BODY_X LH752_C LINK_L").split()
p={k:value(k) for k in keys}
f=next((n for n in tree.body if isinstance(n,ast.FunctionDef) and n.name=="lobed_seal_face"),None)
if not f: raise RuntimeError("Missing master lobed_seal_face")
ns={"cq":cq,"math":math,**p}
exec(compile(ast.Module(body=[f],type_ignores=[]),str(MASTER),"exec"),ns)
wire=ns["lobed_seal_face"](0).wire().val()
area=cq.Face.makeFromWires(wire).Area()
S_L,S_W,S_R=(p[k] for k in ("SERVICE_PLUG_L","SERVICE_OPEN_W","SERVICE_PLUG_R"))
top_area=S_L*S_W-(4-math.pi)*S_R**2 # pressure at rounded-rectangle aperture
top_cx=p["SERVICE_OPEN_X0"]+S_L/2
ax=p["LH_REAR_X"]-p["LH752_BODY_X"][2]+p["LH752_C"][0]+p["LINK_L"]
lift_outer_x=ax-p["LIFT_M4_DRW_PATTERN"][0][0] # M4 into housing
lift_inner_x=ax-p["LIFT_M4_DRW_PATTERN"][1][0] # M4 into top cover
front_x,front_y=p["COVER_FIX_XY"] # M4 into housing
lift_min=ax-(p["LIFT_BASE_L"]-p["LIFT_BASE_BEHIND_A"])
lift_max=ax+p["LIFT_BASE_BEHIND_A"]
front_eng=p["COVER_FIX_L"]-p["SERVICE_T"]
front_edge=front_x-p["SERVICE_PAD_X"][0]-p["ISO7380_M4"][0]
boss_lig=p["SERVICE_OPEN_X0"]-front_x-p["COVER_FIX_BOSS_R"]
# M3x8 is an explicit master screw call (8 mm); ensure source did not change.
if "make_button_screw(150+dx,side*(41-COVER_SCREW_CBORE[1]),45+dz,8,side)" not in source:
    raise RuntimeError("Master M3x8 call changed; update engagement calculation")
m3_eng=8-(p["SIDE_COVER_T"]-p["COVER_SCREW_CBORE"][1])
m3_edge=min(p["SIDE_COVER_L"]/2-max(map(abs,p["COVER_SCREW_DX"])),
            p["SIDE_COVER_H"]/2-max(map(abs,p["COVER_SCREW_DZ"])))-p["COVER_SCREW_CBORE"][0]
checks={
 "closed_source_CAD_seal":"PASS" if wire.IsClosed() and area>0 else "FAIL",
 "24_M3_side_cover_total":"PASS" if 2*len(p["COVER_SCREW_DX"])*len(p["COVER_SCREW_DZ"])==24 else "FAIL",
 "M3_screw_engagement_1D_preliminary":"PASS" if m3_eng>=3 else "FAIL",
 "M3_head_edge_2mm_preliminary":"PASS" if m3_edge>=2 else "FAIL",
 "top_front_M4_engagement_1D_preliminary":"PASS" if front_eng>=4 else "FAIL",
 "top_front_M4_head_edge_2mm_preliminary":"PASS" if front_edge>=2 else "FAIL",
 "top_front_boss_to_aperture_2mm_preliminary":"PASS" if boss_lig>=2 else "FAIL",
 "lift_bridge_geometric_span":"PASS" if lift_min<lift_inner_x<lift_outer_x<lift_max and
   p["SERVICE_OPEN_X0"]<lift_inner_x<p["SERVICE_OPEN_X0"]+S_L<lift_outer_x else "FAIL",
 "lift_M4_engagement_1D_preliminary":"PASS" if p["LIFT_M4_SCREW_L"]-p["LIFT_M4_CLAMP"]>=4 else "FAIL",
 "actual_bolt_reaction_and_preload":"NOT_RUN",
 "lift_base_bending_and_prying":"NOT_RUN",
 "dynamic_axle_pressure_seals":"PHYSICAL_CHECK",
 "pressure_0p4_to_0p7_bar":"PHYSICAL_CHECK"}
cases=[]
for bar in (0.4,0.7):
    pressure=bar*0.1 # N/mm2
    side=pressure*area
    top=pressure*top_area
    front=top*(lift_outer_x-top_cx)/(lift_outer_x-front_x)
    back=top-front
    cases.append({"bar":bar,"each_side_cover_force_N":round(side,2),
      "M3_mean_share_only_N":round(side/12,2),"service_cover_force_N":round(top,2),
      "front_housing_pair_reaction_screen_N":round(front,2),
      "lift_housing_pair_reaction_screen_N":round(back,2),
      "bridge_nominal_moment_Nmm":round(back*(lift_outer_x-lift_inner_x),1)})
report={
 "source":"current/CAD/PX1_Current_Master.py",
 "scope":"nominal 0.4 / 0.7 bar pressure-load equilibrium for both side covers and top-service lid",
 "CAD_lobed_seal_enclosed_area_mm2":round(area,3),
 "CAD_lobed_seal_perimeter_mm":round(wire.Length(),3),
 "service_aperture_rounded_area_mm2":round(top_area,3),
 "fastening":{"front_M4_x_mm":front_x,"lift_inner_x_mm":round(lift_inner_x,2),
  "lift_outer_x_mm":round(lift_outer_x,2),
  "front_M4_length_mm":p["COVER_FIX_L"],
  "front_M4_engagement_mm":round(front_eng,2),
  "front_M4_pad_head_edge_mm":round(front_edge,2),
  "front_M4_boss_to_opening_mm":round(boss_lig,2),
  "side_M3_engagement_mm":round(m3_eng,2),"side_M3_head_edge_mm":round(m3_edge,2)},
 "cases":cases,"checks":checks,
 "assumptions":[
  "0.4-0.7 bar is design target only, NO physical pressure qualification.",
  "Side force uses CAD lobed seal enclosed area; top uses nominal rounded opening from master.",
  "Simple X force/moment balance at housing M4 pairs; not individual bolt loads, preload, FEA or bending.",
  "Rear service-lid restraint DEPENDS on fitted lift base through 2 cover-to-lift and 2 lift-to-housing M4.",
  "1D thread engagement and 2 mm head-edge/boss distances are PX1 SCREEN targets, not standards.",
  "Depressurize before removal of the lift or the service cover. Dynamic shaft seals remain unqualified."]}
(OUT/"PX1_pressure_retention_integration.json").write_text(
 json.dumps(report,ensure_ascii=False,indent=2),encoding="utf-8")
# Honest SVG: sample the actual CAD master side seal wire; all other geometry
# comes directly from the master dimensions, in millimetres (2D projection).
points,_=wire.sample(280)
def XY(x,z): return 100+(x-19)*3,230-z*3
path="M "+" L ".join("%.2f,%.2f"%XY(q.x,q.y) for q in points)+" Z"
def top(x,y): return 105+(x-70)*3.4,552-y*3.4
def dot(x,y,color):
    a,b=top(x,y)
    return f'<circle cx="{a:.2f}" cy="{b:.2f}" r="6.8" fill="white" stroke="{color}" stroke-width="2.5"/>'
dots="".join(f'<circle cx="{XY(150+dx,dz)[0]:.2f}" cy="{XY(150+dx,dz)[1]:.2f}" r="5.1" fill="white" stroke="#34556b"/>'
 for dx in p["COVER_SCREW_DX"] for dz in p["COVER_SCREW_DZ"])
sx,sy=top(p["SERVICE_OPEN_X0"],S_W/2)
padx,pady=top(p["SERVICE_PAD_X"][0],p["SERVICE_PAD_HW"])
lx,ly=top(lift_min,p["LIFT_M4_Y_PX1"][0]+6.45)
last=cases[-1]
svg=f'''<svg xmlns="http://www.w3.org/2000/svg" width="1390" height="810" viewBox="0 0 1390 810">
<rect width="1390" height="810" fill="#f7fafc"/><g font-family="Arial,sans-serif" fill="#172f45">
<text x="40" y="45" font-size="27" font-weight="bold">PX1 CURRENT MASTER | Pressure + retention integrated</text>
<text x="40" y="72" font-size="15">Actual CAD side-seal contour and nominal master geometry. NO stress FEA / pressure qualification.</text>
<text x="75" y="112" font-size="19" font-weight="bold">SIDE COVERS / 12 x M3 per side</text>
<rect x="100" y="140" width="786" height="180" fill="#d5e6f4" stroke="#729bb5"/>
<path d="{path}" fill="none" stroke="#c55c7a" stroke-width="5"/>{dots}
<text x="930" y="150" font-size="20">Enclosed CAD area: {area:.0f} mm2</text>
<text x="930" y="202" font-size="18">0.7 bar: {last['each_side_cover_force_N']:.1f} N / cover</text>
<text x="930" y="247" font-size="17">M3 engagement: {m3_eng:.1f} mm</text>
<text x="70" y="363" font-size="19" font-weight="bold">TOP SERVICE PLUG: retained through attached manual lift</text>
<rect x="{padx:.2f}" y="{pady:.2f}" width="{(p['SERVICE_PAD_X'][1]-p['SERVICE_PAD_X'][0])*3.4:.2f}" height="{p['SERVICE_PAD_HW']*6.8:.2f}" fill="#d4e7f8" stroke="#477da5"/>
<rect x="{sx:.2f}" y="{sy:.2f}" width="{S_L*3.4:.2f}" height="{S_W*3.4:.2f}" rx="{S_R*3.4:.2f}" fill="none" stroke="#c55c7a" stroke-width="5"/>
<rect x="{lx:.2f}" y="{ly:.2f}" width="{p['LIFT_BASE_L']*3.4:.2f}" height="{(p['LIFT_M4_Y_PX1'][0]+6.45)*6.8:.2f}" fill="#d4edd8" fill-opacity=".25" stroke="#418365" stroke-dasharray="7,5" stroke-width="2"/>
{dot(front_x,front_y,'#1d4ed8')}{dot(front_x,-front_y,'#1d4ed8')}
{dot(lift_inner_x,p['LIFT_M4_Y_PX1'][1],'#aa782b')}{dot(lift_inner_x,-p['LIFT_M4_Y_PX1'][1],'#aa782b')}
{dot(lift_outer_x,p['LIFT_M4_Y_PX1'][0],'#418365')}{dot(lift_outer_x,-p['LIFT_M4_Y_PX1'][0],'#418365')}
<text x="865" y="420" font-size="22">0.7 bar uplift: {last['service_cover_force_N']:.1f} N</text>
<text x="865" y="463" font-size="18">Front housing M4 pair: {last['front_housing_pair_reaction_screen_N']:.1f} N</text>
<text x="865" y="501" font-size="18">Rear lift-base M4 pair: {last['lift_housing_pair_reaction_screen_N']:.1f} N</text>
<text x="865" y="544" font-size="18">Front M4x{p['COVER_FIX_L']:.0f}: {front_eng:.1f} mm engagement</text>
<text x="865" y="580" font-size="18">Head edge: {front_edge:.1f} mm</text>
<text x="865" y="616" font-size="18">Boss to opening: {boss_lig:.1f} mm</text>
<text x="100" y="706" font-size="15">BLUE front cover/housing M4; AMBER lid-to-lift M4; GREEN lift-to-housing M4</text>
<text x="40" y="756" font-size="15">PASS only for analytic geometry screens | NOT_RUN: joint preload, FE and prying | PHYSICAL_CHECK: pressure, shaft seals</text>
<text x="40" y="784" font-size="14">Keep lift attached while pressurized. Depressurize before removing cover or lift.</text>
</g></svg>'''
(OUT/"PX1_pressure_retention_integration.svg").write_text(svg,encoding="utf-8")
print(json.dumps(report,ensure_ascii=False,indent=2))
sys.exit(1 if "FAIL" in checks.values() else 0)
