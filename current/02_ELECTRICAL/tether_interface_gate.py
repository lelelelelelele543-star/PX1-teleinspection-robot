"""PX1: six-core tether interface and fault-envelope screen (assumptions, not release).
Run: python current/02_ELECTRICAL/tether_interface_gate.py
No external packages. Generates matching SVG next to this file.
"""
from pathlib import Path
from math import isclose
import html

L_M=40.0
RHO20=0.0175  # ohm mm2/m, ASSUMED
ALPHA=0.00393 # 1/K, ASSUMED
V_SOURCE=24.0
V_MIN=21.0    # provisional robot-side minimum, NOT component specification
AUX_A=0.70    # provisional total non-traction current
MOTOR_A=3.0   # provisional combined traction current
CORES=("PWR+","PWR-","RS485 A","RS485 B","CVBS","VIDEO RETURN")

def loop_r(area_mm2,temp_c):
    if area_mm2<=0 or not -40<=temp_c<=120:
        raise ValueError("invalid conductor area or temperature")
    return 2*L_M*RHO20*(1+ALPHA*(temp_c-20))/area_mm2

def screen(area_mm2,temp_c,motor_a=MOTOR_A,aux_a=AUX_A):
    if min(motor_a,aux_a)<0: raise ValueError("negative load")
    current=motor_a+aux_a
    resistance=loop_r(area_mm2,temp_c)
    return {"current_a":current,"loop_ohm":resistance,
            "drop_v":current*resistance,"robot_v":V_SOURCE-current*resistance,
            "loss_w":current*current*resistance,
            "bus_pass":V_SOURCE-current*resistance>=V_MIN}

def svg():
    lines=['<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 1180 650">',
           '<rect width="1180" height="650" fill="#f8fafc"/>',
           '<text x="30" y="42" font-family="sans-serif" font-size="26">PX1 / six-core 40 m tether interface</text>',
           '<text x="30" y="70" font-family="sans-serif" font-size="15">ENGINEERING 2D / DESIGN ASSUMPTIONS / NOT A VERIFIED WIRING HARNESS</text>']
    for i,(label,color) in enumerate(zip(CORES,("#e11d48","#334155","#2563eb","#0ea5e9","#16a34a","#15803d"))):
        y=105+i*56
        lines.extend([f'<circle cx="65" cy="{y}" r="13" fill="{color}"/>',
                      f'<path d="M85 {y} H800" stroke="{color}" stroke-width="4"/>',
                      f'<text x="110" y="{y-12}" font-family="sans-serif" font-size="16">{html.escape(label)}</text>'])
    lines.extend(['<rect x="795" y="82" width="350" height="345" rx="12" fill="none" stroke="#64748b" stroke-width="2"/>',
                  '<text x="820" y="450" font-family="sans-serif" font-size="16">Robot: DC bus / RS485 / CVBS receiver</text>',
                  '<text x="30" y="495" font-family="sans-serif" font-size="18">40 m copper / 60 C / 24 V supply / 3.7 A assumed total</text>'])
    for i,area in enumerate((1.5,2.5)):
        q=screen(area,60)
        lines.append(f'<text x="30" y="{530+i*35}" font-family="monospace" font-size="18">{area:.1f} mm2 power cores: Rloop={q["loop_ohm"]:.3f} ohm, Vrobot={q["robot_v"]:.2f} V, loss={q["loss_w"]:.1f} W, {"PASS" if q["bus_pass"] else "FAIL"} provisional bus gate</text>')
    lines.extend(['<text x="30" y="620" font-family="sans-serif" font-size="14">NOT_RUN: CVBS attenuation, RS485 eye/EMC, return coupling, start current. PHYSICAL_CHECK: pressure gland, temperature, shielding.</text>','</svg>'])
    return "\n".join(lines)+"\n"

def main():
    assert len(CORES)==6 and len(set(CORES))==6
    assert isclose(loop_r(1.0,20),1.4)
    assert screen(1.5,60)["bus_pass"] is False
    assert screen(2.5,60)["bus_pass"] is True
    assert screen(2.5,60)["loss_w"]<screen(1.5,60)["loss_w"]
    assert screen(1.5,60,0,0)["robot_v"]==V_SOURCE
    assert screen(2.5,60,6,0.7)["bus_pass"] is False
    Path(__file__).with_suffix(".svg").write_text(svg(),encoding="utf-8")
    print("PASS: six-core mapping and DC numerical regression; NOT_RUN: signal integrity")
if __name__=="__main__": main()
