#!/usr/bin/env python3
"""F18 camera-lift kinematic check (DRW-002-744 parallelogram) from PX1_Current_Master.py constants.

The master is parsed with ``ast`` (tools/drawing_measure/check_master_vs_drawings.read_master),
never imported or executed. Checks:
  * camera axis height folded / raised vs CRP150 catalogue 70..257 mm (+-5), CONFIRMED range;
  * parallelogram closure (model exact; drawing AC/BD/AB/CD spread reported);
  * gas spring eye-to-eye over 0..theta_max within ACE bare limits;
  * swept 2-D clearance (XZ) of the translating camera/lift-housing group against the
    crawler housing + service cover (Y overlap assumed, conservative);
  * informative: spring vs gravity moment about A (masses ESTIMATED);
  * F21 camera harness LAPP 0028679: cable length need between the housing clamp P (moves with the lift
    housing) and the fixed point K on the gland bend guide over 0..theta_max, as the shortest planar path with
    bend radius >= 5xOD (Dubins CSC/CCC) through the two sliding lever clips, vs the modeled folded route
    HARNESS_ROUTE. PASS if slack (modeled - need at 0) >= max need increase + 10 mm.
Exit 0 only if every PASS criterion holds.
"""
from __future__ import annotations
import argparse, json, math, sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[2]
sys.path.insert(0, str(ROOT / 'tools' / 'drawing_measure'))
from check_master_vs_drawings import read_master  # noqa: E402

# DRW-002-744 values as recovered (DERIVED), for the closure report only.
DRAWING = {'AC': 200.1, 'BD': 200.0, 'AB': 40.2, 'CD': 40.4}
TOL_HEIGHT = 5.0


def rot(v, t):
    """Rotate a vector (dx toward camera = -X, dz up) upward by t rad; returns PX1 (dX, dZ)."""
    x, z = -v[0], v[1]
    return (x*math.cos(t) + z*math.sin(t), -x*math.sin(t) + z*math.cos(t))


TAU = 2*math.pi


def dubins(p0, h0, p1, h1, R):
    """Shortest planar (X, Z) path length with curvature <= 1/R between oriented points (CSC and CCC words)."""
    def m2(a): return a % TAU
    def ctr(p, h, s): return (p[0] - s*R*math.sin(h), p[1] + s*R*math.cos(h))
    best = float('inf')
    for s0 in (1, -1):
        for s1 in (1, -1):
            c0, c1 = ctr(p0, h0, s0), ctr(p1, h1, s1)
            dx, dz = c1[0] - c0[0], c1[1] - c0[1]; d = math.hypot(dx, dz); th = math.atan2(dz, dx)
            if s0 == s1:
                ln, phi = d, th
            else:
                if d < 2*R:
                    continue
                ln = math.sqrt(d*d - 4*R*R); phi = th + s0*math.atan2(2*R, ln)
            best = min(best, R*m2(s0*(phi - h0)) + ln + R*m2(s1*(h1 - phi)))
        s = s0; c0, c1 = ctr(p0, h0, s), ctr(p1, h1, s)
        dx, dz = c1[0] - c0[0], c1[1] - c0[1]; d = math.hypot(dx, dz)
        if 1e-9 < d <= 4*R:
            hg = math.sqrt(4*R*R - (d/2)**2)
            for k in (1, -1):
                mm = (c0[0] + dx/2 - k*hg*dz/d, c0[1] + dz/2 + k*hg*dx/d)
                f1 = math.atan2(mm[1] - c0[1], mm[0] - c0[0]) + s*math.pi/2
                f2 = math.atan2(c1[1] - mm[1], c1[0] - mm[0]) - s*math.pi/2
                best = min(best, R*(m2(s*(f1 - h0)) + m2(-s*(f2 - f1)) + m2(s*(h1 - f2))))
    return best


def route_walk(start, route):
    """3-D walk of HARNESS_ROUTE (same convention as the master): returns per-segment (end point, end tangent, length, R)."""
    def add(a, b, k=1.0): return tuple(x + k*y for x, y in zip(a, b))
    def cross(a, b): return (a[1]*b[2] - a[2]*b[1], a[2]*b[0] - a[0]*b[2], a[0]*b[1] - a[1]*b[0])
    p, t, out = tuple(start), (1.0, 0.0, 0.0), []
    for sg in route:
        if sg[0] == 'S':
            p = add(p, t, sg[1]); out.append((p, t, sg[1], None))
        else:
            R, a = sg[1], math.radians(sg[2]); n = cross(sg[3], t); c = add(p, n, R)
            p = add(add(c, n, -R*math.cos(a)), t, R*math.sin(a))
            t = add(tuple(x*math.cos(a) for x in t), n, math.sin(a)); out.append((p, t, R*a, R))
    return out


def harness_check(m, L, AX, AZ, tmax, step):
    walk = route_walk(m['HARNESS_START'], m['HARNESS_ROUTE'])
    iP, iK = m['HARNESS_SEG_P'], m['HARNESS_SEG_K']
    P0, K, tK = walk[iP-1][0], walk[iK-1][0], walk[iK-1][1]
    hK = math.atan2(tK[2], tK[0]); Hz = m['HARNESS_TOP_Z']; g1, g2 = m['HARNESS_GUIDE_X']
    Rf = m['HARNESS_R_FLEX']; end = walk[-1][0]
    L_model = sum(w[2] for w in walk); L_fixed = sum(w[2] for w in walk[:iP]) + sum(w[2] for w in walk[iK:])
    def lever(th, x):  # lever-frame point at folded X on the cable level, rotated about A
        d, h = AX - x, Hz - AZ
        return (AX - d*math.cos(th) + h*math.sin(th), AZ + d*math.sin(th) + h*math.cos(th))
    rows = []; theta = 0.0
    while True:
        th = math.radians(theta); dx, dz = L*(1 - math.cos(th)), L*math.sin(th)
        P = (P0[0] + dx, P0[2] + dz); Q1, Q2 = lever(th, g1), lever(th, g2)
        s1 = dubins(P, 0.0, Q1, -th, Rf); s2 = dubins(Q2, -th, (K[0], K[2]), hK, Rf)
        rows.append({'theta_deg': round(theta, 3), 'span_P_to_clip1_mm': round(s1, 2), 'span_clip2_to_K_mm': round(s2, 2),
                     'need_total_mm': round(L_fixed + s1 + (g2 - g1) + s2, 2)})
        if theta >= tmax - 1e-9:
            break
        theta = min(theta + step, tmax)
    n0 = rows[0]['need_total_mm']; worst = max(rows, key=lambda r: r['need_total_mm'])
    dmax = worst['need_total_mm'] - n0; slack = L_model - n0
    dyn = [w[3] for w in walk[iP:iK] if w[3] is not None]
    fixed = [w[3] for w in walk[:iP] + walk[iK:] if w[3] is not None]
    checks = {
        'route_ends_at_gland_exit': math.dist(end, (m['CAM_GLAND_XY'][0], m['CAM_GLAND_XY'][1], m['GLAND_EXIT_Z'] - 6.0)) < 1e-6,
        'dynamic_bends_ge_5xOD': min(dyn) >= m['HARNESS_R_FLEX'] - 1e-9,
        'harness_slack_ge_need_plus_10': slack >= max(dmax, 0.0) + 10.0 - 1e-9,
    }
    sp13_ok = all(r >= m['HARNESS_R_FIXED_MIN'] - 1e-9 for r in fixed if r != m['HARNESS_R_SP13'])
    return checks, {
        'cable': 'LAPP UNITRONIC FD P plus A 0028679, OD %.1f (CONFIRMED), min bend 5xD flexing = %.1f / 3xD fixed = %.1f (CONFIRMED LAPP)'
                 % (m['HARNESS_OD'], m['HARNESS_R_FLEX'], m['HARNESS_R_FIXED_MIN']),
        'modeled_route_length_mm': round(L_model, 2), 'fixed_parts_length_mm': round(L_fixed, 2),
        'need_mm': {'theta_0': n0, 'theta_max': rows[-1]['need_total_mm'], 'max': worst['need_total_mm'], 'max_at_deg': worst['theta_deg']},
        'need_increase_max_mm': round(dmax, 2), 'need_change_at_theta_max_mm': round(rows[-1]['need_total_mm'] - n0, 2),
        'slack_mm': round(slack, 2), 'margin_mm': round(slack - max(dmax, 0.0) - 10.0, 2),
        'points_folded_mm': {'P_housing_clamp': [round(v, 3) for v in P0], 'clip_1_x': g1, 'clip_2_x': g2,
                             'K_fixed_guide': [round(v, 3) for v in K], 'K_heading_deg': round(math.degrees(hK), 3)},
        'bend_radii_mm': {'dynamic_min': min(dyn), 'fixed': fixed, 'fixed_ge_3xOD_except_SP13_exit': sp13_ok,
                          'sp13_exit_R_HOLD': m['HARNESS_R_SP13']},
        'method': 'need(theta) = fixed parts + Dubins(P(theta) heading +X -> clip 1 on lever, heading along lever) + clip pitch '
                  '(cable slides through open clips) + Dubins(clip 2 -> K heading %.1f deg); R = 5xOD; obstacles ignored (lower bound).'
                  % math.degrees(hK),
        'samples': rows[::10] + ([rows[-1]] if (len(rows) - 1) % 10 else []),
        'limits': 'Planar XZ need; the S-loop lies on the lever plate (XY) and is not tensioned. SP13 exit bend R%.1f < 3xOD is HOLD H07 '
                  '(90-degree SP13 boot or connector move). Intermediate-angle 3-D cable shape not modelled.' % m['HARNESS_R_SP13'],
    }


def overlap(a, b):
    return min(a[2], b[2]) - max(a[0], b[0]), min(a[3], b[3]) - max(a[1], b[1])


def main():
    ap = argparse.ArgumentParser(description=__doc__)
    ap.add_argument('--master', type=Path, default=ROOT / 'current/CAD/PX1_Current_Master.py')
    ap.add_argument('--out', type=Path, default=None)
    ap.add_argument('--step', type=float, default=0.5)
    args = ap.parse_args()
    m = read_master(args.master)
    AX, AZ, L = m['LIFT_A_X'], m['LIFT_A_Z'], m['LINK_L']
    tmax = m['LIFT_THETA_MAX']; lo_cat, hi_cat = m['LIFT_CAT_RANGE']
    ab, E, G = m['LIFT_AB'], m['LIFT_GAS_E'], m['LIFT_GAS_G']
    lo, hi = m['ACE_EXTENDED'] - m['ACE_STROKE'], m['ACE_EXTENDED']
    # Points (PX1 X, Z) in folded state.
    A = (AX, AZ); B = (AX - ab[0], AZ + ab[1]); C = (AX - L, AZ); D = (B[0] - L, B[1])
    para = {'AC': math.dist(A, C), 'BD': math.dist(B, D), 'AB': math.dist(A, B), 'CD': math.dist(C, D)}
    model_err = max(abs(para['AC'] - para['BD']), abs(para['AB'] - para['CD']))
    drawing_err = max(abs(DRAWING['AC'] - DRAWING['BD']), abs(DRAWING['AB'] - DRAWING['CD']))
    cam0 = AZ - m['CAM_DROP']
    samples = []; theta = 0.0; gas = []
    while theta <= tmax + 1e-9:
        t = math.radians(theta)
        g = rot(G, t); Ez = (AX - E[0], AZ + E[1])
        Lg = math.dist(Ez, (AX + g[0], AZ + g[1]))
        cz = AZ + L*math.sin(t); dx = L*(1 - math.cos(t))
        samples.append({'theta_deg': round(theta, 3), 'camera_axis_z_mm': round(cz - m['CAM_DROP'], 3),
                        'group_shift_x_mm': round(dx, 3), 'gas_eye_to_eye_mm': round(Lg, 3)})
        gas.append(Lg); theta += args.step
        if theta > tmax and abs(theta - args.step - tmax) > 1e-9:
            theta = tmax
    cam_max = cam0 + L*math.sin(math.radians(tmax))
    # Gas spring lever arm about A and moments (info).
    def arm(t):
        g = rot(G, t); e = (-E[0], E[1]); gg = (g[0], g[1])
        ux, uz = gg[0] - e[0], gg[1] - e[1]; n = math.hypot(ux, uz)
        return abs(e[0]*uz - e[1]*ux) / n
    # Translating group rectangles (X0, Z0, X1, Z1) at theta=0, from master geometry constants.
    lhx1 = 14.0; cam_rear = m['CAM_REAR_X']; cam_l, cam_w, cam_h = m['CAM026_ENVELOPE']; cz0 = m['CAM_Z']
    group = {'camera_CAM026': (cam_rear - cam_l, cz0 - cam_h/2, cam_rear, cz0 + cam_h/2),
             'lift_housing_block': (lhx1 - m['LIFT_HOUSING_L'] - 2, cz0 - 24, lhx1, cz0 + 24),
             'lift_housing_D_lug': (2.0, D[1] - 7.4, 21.0, D[1] + 7.6),
             'lift_housing_C_arm': (0.0, 94.0, C[0] + 7.1, 112.0)}
    obstacles = {'crawler_housing': (18.0, 11.0, 296.0, 75.0),
                 'service_cover': (m['SERVICE_CX'] - m['SERVICE_L']/2, 75.0, m['SERVICE_CX'] + m['SERVICE_L']/2, 82.0)}
    worst = {}
    for s in samples:
        t = math.radians(s['theta_deg']); dx = L*(1 - math.cos(t)); dz = L*math.sin(t)
        for gname, r in group.items():
            rr = (r[0] + dx, r[1] + dz, r[2] + dx, r[3] + dz)
            for oname, o in obstacles.items():
                ox, oz = overlap(rr, o)
                clash = ox > 1e-6 and oz > 1e-6
                gap = -min(ox, oz) if clash else max(-ox, -oz)
                key = f'{gname}|{oname}'
                if key not in worst or gap < worst[key]['clearance_mm']:
                    worst[key] = {'clearance_mm': round(gap, 3), 'theta_deg': s['theta_deg'], 'clash': clash}
    swept_ok = not any(v['clash'] for v in worst.values())
    mass = {'CAM026_kg_CONFIRMED': m['CAM026_MASS_KG'], 'lift_housing_kg_ESTIMATED': 0.25, 'levers_kg_ESTIMATED': 0.20}
    cam_cg_x = cam_rear - cam_l/2
    grav0 = 9.81*(mass['CAM026_kg_CONFIRMED']*(AX - cam_cg_x) + mass['lift_housing_kg_ESTIMATED']*(AX - (-13.0))
                  + mass['levers_kg_ESTIMATED']*L/2)/1000
    hchecks, harness = harness_check(m, L, AX, AZ, tmax, args.step)
    checks = {
        'camera_axis_folded_70pm5': abs(cam0 - lo_cat) <= TOL_HEIGHT,
        'camera_axis_raised_257pm5': abs(cam_max - hi_cat) <= TOL_HEIGHT,
        'parallelogram_model_exact': model_err <= 1e-6,
        'parallelogram_drawing_spread_le_0p5': drawing_err <= 0.5,
        'gas_spring_within_ACE_bare_limits': all(lo <= x <= hi for x in gas),
        'gas_spring_pushes_up_when_raising': gas[-1] > gas[0],
        'swept_group_clear_of_housing_and_cover': swept_ok,
        **hchecks,
    }
    report = {
        'status': 'PASS' if all(checks.values()) else 'FAIL', 'checks': checks,
        'basis': 'CRP150 catalogue manual lift 70..257 mm read as camera-axis height above the floor/pipe invert (CONFIRMED range, '
                 'interpretation ESTIMATED); theta_max = asin(187/200.1) DERIVED; lever 200.1 / base 40.2 DERIVED (DRW-002-744).',
        'points_folded_mm': {'A': A, 'B': B, 'C': C, 'D': D, 'E': (AX - E[0], AZ + E[1]), 'G': (AX - G[0], AZ + G[1])},
        'parallelogram_model_mm': para, 'parallelogram_drawing_mm': DRAWING,
        'parallelogram_error_mm': {'model': model_err, 'drawing_spread': drawing_err},
        'camera_axis_mm': {'folded': cam0, 'raised': cam_max, 'theta_max_deg': tmax, 'catalogue': [lo_cat, hi_cat],
                           'raised_camera_shift_rearward_mm': L*(1 - math.cos(math.radians(tmax)))},
        'gas_spring': {'model': 'ACE GS-12-80-V4A', 'bare_limits_mm': [lo, hi], 'min_mm': min(gas), 'max_mm': max(gas),
                       'used_travel_mm': max(gas) - min(gas), 'margin_to_compressed_mm': min(gas) - lo,
                       'margin_to_extended_mm': hi - max(gas),
                       'lever_arm_about_A_mm': {'folded': arm(0), 'raised': arm(math.radians(tmax))},
                       'spring_moment_Nm_at_150N': {'folded': .150*arm(0), 'raised': .150*arm(math.radians(tmax))},
                       'gravity_moment_Nm_folded_ESTIMATED': grav0,
                       'note': 'Clamp FSS-002-089 + 3x DIN2093 holds the remainder by friction (Proteus concept).'},
        'swept_clearance_worst': worst,
        'masses': mass,
        'camera_harness_F21': harness,
        'folded_height_top_of_lever_mm': AZ + 9.0,
        'samples': samples,
        'limits': 'Planar XZ screen of rectangles; Y-separated parts (front wheels, Y>=42.5 vs camera +-37) not tested here. '
                  'Static 3-D collisions of the folded state are in the CAD build. Stops, end-fitting lengths and real balancing are HOLD.',
    }
    text = json.dumps(report, indent=2, ensure_ascii=False)
    if args.out:
        args.out.write_text(text + '\n', encoding='utf-8')
    short = {k: report[k] for k in ('status', 'checks', 'camera_axis_mm', 'parallelogram_error_mm')}
    short['gas_spring'] = {k: report['gas_spring'][k] for k in ('min_mm', 'max_mm', 'bare_limits_mm', 'spring_moment_Nm_at_150N', 'gravity_moment_Nm_folded_ESTIMATED')}
    short['swept_min_clearance_mm'] = min(v['clearance_mm'] for v in worst.values())
    short['camera_harness_F21'] = {k: harness[k] for k in ('modeled_route_length_mm', 'need_mm', 'need_increase_max_mm',
                                                            'need_change_at_theta_max_mm', 'slack_mm', 'margin_mm', 'bend_radii_mm')}
    print(json.dumps(short, indent=2, ensure_ascii=False))
    return 0 if report['status'] == 'PASS' else 1


if __name__ == '__main__':
    sys.exit(main())
