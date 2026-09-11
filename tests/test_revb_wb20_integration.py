import json
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
VALIDATION = ROOT / 'mechanical' / 'REV_B_WB20_VALIDATION.json'


def load_validation():
    return json.loads(VALIDATION.read_text(encoding='utf-8'))


def test_wb20_keeps_hard_six_wheel_architecture():
    v = load_validation()
    a = v['architecture']
    assert a['wheels_total'] == 6
    assert a['wheel_stations_x_mm'] == [50.0, 150.0, 250.0]
    assert a['z50_total'] == 10
    assert a['z50_positions_x_mm'] == [50.0, 100.0, 150.0, 200.0, 250.0]
    assert a['rear_drive_x_mm'] == 250.0


def test_wb20_full_tilt_screen_clears_floor_gears_and_ideal_dn150():
    v = load_validation()
    t = v['tilt_sweep']
    assert t['range_deg'] == [-105, 105]
    assert t['step_deg'] == 1
    assert t['moving_min_ideal_DN150_clearance_mm'] >= 3.0
    assert t['moving_min_floor_clearance_mm'] >= 3.0
    assert t['moving_lateral_gap_to_Z50_mm'] >= 2.0
    assert t['fixed_lateral_gap_to_Z50_mm'] >= 2.0


def test_wb20_repacked_electronics_remain_inside_dry_volume():
    v = load_validation()
    p = v['electronics_pack']
    assert all(x <= 1e-4 for x in p['component_outside_dry_volume_mm3'].values())
    assert p['component_intersections_mm3'] == {}


def test_wb20_gas_spring_has_end_margin_and_floor_clearance():
    v = load_validation()
    g = v['gas_spring']
    assert g['selected_prototype_family'] == 'ACE GS-12-20-V4A'
    assert g['compression_end_margin_mm'] >= 3.0
    assert g['extension_end_margin_mm'] >= 3.0
    assert min(p['floor_clearance_for_OD12_mm'] for p in g['positions'].values()) >= 3.0
    assert g['positions']['LOW']['ideal_DN150_clearance_for_OD12_mm'] >= 5.0
    assert v['status'].startswith('PASS_SCREEN')
