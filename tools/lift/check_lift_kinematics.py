#!/usr/bin/env python3
"""F18 camera-lift kinematic check (DRW-002-744 parallelogram) from PX1_Current_Master.py constants.

The master is parsed with ``ast`` (tools/drawing_measure/check_master_vs_drawings.read_master),
never imported or executed. Checks:
  * camera axis height folded / raised vs CRP150 catalogue 70..257 mm (+-5), CONFIRMED range;
  * parallelogram closure (model exact; drawing AC/BD/AB/CD spread reported);
  * gas spring over 0..theta_max: bare length (eye-to-eye minus the two ACE A3,5 eyes) within the ACE catalogue
    compressed..extended range with ACE_MARGIN at both ends (F25);
  * swept 2-D clearance (XZ) of the translating camera/lift-housing group against the
    crawler housing + service cover (Y overlap assumed, conservative);
  * informative: spring vs gravity moment about A (masses ESTIMATED);
  * F21 camera harness LAPP 0028679: cable length need between the housing clamp P (moves with the lift
    housing) and the fixed point K on the gland bend guide over 0..theta_max, as the shortest planar path with
    bend radius >= 5xOD (Dubins CSC/CCC) through the two sliding lever clips, vs the modeled folded route
    HARNESS_ROUTE. PASS if slack (modeled - need at 0) >= max need increase + 10 mm.
  * F23 camera exit: bend radii of every modelled arc (external fixed incl. SP13 tail, internal LAPP >= 3xOD, moving >= 5xOD,
    internal core bundle >= 3xD); SP13 potted tail + riser XZ clearance to housing/cover over 0..theta_max (>= 1 mm);
    option (a) right-angle M12 + binder R60 evaluated and must be rejected for option (b) to be the chosen one.
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


def route_walk(start, route, heading=(1.0, 0.0, 0.0)):
    """3-D walk of a master route (HARNESS_ROUTE / INNER_ROUTE / BUNDLE_ROUTE, same convention as the master):
    returns per-segment (end point, end tangent, length, R)."""
    def add(a, b, k=1.0): return tuple(x + k*y for x, y in zip(a, b))
    def cross(a, b): return (a[1]*b[2] - a[2]*b[1], a[2]*b[0] - a[0]*b[2], a[0]*b[1] - a[1]*b[0])
    p, t, out = tuple(start), tuple(float(v) for v in heading), []
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
    bends = bend_radii(m, walk)
    tail = tail_clearance(m, L, tmax, step, walk)
    opt_a = option_a(m)
    checks = {
        'route_ends_at_gland_exit': math.dist(end, (m['CAM_GLAND_XY'][0], m['CAM_GLAND_XY'][1], m['GLAND_EXIT_Z'] - 6.0)) < 1e-6,
        'dynamic_bends_ge_5xOD': min(dyn) >= m['HARNESS_R_FLEX'] - 1e-9,
        'harness_slack_ge_need_plus_10': slack >= max(dmax, 0.0) + 10.0 - 1e-9,
        'fixed_bends_ge_3xOD_incl_sp13_exit': bends['external_fixed_ok'],
        'internal_cable_bends_ge_3xOD': bends['internal_ok'],
        'internal_core_bundle_bends_ge_3xD': bends['bundle_ok'],
        'internal_route_continuous_from_gland': bends['internal_starts_at_harness_end'],
        'sp13_tail_and_riser_clear_of_housing_0_to_theta_max': tail['min_clearance_mm'] >= 1.0,
        'camera_exit_option_b_chosen_option_a_rejected': (not opt_a['fits']) and tail['min_clearance_mm'] >= 1.0 and bends['external_fixed_ok'],
    }
    return checks, {
        'cable': 'LAPP UNITRONIC FD P plus A 0028679, OD %.1f (CONFIRMED), min bend 5xD flexing = %.1f / 3xD fixed = %.1f (CONFIRMED LAPP)'
                 % (m['HARNESS_OD'], m['HARNESS_R_FLEX'], m['HARNESS_R_FIXED_MIN']),
        'modeled_route_length_mm': round(L_model, 2), 'fixed_parts_length_mm': round(L_fixed, 2),
        'need_mm': {'theta_0': n0, 'theta_max': rows[-1]['need_total_mm'], 'max': worst['need_total_mm'], 'max_at_deg': worst['theta_deg']},
        'need_increase_max_mm': round(dmax, 2), 'need_change_at_theta_max_mm': round(rows[-1]['need_total_mm'] - n0, 2),
        'slack_mm': round(slack, 2), 'margin_mm': round(slack - max(dmax, 0.0) - 10.0, 2),
        'points_folded_mm': {'P_housing_clamp': [round(v, 3) for v in P0], 'clip_1_x': g1, 'clip_2_x': g2,
                             'K_fixed_guide': [round(v, 3) for v in K], 'K_heading_deg': round(math.degrees(hK), 3)},
        'bend_radii_mm': {'dynamic_min': min(dyn), 'fixed': fixed, **{k: v for k, v in bends.items() if not k.endswith('_ok')}},
        'camera_exit_F23': {'chosen': 'b: LAPP kept, straight SP13 (clamp nut removed) in a potted bend tail, fixed R%.1f S-riser'
                                      % m['HARNESS_R_FIXED'], 'option_b_tail_clearance': tail, 'option_a_right_angle_m12': opt_a},
        'method': 'need(theta) = fixed parts + Dubins(P(theta) heading +X -> clip 1 on lever, heading along lever) + clip pitch '
                  '(cable slides through open clips) + Dubins(clip 2 -> K heading %.1f deg); R = 5xOD; obstacles ignored (lower bound). '
                  'Bend radii: every arc of HARNESS_ROUTE / INNER_ROUTE / BUNDLE_ROUTE vs 3xD (fixed) / 5xD (moving).' % math.degrees(hK),
        'samples': rows[::10] + ([rows[-1]] if (len(rows) - 1) % 10 else []),
        'limits': 'Planar XZ need; the S-loop lies on the lever plate (XY) and is not tensioned. Tail/riser clearance is a 2-D XZ '
                  'screen against the housing side profile and the service cover (Y overlap assumed). Intermediate-angle 3-D cable '
                  'shape not modelled.',
    }


def bend_radii(m, walk):
    """F23: radii of every modelled arc; external fixed (SP13 tail .. P, K .. gland) >= 3xOD, internal LAPP >= 3xOD,
    core bundle >= 3x bundle D."""
    iP, iK, od = m['HARNESS_SEG_P'], m['HARNESS_SEG_K'], m['HARNESS_OD']
    ext_fixed = [w[3] for w in walk[:iP] + walk[iK:] if w[3] is not None]
    inner = route_walk(m['INNER_START'], m['INNER_ROUTE'], (0.0, 0.0, -1.0))
    bundle = route_walk(inner[-1][0], m['BUNDLE_ROUTE'], (-1.0, 0.0, 0.0))
    r_in = [w[3] for w in inner if w[3] is not None]; r_b = [w[3] for w in bundle if w[3] is not None]
    return {'external_fixed': ext_fixed, 'external_fixed_ok': min(ext_fixed) >= 3*od - 1e-9,
            'internal_lapp': r_in, 'internal_ok': min(r_in) >= 3*od - 1e-9,
            'core_bundle': r_b, 'bundle_od': m['BUNDLE_OD'], 'bundle_ok': min(r_b) >= 3*m['BUNDLE_OD'] - 1e-9,
            'internal_starts_at_harness_end': math.dist(walk[-1][0], m['INNER_START']) < 1e-6,
            'internal_lapp_length_mm': round(sum(w[2] for w in inner), 2),
            'core_bundle_length_mm': round(sum(w[2] for w in bundle), 2),
            'service_connector_face_mm': [round(v, 2) for v in bundle[-1][0]]}


def _seg_dist(p, a, b):
    ax, az = b[0] - a[0], b[1] - a[1]; L2 = ax*ax + az*az
    t = 0.0 if L2 == 0 else max(0.0, min(1.0, ((p[0] - a[0])*ax + (p[1] - a[1])*az)/L2))
    return math.hypot(p[0] - a[0] - t*ax, p[1] - a[1] - t*az)


def _inside(p, poly):
    c = False
    for (x1, z1), (x2, z2) in zip(poly, poly[1:] + poly[:1]):
        if (z1 > p[1]) != (z2 > p[1]) and p[0] < x1 + (p[1] - z1)*(x2 - x1)/(z2 - z1):
            c = not c
    return c


def _poly_clear(p, poly):
    d = min(_seg_dist(p, a, b) for a, b in zip(poly, poly[1:] + poly[:1]))
    return -d if _inside(p, poly) else d


def _sample_route(start, route, heading=(1.0, 0.0, 0.0), ds=0.5):
    """Dense XZ points along a route (arcs and lines)."""
    pts = [(start[0], start[2])]; p = tuple(start); t = heading
    for sg in route:
        n = max(2, int(math.ceil((sg[1] if sg[0] == 'S' else sg[1]*math.radians(sg[2])) / ds)))
        for k in range(1, n + 1):
            sub = (('S', sg[1]*k/n),) if sg[0] == 'S' else (('A', sg[1], sg[2]*k/n, sg[3]),)
            q = route_walk(p, sub, t)[-1][0]; pts.append((q[0], q[2]))
        w = route_walk(p, (sg,), t)[-1]; p, t = w[0], w[1]
    return pts


def tail_clearance(m, L, tmax, step, walk):
    """F23 option (b): potted tail (r = OD/2 + wall) and the bare riser up to P translate with the lift housing; min XZ clearance
    to the housing side profile and the service cover over theta 0..theta_max."""
    r_t = m['HARNESS_OD']/2 + m['HARNESS_TAIL_WALL']; r_c = m['HARNESS_OD']/2
    route = m['HARNESS_ROUTE']; iP = m['HARNESS_SEG_P']
    tail_pts = _sample_route(m['HARNESS_START'], tuple(route[:2]) + (('S', m['HARNESS_TAIL_LINE']),))
    riser_pts = _sample_route(m['HARNESS_START'], tuple(route[:iP]))
    body = [tuple(v) for v in m['profile']]
    cover = [(m['SERVICE_CX'] - m['SERVICE_L']/2, 75.0), (m['SERVICE_CX'] + m['SERVICE_L']/2, 75.0),
             (m['SERVICE_CX'] + m['SERVICE_L']/2, 82.0), (m['SERVICE_CX'] - m['SERVICE_L']/2, 82.0)]
    best = {'min_clearance_mm': float('inf')}; theta = 0.0
    while True:
        th = math.radians(theta); dx, dz = L*(1 - math.cos(th)), L*math.sin(th)
        for name, pts, r in (('tail', tail_pts, r_t), ('riser_cable', riser_pts, r_c)):
            for q in pts:
                p = (q[0] + dx, q[1] + dz)
                for oname, poly in (('housing', body), ('service_cover', cover)):
                    c = _poly_clear(p, poly) - r
                    if c < best['min_clearance_mm']:
                        best = {'min_clearance_mm': round(c, 3), 'theta_deg': theta, 'part': name, 'obstacle': oname,
                                'point_folded_xz': [round(q[0], 2), round(q[1], 2)]}
        if theta >= tmax - 1e-9:
            break
        theta = min(theta + step, tmax)
    best['tail_shell_r_mm'] = r_t
    return best


def option_a(m):
    """F23 option (a): right-angle M12-A 8p moulded (binder 77-3434 family) in place of the SP13 exit, binder PVC cable."""
    d, l = m['CAMEXIT_A_ELBOW']; od, rf = m['CAMEXIT_A_CABLE_OD'], m['CAMEXIT_A_R_FLEX']
    x0 = 14.0                                          # receptacle on the lift-housing rear face (bore exit), elbow along +X
    elbow = (x0, m['CAM_Z'] - d/2, x0 + l, m['CAM_Z'] + d/2)
    body_front, body_top = 18.0, 75.0
    clash_x = elbow[2] - body_front; clash_z = body_top - elbow[1]
    loop_a = math.acos(1 - abs(m['HARNESS_LOOP_Y'])/(2*rf)); loop_len_x = 4*rf*math.sin(loop_a)
    clip_free = m['HARNESS_GUIDE_X'][1] - m['HARNESS_GUIDE_X'][0] - 12.0
    sb = (m['HARNESS_TOP_Z'] + rf + rf*math.cos(math.radians(90 - m['HARNESS_FIX_TURN']))
          - (m['GLAND_EXIT_Z'] + m['HARNESS_R_FIXED']*math.sin(math.radians(m['HARNESS_FIX_TURN']))))/(2*rf)
    crest = m['HARNESS_TOP_Z'] + 2*rf*(1 - sb) + od/2 if abs(sb) <= 1 else None
    crest_gap = (m['PIPE_R'] - math.hypot(abs(m['HARNESS_LOOP_Y']) + od/2, crest - m['PIPE_CENTER_Z'])) if crest else None
    fits = clash_x <= 0 or clash_z <= 0
    fits = fits and loop_len_x <= clip_free
    return {'fits': fits,
            'elbow_envelope_xz_mm': [round(v, 2) for v in elbow], 'elbow_dims_ESTIMATED': [d, l],
            'elbow_vs_housing_front_overlap_mm': {'x': round(clash_x, 2), 'z': round(clash_z, 2), 'clash': clash_x > 0 and clash_z > 0},
            'binder_cable': {'od_mm': od, 'moving_bend_min_mm': rf,
                             'lever_s_loop_x_span_needed_mm': round(loop_len_x, 1), 'lever_free_x_between_clips_mm': round(clip_free, 1),
                             's_bend_crest_top_z_mm': round(crest, 2) if crest else None,
                             'crest_gap_to_dn150_mm': round(crest_gap, 2) if crest_gap is not None else None},
            'verdict': 'REJECTED: elbow (27 along X behind the housing rear X14) overlaps the crawler housing front (X18, top Z75); '
                       'binder PVC R>=60 S-loop does not fit between the lever clips, so the moving section would stay LAPP via a potted '
                       'inline joint (extra leak path) and the elbow still needs a new exit position in DRW-002-752.'}


def drw752_check(m, A, B, C, D):
    """F24: DRW-002-752 lift housing. (1) CD of 752 (C, D in the housing, 1:1) vs AB of 744 (parallelogram consistency);
    (2) model D vs 752 D (F25: 752 pivots used directly, no PX1 yoke); (3) camera axis below C;
    (4) the fixed cable riser / clamp P vs the C axle FSS-002-076 (Ø7.05, through) and the D blind taps (|Y| >= W/2 - 8):
    3-D clearance >= 1 mm (riser runs in Y0; XZ distance used for the through C axle, Y gap for the D taps)."""
    c752, d752 = m['LH752_C'], m['LH752_D']; ab = m['LIFT_AB']
    cd = (c752[0] - d752[0], c752[1] - d752[1]); cd_len = math.hypot(*cd); ab_len = math.hypot(*ab)
    ang_752 = math.degrees(math.atan2(cd[1], cd[0])); ang_744 = math.degrees(math.atan2(-ab[1], ab[0]))
    x0, cz = m['LH_X0'], m['CAM_Z']; sh = (0.0, 0.0)          # F25: no PX1 yoke, 752 pivots used directly
    d_752_px1 = (x0 + d752[0] + sh[0], cz + d752[1] + sh[1]); c_752_px1 = (x0 + c752[0] + sh[0], cz + c752[1] + sh[1])
    d_dev = math.dist(d_752_px1, D); c_dev = math.dist(c_752_px1, C)
    route = m['HARNESS_ROUTE']; iP = m['HARNESS_SEG_P']; r_cab = m['HARNESS_OD']/2; r_tail = r_cab + m['HARNESS_TAIL_WALL']
    pts = _sample_route(m['HARNESS_START'], tuple(route[:iP + 1]))
    r_c = m['LH752_C_AXLE_D']/2
    c_xz = min(math.dist(q, C) for q in pts) - r_c - r_cab
    tap_y0 = m['LIFT_HOUSING_W']/2 - m['LH752_D_TAP'][1]
    d_y_gap = tap_y0 - r_tail
    d_xz = min(math.dist(q, D) for q in pts) - m['LIFT_D_PIN'][0] - r_tail
    folded_752 = m['LIFT_A_Z'] - c752[1]; proteus_A_z = m['SERVICE_Z'] + m['LIFT_A_ABOVE_BASE']
    checks = {
        'drw752_cd_equals_744_ab_within_0p5': abs(cd_len - ab_len) <= 0.5,
        'drw752_cd_direction_within_1deg_of_744_ab': abs(ang_752 - ang_744) <= 1.0,
        'd_on_752_pattern_within_0p6_c_exact': d_dev <= 0.6 and c_dev <= 1e-6,
        'riser_clear_of_c_axle_ge_1': c_xz >= 1.0,
        'riser_clear_of_d_taps_ge_1': d_y_gap >= 1.0 or d_xz >= 1.0,
    }
    return {'checks': checks, 'report': {
        'cd_752_vs_ab_744': {'cd_752_mm': round(cd_len, 3), 'ab_744_mm': round(ab_len, 3), 'diff_mm': round(cd_len - ab_len, 3),
                             'angle_752_deg': round(ang_752, 2), 'angle_744_deg': round(ang_744, 2),
                             'note': 'parallelogram kept exact on 744 (AB = CD); 752 differs by the listed angle -> camera tilt '
                                     '<= that angle if 752 were used literally (within 744 1:1.5 reading +-0.3 mm)'},
        'd_model_vs_752_mm': round(d_dev, 3), 'c_model_vs_752_mm': round(c_dev, 6), 'pivot_shift_px1_mm': [0.0, 0.0],
        'camera_axis_below_c': {'drw752_mm': c752[1], 'px1_mm': round(m['LIFT_A_Z'] - cz, 3),
                                'px1_folded_if_752_literal_mm': round(folded_752, 2),
                                'proteus_folded_752_literal_mm': round(proteus_A_z - c752[1], 2),
                                'catalogue_mm': m['LIFT_CAT_RANGE'][0]},
        'riser_to_pivots': {'c_axle_xz_clearance_mm': round(c_xz, 2), 'd_taps_y_gap_mm': round(d_y_gap, 2),
                            'd_taps_xz_clearance_mm': round(d_xz, 2),
                            'note': 'D = blind taps 8 deep from each side (752 C-C), riser + potted tail in Y0 -> no crossing'},
    }}


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
    fit, gmar = 2*m['ACE_EYE_L'], m['ACE_MARGIN']
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
    cam_rear = m['CAM_REAR_X']; cam_l, cam_w, cam_h = m['CAM026_ENVELOPE']; cz0 = m['CAM_Z']
    x0 = m['LH_X0']; bx = m['LH752_BODY_X']; zb, zt, zl = (cz0 + v for v in m['LH752_Z']); la, ll, _ = m['LH752_LIGHT']
    group = {'camera_CAM026': (cam_rear - cam_l, cz0 - cam_h/2, cam_rear, cz0 + cam_h/2),            # F24: DRW-002-752 parts
             'lock_ring_FSS001889': (x0, cz0 - m['LH752_LOCK'][0]/2, x0 + m['LH752_LOCK'][2], cz0 + m['LH752_LOCK'][0]/2),
             'housing_body_and_lift_cover': (x0 + bx[0], zb, x0 + bx[2], zt),
             'light_cover_FAL002080': (x0 + la - ll/2, zt, x0 + la + ll/2, zl),
             'fork_lugs_C_752': (x0 + bx[1] - .5, m['LH_LUG_Z0'], x0 + m['LH752_FORK'][2], C[1] + 7.0),
             'px1_cable_spine': (x0 + bx[1] - .5, m['LH_LUG_Z0'], C[0] + 7.1, AZ + 7.1)}
    obstacles = {'crawler_housing': (18.0, 11.0, 296.0, 75.0),
                 'service_cover_pad': (m['SERVICE_CX'] - m['SERVICE_L']/2, 75.0, m['SERVICE_CX'] + m['SERVICE_L']/2, 75.0 + m['SERVICE_T']),
                 'fitting_holder': (m['HOLDER_X'][0], 75.0, m['HOLDER_X'][1], 75.0 + m['HOLDER_T'])}
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
    grav0 = 9.81*(mass['CAM026_kg_CONFIRMED']*(AX - cam_cg_x) + mass['lift_housing_kg_ESTIMATED']*(AX - (x0 + (bx[0] + bx[2])/2))
                  + mass['levers_kg_ESTIMATED']*L/2)/1000
    hchecks, harness = harness_check(m, L, AX, AZ, tmax, args.step)
    h752 = drw752_check(m, A, B, C, D)
    checks = {
        'camera_axis_folded_70pm5': abs(cam0 - lo_cat) <= TOL_HEIGHT,
        'camera_axis_raised_257pm5': abs(cam_max - hi_cat) <= TOL_HEIGHT,
        'parallelogram_model_exact': model_err <= 1e-6,
        'parallelogram_drawing_spread_le_0p5': drawing_err <= 0.5,
        'gas_spring_bare_within_ACE_stroke_with_margin': all(lo + gmar <= x - fit <= hi - gmar for x in gas),
        'gas_spring_pushes_up_when_raising': gas[-1] > gas[0],
        'swept_group_clear_of_housing_and_cover': swept_ok,
        **hchecks,
        **h752['checks'],
    }
    report = {
        'status': 'PASS' if all(checks.values()) else 'FAIL', 'checks': checks,
        'basis': 'CRP150 catalogue manual lift 70..257 mm read as camera-axis height above the floor/pipe invert (CONFIRMED range, '
                 'interpretation ESTIMATED); theta_max 69 deg (stop ESTIMATED); lever 200.1 / base 40.2 DERIVED (DRW-002-744).',
        'points_folded_mm': {'A': A, 'B': B, 'C': C, 'D': D, 'E': (AX - E[0], AZ + E[1]), 'G': (AX - G[0], AZ + G[1])},
        'parallelogram_model_mm': para, 'parallelogram_drawing_mm': DRAWING,
        'parallelogram_error_mm': {'model': model_err, 'drawing_spread': drawing_err},
        'camera_axis_mm': {'folded': cam0, 'raised': cam_max, 'theta_max_deg': tmax, 'catalogue': [lo_cat, hi_cat],
                           'raised_camera_shift_rearward_mm': L*(1 - math.cos(math.radians(tmax)))},
        'gas_spring': {'model': 'ACE GS-12-60-V4A + 2x A3,5-V4A eye', 'bare_limits_mm': [lo, hi], 'eye_fittings_mm': fit,
                       'required_margin_mm': gmar, 'eye_to_eye_min_mm': min(gas), 'eye_to_eye_max_mm': max(gas),
                       'min_mm': min(gas) - fit, 'max_mm': max(gas) - fit,
                       'used_travel_mm': max(gas) - min(gas), 'margin_to_compressed_mm': min(gas) - fit - lo,
                       'margin_to_extended_mm': hi - (max(gas) - fit),
                       'f18_f24_note': 'GS-12-80 (112..192) compared eye-to-eye 119.3/138.8 with the bare length: with the eyes the '
                                       'bare length is 103.3..122.8 < 112 -> GS-12-80 would be blocked; GS-12-60 selected (F25)',
                       'lever_arm_about_A_mm': {'folded': arm(0), 'raised': arm(math.radians(tmax))},
                       'spring_moment_Nm_at_150N': {'folded': .150*arm(0), 'raised': .150*arm(math.radians(tmax))},
                       'gravity_moment_Nm_folded_ESTIMATED': grav0,
                       'note': 'Clamp FSS-002-089 + 3x DIN2093 holds the remainder by friction (Proteus concept).'},
        'swept_clearance_worst': worst,
        'masses': mass,
        'camera_harness_F21': harness,
        'lift_housing_DRW002752_F24': h752['report'],
        'folded_height_top_of_lever_mm': AZ + 9.0,
        'folded_height_top_of_light_window_mm': cz0 + m['LH752_Z'][2], 'folded_camera_top_mm': cz0 + cam_h/2,
        'samples': samples,
        'limits': 'Planar XZ screen of rectangles; Y-separated parts (front wheels, Y>=42.5 vs camera +-37) not tested here. '
                  'Static 3-D collisions of the folded state are in the CAD build. Stops, end-fitting lengths and real balancing are HOLD.',
    }
    text = json.dumps(report, indent=2, ensure_ascii=False)
    if args.out:
        args.out.write_text(text + '\n', encoding='utf-8')
    short = {k: report[k] for k in ('status', 'checks', 'camera_axis_mm', 'parallelogram_error_mm')}
    short['gas_spring'] = {k: report['gas_spring'][k] for k in ('min_mm', 'max_mm', 'bare_limits_mm', 'margin_to_compressed_mm',
                                                               'margin_to_extended_mm', 'spring_moment_Nm_at_150N', 'gravity_moment_Nm_folded_ESTIMATED')}
    short['swept_min_clearance_mm'] = min(v['clearance_mm'] for v in worst.values())
    short['camera_harness_F21'] = {k: harness[k] for k in ('modeled_route_length_mm', 'need_mm', 'need_increase_max_mm',
                                                            'need_change_at_theta_max_mm', 'slack_mm', 'margin_mm', 'bend_radii_mm')}
    short['lift_housing_F24'] = {k: h752['report'][k] for k in ('cd_752_vs_ab_744', 'd_model_vs_752_mm', 'riser_to_pivots')}
    short['camera_exit_F23'] = {'chosen': harness['camera_exit_F23']['chosen'],
                                'tail_clearance': harness['camera_exit_F23']['option_b_tail_clearance'],
                                'option_a_verdict': harness['camera_exit_F23']['option_a_right_angle_m12']['verdict']}
    print(json.dumps(short, indent=2, ensure_ascii=False))
    return 0 if report['status'] == 'PASS' else 1


if __name__ == '__main__':
    sys.exit(main())
