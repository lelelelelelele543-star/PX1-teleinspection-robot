import cadquery as cq
import math, json, os

# PX-1 Rev.GT — common rotary Quad-Ring packaging check
# Prototype engineering baseline; NOT machining release.
# Coordinates follow active Rev.GF / Rev.GL left-side Y stack.

OUT = os.path.abspath('build_revgt')
os.makedirs(OUT, exist_ok=True)

# Common dynamic seal candidate (Trelleborg Quad-Ring rotary/internal installation table)
SHAFT_D = 18.0
GROOVE_ROOT_D = 22.8
GROOVE_W = 2.8
GROOVE_R = 0.30
MAX_RADIAL_GAP = 0.08
QUADRING_ID = 18.72
QUADRING_CS = 2.62

# X200 active Rev.GL axial stack (positive-Y side)
X200_OLD_SEAL_Y0 = 34.5
X200_OLD_SEAL_Y1 = 41.5
X200_GROOVE_Y0 = 36.6
X200_GROOVE_Y1 = X200_GROOVE_Y0 + GROOVE_W
X200_Z50_Y0 = 42.0
X200_Z50_Y1 = 45.5
X200_HOUSING_OD = 30.0  # stays inside old 18x30x7 seal pocket envelope

# Wheel active Rev.GF / GT stack (positive-Y side)
BEARING_61903_Y0 = 51.35
BEARING_61903_Y1 = 58.35
WHEEL_SEAL_LAND_Y0 = BEARING_61903_Y1
WHEEL_SEAL_LAND_Y1 = 62.15
WHEEL_GROOVE_Y0 = 58.85
WHEEL_GROOVE_Y1 = WHEEL_GROOVE_Y0 + GROOVE_W
WHEEL_SEAT_Y0 = 62.15
WHEEL_SEAT_D = 17.0
STATIC_FLANGE_ORING_ID = 32.0
FLANGE_OD = 50.0

# Reference speed from current 54 rpm motor / 2.5:1 bevel stage
MOTOR_RPM = 54.0
BEVEL_RATIO = 2.5
WHEEL_RPM = MOTOR_RPM / BEVEL_RATIO


def wp(shape):
    return cq.Workplane('XY').newObject([shape])


def cyl_y(y0, r, length):
    return wp(cq.Solid.makeCylinder(r, length, cq.Vector(0, y0, 0), cq.Vector(0, 1, 0)))


def ring_y(y0, outer_d, inner_d, length):
    outer = cyl_y(y0, outer_d / 2.0, length)
    inner = cyl_y(y0, inner_d / 2.0, length)
    return wp(outer.val().cut(inner.val()))


def cut(a, b):
    return wp(a.val().cut(b.val()))


def inter_vol(a, b):
    return a.val().intersect(b.val()).Volume()


# X200 fixed housing sleeve. The old Ø30 x 7 lip-seal envelope is retained externally.
x200_housing = ring_y(
    X200_OLD_SEAL_Y0,
    X200_HOUSING_OD,
    SHAFT_D + 2 * MAX_RADIAL_GAP,
    X200_OLD_SEAL_Y1 - X200_OLD_SEAL_Y0,
)
x200_groove_cutter = ring_y(
    X200_GROOVE_Y0,
    GROOVE_ROOT_D,
    SHAFT_D + 2 * MAX_RADIAL_GAP,
    GROOVE_W,
)
x200_housing = cut(x200_housing, x200_groove_cutter)
x200_shaft = cyl_y(
    X200_OLD_SEAL_Y0 - 2.0,
    SHAFT_D / 2.0,
    (X200_Z50_Y1 - X200_OLD_SEAL_Y0) + 4.0,
)
x200_z50_envelope = ring_y(
    X200_Z50_Y0,
    52.0,
    12.0,
    X200_Z50_Y1 - X200_Z50_Y0,
)

# Wheel fixed flange/housing sleeve over the new Ø18 dynamic seal land.
wheel_housing = ring_y(
    WHEEL_SEAL_LAND_Y0,
    FLANGE_OD,
    SHAFT_D + 2 * MAX_RADIAL_GAP,
    WHEEL_SEAL_LAND_Y1 - WHEEL_SEAL_LAND_Y0,
)
wheel_groove_cutter = ring_y(
    WHEEL_GROOVE_Y0,
    GROOVE_ROOT_D,
    SHAFT_D + 2 * MAX_RADIAL_GAP,
    GROOVE_W,
)
wheel_housing = cut(wheel_housing, wheel_groove_cutter)
wheel_shaft18 = cyl_y(
    WHEEL_SEAL_LAND_Y0,
    SHAFT_D / 2.0,
    WHEEL_SEAL_LAND_Y1 - WHEEL_SEAL_LAND_Y0,
)
wheel_seat17 = cyl_y(WHEEL_SEAT_Y0, WHEEL_SEAT_D / 2.0, 7.0)

# Packaging / geometry checks
x200_land_len = X200_OLD_SEAL_Y1 - X200_OLD_SEAL_Y0
x200_shoulder_in = X200_GROOVE_Y0 - X200_OLD_SEAL_Y0
x200_shoulder_out = X200_OLD_SEAL_Y1 - X200_GROOVE_Y1
wheel_land_len = WHEEL_SEAL_LAND_Y1 - WHEEL_SEAL_LAND_Y0
wheel_shoulder_in = WHEEL_GROOVE_Y0 - WHEEL_SEAL_LAND_Y0
wheel_shoulder_out = WHEEL_SEAL_LAND_Y1 - WHEEL_GROOVE_Y1
surface_speed = math.pi * (SHAFT_D / 1000.0) * (WHEEL_RPM / 60.0)
ring_id_oversize_pct = 100.0 * (QUADRING_ID - SHAFT_D) / SHAFT_D
radial_ligament_to_static_oring_id = (STATIC_FLANGE_ORING_ID - GROOVE_ROOT_D) / 2.0

checks = {
    'common_seal': {
        'part': 'Trelleborg QRAR04116-V7002 candidate',
        'natural_id_mm': QUADRING_ID,
        'cross_section_mm': QUADRING_CS,
        'shaft_d_mm': SHAFT_D,
        'shaft_fit': 'f7 target per rotary table',
        'groove_root_d_mm': GROOVE_ROOT_D,
        'groove_root_fit': 'H8 target per rotary table',
        'groove_width_mm': GROOVE_W,
        'groove_width_tolerance_plus_mm': 0.2,
        'groove_corner_radius_mm': GROOVE_R,
        'max_radial_extrusion_gap_mm': MAX_RADIAL_GAP,
        'seal_id_larger_than_shaft_pct': ring_id_oversize_pct,
    },
    'x200': {
        'old_seal_zone_length_mm': x200_land_len,
        'groove_y_mm': [X200_GROOVE_Y0, X200_GROOVE_Y1],
        'inboard_shoulder_mm': x200_shoulder_in,
        'outboard_shoulder_mm': x200_shoulder_out,
        'gap_groove_to_z50_mm': X200_Z50_Y0 - X200_GROOVE_Y1,
        'housing_od_mm': X200_HOUSING_OD,
        'housing_valid': x200_housing.val().isValid(),
        'shaft_valid': x200_shaft.val().isValid(),
        'housing_z50_intersection_mm3': inter_vol(x200_housing, x200_z50_envelope),
    },
    'wheel_station': {
        '61903_end_y_mm': BEARING_61903_Y1,
        'seal_land_y_mm': [WHEEL_SEAL_LAND_Y0, WHEEL_SEAL_LAND_Y1],
        'seal_land_length_mm': wheel_land_len,
        'groove_y_mm': [WHEEL_GROOVE_Y0, WHEEL_GROOVE_Y1],
        'inboard_shoulder_mm': wheel_shoulder_in,
        'outboard_shoulder_mm': wheel_shoulder_out,
        'wheel_seat_start_y_mm': WHEEL_SEAT_Y0,
        'wheel_seat_d_mm': WHEEL_SEAT_D,
        'radial_ligament_groove_root_to_static_oring_id_mm': radial_ligament_to_static_oring_id,
        'housing_valid': wheel_housing.val().isValid(),
        'shaft_valid': wheel_shaft18.val().isValid(),
        'seal_land_to_wheel_seat_axial_gap_mm': WHEEL_SEAT_Y0 - WHEEL_SEAL_LAND_Y1,
    },
    'kinematics': {
        'motor_rpm_reference': MOTOR_RPM,
        'bevel_ratio': BEVEL_RATIO,
        'shaft_rpm_reference': WHEEL_RPM,
        'shaft_surface_speed_m_s': surface_speed,
    },
}

pass_rules = {
    'x200_inboard_shoulder_ge_1_5': x200_shoulder_in >= 1.5,
    'x200_outboard_shoulder_ge_1_5': x200_shoulder_out >= 1.5,
    'x200_gap_to_z50_ge_0_4': (X200_Z50_Y0 - X200_GROOVE_Y1) >= 0.4,
    'x200_zero_housing_z50_collision': inter_vol(x200_housing, x200_z50_envelope) < 1e-6,
    'wheel_inboard_shoulder_ge_0_5': wheel_shoulder_in >= 0.5 - 1e-9,
    'wheel_outboard_shoulder_ge_0_5': wheel_shoulder_out >= 0.5 - 1e-9,
    'wheel_radial_ligament_ge_4_0': radial_ligament_to_static_oring_id >= 4.0,
    'wheel_seal_land_meets_wheel_seat_without_axial_gap': abs(WHEEL_SEAT_Y0 - WHEEL_SEAL_LAND_Y1) < 1e-9,
    'surface_speed_lt_0_1_m_s': surface_speed < 0.1,
    'seal_id_is_2_to_5_pct_larger_than_shaft': 2.0 <= ring_id_oversize_pct <= 5.0,
    'all_solids_valid': all([
        x200_housing.val().isValid(),
        x200_shaft.val().isValid(),
        wheel_housing.val().isValid(),
        wheel_shaft18.val().isValid(),
    ]),
}
checks['pass_rules'] = pass_rules
checks['status'] = 'PASS' if all(pass_rules.values()) else 'FAIL'

assy = cq.Assembly(name='PX1_Dynamic_Seals_RevGT')
assy.add(x200_housing, name='X200_Fixed_QuadRing_Housing')
assy.add(x200_shaft, name='X200_Shaft_D18')
assy.add(x200_z50_envelope, name='X200_Z50_Envelope')
assy.add(wheel_housing.translate((60, 0, 0)), name='Wheel_Fixed_QuadRing_Housing')
assy.add(wheel_shaft18.translate((60, 0, 0)), name='Wheel_Shaft_D18_SealLand')
assy.add(wheel_seat17.translate((60, 0, 0)), name='Wheel_Seat_D17')
assy.save(os.path.join(OUT, 'PX1_Dynamic_Seals_RevGT.step'))

with open(os.path.join(OUT, 'REV_GT_DYNAMIC_SEAL_VALIDATION.json'), 'w') as f:
    json.dump(checks, f, indent=2)

print(json.dumps(checks, indent=2))
if checks['status'] != 'PASS':
    raise SystemExit(2)
