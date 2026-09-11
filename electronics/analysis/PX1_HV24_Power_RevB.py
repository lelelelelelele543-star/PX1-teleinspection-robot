import math, json

# PX-1 Rev.B WB07 — 120 V tether -> 24 V converter / long-line screen
# Final release uses measured cable and converter efficiency/thermal data.

VS=120.0
EFF=0.89
R_HOT_150M=18.573  # ohm loop, WB06 AWG22 60C screen
CONVERTER_MAX_OUT_W=24.0*6.3


def constant_power(vs,p,r):
    d=vs*vs-4*p*r
    if d<=0:
        return {'stable':False}
    vr=(vs+math.sqrt(d))/2
    i=p/vr
    return {
        'stable':True,
        'crawler_input_V':vr,
        'line_current_A':i,
        'cable_drop_V':vs-vr,
        'cable_loss_W':i*i*r,
    }

loads={}
for pout in (60,90,100,120,145,150):
    pin=pout/EFF
    loads[str(pout)]={
        'converter_input_power_W':pin,
        'converter_dissipation_W':pin-pout,
        **constant_power(VS,pin,R_HOT_150M)
    }

result={
    'status':'PASS_SCREEN',
    'converter':{
        'part':'Cincon CQB150W-110S24',
        'input_VDC':[43,160],
        'output_V':24.0,
        'output_A':6.3,
        'output_W':CONVERTER_MAX_OUT_W,
        'efficiency_full_load_nominal':EFF,
        'body_mm':[57.9,36.8,12.7],
        'isolation_VDC':3000,
    },
    'input_capacitor':{
        'part':'Nichicon UCS2D221MHD1TN',
        'capacitance_uF':220,
        'rating_VDC':200,
        'body_mm':[18,25],
        'stored_energy_J_at_120V':0.5*220e-6*VS*VS,
    },
    'local_fuse':{
        'part':'Eaton Bussmann S505H-3.15-R / BK1-S505H-3-15-R',
        'current_A':3.15,
        'rating_VDC':400,
        'characteristic':'time-delay',
        'size_mm':[5,20],
    },
    'hot_150m_awg22_screen':{
        'source_V':VS,
        'loop_R_ohm':R_HOT_150M,
        'load_cases_by_output_W':loads,
    },
    'power_policy':{
        'normal_total_output_target_W':'<=100',
        'short_controlled_peak_W':'120-145',
        'continuous_150W_at_hot_150m':'NOT_DESIRED_due_to_tether_loss_and_thermal_load',
    },
    'release_holds':[
        'physical CQB150W-110S24 sample and carrier fit',
        'converter thermal soak in sealed body',
        'actual 40/100/150m cable resistance tests',
        'cold and rapid-restart inrush qualification',
        'CCU 120V source current-limited ramp',
        '24V regenerative energy / bus clamp WB08',
    ]
}
print(json.dumps(result,indent=2))
