"""PX1 pressure-boundary integration audit, DESIGN ASSUMPTIONS only.
Independent Python 3 check of lid, eight bolts, six dynamic shaft seals.
No pressure or mechanical qualification is claimed.
"""
import json, math
from pathlib import Path
P={"opening_x_mm":170,"opening_y_mm":60,"lid_x_mm":190,"lid_y_mm":78,
   "gasket_outer_x_mm":176,"gasket_outer_y_mm":66,
   "gasket_inner_x_mm":170,"gasket_inner_y_mm":60,
   "lid_thickness_mm":4,"lid_bolts":8,"shaft_diameter_mm":10,
   "shaft_count":6,"pressure_bar_min":0.4,"pressure_bar_max":0.7,
   "gasket_nominal_mm":1.0,"gasket_compression_mm":0.3,
   "seal_cartridge_axial_mm":4,"seal_axial_space_mm":5}
def audit(p):
    pressure_pa=p["pressure_bar_max"]*100000
    area_m2=p["opening_x_mm"]*p["opening_y_mm"]*1e-6
    lid_force_n=pressure_pa*area_m2
    shaft_force_n=pressure_pa*math.pi*(p["shaft_diameter_mm"]*1e-3)**2/4
    checks={
      "lid_opening_within_lid":"PASS" if p["lid_x_mm"]>p["opening_x_mm"] and p["lid_y_mm"]>p["opening_y_mm"] else "FAIL",
      "gasket_inner_matches_aperture":"PASS" if p["gasket_inner_x_mm"]==p["opening_x_mm"] and p["gasket_inner_y_mm"]==p["opening_y_mm"] else "FAIL",
      "gasket_footprint_within_lid":"PASS" if p["gasket_outer_x_mm"]<=p["lid_x_mm"] and p["gasket_outer_y_mm"]<=p["lid_y_mm"] else "FAIL",
      "gasket_nominal_compression":"PASS" if 0<p["gasket_compression_mm"]<p["gasket_nominal_mm"] else "FAIL",
      "seal_axial_envelope":"PASS" if p["seal_cartridge_axial_mm"]<=p["seal_axial_space_mm"] else "FAIL",
      "pressure_rated_dynamic_seals":"PHYSICAL_CHECK",
      "lid_deflection_and_fastener_preload":"NOT_RUN",
      "pressure_test":"PHYSICAL_CHECK"}
    return {"status":"FAIL" if "FAIL" in checks.values() else "CONDITIONAL",
       "assumptions":p,"checks":checks,
       "lid_force_N_at_max_pressure":round(lid_force_n,2),
       "nominal_force_per_bolt_N_NOT_PRELOAD":round(lid_force_n/p["lid_bolts"],2),
       "axial_pressure_force_per_shaft_N":round(shaft_force_n,2),
       "all_six_shaft_axial_force_N":round(shaft_force_n*p["shaft_count"],2),
       "note":"Forces are ideal pressure-area loads, NOT bolt preload, stress, seal rating or safe pressure proof."}
if __name__=="__main__":
    r=audit(P)
    target=Path(__file__).with_suffix(".json")
    target.write_text(json.dumps(r,indent=2,ensure_ascii=False)+"\\n",encoding="utf-8")
    print(json.dumps(r,indent=2,ensure_ascii=False))
    if "FAIL" in r["checks"].values(): raise SystemExit(2)
