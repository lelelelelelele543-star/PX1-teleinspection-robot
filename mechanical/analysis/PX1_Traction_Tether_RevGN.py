import math, csv, json, os

# PX-1 Rev.GN — traction / ballast / tether screening model
# Engineering screening only; NOT release data.
# Update measured friction, mass and motor data after physical tests.

OUT = os.path.abspath('build_revgn')
os.makedirs(OUT, exist_ok=True)

G = 9.80665
PIPE_R_M = 0.075
CONTACT_Y_M = 0.054      # active Ø90 crown contact from Rev.DL/GF
WHEEL_R_M = 0.045
SUPPORT_VERTICAL = math.sqrt(PIPE_R_M**2 - CONTACT_Y_M**2) / PIPE_R_M

BASE_MASS_KG = 7.0       # current nominal screen inside Rev.GM 6.3–7.7 kg estimate
BALLAST_KG = [0.0, 0.5, 1.0, 1.5]
MU_TIRE = [0.30, 0.40, 0.50, 0.60]
SLOPE_DEG = [0, 5, 10, 20, 30]
ROLLING_RESISTANCE = 0.02  # placeholder sensitivity value; measure on physical crawler

# Current protected drivetrain screen from Rev.GJ/GK.
MOTOR_TORQUE_LIMIT_EACH_NM = 1.0
BEVEL_RATIO = 2.5
DRIVETRAIN_EFFICIENCY = 0.75  # conservative whole path screen; measure later
MOTOR_FORCE_CAP_N = (2 * MOTOR_TORQUE_LIMIT_EACH_NM * BEVEL_RATIO *
                     DRIVETRAIN_EFFICIENCY / WHEEL_R_M)

# 0.054 kg/m is a manufacturer-published Proteus Lite cable reference, not PX-1 cable mass.
# 0.080 kg/m is an internal conservative sensitivity point until PX-1 tether is weighed.
TETHER_MASS_KGPM = [0.054, 0.080]
TETHER_SLIDING_MU = [0.15, 0.20, 0.30]


def robot_available_pull(mass_kg, mu_tire, slope_deg, crr=ROLLING_RESISTANCE):
    th = math.radians(slope_deg)
    normal_total = mass_kg * G * math.cos(th) / SUPPORT_VERTICAL
    adhesion_limit = mu_tire * normal_total
    drive_limit = min(adhesion_limit, MOTOR_FORCE_CAP_N)
    grade_force = mass_kg * G * math.sin(th)
    rolling_force = crr * mass_kg * G * math.cos(th)
    net_tether_pull = drive_limit - grade_force - rolling_force
    return {
        'normal_total_N': normal_total,
        'adhesion_limit_N': adhesion_limit,
        'motor_force_cap_N': MOTOR_FORCE_CAP_N,
        'drive_limit_N': drive_limit,
        'grade_force_N': grade_force,
        'rolling_force_N': rolling_force,
        'net_tether_pull_N': net_tether_pull,
    }


def tether_drag_per_m(mass_kgpm, mu_slide, slope_deg):
    # Entire deployed length on the same uphill grade, sliding on pipe floor.
    # Conservative straight-pipe screening model; bends, reel tension and buoyancy are separate.
    th = math.radians(slope_deg)
    return mass_kgpm * G * (math.sin(th) + mu_slide * math.cos(th))


def min_mu_for_self_climb(slope_deg, crr=ROLLING_RESISTANCE):
    # Adhesion threshold before any positive reserve remains for tether pull.
    th = math.radians(slope_deg)
    return SUPPORT_VERTICAL * (math.tan(th) + crr)


rows = []
for ballast in BALLAST_KG:
    mass = BASE_MASS_KG + ballast
    for mu in MU_TIRE:
        for slope in SLOPE_DEG:
            r = robot_available_pull(mass, mu, slope)
            for mpm in TETHER_MASS_KGPM:
                for mu_c in TETHER_SLIDING_MU:
                    dpm = tether_drag_per_m(mpm, mu_c, slope)
                    lmax = max(0.0, r['net_tether_pull_N'] / dpm) if dpm > 0 else float('inf')
                    rows.append({
                        'robot_mass_kg': mass,
                        'ballast_kg': ballast,
                        'tire_mu': mu,
                        'slope_deg': slope,
                        'tether_mass_gpm': mpm * 1000,
                        'tether_slide_mu': mu_c,
                        'adhesion_limit_N': r['adhesion_limit_N'],
                        'motor_force_cap_N': r['motor_force_cap_N'],
                        'net_tether_pull_N': r['net_tether_pull_N'],
                        'tether_drag_N_per_m': dpm,
                        'max_straight_uphill_tether_m': lmax,
                    })

csv_path = os.path.join(OUT, 'REV_GN_TRACTION_MATRIX.csv')
with open(csv_path, 'w', newline='') as f:
    w = csv.DictWriter(f, fieldnames=list(rows[0].keys()))
    w.writeheader(); w.writerows(rows)

summary = {
    'support_vertical_factor': SUPPORT_VERTICAL,
    'contact_wall_normal_angle_from_vertical_deg': math.degrees(math.acos(SUPPORT_VERTICAL)),
    'motor_force_cap_N': MOTOR_FORCE_CAP_N,
    'minimum_tire_mu_for_self_climb': {str(d): min_mu_for_self_climb(d) for d in SLOPE_DEG},
    'nominal_7kg_mu04': {str(d): robot_available_pull(7.0, 0.40, d)['net_tether_pull_N'] for d in SLOPE_DEG},
    'nominal_7kg_mu05': {str(d): robot_available_pull(7.0, 0.50, d)['net_tether_pull_N'] for d in SLOPE_DEG},
    'status': 'SCREENING ONLY — replace assumed friction/mass/efficiency with measured data before release',
}
with open(os.path.join(OUT, 'REV_GN_SUMMARY.json'), 'w') as f:
    json.dump(summary, f, indent=2)

print(json.dumps(summary, indent=2))
