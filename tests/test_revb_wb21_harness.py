import json
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
VALIDATION = ROOT / 'mechanical' / 'REV_B_WB21_VALIDATION.json'


def load_validation():
    return json.loads(VALIDATION.read_text(encoding='utf-8'))


def test_wb21_preserves_six_wheel_architecture():
    v = load_validation()
    a = v['architecture']
    assert a['wheels_total'] == 6
    assert a['wheel_stations_x_mm'] == [50.0, 150.0, 250.0]
    assert a['z50_total'] == 10
    assert a['rear_drive_x_mm'] == 250.0


def test_wb21_worst_tolerance_bend_radius_meets_gate():
    v = load_validation()
    req = v['moving_flex']['required_min_radius_mm']
    states = v['moving_flex']['states']
    assert min(s['radius_at_plus_0p5_length_mm'] for s in states.values()) >= req
    assert states['MID']['radius_at_plus_0p5_length_mm'] > 42.0


def test_wb21_low_dn150_and_static_ingress_clearances():
    v = load_validation()
    assert v['moving_flex']['states']['LOW']['ideal_DN150_clearance_nominal_mm'] >= 5.0
    assert v['body_ingress']['gland_min_ideal_DN150_clearance_mm'] >= 5.0
    assert v['body_ingress']['static_cable_min_ideal_DN150_clearance_mm'] >= 5.0


def test_wb21_all_screened_solid_collisions_are_zero():
    v = load_validation()
    for state in ('LOW', 'MID', 'HIGH'):
        s = v['moving_flex']['states'][state]
        assert s['arm_collision_mm3'] <= 1e-4
        assert s['camera_fixed_collision_mm3'] <= 1e-4
        assert s['camera_moving_max_collision_mm3_1deg'] <= 1e-4
        for value in v['solid_collision_screen'][state].values():
            assert value <= 1e-4


def test_wb21_electrical_screen_has_margin():
    v = load_validation()
    e = v['electrical_screen']
    assert e['current_per_parallel_power_core_A'] < v['cable_candidate']['current_rating_per_core_A_at_30C']
    assert e['voltage_drop_percent_of_12V'] < 2.0
    assert v['status'].startswith('PASS_SCREEN')
