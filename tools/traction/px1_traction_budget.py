#!/usr/bin/env python3
"""PX1 traction / speed budget (F09, motor/rolling/tether corrected 2026-11-20). Calculation only — not measured.

Usage: python tools/traction/px1_traction_budget.py --out current/07_TESTS/traction_budget_F17_steel.json
       [--motor zw62|ga24] [--ballast-density 17.5]

Every input carries a tag: CONFIRMED (source), DERIVED (computed), ESTIMATED (engineering guess).
Outputs JSON with motor-limited force, adhesion-limited force, and required pull for tether lengths.
"""
import argparse, ast, json, math
from collections import defaultdict
from pathlib import Path

ROOT = Path(__file__).resolve().parents[2]
G = 9.81

# ---- motor presets -------------------------------------------------------------------------------
# 'zw62' (default, current candidate F12/F16/F19): ZHAOWEI ZWSMD026026 3-stage i=62 + MP2238 24 V winding.
#   Rated output torque = 16.6 mN·m (CONFIRMED, MP2238-01 catalogue) x i x eta_gear.
#   eta_gear 0.81 ESTIMATED (3-stage planetary typ. 0.73-0.81; ZHAOWEI 26 mm page: max 87 % catalogue max).
#   Speeds DERIVED from the 24 V winding model of current/02_ELECTRICAL/POWER_BUDGET_F19_20261119.md
#   (R 8.0 Ohm, Kt 36 mN·m/A, friction 5.0 mN·m).
# 'ga24' (history, F09): NFP GA24Y-370-2485 138:1 table values.
ZW = dict(T_rated_mNm=16.6, Kt12=18.0, I_rated12=1.2, R12=2.0, i=62.0, eta=0.81, eta_max=0.87, V=24.0)


def zw62_preset():
    Kt = 2 * ZW['Kt12']; R = 4 * ZW['R12']                     # 24 V winding: 2x turns, same copper (DERIVED)
    Tf = ZW['Kt12'] * ZW['I_rated12'] - ZW['T_rated_mNm']       # 5.0 mN·m
    Ke = Kt / 1000

    def rpm_out(T_motor_mNm):
        I = (T_motor_mNm + Tf) / Kt
        return (ZW['V'] - I * R) / Ke * 60 / (2 * math.pi) / ZW['i'], I
    T_out = ZW['T_rated_mNm'] / 1000 * ZW['i'] * ZW['eta']
    n_rated, I_rated = rpm_out(ZW['T_rated_mNm'])
    n0, _ = rpm_out(0.0)
    n_1Nm, I_1Nm = rpm_out(1000 / (ZW['i'] * ZW['eta']))
    src = 'ZHAOWEI ZWSMD026026 i=62 + MP2238 24 V winding (candidate, not purchased)'
    return {
        'motor_rated_torque_Nm': (T_out, 'DERIVED', f'{src}: 16.6 mN·m CONFIRMED x 62 x eta 0.81 ESTIMATED (catalogue max 0.87 -> {16.6e-3*62*0.87:.3f})'),
        'motor_rated_rpm': (n_rated, 'DERIVED', f'24 V winding model at rated current {I_rated:.2f} A'),
        'motor_no_load_rpm': (n0, 'DERIVED', '24 V winding model, friction torque only'),
        'motor_1Nm_point': ({'T_out_Nm': 1.0, 'I_A': I_1Nm, 'n_out_rpm': n_1Nm, 'above_continuous': I_1Nm > I_rated},
                            'DERIVED', 'F12 1.0 N·m target is ABOVE the continuous rating: short-time only'),
    }


GA24 = {
    'motor_rated_torque_Nm': (0.6865, 'CONFIRMED', 'NFP GA24Y-370-2485 138:1 table, 7 kgf·cm (08_PROCUREMENT/GA24Y_370_SELECTION_20261119.md)'),
    'motor_rated_rpm': (52.0, 'CONFIRMED', 'same table, rated speed'),
    'motor_no_load_rpm': (61.0, 'CONFIRMED', 'same table'),
}

INPUTS = {
    'motors': (2, 'CONFIRMED', 'frozen baseline: two traction motors'),
    'bevel_ratio': (40/16, 'CONFIRMED', 'Z16->Z40 GEA-002-531/-530'),
    'z50_train_ratio': (1.0, 'DERIVED', '5x Z50 idler train, equal teeth'),
    'drivetrain_efficiency': (0.75, 'ESTIMATED', 'bevel ~0.95, 4 spur meshes ~0.97^4, seals/X-rings/bearings (motor gearhead not included)'),
    'wheel_rolling_radius_m': (0.045, 'CONFIRMED', 'QRW90 D90 crown (catalogue 90 mm wheel)'),
    'proteus_crp150_mass_kg': (9.25, 'CONFIRMED', 'Mini-Cam catalogue via GAP Group sy1083, CRP150 9.25 kg'),
    'mu_wheel_pipe': ({'slime/grease': 0.3, 'wet concrete/PVC': 0.5, 'dry/clean': 0.7}, 'ESTIMATED', 'soft rubber on pipe wall'),
    'rolling_resistance_coeff': (0.03, 'ESTIMATED', 'soft rubber tyre; applied to the wall NORMAL force (x normal_force_factor) since 2026-11-20'),
    'pipe_slope': (0.02, 'ESTIMATED', 'gravity sewer up-slope 2%'),
    'tether_linear_mass_kg_per_m': (0.07, 'ESTIMATED', 'Proteus cable Ø6.8 CONFIRMED; 6x0.5 mm² + PU ~0.06-0.08 kg/m (05_TETHER_REEL/TETHER_CABLE_SEARCH_20261119.md)'),
    'tether_linear_mass_conservative_kg_per_m': (0.12, 'ESTIMATED', 'F09 conservative case (reinforced ~Ø9 cable)'),
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
    ('BALLAST', 7.85, 'F17 ballast blocks, steel by default (override --ballast-density)'),
    ('QRW90_HUB_AL', 2.7, 'F17 wheel hub, aluminium ESTIMATED'),
    ('WEIGHT_PLATE', 7.9, 'FSS-002-060 Waight Plate (DRW375)'),
    ('AXLE_FLANGE', 7.9, 'FSS-002-061 Axle Flange (DRW374)'),
    ('CAM026', 1.727, 'F18: CAM026 envelope density scaled to catalogue 0.864 kg (CONFIRMED mass)'),
    ('CENTRAL_LEVER_ASS002723', 2.7, 'F18: ASS-002-723 lever arm assy, Al body ESTIMATED'),
    ('_FSS0020', 7.9, 'F18: FSS lift parts DRW-002-744 (side links, axles, clamp axle, washer) stainless'),
    ('DIN2093', 7.85, 'F18: disc springs FIX-002-726 spring steel'),
    ('ISO4035', 7.9, 'F18: M10 nuts FIX-002-725 A2'),
    ('LIFT_GAS_SPRING', 7.9, 'F18: gas spring pins (FIX-002-749 M6x18) A2'),
    ('FSS001889', 7.9, 'F24: lock ring FSS-001-889 (DRW-002-752) stainless'),
    ('DIN471', 7.85, 'F24: retaining rings DIN 471 spring steel'),
    ('BRASS_SHIM', 8.5, 'F25: lift shims FBR-002-750/751 brass'),
    ('LIFT_GAS_SPRING_PIN', 7.9, 'F25: gas spring pins Ø4 A2'),
    ('SIDE_COVER', 2.7, 'FAL-002-062 Side cover'),
    ('CINCON_CQB150W', 2.546, 'F20: CQB150W envelope density scaled to datasheet 68 g (CONFIRMED mass)'),
    ('THERMAL_PAD', 3.0, 'F20: silicone gap pad ~3 g/cm3 ESTIMATED'),
    ('BRAKE_SHUNT_10R', 2.7, 'F20: Al-housed resistor envelope, aluminium ESTIMATED'),
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
    ap.add_argument('--out', type=Path, required=True,
                    help='output JSON (required: no silent overwrite of the F09 history file)')
    ap.add_argument('--motor', choices=['zw62', 'ga24'], default='zw62',
                    help='zw62 = current candidate (default); ga24 = F09 history')
    ap.add_argument('--motor-torque', type=float, help='override continuous output torque per motor, N·m')
    ap.add_argument('--motor-rpm', type=float, help='override loaded output speed, rpm')
    ap.add_argument('--label', default=None)
    ap.add_argument('--ballast-density', type=float, help='g/cm3 for HOLD_BALLAST blocks (steel 7.85, W-alloy 17.5)')
    a = ap.parse_args()
    if a.out.resolve() == (ROOT/'current/07_TESTS/traction_budget_F09.json').resolve() and a.motor != 'ga24':
        ap.error('traction_budget_F09.json is the GA24 history file; use --motor ga24 or another --out')
    INPUTS.update(zw62_preset() if a.motor == 'zw62' else GA24)
    label = a.label or ('ZW026 i62 + MP2238 24V' if a.motor == 'zw62' else 'GA24Y-370-2485 138:1')
    if a.motor_torque: INPUTS['motor_rated_torque_Nm'] = (a.motor_torque, 'ESTIMATED', f'override {label}')
    if a.motor_rpm: INPUTS['motor_rated_rpm'] = (a.motor_rpm, 'ESTIMATED', f'override {label}'); INPUTS['motor_no_load_rpm'] = (a.motor_rpm*1.08, 'ESTIMATED', 'no-load ~ loaded x1.08')
    if a.ballast_density:
        NAME_DENSITY[0] = ('BALLAST', a.ballast_density, f'ballast override {a.ballast_density}')
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
    out['motor_preset'] = a.motor
    for name, m in cases.items():
        W = m * G
        # rolling resistance acts on the wall normal force (= W x normal_factor), slope on the weight
        base = W * (v['rolling_resistance_coeff'] * normal_factor + v['pipe_slope'])
        adh = {k: mu * W * normal_factor for k, mu in v['mu_wheel_pipe'].items()}
        limit = {k: min(F_motor, f) for k, f in adh.items()}
        rows = []
        for L in v['tether_lengths_m']:
            row = {'tether_m': L}
            for suf, mpl in (('', v['tether_linear_mass_kg_per_m']), ('_conservative', v['tether_linear_mass_conservative_kg_per_m'])):
                tether = mpl * L * G * v['tether_friction_coeff']
                req = base + tether
                row.update({f'tether_drag_N{suf}': round(tether, 1), f'required_N{suf}': round(req, 1),
                            f'margin_N{suf}': {k: round(f - req, 1) for k, f in limit.items()},
                            f'ok{suf}': {k: f >= req for k, f in limit.items()}})
            row['available_N'] = {k: round(f, 1) for k, f in limit.items()}
            rows.append(row)
        out['cases'][name] = {'mass_kg': round(m, 2), 'weight_N': round(W, 1), 'base_resistance_N': round(base, 1),
                              'adhesion_limit_N': {k: round(f, 1) for k, f in adh.items()}, 'by_tether_length': rows}
    a.out.parent.mkdir(parents=True, exist_ok=True)
    a.out.write_text(json.dumps(out, ensure_ascii=False, indent=2) + '\n')
    print(json.dumps({'motor_limited_force_N': round(F_motor, 1), 'speed_rated_m_min': round(speed, 2),
                      'cad_mass_kg': round(m_cad, 2), 'cases': {n: {'adhesion': c_['adhesion_limit_N'],
                      'tether': [(r['tether_m'], r['required_N'], r['required_N_conservative'], r['margin_N']) for r in c_['by_tether_length']]}
                      for n, c_ in out['cases'].items()}}, ensure_ascii=False, indent=1))

if __name__ == '__main__':
    main()
