import math, json

# PX-1 Rev.B WB06 — six-core tether power/signal screen
# Engineering screen only; final release uses measured cable resistance.

VS = 120.0
P_REMOTE_INPUT = 111.1  # W, ~100W useful load with 90% downstream-converter screen
R22_20 = 53.5            # ohm/km per conductor, conservative nominal AWG22 screen
R24_20 = 84.2            # ohm/km per conductor, nominal AWG24 screen
ALPHA_CU = 0.00393

lengths = [40, 100, 150]
temps = [20, 60]


def solve_constant_power(vs, p, rloop):
    disc = vs**2 - 4*p*rloop
    if disc <= 0:
        return {'stable_solution': False}
    vr = (vs + math.sqrt(disc))/2
    i = p/vr
    return {
        'stable_solution': True,
        'crawler_HV_input_V': vr,
        'line_current_A': i,
        'drop_V': vs-vr,
        'line_loss_W': i*i*rloop,
    }

power = {}
for temp in temps:
    factor = 1 + ALPHA_CU*(temp-20)
    power[str(temp)] = {}
    for L in lengths:
        rloop = 2 * R22_20 * factor * L / 1000
        power[str(temp)][str(L)] = {
            'loop_resistance_ohm': rloop,
            **solve_constant_power(VS, P_REMOTE_INPUT, rloop)
        }

signal = {}
for temp in temps:
    factor = 1 + ALPHA_CU*(temp-20)
    signal[str(temp)] = {
        str(L): 2*R24_20*factor*L/1000 for L in lengths
    }

# Demonstrate why six equal 26AWG conductors are not selected for the 150m power pair.
R26_20 = 133.9
r26_150 = 2*R26_20*150/1000
alt_26 = solve_constant_power(VS, P_REMOTE_INPUT, r26_150)

out = {
    'status': 'PASS_SCREEN',
    'topology': '2x22AWG power + 2x2x24AWG differential signal pairs = exactly 6 functional copper cores',
    'source_VDC': VS,
    'remote_input_power_W': P_REMOTE_INPUT,
    'power_loop_results': power,
    'signal_pair_loop_resistance_ohm': signal,
    'equal_26AWG_150m_power_rejection_screen': {
        'loop_resistance_20C_ohm': r26_150,
        **alt_26
    },
    'contact_freeze': {
        'male': 'LAPP 13162500 H-D SCEM AU 0.14-0.37',
        'female': 'LAPP 13163500 H-D BCEM AU 0.14-0.37',
        'reason': 'both ~0.33mm2 AWG22 and ~0.205mm2 AWG24 fit the same crimp barrel range'
    },
    'release_holds': [
        'measure actual 40m Proteus cable',
        'supplier-controlled custom tether drawing and guaranteed resistance/OD/mass',
        'pair impedance/capacitance and CVBS test',
        'tensile-member breaking load and tail clamp proof',
        'slip-ring/contact resistance in full 100/150m power budget',
        'HV converter input range and protected startup/inrush qualification'
    ]
}

print(json.dumps(out, indent=2))
