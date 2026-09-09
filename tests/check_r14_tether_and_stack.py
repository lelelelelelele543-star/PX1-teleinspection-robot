"""Analytical screen for tether line resistance and the R14 wheel stack.

The cable resistance is an input to this script, never a claimed measurement.
The report is useful for selecting a safe test point; it is not an electrical
or mechanical acceptance test.
"""
from pathlib import Path
import argparse, json, math

ROOT = Path(__file__).resolve().parents[1]


def operating_point(source_v, loop_ohm, output_w, efficiency=.90):
    pin = output_w / efficiency
    disc = source_v * source_v - 4 * loop_ohm * pin
    if disc < 0:
        return {"equilibrium": False, "reason": "no DC constant-power equilibrium"}
    robot_v = (source_v + math.sqrt(disc)) / 2
    line_a = pin / robot_v
    return {
        "equilibrium": True, "V_robot": robot_v, "A_line": line_a,
        "W_loop_loss": line_a * line_a * loop_ohm,
        "W_source": source_v * line_a,
        "RSD_input_window": 67.2 <= robot_v <= 143.0,
        "power_residual_W": source_v * line_a - (pin + line_a * line_a * loop_ohm)
    }


def run(out):
    cases = [{"source_V": v, "loop_ohm": r, "load_W": p,
              **operating_point(v, r, p)}
             for v in (100, 110, 120) for r in (5, 10, 20, 30)
             for p in (56, 80, 100.8)]
    report = {
        "revision": "R14", "status": "CALCULATED_SCENARIOS_ONLY",
        "physical_measurements": False,
        "converter": "MEAN WELL RSD-100D-24",
        "continuous_input_V": [67.2, 143.0], "output_V": 24,
        "output_A": 4.2, "assumed_efficiency": .90, "cases": cases,
        "boundary_Rloop_ohm_at_100p8W": {
            str(v): .90 * 67.2 * (v - 67.2) / 100.8 for v in (100, 110, 120)
        },
        "wheel_stack_mm": {
            "bearing_abs_Y": [36.65, 43.65], "clip_groove_abs_Y": [35.55, 36.65],
            "inner_spacer_abs_Y": [43.65, 44.5], "outer_spacer_abs_Y": [43.65, 44.4],
            "seal_land_abs_Y": [44.5, 50.5], "wheel_seat_abs_Y": [50.5, 61.0],
            "washer_abs_Y": [61.0, 63.0], "nut_abs_Y": [63.0, 71.0],
            "thread_tip_abs_Y": 73.6, "thread_protrusion_mm": 2.6,
            "M8_pitch_mm": 1.25, "protruding_pitches": 2.08,
            "overall_width_at_thread_tips_mm": 147.2
        },
        "limitations": [
            "Rloop is not measured; it must include both HV conductors, connectors and slip ring.",
            "Boundary values have zero voltage margin and are not design limits.",
            "No inrush, transients, current limit, isolation, thermal or discharge test.",
            "Wheel dimensions omit tolerances, chamfers, fits, tightening and fatigue."
        ]
    }
    out.parent.mkdir(parents=True, exist_ok=True)
    out.write_text(json.dumps(report, indent=2))
    print(json.dumps({"status": report["status"],
                      "boundary_Rloop_ohm_at_100p8W": report["boundary_Rloop_ohm_at_100p8W"],
                      "example_110V_10ohm_56W": operating_point(110, 10, 56)}, indent=2))


if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument("--out", type=Path,
                        default=ROOT / "validation/r14/analytical_review.json")
    parser.add_argument("--source-volts", type=float, default=110)
    parser.add_argument("--loop-ohm", type=float)
    parser.add_argument("--load-watts", type=float, default=56)
    args = parser.parse_args()
    if args.loop_ohm is None:
        run(args.out)
    else:
        print(json.dumps(operating_point(args.source_volts, args.loop_ohm,
                                          args.load_watts), indent=2))
