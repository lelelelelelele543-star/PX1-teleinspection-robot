import math

# PX-1 Rev.B Work Block 01
# X250 driven-station first-order packaging / torque screen.
# NOT a manufacturing release.

SIDE_BAY_DEPTH_MM = 12.0
COUPLING_HUB_OD_MM = 20.0
COUPLING_HUB_LEN_MM = 7.5
COUPLING_BORE_MM = 10.0
COUPLING_KEY_B_MM = 3.0
COUPLING_KEY_H_MM = 3.0
COUPLING_KEY_L_MM = 7.0
BEARING_6704 = (20.0, 27.0, 4.0)  # d, D, B
GEAR_FACE_MM = 4.0
GEAR_CLEARANCE_MM = 0.15
COVER_CLEARANCE_TARGET_MM = 0.30
DESIGN_TORQUE_NM = 4.0
Z50_PITCH_RADIUS_MM = 25.0
PRESSURE_ANGLE_DEG = 20.0
WHEEL_DIAMETER_MM = 90.0
BEVEL_RATIO = 2.5
MOTOR_RPM_RANGE = (45.0, 65.0)
MOTOR_TORQUE_RANGE_NM = (1.0, 1.3)


def key_stress(T_Nm, d_mm, b_mm, h_mm, l_mm):
    T_Nmm = T_Nm * 1000.0
    tau = 2.0 * T_Nmm / (d_mm * b_mm * l_mm)
    sigma_b = 4.0 * T_Nmm / (d_mm * h_mm * l_mm)
    return tau, sigma_b


def shaft_torsion(T_Nm, d_mm):
    T_Nmm = T_Nm * 1000.0
    return 16.0 * T_Nmm / (math.pi * d_mm**3)


def spur_mesh_force(T_Nm, pitch_radius_mm, pressure_angle_deg):
    Ft = T_Nm * 1000.0 / pitch_radius_mm
    Fr = Ft * math.tan(math.radians(pressure_angle_deg))
    resultant = math.hypot(Ft, Fr)
    return Ft, Fr, resultant


def crawler_speed(motor_rpm, bevel_ratio, wheel_diameter_mm):
    wheel_rpm = motor_rpm / bevel_ratio
    speed_m_s = math.pi * (wheel_diameter_mm / 1000.0) * wheel_rpm / 60.0
    return wheel_rpm, speed_m_s


def ideal_tractive_force(motor_torque_Nm, bevel_ratio, wheel_diameter_mm):
    side_torque = motor_torque_Nm * bevel_ratio
    radius_m = wheel_diameter_mm / 2000.0
    force = side_torque / radius_m
    return side_torque, force


# Local Y packaging: hub overlaps 6704 support.
bearing_y0 = COUPLING_HUB_LEN_MM - BEARING_6704[2]
bearing_y1 = COUPLING_HUB_LEN_MM
gear_y0 = bearing_y1 + GEAR_CLEARANCE_MM
gear_y1 = gear_y0 + GEAR_FACE_MM
cover_clearance = SIDE_BAY_DEPTH_MM - gear_y1

key_tau, key_bearing = key_stress(
    DESIGN_TORQUE_NM,
    COUPLING_BORE_MM,
    COUPLING_KEY_B_MM,
    COUPLING_KEY_H_MM,
    COUPLING_KEY_L_MM,
)
shaft_tau_12 = shaft_torsion(DESIGN_TORQUE_NM, 12.0)
Ft, Fr, Fresult = spur_mesh_force(
    DESIGN_TORQUE_NM,
    Z50_PITCH_RADIUS_MM,
    PRESSURE_ANGLE_DEG,
)

print("PX1 X250 Rev.B first-order screen")
print("----------------------------------")
print(f"Side bay depth: {SIDE_BAY_DEPTH_MM:.2f} mm")
print(f"Hub: OD {COUPLING_HUB_OD_MM:.1f} x L {COUPLING_HUB_LEN_MM:.1f} mm")
print(f"6704 zone: Y {bearing_y0:.2f}..{bearing_y1:.2f} mm")
print(f"Z50 B4 zone: Y {gear_y0:.2f}..{gear_y1:.2f} mm")
print(f"Nominal clearance to cover: {cover_clearance:.2f} mm")
print(f"Target minimum packaging clearance: {COVER_CLEARANCE_TARGET_MM:.2f} mm")
print("PACKAGING:", "PASS" if cover_clearance >= COVER_CLEARANCE_TARGET_MM else "HOLD")
print()
print(f"3x3x7 key shear @ {DESIGN_TORQUE_NM:.1f} N.m: {key_tau:.1f} MPa")
print(f"3x3x7 key bearing @ {DESIGN_TORQUE_NM:.1f} N.m: {key_bearing:.1f} MPa")
print(f"Ø12 shaft torsion @ {DESIGN_TORQUE_NM:.1f} N.m: {shaft_tau_12:.1f} MPa")
print(f"Z50 mesh force @ {DESIGN_TORQUE_NM:.1f} N.m: Ft={Ft:.1f} N, Fr={Fr:.1f} N, R={Fresult:.1f} N")
print()

for rpm in MOTOR_RPM_RANGE:
    wrpm, v = crawler_speed(rpm, BEVEL_RATIO, WHEEL_DIAMETER_MM)
    print(f"Motor geared output {rpm:.0f} rpm -> wheel {wrpm:.1f} rpm -> {v:.3f} m/s")

for torque in MOTOR_TORQUE_RANGE_NM:
    side_torque, force = ideal_tractive_force(torque, BEVEL_RATIO, WHEEL_DIAMETER_MM)
    print(f"Motor {torque:.1f} N.m -> ideal side torque {side_torque:.2f} N.m -> {force:.1f} N/side")

print()
print("Release holds:")
print("- exact 6704 brand/internal clearance and fit")
print("- full coupling keyway stress concentration / fatigue")
print("- real Z50 hub/retention geometry")
print("- complete outboard 61801 + 61903 + X-ring flange solid")
print("- full DN150 solid sweep")
print("- first-article torque/seal/immersion test")
