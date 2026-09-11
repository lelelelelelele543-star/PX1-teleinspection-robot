import math, json

# PX-1 Rev.B WB03 — bevel / traction motor torque screen
# Engineering screening only; not ISO 10300 gear rating.

WHEEL_D_M = 0.090
WHEEL_R_M = WHEEL_D_M / 2
BEVEL_RATIO = 2.5
PATH_EFF = 0.75
SIDES = 2

# Reconstructed source-compatible bevel geometry
MODULE = 1.0
Z1 = 16
Z2 = 40
FACE_W_MM = 6.5
PRESSURE_ANGLE_DEG = 20.0

# Leading motor candidate, controlled by manufacturer technical datasheet
MOTOR_RATED_RPM = 49.0
MOTOR_NOLOAD_RPM = 60.0
MOTOR_RATED_TORQUE_NM = 18.0 * 0.0980665
MOTOR_GEARBOX_LIMIT_NM = 40.0 * 0.0980665


def motor_torque_for_total_pull(force_n):
    return force_n * WHEEL_R_M / (SIDES * BEVEL_RATIO * PATH_EFF)


def crawler_speed_for_motor_rpm(rpm):
    wheel_rpm = rpm / BEVEL_RATIO
    speed = wheel_rpm * math.pi * WHEEL_D_M / 60.0
    return wheel_rpm, speed


def bevel_geometry():
    d1 = MODULE * Z1
    d2 = MODULE * Z2
    delta1 = math.atan(Z1 / Z2)
    delta2 = math.pi / 2 - delta1
    cone_r = 0.5 * MODULE * math.sqrt(Z1**2 + Z2**2)
    mean_factor = (cone_r - FACE_W_MM / 2) / cone_r
    return {
        'pinion_pitch_angle_deg': math.degrees(delta1),
        'gear_pitch_angle_deg': math.degrees(delta2),
        'cone_distance_mm': cone_r,
        'pinion_pitch_diameter_mm': d1,
        'gear_pitch_diameter_mm': d2,
        'pinion_mean_pitch_diameter_mm': d1 * mean_factor,
        'gear_mean_pitch_diameter_mm': d2 * mean_factor,
    }


def pinion_forces(torque_nm):
    g = bevel_geometry()
    dm1 = g['pinion_mean_pitch_diameter_mm']
    delta1 = math.radians(g['pinion_pitch_angle_deg'])
    phi = math.radians(PRESSURE_ANGLE_DEG)
    ft = 2.0 * torque_nm * 1000.0 / dm1
    fr = ft * math.tan(phi) * math.cos(delta1)
    fa = ft * math.tan(phi) * math.sin(delta1)
    return {'Ft_N': ft, 'Fr_N': fr, 'Fa_N': fa}


def shaft_tau_mpa(torque_nm, diameter_mm):
    return 16.0 * torque_nm * 1000.0 / (math.pi * diameter_mm**3)


pull_targets = {str(f): motor_torque_for_total_pull(f) for f in (40, 50, 60, 66.7, 83.3)}
forces = {str(t): pinion_forces(t) for t in (0.60, 0.80, 1.00, 2.00)}
wheel_rpm_rated, speed_rated = crawler_speed_for_motor_rpm(MOTOR_RATED_RPM)
wheel_rpm_noload, speed_noload = crawler_speed_for_motor_rpm(MOTOR_NOLOAD_RPM)

result = {
    'inputs': {
        'wheel_diameter_m': WHEEL_D_M,
        'bevel_ratio': BEVEL_RATIO,
        'whole_path_efficiency_screen': PATH_EFF,
        'drive_sides': SIDES,
        'bevel_module': MODULE,
        'bevel_teeth': [Z1, Z2],
        'face_width_mm_screen': FACE_W_MM,
        'pressure_angle_deg': PRESSURE_ANGLE_DEG,
    },
    'motor_candidate': {
        'part': 'ISL PGM-32P-24-100-60-02 / MOT-IG32PGM 100',
        'rated_speed_rpm': MOTOR_RATED_RPM,
        'no_load_speed_rpm': MOTOR_NOLOAD_RPM,
        'rated_torque_Nm': MOTOR_RATED_TORQUE_NM,
        'gearbox_limit_Nm': MOTOR_GEARBOX_LIMIT_NM,
        'rated_wheel_rpm': wheel_rpm_rated,
        'rated_crawler_speed_mps': speed_rated,
        'noload_wheel_rpm': wheel_rpm_noload,
        'noload_crawler_speed_mps': speed_noload,
    },
    'motor_torque_required_per_side_Nm_by_total_pull_N': pull_targets,
    'bevel_geometry': bevel_geometry(),
    'pinion_force_screen': forces,
    'large_bevel_output_at_2Nm_input_Nm': 2.0 * BEVEL_RATIO,
    'nominal_tau_10mm_shaft_at_5Nm_MPa': shaft_tau_mpa(5.0, 10.0),
    'revB_min_pair_gate': {'continuous_pinion_Nm': 1.0, 'short_overload_pinion_Nm': 2.0},
    'status': 'soft stock m1 pair rejected; matched hardened compact pair required for traction release',
}

print(json.dumps(result, indent=2))
