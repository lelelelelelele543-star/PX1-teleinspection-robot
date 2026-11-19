#!/usr/bin/env python3
"""PX1 traction / speed budget (F09). Calculation only — not a measured result.

Every input carries a tag: CONFIRMED (source), DERIVED (computed), ESTIMATED (engineering guess).
Outputs JSON with motor-limited force, adhesion-limited force, and required pull for tether lengths.
"""
import argparse, ast, json, math
from collections import defaultdict
from pathlib import Path

ROOT = Path(__file__).resolve().parents[2]
G = 9.81

INPUTS = {
    'motor_rated_torque_Nm': (0.6865, 'CONFIRMED', 'NFP GA24Y-370-2485 138:1 table, 7 kgf·cm (08_PROCUREMENT/GA24Y_370_SELECTION_20261119.md)'),
    'motor_rated_rpm': (52.0, 'CONFIRMED', 'same table, rated speed'),
    'motor_no_load_rpm': (61.0, 'CONFIRMED', 'same table'),
    'motors': (2, 'CONFIRMED', 'frozen baseline: two traction motors'),
    'bevel_ratio': (40/16, 'CONFIRMED', 'Z16->Z40 GEA-002-531/-530'),
    'z50_train_ratio': (1.0, 'DERIVED', '5x Z50 idler train, equal teeth'),
    'drivetrain_efficiency': (0.75, 'ESTIMATED', 'bevel ~0.95, 4 spur meshes ~0.97^4, seals/X-rings/bearings'),
    'wheel_rolling_radius_m': (0.045, 'CONFIRMED', 'QRW90 D90 crown (catalogue 90 mm wheel)'),
    'proteus_crp150_mass_kg': (9.25, 'CONFIRMED', 'Mini-Cam catalogue via GAP Group sy1083, CRP150 9.25 kg'),
    'mu_wheel_pipe': ({'slime/grease': 0.3, 'wet concrete/PVC': 0.5, 'dry/clean': 0.7}, 'ESTIMATED', 'soft rubber on pipe wall'),
    'rolling_resistance_coeff': (0.03, 'ESTIMATED', 'soft rubber tyre'),
    'pipe_slope': (0.02, 'ESTIMATED', 'gravity sewer up-slope 2%'),
    'tether_linear_mass_kg_per_m': (0.12, 'ESTIMATED', '6-core reinforced copper ~Ø9 (article HOLD H07)'),
    'tether_friction_coeff': (0.3, 'ESTIMATED', 'PU jacket on wet pipe invert, straight pipe'),
    'tether_lengths_m': ([40, 100, 150], 'CONFIRMED', 'AGENTS.md: first 40 m, later 100-150 m'),
}
DENSITY = {  # g/cm3, ESTIMATED material assumptions per CAD category
    'body': 2.70, 'metal': 2.70, 'shaft': 7.85, 'gear': 7.85, 'bevel': 7.85, 'bearing': 7.80,
    'seal': 1.20, 'wheel': 1.20, 'purchased': 4.00, 'valve': 7.85, 'lift': 2.70, 'camera': 2.70,
    'connector': 4.00, 'wire': 8.9, 'cable': 2.0, 'print': 1.2, 'electronics': 1.5, 'electronics_hold': 1.5}


def master_constants(path):
    vals = {}
    for node in ast.parse(path.read_text()).body:
        if isinstance(node, ast.Assign):
            try: v = ast.literal_eval(node.value)
            except (ValueError, TypeError): continue
            for t in node.targets:
                if isinstance(t, ast.Name): vals[t.id] = v
    return vals


# Mini-Cam part-code prefixes in DRW-002-374/375/386: FAL = aluminium, FSS = stainless, FBR = brass.
NAME_DENSITY = [  # (substring, g/cm3, reason) — first match wins, overrides category
    ('WEIGHT_PLATE', 7.9, 'FSS-002-060 Waight Plate (DRW375)'),
    ('AXLE_FLANGE', 7.9, 'FSS-002-061 Axle Flange (DRW374)'),
    ('LIFT_SIDE_ARM', 7.9, 'FSS lift parts (DRW375 FSS-002-084/373)'),
    ('LIFT_SIDE_PIN', 7.9, 'FSS-002-373 Axle Lift'),
    ('SIDE_COVER', 2.7, 'FAL-002-062 Side cover'),
    ('PRESSURE_BODY', 2.7, 'FAL-002-058 Crawler Housing'),
]


def cad_mass(registry):
    by = defaultdict(float)
    for item in registry:
        rho = DENSITY.get(item['category'], 2.7)
        key = item['category']
        for sub, d, _ in NAME_DENSITY:
            if sub in item['id']:
                rho, key = d, sub
                break
        by[key] += item.get('volume_mm3', 0.0) / 1000.0 * rho
    mass = {k: v / 1000.0 for k, v in by.items()}
    return sum(mass.values()), {k: round(v, 3) for k, v in sorted(mass.items(), key=lambda kv: -kv[1])}


def main():
    ap = argparse.ArgumentParser(description=__doc__)
    ap.add_argument('--registry', type=Path, default=ROOT/'current/component_registry.json')
    ap.add_argument('--out', type=Path, default=ROOT/'current/07_TESTS/traction_budget_F09.json')
    ap.add_argument('--motor-torque', type=float, help='override continuous output torque per motor, N·m')
    ap.add_argument('--motor-rpm', type=float, help='override loaded output speed, rpm')
    ap.add_argument('--label', default='GA24Y-370-2485 138:1')
    a = ap.parse_args()
    if a.motor_torque: INPUTS['motor_rated_torque_Nm'] = (a.motor_torque, 'ESTIMATED', f'candidate {a.label}')
    if a.motor_rpm: INPUTS['motor_rated_rpm'] = (a.motor_rpm, 'ESTIMATED', f'candidate {a.label}'); INPUTS['motor_no_load_rpm'] = (a.motor_rpm*1.08, 'ESTIMATED', 'no-load ~ loaded x1.08')
    v = {k: x[0] for k, x in INPUTS.items()}
    c = master_constants(ROOT/'current/CAD/PX1_Current_Master.py')
    # Contact geometry DERIVED from master: crown contacts on lower wall, normal tilted.
    cos_n = math.sqrt(c['PIPE_R']**2 - c['WHEEL_CENTRE_Y']**2) / c['PIPE_R']
    normal_factor = 1.0 / cos_n                   # sum of contact normals / weight
    T_wheel = v['motors'] * v['motor_rated_torque_Nm'] * v['bevel_ratio'] * v['z50_train_ratio'] * v['drivetrain_efficiency']
    F_motor = T_wheel / v['wheel_rolling_radius_m']
    wheel_rpm = v['motor_rated_rpm'] / v['bevel_ratio']
    speed = wheel_rpm * 2 * math.pi * v['wheel_rolling_radius_m']
    speed_nl = v['motor_no_load_rpm'] / v['bevel_ratio'] * 2 * math.pi * v['wheel_rolling_radius_m']
    m_cad, m_parts = cad_mass(json.loads(a.registry.read_text()))
    cases = {'PX1_CAD_estimate': m_cad, 'Proteus_CRP150_mass': v['proteus_crp150_mass_kg']}
    out = {'status': 'CALCULATION_ONLY_NOT_MEASURED', 'inputs': {k: {'value': x[0], 'tag': x[1], 'source': x[2]} for k, x in INPUTS.items()},
           'derived': {'contact_normal_vertical_fraction': cos_n, 'normal_force_factor': normal_factor,
                       'wheel_torque_total_Nm': T_wheel, 'motor_limited_force_N': F_motor,
                       'wheel_rpm_rated': wheel_rpm, 'speed_rated_m_min': speed, 'speed_no_load_m_min': speed_nl},
           'cad_mass_estimate': {'total_kg': m_cad, 'by_category_kg': m_parts, 'tag': 'ESTIMATED (densities assumed, many envelope solids)'},
           'cases': {}}
    for name, m in cases.items():
        W = m * G
        base = W * (v['rolling_resistance_coeff'] + v['pipe_slope'])
        adh = {k: mu * W * normal_factor for k, mu in v['mu_wheel_pipe'].items()}
        rows = []
        for L in v['tether_lengths_m']:
            tether = v['tether_linear_mass_kg_per_m'] * L * G * v['tether_friction_coeff']
            req = base + tether
            limit = {k: min(F_motor, f) for k, f in adh.items()}
            rows.append({'tether_m': L, 'tether_drag_N': round(tether, 1), 'required_N': round(req, 1),
                         'available_N': {k: round(f, 1) for k, f in limit.items()},
                         'margin_N': {k: round(f - req, 1) for k, f in limit.items()},
                         'ok': {k: f >= req for k, f in limit.items()}})
        out['cases'][name] = {'mass_kg': round(m, 2), 'weight_N': round(W, 1), 'base_resistance_N': round(base, 1),
                              'adhesion_limit_N': {k: round(f, 1) for k, f in adh.items()}, 'by_tether_length': rows}
    a.out.parent.mkdir(parents=True, exist_ok=True)
    a.out.write_text(json.dumps(out, ensure_ascii=False, indent=2) + '\n')
    print(json.dumps({'motor_limited_force_N': round(F_motor, 1), 'speed_rated_m_min': round(speed, 2),
                      'cad_mass_kg': round(m_cad, 2), 'cases': {n: {'adhesion': c_['adhesion_limit_N'],
                      'tether': [(r['tether_m'], r['required_N'], r['ok']) for r in c_['by_tether_length']]}
                      for n, c_ in out['cases'].items()}}, ensure_ascii=False, indent=1))

if __name__ == '__main__':
    main()
