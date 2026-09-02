import json
import math
from pathlib import Path

# PX-1 Rev.PT screening calculation for the one-tool wheel retention.
# Units: N, mm, MPa. Prototype screen only; not a fatigue release.

D_SHAFT = 17.0
M8_INTERNAL_MINOR = 6.647  # ISO metric coarse basic internal minor diameter class
M8_EXTERNAL_STRESS_D = 6.466
RADIAL_LOAD = 200.0
LOAD_OVERHANG = 25.0
SIDE_TORQUE_NMM = 3.375 * 1000.0
KT_SCREEN = 2.5
IMPACT_FACTOR = 5.0
M8_TENSILE_AREA = 36.6
A4_80_PROOF_MPA = 600.0
THREAD_ENGAGEMENT = 10.0


def annulus(D, d, moment, torque):
    I = math.pi * (D**4 - d**4) / 64.0
    J = math.pi * (D**4 - d**4) / 32.0
    sigma = moment * (D / 2.0) / I
    tau = torque * (D / 2.0) / J
    vm = math.sqrt(sigma**2 + 3.0 * tau**2)
    return {
        "I_mm4": I,
        "J_mm4": J,
        "bending_MPa": sigma,
        "torsion_MPa": tau,
        "von_mises_MPa": vm,
    }


moment = RADIAL_LOAD * LOAD_OVERHANG
internal = annulus(D_SHAFT, M8_INTERNAL_MINOR, moment, SIDE_TORQUE_NMM)
solid = annulus(D_SHAFT, 0.0, moment, SIDE_TORQUE_NMM)

# Deliberately pessimistic comparison if an external M8 root itself carried the
# full wheel bending moment. The selected shoulder design does not rely on it.
external = annulus(M8_EXTERNAL_STRESS_D, 0.0, moment, SIDE_TORQUE_NMM)

result = {
    "inputs": {
        "shaft_od_mm": D_SHAFT,
        "internal_M8_minor_diameter_mm": M8_INTERNAL_MINOR,
        "radial_load_N": RADIAL_LOAD,
        "load_overhang_mm": LOAD_OVERHANG,
        "bending_moment_Nmm": moment,
        "side_torque_Nm": SIDE_TORQUE_NMM / 1000.0,
        "stress_concentration_screen": KT_SCREEN,
        "impact_factor_screen": IMPACT_FACTOR,
    },
    "solid_D17_reference": solid,
    "D17_with_internal_M8": internal,
    "external_M8_root_pessimistic_comparison": external,
    "internal_hole_section_modulus_loss_percent": 100.0 * (1.0 - internal["I_mm4"] / solid["I_mm4"]),
    "internal_M8_local_screen_MPa": internal["von_mises_MPa"] * KT_SCREEN,
    "internal_M8_5x_impact_local_screen_MPa": internal["von_mises_MPa"] * KT_SCREEN * IMPACT_FACTOR,
    "M8_A4_80_nominal_proof_load_N": M8_TENSILE_AREA * A4_80_PROOF_MPA,
    "minimum_full_thread_engagement_mm": THREAD_ENGAGEMENT,
    "decision": "INTERNAL_M8_PROTOTYPE_BASELINE",
    "rules": [
        "shaft shoulder and key carry wheel load and torque; screw retains axially only",
        "blind thread must stop before dynamic-seal land and wheel-bearing journal",
        "use retaining disk and wedge-lock pair under protective cap",
        "use anti-galling compound and controlled tightening torque",
        "first article requires 5x radial proof, reversal, removal-cycle and crack inspection",
    ],
}

result["status"] = "PASS_SCREEN" if (
    result["internal_hole_section_modulus_loss_percent"] < 5.0
    and result["internal_M8_5x_impact_local_screen_MPa"] < 200.0
    and result["M8_A4_80_nominal_proof_load_N"] > 15000.0
) else "FAIL_SCREEN"

out = Path(__file__).with_name("REV_PT_M8_WHEEL_RETENTION.json")
out.write_text(json.dumps(result, indent=2), encoding="utf-8")
print(json.dumps(result, indent=2))
if result["status"] != "PASS_SCREEN":
    raise SystemExit(2)

