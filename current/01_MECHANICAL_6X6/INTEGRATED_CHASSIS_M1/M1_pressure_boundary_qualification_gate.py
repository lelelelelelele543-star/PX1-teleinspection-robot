"""PX1 M1 — integrated pressure-boundary audit. Pure Python 3.10+, no FreeCAD.
Design assumptions from current integrated chassis generator, NOT manufacturer dimensions.
Checks all six axle penetrations, lid aperture, gasket land and fastener proximity.
"""
import json, math
from pathlib import Path

P = dict(body_L=307., body_W=78., body_H=70., wall=5.,
         opening_L=170., opening_W=60., lid_L=190., lid_W=78.,
         gasket_outer_L=176., gasket_outer_W=66.,
         shaft_d=10., bearing_d=22., seal_cartridge_d=23.,
         seal_cartridge_length=4., pressure_bar=0.7,
         wheel_inner_y=46., bearing_start_y=34., bearing_length=7.)
stations=(-100.,0.,100.)
bolts=[(x,y) for x in (-90.,0.,90.) for y in (-35.5,35.5)]+[(-90.,0.),(90.,0.)]
checks={}
def check(key, passed, value, note):
    checks[key]=dict(status="PASS" if passed else "FAIL", value=value, note=note)

p=P["pressure_bar"]*1e5
area=P["opening_L"]*P["opening_W"]
force=p*area*1e-6
check("lid_force",True,round(force,2),"N, nominal opening force; bolt preload NOT calculated")
check("six_penetrations",len(stations)*2==6,len(stations)*2,"Six shaft passages")
check("gasket_land_x",(P["gasket_outer_L"]-P["opening_L"])/2>=3,
      (P["gasket_outer_L"]-P["opening_L"])/2,"mm gasket radial width X")
check("gasket_land_y",(P["gasket_outer_W"]-P["opening_W"])/2>=3,
      (P["gasket_outer_W"]-P["opening_W"])/2,"mm gasket radial width Y")
# Gasket occupies 85..88 in X, 30..33 in Y. Eight bolts lie outside its outer edge.
# Distance from each bolt center to nearest gasket-outer rectangle is a lower-bound
# center-to-material distance; fastener head diameter 5.6 mm matters.
for i,(x,y) in enumerate(bolts):
    dx=max(abs(x)-P["gasket_outer_L"]/2,0)
    dy=max(abs(y)-P["gasket_outer_W"]/2,0)
    distance=math.hypot(dx,dy)
    check("bolt_gasket_"+str(i+1),distance>=2.8,round(distance,3),
          "mm bolt center to outer gasket boundary; head radius 2.8 mm")
bearing_end=P["bearing_start_y"]+P["bearing_length"]
axial_gap=P["wheel_inner_y"]-bearing_end
check("seal_axial_space",axial_gap>=P["seal_cartridge_length"]+1,
      axial_gap,"mm available between bearing and wheel; 1 mm reserved")
# Critically: Ø23 cartridge extends beyond the Ø22 bearing counterbore; no retention
# or dedicated machined seat is present in the CAD source.
check("seal_cartridge_seat",False,
      dict(cartridge_d=P["seal_cartridge_d"],bearing_counterbore_d=P["bearing_d"]),
      "FAIL: separate Ø23 cartridge retention/seat NOT modeled")
check("seal_pressure_rating",False,"UNVERIFIED",
      "FAIL qualification gate: 0.7 bar dynamic lip seal and runout not sourced")
check("lid_fastener_preload",False,"UNVERIFIED",
      "FAIL qualification gate: bolt preload, engagement and gasket compression not demonstrated")
report=dict(status="FAIL" if any(c["status"]=="FAIL" for c in checks.values()) else "PASS",
            assumptions=P, checks=checks, limitation="Analytical audit only, no FreeCAD Boolean or physical pressure test")
Path(__file__).with_name("M1_pressure_boundary_gate_result.json").write_text(
    json.dumps(report,indent=2,ensure_ascii=False),encoding="utf-8")
print(json.dumps(report,indent=2,ensure_ascii=False))
