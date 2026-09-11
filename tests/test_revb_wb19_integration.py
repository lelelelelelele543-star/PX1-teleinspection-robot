import json
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
VALIDATION = ROOT / 'mechanical' / 'REV_B_WB19_VALIDATION.json'


def load_validation():
    return json.loads(VALIDATION.read_text(encoding='utf-8'))


def test_wb19_keeps_hard_six_wheel_architecture():
    v = load_validation()
    a = v['architecture']
    assert a['axles'] == 3
    assert a['wheels_total'] == 6
    assert a['wheel_x_mm'] == [50.0, 150.0, 250.0]
    assert a['drive_station_x_mm'] == 250.0


def test_wb19_candidate_does_not_collide_with_tilt_sweep():
    v = load_validation()
    c = v['candidate_SP13']
    assert c['max_moving_vs_candidate_fixed_collision_mm3'] <= 1e-4
    assert c['fixed_package_min_ideal_DN150_clearance_mm'] >= 5.0
    assert c['moving_camera_min_ideal_DN150_clearance_mm'] >= 3.0


def test_wb19_low_r55_route_meets_screen_clearances():
    v = load_validation()
    low = v['R55_harness_screen']['position_routes']['LOW']
    assert low['min_ideal_DN150_cable_clearance_mm'] >= 5.0
    # Numeric JSON is produced from floating point geometry; 2.999 is the guard threshold.
    assert low['min_central_body_clearance_mm'] >= 2.999


def test_wb19_current_wb18_connector_is_rejected_for_r55_body_routing():
    v = load_validation()
    f = v['current_WB18_routing_failure']
    assert f['minimum_forward_run_for_that_R55_rise_mm'] > f['available_forward_run_before_saddle_mm']
    assert v['status'].startswith('PASS_SCREEN')
