"""PX1 first-order, intentionally limited engineering models.

These equations are NOT a CAD collision simulation, finite element analysis,
signal-integrity simulation, waterproofing test, or verified physical prototype.
Assumptions correspond to Rev.A A0/A2 candidates and must not be treated as
vendor-confirmed hardware ratings.
"""
from __future__ import annotations

import math


def wheel_speed_m_min(
    motor_rpm: float,
    gearbox_ratio: float = 66.2204,
    input_teeth: int = 16,
    output_teeth: int = 40,
    wheel_diameter_mm: float = 90.0,
    gearbox_max_input_rpm: float = 4000.0,
) -> float:
    if gearbox_ratio <= 0 or input_teeth <= 0 or output_teeth <= 0:
        raise ValueError("Gear ratios and tooth counts must be positive")
    if wheel_diameter_mm <= 0 or gearbox_max_input_rpm <= 0:
        raise ValueError("Wheel diameter and speed limit must be positive")
    if abs(motor_rpm) > gearbox_max_input_rpm:
        raise ValueError("Gearhead input RPM exceeds the candidate limit")
    return (
        motor_rpm / gearbox_ratio
        * input_teeth / output_teeth
        * math.pi * wheel_diameter_mm / 1000.0
    )


def dc_feeder(
    source_v: float,
    delivered_w: float,
    length_m: float,
    section_mm2: float,
    efficiency: float = 1.0,
    copper_temperature_factor: float = 1.20,
) -> dict:
    """Steady-state 2-wire constant-power feeder; stable quadratic root.

    Does NOT verify insulation, safety isolation, EMC, transient loads, video
    integrity, RS-485 stability, reel slip ring or connector ratings.
    """
    if min(source_v, length_m, section_mm2, copper_temperature_factor) <= 0:
        raise ValueError("Positive supply, length, section and factor required")
    if delivered_w < 0 or not (0 < efficiency <= 1):
        raise ValueError("Invalid load or converter efficiency")
    r = 2 * length_m * 0.0175 / section_mm2 * copper_temperature_factor
    discriminant = source_v ** 2 - 4 * r * delivered_w / efficiency
    result = {
        "source_v": source_v, "delivered_w": delivered_w,
        "length_m": length_m, "section_mm2": section_mm2,
        "loop_r_ohm": r,
        "equilibrium_exists": discriminant >= 0,
        "cable_input_v": None, "line_current_a": None,
        "copper_loss_w": None, "power_balance_error_w": None,
    }
    if discriminant < 0:
        return result
    cable_input_v = (source_v + math.sqrt(discriminant)) / 2
    current = delivered_w / efficiency / cable_input_v if delivered_w else 0.0
    copper_loss_w = current ** 2 * r
    result.update({
        "cable_input_v": cable_input_v,
        "line_current_a": current,
        "copper_loss_w": copper_loss_w,
        "power_balance_error_w": abs(
            source_v * current - delivered_w / efficiency - copper_loss_w
        ),
    })
    return result


def watchdog_timeline(
    duration_ms: int = 450,
    period_ms: int = 10,
    watchdog_limit_ms: int = 250,
    valid_commands_ms: tuple[int, ...] = (0, 50, 100, 400),
    corrupted_commands_ms: tuple[int, ...] = (150,),
) -> dict[int, bool]:
    """Reference *model* of V1 watchdog, not a firmware execution."""
    if duration_ms < 0 or period_ms <= 0 or watchdog_limit_ms <= 0:
        raise ValueError("Invalid timing")
    last_valid = None
    timeline: dict[int, bool] = {}
    valid = set(valid_commands_ms)
    corrupted = set(corrupted_commands_ms)
    if valid & corrupted:
        raise ValueError("A command cannot be both valid and corrupted")
    for t in range(0, duration_ms + 1, period_ms):
        if t in valid:
            last_valid = t
        # CRC/version-invalid frames NEVER refresh the watchdog.
        timeline[t] = last_valid is not None and (t - last_valid) <= watchdog_limit_ms
    return timeline


def evaluate_model_suite() -> dict:
    normal = wheel_speed_m_min(3500)
    ceiling = wheel_speed_m_min(4000)
    overloaded = dc_feeder(24.0, 96.0, 40.0, 0.75)
    candidate = dc_feeder(110.0, 150.0, 40.0, 0.75, 0.89)
    thin = dc_feeder(110.0, 150.0, 40.0, 0.50, 0.89)
    watchdog = watchdog_timeline()
    checks = {
        "drive_speed_in_source_bench_range": 5.8 < normal < 6.2,
        "gearbox_ceiling_in_source_bench_range": 6.7 < ceiling < 7.0,
        "24V_96W_40m_candidate_cannot_run": not overloaded["equilibrium_exists"],
        "110V_150W_40m_math_has_operating_point": (
            candidate["equilibrium_exists"]
            and 43 < candidate["cable_input_v"] < 160
            and candidate["power_balance_error_w"] < 1e-8
        ),
        "110V_150W_0p5mm2_math_has_operating_point": (
            thin["equilibrium_exists"] and thin["power_balance_error_w"] < 1e-8
        ),
        "corrupt_frame_does_not_refresh_watchdog": (
            watchdog[100] and not watchdog[360] and watchdog[400]
        ),
    }
    return {
        "status": "PASS_MODEL_ONLY" if all(checks.values()) else "FAIL_MODEL",
        "checks": checks,
        "assumptions": {
            "motor": "FAULHABER 2250S024BX4 + 26/1S 66.2204:1 candidate",
            "motor_rpm_test": 3500,
            "gearhead_input_rpm_limit": 4000,
            "wheel_diameter_mm": 90,
            "bevel_teeth": "Z16/Z40",
            "cable": "COPPER ASSUMED, 40 m, 2 conductors, hot factor 1.20",
            "converter": "assumed 0.89 efficiency for 110V case",
            "watchdog_ms": 250,
            "physical_proof": False,
        },
        "computed": {
            "speed_at_3500_rpm_m_min": normal,
            "speed_at_4000_rpm_m_min": ceiling,
            "dc_24v_96w": overloaded,
            "dc_110v_150w_0p75": candidate,
            "dc_110v_150w_0p50": thin,
            "traction_command_after_360ms": watchdog[360],
            "traction_command_after_recovery_400ms": watchdog[400],
        },
        "not_simulated": [
            "actual traction torque, terrain, wheel slip and tether drag",
            "geometric interference (read from separate existing CAD validation)",
            "camera seals, ingress, temperature and structural fatigue",
            "electrical isolation / shock hazards at elevated tether voltage",
            "EMC, video quality, RS-485 noise, slip ring contact reliability",
            "real compiled/installed firmware or physical emergency stop",
        ],
    }
