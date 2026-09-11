import math, json

# PX-1 Rev.B / WB16
# Calculation-only screen. Does not claim full cable solid/pipe clearance.

CABLE_ARTICLE = "LAPP 0027429 UNITRONIC FD CY 7X0.25"
CABLE_OD_MM = 6.7
R_DYNAMIC_MFR_MM = 50.3
R_ROUTE_DESIGN_MM = 55.0
MAX_ONE_WAY_LENGTH_M = 0.50
R_CORE_OHM_PER_KM = 79.0
MASS_KG_PER_KM = 75.0

# Existing Rev.FN parallelogram kinematics.
BODY_ANCHOR = (200.0, 102.0)
HEAD_POSITIONS = {
    "LOW": (83.557, 75.0),
    "MID": (82.851, 130.0),
    "HIGH": (135.200, 205.0),
}


def dist(a, b):
    return math.hypot(a[0]-b[0], a[1]-b[1])

anchor_distances = {k: dist(BODY_ANCHOR, v) for k, v in HEAD_POSITIONS.items()}
span = max(anchor_distances.values()) - min(anchor_distances.values())

r_one = R_CORE_OHM_PER_KM * (MAX_ONE_WAY_LENGTH_M / 1000.0)
r_loop = 2.0 * r_one

currents = [0.5, 1.0, 1.2, 2.0, 3.0]
drop = {f"{i:.1f}A": {"drop_V": i*r_loop, "pair_loss_W": i*i*r_loop} for i in currents}

result = {
    "project": "PX-1",
    "revision": "Rev.B",
    "work_block": "WB16",
    "cable": {
        "article": CABLE_ARTICLE,
        "cores": 7,
        "core_mm2": 0.25,
        "OD_mm": CABLE_OD_MM,
        "manufacturer_dynamic_bend_mm": R_DYNAMIC_MFR_MM,
        "design_dynamic_bend_mm": R_ROUTE_DESIGN_MM,
        "max_core_resistance_ohm_per_km": R_CORE_OHM_PER_KM,
        "mass_kg_per_km": MASS_KG_PER_KM,
        "prototype_one_way_length_limit_m": MAX_ONE_WAY_LENGTH_M,
    },
    "electrical": {
        "one_core_R_ohm_at_length_limit": r_one,
        "power_loop_R_ohm_at_length_limit": r_loop,
        "current_screens": drop,
    },
    "lift_anchor_screen": {
        "body_anchor_XZ_mm": BODY_ANCHOR,
        "head_positions_XZ_mm": HEAD_POSITIONS,
        "straight_anchor_distances_mm": anchor_distances,
        "distance_span_mm": span,
        "interpretation": "parallelogram keeps anchor distance almost constant; route alongside one lift arm and absorb angle at controlled end arcs rather than a hanging travel loop"
    },
    "status": "ELECTRICAL_PASS_SCREEN / FULL_R55_DN150_CABLE_SOLID_HOLD",
    "holds": [
        "actual clamp coordinates",
        "R55 cable solid in LOW/MID/HIGH",
        "DN150 LOW and DN150_SAFE collision test",
        "actual purchased cable OD and resistance",
        "CVBS test through SP13 plus cable",
        "numeric SP13 contact numbering"
    ]
}

print(json.dumps(result, indent=2))
