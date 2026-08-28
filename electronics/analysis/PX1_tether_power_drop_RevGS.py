#!/usr/bin/env python3
"""PX-1 Rev.GS tether power-drop calculator.

Planning/measurement tool for the single reinforced 6-core copper inspection cable.
The two power conductors are modeled as one round-trip loop resistance.
No assumption is made that the cable is Ethernet cable, coax or fiber.

Examples:
  python PX1_tether_power_drop_RevGS.py
  python PX1_tether_power_drop_RevGS.py --length 150 --source 60 --load 100 --oneway-mohm-m 17.5
  python PX1_tether_power_drop_RevGS.py --length 150 --source 60 --load 100 --measured-loop-ohm 5.10
"""

import argparse
import json
import math

COPPER_RHO_OHM_MM2_M = 0.0175  # conservative planning value near room temperature; sample measurement wins


def loop_r_from_area(length_m: float, area_mm2: float) -> float:
    return 2.0 * COPPER_RHO_OHM_MM2_M * length_m / area_mm2


def loop_r_from_oneway(length_m: float, oneway_mohm_m: float) -> float:
    return 2.0 * length_m * (oneway_mohm_m / 1000.0)


def solve_constant_power(source_v: float, loop_r: float, delivered_w: float):
    """High-voltage branch of Vload*(Vs-Vload)/R = P.

    Returns None if the requested constant power is physically impossible at
    the stated source voltage/resistance (above max-power-transfer point).
    """
    if loop_r <= 0:
        return {
            "load_voltage_v": source_v,
            "line_current_a": delivered_w / source_v,
            "line_loss_w": 0.0,
            "line_efficiency": 1.0,
            "max_deliverable_w": float("inf"),
        }
    pmax = source_v * source_v / (4.0 * loop_r)
    disc = source_v * source_v - 4.0 * loop_r * delivered_w
    if disc < 0:
        return None
    vload = 0.5 * (source_v + math.sqrt(disc))
    current = delivered_w / vload
    loss = current * current * loop_r
    return {
        "load_voltage_v": vload,
        "line_current_a": current,
        "line_loss_w": loss,
        "line_efficiency": delivered_w / (delivered_w + loss),
        "max_deliverable_w": pmax,
    }


def scenario(length_m, source_v, delivered_w, loop_r):
    s = solve_constant_power(source_v, loop_r, delivered_w)
    out = {
        "length_m": length_m,
        "source_v": source_v,
        "delivered_power_w": delivered_w,
        "loop_resistance_ohm": loop_r,
        "max_power_transfer_w": source_v * source_v / (4.0 * loop_r) if loop_r > 0 else None,
    }
    if s is None:
        out.update({"status": "IMPOSSIBLE_AT_REQUESTED_POWER"})
    else:
        out.update(s)
        out["status"] = "SOLVABLE"
    return out


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--length", type=float, default=150.0, help="one-way tether length, m")
    ap.add_argument("--source", type=float, default=60.0, help="console tether source voltage, VDC")
    ap.add_argument("--load", type=float, default=100.0, help="power required at crawler tether input, W")
    ap.add_argument("--area", type=float, default=None, help="planning power-conductor copper area, mm^2 each")
    ap.add_argument("--oneway-mohm-m", type=float, default=None, help="measured/known resistance of ONE power conductor, mOhm/m")
    ap.add_argument("--measured-loop-ohm", type=float, default=None, help="direct measured round-trip resistance for the actual cable length")
    args = ap.parse_args()

    methods = sum(x is not None for x in (args.area, args.oneway_mohm_m, args.measured_loop_ohm))
    if methods > 1:
        raise SystemExit("Choose only one of --area, --oneway-mohm-m or --measured-loop-ohm")

    if args.measured_loop_ohm is not None:
        rloop = args.measured_loop_ohm
        basis = "measured_loop"
    elif args.oneway_mohm_m is not None:
        rloop = loop_r_from_oneway(args.length, args.oneway_mohm_m)
        basis = "measured_or_specified_oneway_resistance"
    elif args.area is not None:
        rloop = loop_r_from_area(args.length, args.area)
        basis = "copper_area_planning_only"
    else:
        # default planning reference = 1.0 mm2 per power conductor
        rloop = loop_r_from_area(args.length, 1.0)
        basis = "default_1.0mm2_planning_only"

    result = scenario(args.length, args.source, args.load, rloop)
    result["resistance_basis"] = basis

    # Reference matrix to make 40/100/150 m decisions visible without editing code.
    matrix = []
    for L in (40.0, 100.0, 150.0):
        for area in (0.50, 0.75, 1.00, 1.50):
            R = loop_r_from_area(L, area)
            for Vs in (48.0, 60.0):
                for P in (70.0, 100.0, 130.0):
                    row = scenario(L, Vs, P, R)
                    row["planning_area_mm2_each"] = area
                    matrix.append(row)
    result["reference_matrix"] = matrix

    print(json.dumps(result, indent=2))


if __name__ == "__main__":
    main()
