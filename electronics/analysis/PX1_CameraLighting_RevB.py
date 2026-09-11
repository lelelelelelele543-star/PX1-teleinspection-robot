import math, json

# PX-1 Rev.B WB14 — camera front LED ring + slip-ring packaging screen
# Analytical screening only; exact purchased MCPCB/lens/front-retainer CAD governs release.

HEAD_OD_MM = 52.0
WINDOW_OD_MM = 28.0
LED_BOARD_BOX_MM = 8.0  # worst-case square envelope for an 8 mm-class MCPCB
LED_PCD_MM = 40.0
LED_COUNT = 6

ROLL_BEARING_ID_MM = 17.0  # 6803 / 61803
CAM_SLIP_RING_OD_MM = 12.5 # SenRing M125
CAM_SLIP_RING_L_MM = 13.5

LED_CURRENT_A = 0.300
CAMERA_12V_DESIGN_A = 0.120
P4115_MIN_HEADROOM_V = 2.0

r = LED_PCD_MM / 2.0
h = LED_BOARD_BOX_MM / 2.0
head_r = HEAD_OD_MM / 2.0
window_r = WINDOW_OD_MM / 2.0

# Boards are treated as 8x8 squares locally aligned radial/tangential.
outer_corner_r = math.hypot(r + h, h)
inner_corner_r = math.hypot(r - h, h)
adjacent_centres = 2.0 * r * math.sin(math.pi / LED_COUNT)
board_diagonal = LED_BOARD_BOX_MM * math.sqrt(2.0)

geom = {
    'head_od_mm': HEAD_OD_MM,
    'window_od_mm': WINDOW_OD_MM,
    'led_count': LED_COUNT,
    'led_board_worst_case_box_mm': LED_BOARD_BOX_MM,
    'led_pcd_mm': LED_PCD_MM,
    'outer_corner_radius_mm': outer_corner_r,
    'outer_radial_margin_to_head_od_mm': head_r - outer_corner_r,
    'inner_corner_radius_mm': inner_corner_r,
    'inner_radial_margin_to_window_mm': inner_corner_r - window_r,
    'adjacent_centre_spacing_mm': adjacent_centres,
    'board_diagonal_mm': board_diagonal,
    'minimum_simple_interboard_gap_mm': adjacent_centres - board_diagonal,
}

slip = {
    'bearing_id_mm': ROLL_BEARING_ID_MM,
    'slip_ring_od_mm': CAM_SLIP_RING_OD_MM,
    'slip_ring_length_mm': CAM_SLIP_RING_L_MM,
    'diametral_clearance_mm': ROLL_BEARING_ID_MM - CAM_SLIP_RING_OD_MM,
    'radial_clearance_mm': (ROLL_BEARING_ID_MM - CAM_SLIP_RING_OD_MM) / 2.0,
}

# Three white LEDs per P4115adj string on nominal 12 V.
# Do not infer final Vf; screen a useful range and make release conditional on measured sample.
dropout = {}
for vf in (2.8, 2.9, 3.0, 3.1, 3.2, 3.3, 3.4):
    string_v = 3.0 * vf
    headroom = 12.0 - string_v
    dropout[f'{vf:.1f}'] = {
        'string_v': string_v,
        'headroom_v_at_12V': headroom,
        'meets_2V_screen_at_exact_12V': headroom >= P4115_MIN_HEADROOM_V,
        'six_led_electrical_power_W_at_300mA': 6.0 * vf * LED_CURRENT_A,
    }

result = {
    'status_geometry': 'PASS_SCREEN' if (
        geom['outer_radial_margin_to_head_od_mm'] > 1.0 and
        geom['inner_radial_margin_to_window_mm'] > 1.0 and
        geom['minimum_simple_interboard_gap_mm'] > 1.0 and
        slip['radial_clearance_mm'] > 1.0
    ) else 'FAIL_SCREEN',
    'status_led_driver': 'HOLD_MEASURED_VF_AND_12V_MIN',
    'geometry': geom,
    'camera_slip_ring': slip,
    'camera_power_reservation': {
        'camera_12V_design_A': CAMERA_12V_DESIGN_A,
        'camera_12V_design_W': 12.0 * CAMERA_12V_DESIGN_A,
        'M125_per_circuit_rating_A': 1.5,
        'simple_current_margin_ratio': 1.5 / CAMERA_12V_DESIGN_A,
    },
    'lighting': {
        'topology': '2 independent strings x 3 LEDs, 1 P4115adj per string',
        'initial_string_current_A': LED_CURRENT_A,
        'p4115_min_headroom_screen_V': P4115_MIN_HEADROOM_V,
        'dropout_screen_by_single_LED_Vf': dropout,
    },
    'release_holds': [
        'actual 8mm MCPCB thickness/shape and exact emitter order code',
        'front window O-ring groove and bezel/retainer fastener solids',
        'actual 12V minimum rail at camera head under simultaneous axis load',
        'three-LED cold/hot forward-voltage at 300mA',
        'physical placement of two P4115adj boards on fixed-side carrier',
        'full-light thermal test and CVBS PWM-noise test',
        'exact M125-06 sample/drawing and raw-CVBS rotation test'
    ]
}

print(json.dumps(result, indent=2))
