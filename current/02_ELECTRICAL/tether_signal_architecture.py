"""PX1 40m six-core signal architecture screening (DESIGN ASSUMPTIONS).
Run: python current/02_ELECTRICAL/tether_signal_architecture.py
Produces tether_signal_architecture.svg and .json alongside source.
This is NOT a measured cable model or validated CVBS/RS485 performance.
"""
from pathlib import Path
import json, math

L_M=40.0
V_SUPPLY=24.0
I_TOTAL=3.7
COPPER_MM2=2.5
RHO20=0.0175
ALPHA=0.00393
TEMP_C=60.0
VIDEO_OHM=75.0
VIDEO_MHZ=5.0
BAUD=115200
V_PROP_M_S=2e8
# Unverified cable parameters: sweep to expose sensitivity, not to predict picture quality
CAP_PF_M=(40,70,100,150)
VIDEO_RETURN_MM2=(0.25,0.5,1.0)
# CVBS unbalanced, no coax: shield/return geometry and crosstalk UNKNOWN
def dc_voltage(area_mm2=COPPER_MM2, amps=I_TOTAL, temp=TEMP_C):
    rho=RHO20*(1+ALPHA*(temp-20))
    loop=2*L_M*rho/area_mm2
    return {"loop_ohm":loop,"load_v":V_SUPPLY-amps*loop,
            "loss_w":amps*amps*loop}
def video_screen(cap_pf_m, return_mm2, freq_mhz=VIDEO_MHZ):
    # R distributed on a single video return wire; assumes 75-ohm load.
    # Lumped low-pass is a deliberately crude bounding sensitivity model.
    rho=RHO20*(1+ALPHA*(TEMP_C-20))
    r_return=L_M*rho/return_mm2
    c=L_M*cap_pf_m*1e-12
    r_th=VIDEO_OHM/2+r_return
    ratio=1/math.sqrt(1+(2*math.pi*freq_mhz*1e6*r_th*c)**2)
    return {"return_ohm":r_return,"cap_nf":c*1e9,"rc_ratio":ratio}
def rs485_screen(baud=BAUD):
    delay=L_M/V_PROP_M_S
    bit=1/baud
    # Does NOT estimate BER: unpaired conductors, motor EMI and common-mode unknown
    return {"one_way_us":delay*1e6,"bit_us":bit*1e6,
            "one_way_bit_fraction":delay/bit,
            "termination_each_end_ohm":120,
            "termination_power_at_2v_diff_w":4/120}
def generate():
    power=dc_voltage()
    rs=rs485_screen()
    sweep=[{"cap_pf_m":cap,"return_mm2":area,**video_screen(cap,area)}
           for cap in CAP_PF_M for area in VIDEO_RETURN_MM2]
    assert abs(power["load_v"]-21.6023)<0.01
    assert abs(power["loss_w"]-8.8716)<0.01
    assert abs(rs["one_way_us"]-0.2)<1e-9
    assert all(0<x["rc_ratio"]<1 for x in sweep)
    assert video_screen(150,0.25)["rc_ratio"]<video_screen(40,1.0)["rc_ratio"]
    data={"classification":"DESIGN ASSUMPTIONS / ANALYTICAL SCREEN ONLY",
          "power":power,"rs485":rs,"video_sweep":sweep,
          "pinout":{"1":"DC +24V","2":"DC return","3":"RS485 A","4":"RS485 B",
                    "5":"CVBS signal","6":"CVBS return"},
          "blockers":["Video attenuation, reflections and crosstalk require measured cable RLGC / VNA or test pattern",
                      "RS485 BER and common-mode under motor PWM NOT_RUN",
                      "Return current coupling, pressure gland and bend fatigue PHYSICAL_CHECK",
                      "Do not treat 120 ohm termination as verified cable characteristic impedance"]}
    out=Path(__file__).resolve().parent
    (out/"tether_signal_architecture.json").write_text(json.dumps(data,indent=2,ensure_ascii=False)+"\n",encoding="utf-8")
    rows=''.join(f'<text x="70" y="{280+i*28}" font-size="16">{p}: {v}</text>'
                 for i,(p,v) in enumerate(data["pinout"].items()))
    bars=''.join(f'<rect x="{620+i*49}" y="{525-200*x["rc_ratio"]:.1f}" width="28" height="{200*x["rc_ratio"]:.1f}" fill="#3984aa"/>' for i,x in enumerate(sweep))
    svg=f'''<svg xmlns="http://www.w3.org/2000/svg" width="1280" height="650" viewBox="0 0 1280 650">
<rect width="1280" height="650" fill="#f8fafc"/>
<text x="50" y="55" font-size="29" font-family="sans-serif" font-weight="bold">PX1 | 40 m / six-core tether interface</text>
<text x="50" y="88" font-size="17" font-family="sans-serif" fill="#9b4b13">DESIGN ASSUMPTIONS — NOT A VERIFIED TRANSMISSION LINE</text>
<rect x="50" y="120" width="340" height="470" rx="12" fill="#e5edf5" stroke="#66788a"/>
<text x="70" y="157" font-size="23" font-family="sans-serif">Six copper cores</text>
<text x="70" y="193" font-size="16" font-family="sans-serif">40 m, no coax, no twisted pair</text>
<g font-family="sans-serif">{rows}</g>
<rect x="430" y="120" width="800" height="180" rx="12" fill="#e7f2e9" stroke="#6b8970"/>
<g font-family="sans-serif" font-size="19">
<text x="455" y="158">Power: 24 V / 3.7 A / 2.5 mm² @ 60 °C</text>
<text x="455" y="194">Load voltage: {power["load_v"]:.2f} V; cable loss: {power["loss_w"]:.2f} W</text>
<text x="455" y="230">RS485 one-way delay: {rs["one_way_us"]:.2f} µs / {rs["bit_us"]:.2f} µs bit</text>
<text x="455" y="265" fill="#a23a2a">RS485 BER, EMI and CVBS quality: NOT_RUN</text>
</g>
<rect x="430" y="322" width="800" height="268" rx="12" fill="#f3eee7" stroke="#99836c"/>
<g font-family="sans-serif"><text x="455" y="355" font-size="20">CVBS lumped RC sensitivity (NOT picture-quality prediction)</text>
<text x="455" y="380" font-size="15">12 cases: 40–150 pF/m × 0.25–1.0 mm² video return</text>
<line x1="600" y1="525" x2="1210" y2="525" stroke="#333"/>
<line x1="600" y1="325" x2="600" y2="525" stroke="#333"/>
{bars}
<text x="610" y="562" font-size="15">Scenario index (capacitance × return area)</text>
</g>
<text x="50" y="625" font-family="sans-serif" font-size="16">PASS: arithmetic assertions in Python | PHYSICAL_CHECK: cable, video, RS485, gland, pressure</text>
</svg>'''
    (out/"tether_signal_architecture.svg").write_text(svg,encoding="utf-8")
    print("PASS arithmetic assertions; generated SVG and JSON; NOT_RUN physical signal tests")
if __name__=="__main__":
    generate()
