from __future__ import annotations

import argparse
import csv
import json
import math
from dataclasses import asdict, dataclass
from pathlib import Path

COPPER_RHO_20_OHM_MM2_M = 0.0175
DEFAULT_HOT_MULTIPLIER = 1.20


@dataclass
class Case:
    length_m: float
    conductor_mm2: float
    source_v: float
    crawler_output_w: float
    conversion_efficiency: float
    hot_multiplier: float
    loop_r_ohm: float
    converter_input_v: float | None
    line_current_a: float | None
    cable_drop_v: float | None
    cable_loss_w: float | None
    feasible_constant_power: bool


def loop_resistance(length_m: float, conductor_mm2: float,
                    hot_multiplier: float = DEFAULT_HOT_MULTIPLIER) -> float:
    if length_m <= 0 or conductor_mm2 <= 0 or hot_multiplier <= 0:
        raise ValueError("positive length, section and hot multiplier required")
    return (COPPER_RHO_20_OHM_MM2_M * 2.0 * length_m / conductor_mm2) * hot_multiplier


def constant_power_feed(source_v: float, output_w: float, loop_r_ohm: float,
                        efficiency: float = 1.0) -> tuple[float, float, float, float] | None:
    """Solve a two-wire DC feeder driving a constant-power load.

    efficiency is the downstream DC/DC efficiency.  For direct feed use 1.0.
    Returns load/input voltage, line current, cable drop and cable loss.
    The high-voltage stable root is selected.  None means no real operating
    point exists under this simple constant-power model.
    """
    if source_v <= 0 or output_w < 0 or loop_r_ohm < 0 or not (0 < efficiency <= 1.0):
        raise ValueError("invalid electrical input")
    if output_w == 0:
        return source_v, 0.0, 0.0, 0.0
    pin_w = output_w / efficiency
    disc = source_v * source_v - 4.0 * pin_w * loop_r_ohm
    if disc < 0:
        return None
    vin = 0.5 * (source_v + math.sqrt(disc))
    current = pin_w / vin
    drop = source_v - vin
    loss = current * current * loop_r_ohm
    return vin, current, drop, loss


def make_case(length_m: float, conductor_mm2: float, source_v: float,
              output_w: float, efficiency: float,
              hot_multiplier: float = DEFAULT_HOT_MULTIPLIER) -> Case:
    r = loop_resistance(length_m, conductor_mm2, hot_multiplier)
    solved = constant_power_feed(source_v, output_w, r, efficiency)
    if solved is None:
        return Case(length_m, conductor_mm2, source_v, output_w, efficiency,
                    hot_multiplier, r, None, None, None, None, False)
    vin, current, drop, loss = solved
    return Case(length_m, conductor_mm2, source_v, output_w, efficiency,
                hot_multiplier, r, vin, current, drop, loss, True)


def build_matrix() -> list[Case]:
    rows: list[Case] = []
    # Candidate sections bracket thin multicore and the 0.75 mm² power-core
    # reference found in an iPEK service cable.  They are not claims about the
    # still-unidentified PX1/Proteus tether.
    sections = (0.25, 0.34, 0.50, 0.75, 1.00)
    loads = (48.0, 96.0, 150.0)
    for section in sections:
        for load in loads:
            rows.append(make_case(40.0, section, 24.0, load, 1.0))
            rows.append(make_case(40.0, section, 110.0, load, 0.89))
    return rows


def write_outputs(out_dir: Path) -> None:
    out_dir.mkdir(parents=True, exist_ok=True)
    rows = build_matrix()
    fields = list(asdict(rows[0]).keys())
    with (out_dir / "PX1_A2_Tether_Power_Matrix.csv").open("w", newline="", encoding="utf-8") as f:
        w = csv.DictWriter(f, fieldnames=fields)
        w.writeheader()
        for row in rows:
            w.writerow(asdict(row))

    reference = {
        "status": "A2_ENGINEERING_SCREEN__CABLE_AND_CONNECTOR_RATINGS_NOT_RELEASED",
        "model": "constant-power two-wire feeder, copper rho20=0.0175 ohm*mm2/m, hot multiplier 1.20",
        "tether_length_m": 40.0,
        "six_core_assignment": ["POWER+", "POWER-", "RS485_A", "RS485_B", "CVBS_SIGNAL", "CVBS_RETURN"],
        "reference_only_iPEK_service_cable": {
            "power_cores_mm2": 0.75,
            "signal_cores_mm2": 0.14,
            "note": "reference architecture only; not proof of PX1/Proteus tether construction"
        },
        "dc_dc_candidate": {
            "part": "Cincon CQB150W-110S24",
            "input_vdc": [43.0, 160.0],
            "nominal_input_vdc": 110.0,
            "output_vdc": 24.0,
            "output_max_a": 6.3,
            "full_load_efficiency_fraction": 0.89,
            "full_load_input_a_at_nominal": 1.54
        },
        "key_cases_hot_copper": {
            "0p75mm2_24V_48W": asdict(make_case(40, 0.75, 24, 48, 1.0)),
            "0p75mm2_24V_96W": asdict(make_case(40, 0.75, 24, 96, 1.0)),
            "0p75mm2_110V_96W": asdict(make_case(40, 0.75, 110, 96, 0.89)),
            "0p75mm2_110V_150W": asdict(make_case(40, 0.75, 110, 150, 0.89)),
            "0p50mm2_110V_150W": asdict(make_case(40, 0.50, 110, 150, 0.89))
        },
        "release_gates": [
            "exact tether conductor construction and loop resistance",
            "tether insulation continuous voltage rating",
            "all connector/contact continuous voltage and current ratings",
            "touch-safe current-limited operator power source",
            "precharge/inrush control for converter input capacitance",
            "40m loaded power + RS485 + video EMC test"
        ]
    }
    (out_dir / "PX1_A2_Tether_Power_Validation.json").write_text(
        json.dumps(reference, indent=2, ensure_ascii=False), encoding="utf-8")


if __name__ == "__main__":
    p = argparse.ArgumentParser()
    p.add_argument("--out", default=str(Path(__file__).resolve().parent / "generated"))
    args = p.parse_args()
    write_outputs(Path(args.out))
