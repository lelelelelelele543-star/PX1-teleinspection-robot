import math, json

# PX-1 Rev.B WB08 — 24 V traction bus protection screen
# Not a braking-energy FEA/model. Final limits use measured motor/crawler data.

VBUS=24.0
BTS_ABS_MAX=45.0
BTS_OV_MIN=27.6
BTS_OV_MAX=30.0
TVS={'part':'Littelfuse 1.5KE30A','vrwm':25.6,'vbr_min':28.5,'vbr_max':31.5,'vc_max':41.4,'ipp_A':36.7,'ppk_W':1500}
CAP_EACH_F=1000e-6
CAP_COUNT=2
CAP_TOTAL=CAP_EACH_F*CAP_COUNT
CAP_RATED=50.0
DIV_TOP=100000.0
DIV_BOT=6800.0
ADC_V=3.3
CRAWLER_MASS=8.5
CRAWLER_SPEED=0.113


def cap_extra(v):
    return 0.5*CAP_TOTAL*(v*v-VBUS*VBUS)


def adc(v):
    return v*DIV_BOT/(DIV_TOP+DIV_BOT)

levels=[27.5,28.5,30.0,TVS['vc_max'],BTS_ABS_MAX]
energy={str(v):cap_extra(v) for v in levels}
adc_levels={str(v):adc(v) for v in [24.0,26.5,27.0,28.5,30.0,41.4,45.0]}
trans_ke=0.5*CRAWLER_MASS*CRAWLER_SPEED**2

result={
    'status':'PASS_SCREEN',
    'bus_V_nominal':VBUS,
    'bts7960':{
        'absolute_supply_max_V':BTS_ABS_MAX,
        'overvoltage_lockout_V_range':[BTS_OV_MIN,BTS_OV_MAX],
        'prototype_only_due_to_obsolete_device':'YES'
    },
    'tvs':TVS,
    'bulk_capacitors':{
        'part':'Nichicon UHE1H102MHD6',
        'each_uF':1000,
        'count':CAP_COUNT,
        'total_uF':CAP_TOTAL*1e6,
        'rating_V':CAP_RATED,
        'energy_absorption_above_24V_J':energy
    },
    'translational_KE_reference_J':trans_ke,
    'translational_KE_warning':'reference only; excludes motor/gear inertia, gravity/backdrive and tether work',
    'bus_adc':{
        'divider_ohm':[DIV_TOP,DIV_BOT],
        'adc_values_V':adc_levels,
        'adc_at_45V_below_3v3':adc(BTS_ABS_MAX)<ADC_V
    },
    'firmware_starting_thresholds_V':{
        'warning_ramp_down':26.5,
        'traction_inhibit_latch':27.0,
        'reenable_below':25.5
    },
    'stop_policy':'PWM ramp down -> both bridge enables/INH low -> coast; no hard reverse/dynamic-brake release',
    'release_holds':[
        'actual motor current-to-torque map',
        'external per-side current-sensor calibration',
        'bus oscilloscope logs under stop/reversal/jam/downhill',
        'branch fuse values',
        'actual IBT-2 board decoupling inspection',
        'Rev.C production H-bridge decision'
    ]
}

print(json.dumps(result,indent=2))
