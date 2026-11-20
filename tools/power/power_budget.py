#!/usr/bin/env python3
"""PX1 power budget (F19). Calculation only — not a measured result.

Every input carries a tag: CONFIRMED (source), DERIVED (computed from other inputs),
ESTIMATED (engineering assumption). Run:  python tools/power/power_budget.py [--json OUT]
Doc: current/02_ELECTRICAL/POWER_BUDGET_F19_20261119.md
"""
import argparse, json, math
from pathlib import Path

ROOT = Path(__file__).resolve().parents[2]

I = {  # name: (value, tag, source)
    # --- Cincon CQB150W-110S24 (app notes V12, Mouser) ---
    'cincon_pout_max_W': (150.0, 'CONFIRMED', 'CQB150W-110S24, 24 V / 6.3 A'),
    'cincon_iout_max_A': (6.3, 'CONFIRMED', 'datasheet'),
    'cincon_ocp_min_frac': (1.10, 'CONFIRMED', 'OCP 110-160 % rated, hiccup'),
    'cincon_ovp_min_V': (24 * 1.15, 'CONFIRMED', 'OVP 115-140 % (typ 125 %)'),
    'cincon_vin_min_V': (43.0, 'CONFIRMED', 'input 43-160 V; UVLO off 37-39 V'),
    'cincon_eff_full': (0.89, 'CONFIRMED', '89 % @ 110 V full load'),
    'cincon_eff_part': (0.87, 'ESTIMATED', 'typical part-load efficiency < 50 % load'),
    'cincon_tc_max_C': (105.0, 'CONFIRMED', 'case -40..105 C, OTP 110 C at baseplate'),
    'cincon_tc_design_C': (95.0, 'ESTIMATED', '10 K margin below Tc max'),
    'cincon_rca_bare_KpW': (10.1, 'CONFIRMED', 'Rca natural convection, no heatsink'),
    'cincon_rcs_bonded_KpW': (0.4, 'ESTIMATED', 'baseplate -> pad -> Al cover L01 -> body wall (F20 README: 0.12+0.10+0.17; F19 had 0.3)'),
    'cincon_cout_max_uF': (6300.0, 'CONFIRMED', 'max output capacitance'),
    'derating_frac': (0.80, 'ESTIMATED', 'design continuous limit 80 % of rating'),
    # --- Pololu G2 24v13 #2992 ---
    'g2_cs_V_per_A': (0.040, 'CONFIRMED', 'pololu.com/product/2992: ~40 mV/A + 50 mV'),
    'g2_cs_offset_V': (0.050, 'CONFIRMED', 'same'),
    'g2_ilim_default_A': (30.0, 'CONFIRMED', 'default current-limit threshold ~30 A'),
    'g2_vabs_max_V': (40.0, 'CONFIRMED', 'absolute max supply'),
    'g2_cbulk_onboard_uF': (100.0, 'CONFIRMED', 'onboard capacitor'),
    'g2_loss_W': (0.3, 'ESTIMATED', 'per board at <=2 A, 20 kHz'),
    'pwm_hz': (20e3, 'CONFIRMED', 'ELECTRICAL_Current.md bench setting'),
    # --- motor: ZHAOWEI MP2238 family, 12 V catalogue ---
    'R12_ohm': (2.0, 'CONFIRMED', 'MP2238-01 12 V catalogue'),
    'Kt12_mNm_A': (18.0, 'CONFIRMED', 'MP2238-01 (Kv ~525 rpm/V)'),
    'Irated12_A': (1.2, 'CONFIRMED', 'rated 16.6 mN·m / 1.2 A'),
    'Trated_mNm': (16.6, 'CONFIRMED', 'rated torque (winding-independent)'),
    'Istall12_A': (6.0, 'CONFIRMED', 'stall 99.5 mN·m / 6 A @ 12 V'),
    'Tstall12_mNm': (99.5, 'CONFIRMED', 'same'),
    'winding_scale': (2.0, 'DERIVED', '24 V winding = 2x turns, same copper volume'),
    'R_tol': (0.90, 'ESTIMATED', 'cold/tolerance: R -10 % -> stall +11 %'),
    'J_rotor_kgm2': (8e-7, 'ESTIMATED', 'Ø22 rotor class (maxon DCX22L 8.6 g·cm²)'),
    'gear_ratio': (62.0, 'DERIVED', 'F12 note: 24 V winding needs i=62 for ~85 rpm (62 listed on ZHAOWEI 26 mm page)'),
    # 2026-11-20 review: was 0.90 'CONFIRMED'. ZHAOWEI 26 mm planetary page gives only a catalogue MAXIMUM
    # efficiency 87 %; 3-stage planetary at rated load is typically 0.73-0.81 -> use 0.81 ESTIMATED.
    'gear_eff': (0.81, 'ESTIMATED', '3-stage planetary typ. 0.73-0.81 at load; upper end used'),
    'gear_eff_catalogue_max': (0.87, 'CONFIRMED', 'zwgearbox.com 26mm-high-performance-planetary-gearbox-2: max efficiency 87 %'),
    'T_out_duty_Nm': (1.0, 'ESTIMATED', 'F12 duty target per motor (NOT a derated value: above continuous rating, see motor24)'),
    'n_out_target_rpm': (87.0, 'ESTIMATED', 'F12 target'),
    'bevel_ratio': (2.5, 'CONFIRMED', 'Z16->Z40'),
    'wheel_r_m': (0.045, 'CONFIRMED', 'D90 wheel'),
    'mass_kg': (9.25, 'CONFIRMED', 'Proteus CRP150 catalogue mass'),
    'motors': (2, 'CONFIRMED', 'two traction motors'),
    # --- 12 V head ---
    'cam_W': (12 * 0.12, 'CONFIRMED', 'RunCam Phoenix 2: 85-120 mA @ 12 V (A3_CAMERA_LIGHT_BENCH.md)'),
    'led_strings': (2, 'CONFIRMED', '2 strings x 3 LED (A3 bench)'),
    'led_I_A': (0.35, 'CONFIRMED', 'initial 350 mA per string (A3 bench)'),
    'led_Vf_V': (3.1, 'ESTIMATED', 'XP-G class Vf @ 350 mA'),
    'led_drv_eff': (0.90, 'ESTIMATED', 'P4115 buck module'),
    'pan_rot_run_W': (2 * 12 * 0.12, 'ESTIMATED', '2x N20 12 V running ~0.12 A'),
    'pan_rot_peak_W': (2 * 12 * 0.5, 'ESTIMATED', '2x N20 12 V stalled/limited 0.5 A'),
    'head_ctrl_W': (0.4, 'ESTIMATED', 'RP2040-Zero + 2x AS5600 + DRV8871 quiescent'),
    'reg12_eff': (0.90, 'ESTIMATED', 'Pololu 5577 D42V55F12 @ 24 V in'),
    # --- 5 V logic ---
    'logic5_W': (1.5, 'ESTIMATED', 'WeAct F446 0.25 + iso RS-485 0.4 + sensors/LEDs/margin'),
    'reg5_eff': (0.85, 'ESTIMATED', 'Pololu 5571 D42V55F5 light load'),
    # --- tether ---
    'src_V': (110.0, 'CONFIRMED', 'A2 design point'),
    'src_V_low': (100.0, 'CONFIRMED', 'CCU range 100-120 V (ELECTRICAL_Current.md)'),
    'tether_m': (150.0, 'CONFIRMED', 'AGENTS.md later 100-150 m'),
    'core_ohm_per_km': (40.1, 'CONFIRMED', '0.5 mm² Cu class 5 @ 20 C'),
    'hot_mult': (1.20, 'ESTIMATED', 'hot copper / reel, as A2 calc'),
    # --- thermal ---
    'Ta_C': (40.0, 'ESTIMATED', 'worst: dry pipe / bench in summer, still air'),
    'body_area_m2': (0.082, 'DERIVED', '278x68x64 box surface'),
    'h_W_m2K': (10.0, 'ESTIMATED', 'natural convection + radiation, still air'),
    'dT_air_internal_K': (10.0, 'ESTIMATED', 'internal air above wall, sealed 1 bar, no fan'),
    'T_air_int_max_C': (85.0, 'ESTIMATED', 'commercial boards (G2, WeAct, Pololu regs) rated to 85 C ambient'),
    'c_steel_JkgK': (480.0, 'ESTIMATED', 'steel / stainless 460-500'),
    'c_al_JkgK': (900.0, 'ESTIMATED', 'aluminium alloy'),
    'c_purchased_JkgK': (450.0, 'ESTIMATED', 'motors/gearheads: steel+copper'),
    'mass_breakdown_json': ('current/07_TESTS/traction_budget_F17_steel.json', 'DERIVED', 'CAD mass by category (model 8.05 kg, densities ESTIMATED)'),
    'g2_loss_ref_A': (2.0, 'ESTIMATED', 'g2_loss_W valid up to this current; scaled with I^2 above'),
    'head_heat_inside_body': (False, 'ESTIMATED', '12 V head loads (camera, LED + P4115, N20, RP2040) dissipate in the separately sealed camera head; only the 5577 regulator loss is inside the crawler body'),
    # --- firmware choices ---
    'I_peak_lim_A': (1.8, 'DERIVED', 'per motor: <= I_lim_max (1.96 A) with ~8 % margin'),
    'ramp_s': (0.5, 'ESTIMATED', 'proposed 0->100 % duty'),
    'C_add_per_G2_uF': (330.0, 'DERIVED', 'ripple calc below'),
    'C_cincon_out_uF': (470.0, 'ESTIMATED', 'at Cincon output'),
}
v = {k: x[0] for k, x in I.items()}


def feed(src, p_in, r):
    d = src * src - 4 * p_in * r
    if d < 0:
        return None
    vin = 0.5 * (src + math.sqrt(d))
    return vin, p_in / vin, src - vin


def main():
    out = {}
    m = v['motors']
    # ---- motor 24 V winding ----
    s = v['winding_scale']
    R24 = v['R12_ohm'] * s ** 2
    Kt24 = v['Kt12_mNm_A'] * s
    Tf = v['Kt12_mNm_A'] * v['Irated12_A'] - v['Trated_mNm']  # friction mN·m
    I0_24 = Tf / Kt24
    Ke = Kt24 / 1000  # V·s/rad
    Kv = 60 / (2 * math.pi * Ke)
    Istall24 = 24 / R24
    Istall24_cold = 24 / (R24 * v['R_tol'])
    Tstall24 = Kt24 * Istall24 - Tf
    Irated24 = (v['Trated_mNm'] + Tf) / Kt24
    Tm = v['T_out_duty_Nm'] * 1000 / (v['gear_ratio'] * v['gear_eff'])
    Iduty = (Tm + Tf) / Kt24
    w = (24 - Iduty * R24) / Ke
    n_out = w * 60 / (2 * math.pi) / v['gear_ratio']
    V_for_target = v['n_out_target_rpm'] * v['gear_ratio'] * 2 * math.pi / 60 * Ke + Iduty * R24
    P_motor_duty = 24 * Iduty
    P_mech = v['T_out_duty_Nm'] * n_out * 2 * math.pi / 60
    out['motor24'] = dict(R_ohm=R24, Kt_mNm_A=Kt24, Kv_rpm_V=Kv, T_friction_mNm=Tf, I0_A=I0_24,
                          I_stall_A=Istall24, I_stall_cold_A=Istall24_cold, T_stall_mNm=Tstall24,
                          I_rated_A=Irated24, T_motor_duty_mNm=Tm, I_duty_A=Iduty,
                          n_out_at_24V_rpm=n_out, V_needed_for_target_rpm=V_for_target,
                          P_el_duty_W=P_motor_duty, P_mech_out_W=P_mech)
    # seller table cross-check (i=138, 87 rpm @ 24 V) -> implies 12 V winding
    n_motor_seller = 87 * 138
    out['seller_check'] = dict(motor_rpm=n_motor_seller, kv_needed=n_motor_seller / 24,
                               kv_24V_winding=Kv, kv_12V_winding=Kv * 2,
                               I_stall_12V_winding_at_24V_A=24 / v['R12_ohm'])

    # ---- rails ----
    led_W = v['led_strings'] * 3 * v['led_Vf_V'] * v['led_I_A'] / v['led_drv_eff']
    head_nom = v['cam_W'] + led_W + v['pan_rot_run_W'] + v['head_ctrl_W']
    head_pk = v['cam_W'] + led_W + v['pan_rot_peak_W'] + v['head_ctrl_W']
    head24_nom, head24_pk = head_nom / v['reg12_eff'], head_pk / v['reg12_eff']
    logic24 = v['logic5_W'] / v['reg5_eff']
    aux24_nom, aux24_pk = head24_nom + logic24, head24_pk + logic24
    g2 = m * v['g2_loss_W']
    out['rails'] = dict(led_W=led_W, head12_nom_W=head_nom, head12_peak_W=head_pk,
                        head_from24_nom_W=head24_nom, head_from24_peak_W=head24_pk,
                        logic_from24_W=logic24)

    lim = v['cincon_pout_max_W'] * v['derating_frac']
    # current limit: worst = both motors at limit at full speed (bus I ~= motor I)
    I_lim_max = (lim - aux24_pk - g2) / (m * 24)
    Ipk = v['I_peak_lim_A']
    cases = {
        'A_duty_1Nm': m * P_motor_duty + g2 + aux24_nom,
        'B_both_at_Ilim_full_speed': m * 24 * Ipk + g2 + aux24_pk,
        'B2_both_stalled_chopping_at_Ilim': m * Ipk ** 2 * R24 + g2 + aux24_pk,
        'C_uncontrolled_start_24V_winding': m * 24 * Istall24 + g2 + aux24_pk,
        'C2_same_cold_R-10%': m * 24 * Istall24_cold + g2 + aux24_pk,
        'D_12V_winding_on_24V_stall': m * 24 * 24 / v['R12_ohm'] + g2 + aux24_pk,
    }
    out['I_lim_max_per_motor_A'] = I_lim_max
    out['cincon_design_limit_W'] = lim
    out['cases_W_24V'] = {k: dict(P_W=p, I_bus_A=p / 24, pct_of_150W=100 * p / v['cincon_pout_max_W'],
                                  over_rating=p > v['cincon_pout_max_W'],
                                  over_ocp_min=p / 24 > v['cincon_iout_max_A'] * v['cincon_ocp_min_frac'])
                          for k, p in cases.items()}

    # ---- thermal (2026-11-20 review correction: one consistent heat balance per case) ----
    # P_int = Cincon loss + motor copper I^2R (both) + motor friction + gearhead loss + G2 + 12 V/5 V regulator
    # losses + 5 V logic.  Head 12 V loads heat the camera head, not the body (ESTIMATED, see inputs).
    R_ha = 1 / (v['body_area_m2'] * v['h_W_m2K'])
    eta_g = v['gear_eff']
    reg_loss_nom = head24_nom - head_nom + logic24 - v['logic5_W']
    reg_loss_pk = head24_pk - head_pk + logic24 - v['logic5_W']

    def motor_state(I):
        """24 V winding, 100 % duty, current I per motor -> losses per motor."""
        wm = max(0.0, (24 - I * R24) / Ke)
        T_shaft = max(0.0, Kt24 * I - Tf) / 1000  # N·m at motor shaft
        return dict(I_A=I, P_cu_W=I * I * R24, P_fric_W=Tf / 1000 * wm, P_gear_W=T_shaft * wm * (1 - eta_g),
                    P_out_W=T_shaft * wm * eta_g, T_out_Nm=T_shaft * v['gear_ratio'] * eta_g,
                    n_out_rpm=wm * 60 / (2 * math.pi) / v['gear_ratio'])

    def heat(p_out, I, reg_loss):
        eff = v['cincon_eff_full'] if p_out > 75 else v['cincon_eff_part']
        ms = motor_state(I)
        g2l = m * v['g2_loss_W'] * max(1.0, (I / v['g2_loss_ref_A']) ** 2)
        parts = dict(cincon_W=p_out * (1 / eff - 1), motor_cu_W=m * ms['P_cu_W'],
                     motor_fric_W=m * ms['P_fric_W'], gearhead_W=m * ms['P_gear_W'], g2_W=g2l,
                     regulators_W=reg_loss, logic5_W=v['logic5_W'])
        P = sum(parts.values())
        Tw = v['Ta_C'] + P * R_ha
        Tc = Tw + parts['cincon_W'] * v['cincon_rcs_bonded_KpW']
        Tw_lim = min(v['T_air_int_max_C'] - v['dT_air_internal_K'],
                     v['cincon_tc_design_C'] - parts['cincon_W'] * v['cincon_rcs_bonded_KpW'])
        return dict(P_out_cincon_W=p_out, I_motor_A=I, motor=ms, losses_W=parts, P_internal_W=P,
                    T_wall_ss_C=Tw, T_air_ss_C=Tw + v['dT_air_internal_K'], Tc_cincon_ss_C=Tc,
                    T_wall_limit_C=Tw_lim, steady_state_ok=Tw <= Tw_lim)

    def I_for_pout(p_out, aux):
        return max(0.0, (p_out - aux - m * v['g2_loss_W']) / (m * 24))

    Irated = Irated24
    th = {
        'A_duty_1Nm': heat(cases['A_duty_1Nm'], Iduty, reg_loss_nom),
        'A0_rated_continuous': heat(m * 24 * Irated + g2 + aux24_nom, Irated, reg_loss_nom),
        'B_Ilim_1p8A_both': heat(cases['B_both_at_Ilim_full_speed'], Ipk, reg_loss_pk),
        'P120W': heat(120.0, I_for_pout(120.0, aux24_pk), reg_loss_pk),
        'P150W': heat(150.0, I_for_pout(150.0, aux24_pk), reg_loss_pk),
    }
    # lumped heat capacity of the body + thermally coupled internals (camera head, lift, tyres excluded)
    mb = json.loads((ROOT / v['mass_breakdown_json']).read_text())['cad_mass_estimate']['by_category_kg']
    steel = ['WEIGHT_PLATE', 'BALLAST', 'gear', 'shaft', '_FSS0020', 'AXLE_FLANGE', 'bearing', 'bevel',
             'ISO4035', 'DIN2093', 'valve', 'LIFT_GAS_SPRING']
    alu = ['PRESSURE_BODY', 'SIDE_COVER', 'metal', 'QRW90_HUB_AL', 'CINCON_CQB150W', 'BRAKE_SHUNT_10R']
    m_st = sum(mb.get(k, 0) for k in steel); m_al = sum(mb.get(k, 0) for k in alu); m_pu = mb.get('purchased', 0)
    C = m_st * v['c_steel_JkgK'] + m_al * v['c_al_JkgK'] + m_pu * v['c_purchased_JkgK']
    tau = R_ha * C
    T0 = th['A_duty_1Nm']['T_wall_ss_C']
    def t_lim(t, start):
        if t['steady_state_ok']:
            return None
        if start >= t['T_wall_limit_C']:
            return 0.0
        return tau * math.log((t['T_wall_ss_C'] - start) / (t['T_wall_ss_C'] - t['T_wall_limit_C']))
    for k, t in th.items():
        t['time_to_limit_from_A_s'] = t_lim(t, T0)          # after long running at the 1.0 N·m point
        t['time_to_limit_from_cold_s'] = t_lim(t, v['Ta_C'])  # body soaked at ambient
    # firmware I^2t budget (adiabatic, conservative): extra heat above the operating point until the wall limit
    E_budget = C * (v['T_air_int_max_C'] - v['dT_air_internal_K'] - T0)
    out['thermal'] = dict(R_body_amb_KpW=R_ha, R_cincon_base_wall_KpW=v['cincon_rcs_bonded_KpW'],
                          heat_capacity_J_per_K=C, coupled_mass_kg=dict(steel=m_st, aluminium=m_al, motors=m_pu),
                          tau_s=tau, T_wall_start_C=T0, E_budget_above_A_J=E_budget,
                          I2t_budget_per_motor_A2s=E_budget / (m * R24),
                          cases=th,
                          cincon_pout_allowed_bare_W=max(0.0, (v['cincon_tc_design_C'] - th['A_duty_1Nm']['T_air_ss_C'])
                                                         / v['cincon_rca_bare_KpW'] / (1 / v['cincon_eff_part'] - 1)))

    # ---- capacitance / regen ----
    D = 0.5
    C_ripple = Ipk * D * (1 - D) / (v['pwm_hz'] * 0.1) * 1e6  # uF for 0.1 V
    C_bus = (m * (v['g2_cbulk_onboard_uF'] + v['C_add_per_G2_uF']) + v['C_cincon_out_uF']) * 1e-6
    vel = n_out / v['bevel_ratio'] * 2 * math.pi / 60 * v['wheel_r_m']
    E_robot = 0.5 * v['mass_kg'] * vel ** 2
    E_rot = m * 0.5 * v['J_rotor_kgm2'] * w ** 2
    E = E_robot + E_rot
    V_dump = math.sqrt(24 ** 2 + 2 * E / C_bus)
    C_needed_27 = 2 * E / (27 ** 2 - 24 ** 2) * 1e6
    regen_W_ramp = E / v['ramp_s']
    # duty cap at standstill, mech accel time
    D_start = Ipk * R24 / 24
    J_refl = v['mass_kg'] * v['wheel_r_m'] ** 2 / m / (v['gear_ratio'] * v['bevel_ratio']) ** 2
    t_acc_free = (v['J_rotor_kgm2'] + J_refl) * w / ((Kt24 * Ipk - Tf - Tm) / 1000)
    out['caps_regen'] = dict(C_per_G2_for_0p1V_ripple_uF=C_ripple, C_bus_total_uF=C_bus * 1e6,
                             v_m_s=vel, E_robot_J=E_robot, E_rotors_J=E_rot, E_total_J=E,
                             V_bus_if_dumped_no_load=V_dump, C_needed_for_27V_uF=C_needed_27,
                             regen_W_with_ramp=regen_W_ramp, aux_load_min_W=logic24 + v['cam_W'] / v['reg12_eff'],
                             D_start_cap=D_start, J_reflected_kgm2=J_refl, t_accel_at_Ilim_s=t_acc_free,
                             cs_V_at_Ilim=v['g2_cs_offset_V'] + v['g2_cs_V_per_A'] * Ipk)

    # ---- tether ----
    r20 = 2 * v['tether_m'] * v['core_ohm_per_km'] / 1000
    tet = {}
    for name, pout in [('A_duty', cases['A_duty_1Nm']), ('B_limit', cases['B_both_at_Ilim_full_speed']),
                       ('cincon_150W', v['cincon_pout_max_W'])]:
        eff = v['cincon_eff_full'] if pout > 75 else v['cincon_eff_part']
        pin = pout / eff
        for src in (v['src_V'], v['src_V_low']):
            for tag, r in (('20C', r20), ('hot', r20 * v['hot_mult'])):
                res = feed(src, pin, r)
                tet[f'{name}|{src:.0f}V|{tag}'] = dict(P_in_W=pin, R_loop_ohm=r,
                    Vin=res[0] if res else None, I_A=res[1] if res else None, drop_V=res[2] if res else None,
                    margin_to_43V=(res[0] - v['cincon_vin_min_V']) if res else None)
    out['tether'] = tet
    out['tether_Pmax_collapse_W'] = v['src_V'] ** 2 / (4 * r20 * v['hot_mult'])
    out['inputs'] = {k: dict(value=x[0], tag=x[1], source=x[2]) for k, x in I.items()}
    return out


def show(o):
    m = o['motor24']
    print('Motor 24 V winding (DERIVED): R=%.1f Ω Kt=%.0f mN·m/A Kv=%.0f I0=%.2f A Istall=%.2f A (cold %.2f) Tstall=%.0f mN·m Irated=%.2f A'
          % (m['R_ohm'], m['Kt_mNm_A'], m['Kv_rpm_V'], m['I0_A'], m['I_stall_A'], m['I_stall_cold_A'], m['T_stall_mNm'], m['I_rated_A']))
    print('Duty 1.0 N·m i=62: Tm=%.1f mN·m I=%.2f A n_out@24V=%.1f rpm (87 rpm needs %.1f V) Pel=%.1f W Pmech=%.1f W'
          % (m['T_motor_duty_mNm'], m['I_duty_A'], m['n_out_at_24V_rpm'], m['V_needed_for_target_rpm'], m['P_el_duty_W'], m['P_mech_out_W']))
    s = o['seller_check']
    print('Seller i=138/87 rpm -> motor %.0f rpm, Kv %.0f needed (24 V winding %.0f, 12 V winding %.0f) -> 12 V winding; its stall @24 V = %.0f A'
          % (s['motor_rpm'], s['kv_needed'], s['kv_24V_winding'], s['kv_12V_winding'], s['I_stall_12V_winding_at_24V_A']))
    print('Rails:', {k: round(x, 2) for k, x in o['rails'].items()})
    print('Design limit %.0f W; max I_lim per motor %.2f A' % (o['cincon_design_limit_W'], o['I_lim_max_per_motor_A']))
    for k, c in o['cases_W_24V'].items():
        print('  %-36s %6.1f W  %5.2f A  %5.0f %%  over150=%s overOCPmin=%s' % (k, c['P_W'], c['I_bus_A'], c['pct_of_150W'], c['over_rating'], c['over_ocp_min']))
    t = o['thermal']
    print('Thermal: R_ha=%.2f K/W  C=%.0f J/K  tau=%.0f s  wall start %.1f C  I2t budget/motor %.0f A2s  bare Cincon %.1f W'
          % (t['R_body_amb_KpW'], t['heat_capacity_J_per_K'], t['tau_s'], t['T_wall_start_C'], t['I2t_budget_per_motor_A2s'], t['cincon_pout_allowed_bare_W']))
    for k, c in t['cases'].items():
        tl = c['time_to_limit_from_A_s']
        print('  %-22s Pout=%5.1f W I=%.2f A Pint=%5.1f W (Cincon %.1f, Cu %.1f, fric+gear %.1f) wall=%5.1f air=%5.1f Tc=%5.1f lim_wall=%.1f %s'
              % (k, c['P_out_cincon_W'], c['I_motor_A'], c['P_internal_W'], c['losses_W']['cincon_W'], c['losses_W']['motor_cu_W'],
                 c['losses_W']['motor_fric_W'] + c['losses_W']['gearhead_W'], c['T_wall_ss_C'], c['T_air_ss_C'], c['Tc_cincon_ss_C'],
                 c['T_wall_limit_C'], 'steady OK' if tl is None else 'SHORT-TIME %.0f s (cold %.0f s)' % (tl, c['time_to_limit_from_cold_s'])))
    print('Caps/regen:', {k: round(x, 4) for k, x in o['caps_regen'].items()})
    print('Tether collapse power (hot) %.0f W' % o['tether_Pmax_collapse_W'])
    for k, t in o['tether'].items():
        print('  %-26s Pin=%5.1f R=%5.2f Vin=%5.1f I=%4.2f drop=%4.1f margin43=%4.1f'
              % (k, t['P_in_W'], t['R_loop_ohm'], t['Vin'], t['I_A'], t['drop_V'], t['margin_to_43V']))


if __name__ == '__main__':
    ap = argparse.ArgumentParser()
    ap.add_argument('--json', default=str(ROOT / 'current/07_TESTS/power_budget_F19.json'))
    a = ap.parse_args()
    o = main()
    show(o)
    Path(a.json).write_text(json.dumps(o, indent=2, ensure_ascii=False))
    print('wrote', a.json)
