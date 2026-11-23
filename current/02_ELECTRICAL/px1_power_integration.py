"""PX1 40 m tether: combined motor + auxiliary current screen. DESIGN ASSUMPTIONS only.
Run: python current/02_ELECTRICAL/px1_power_integration.py
"""
from pathlib import Path
from math import isclose
L=40.0; RHO=0.0175; ALPHA=0.00393; VIN=24.0; VMIN=21.0; AUX=0.70
AREAS=(1.0,1.5,2.5)
def resistance(area,temp):
    if area<=0 or not -40<=temp<=120: raise ValueError("area/temp")
    return 2*L*RHO*(1+ALPHA*(temp-20))/area
def evaluate(area,temp,motors):
    if motors<0: raise ValueError("motor current")
    total=AUX+motors; r=resistance(area,temp)
    return {"robot_v":VIN-total*r,"heat_w":total*total*r,"pass_bus":VIN-total*r>=VMIN}
def budget(area,temp):
    return (VIN-VMIN)/resistance(area,temp)-AUX
def svg():
    s=['<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 1100 550">',
       '<rect width="1100" height="550" fill="#f8fafc"/>',
       '<text x="30" y="45" font-family="sans-serif" font-size="26">PX1 / 40 m / power integration</text>',
       '<text x="30" y="75" font-family="sans-serif" font-size="15">PARAMETRIC 2D — all dimensions and currents are DESIGN ASSUMPTIONS</text>']
    for x,w,label,fill in [(30,230,"24 V console","#dbeafe"),(360,300,"40 m power pair","#fef3c7"),(760,300,"Robot: motors + aux","#dcfce7")]:
        s += [f'<rect x="{x}" y="110" width="{w}" height="90" rx="8" fill="{fill}" stroke="#334155"/>',
              f'<text x="{x+15}" y="155" font-family="sans-serif" font-size="19">{label}</text>']
    s += ['<path d="M260 155 H360 M660 155 H760" stroke="#334155" stroke-width="3"/>',
          '<text x="30" y="245" font-family="sans-serif" font-size="20">60 C copper / 21 V assumed minimum / 0.70 A auxiliary current</text>']
    for i,a in enumerate(AREAS):
        q=evaluate(a,60,3); y=295+i*58
        s += [f'<rect x="30" y="{y-30}" width="1030" height="42" fill="{("#dbeafe" if i==1 else "#e2e8f0")}"/>',
              f'<text x="48" y="{y}" font-family="monospace" font-size="18">{a:.1f} mm2  motor budget {budget(a,60):.2f} A   at 3 A motors: {q["robot_v"]:.2f} V / {q["heat_w"]:.1f} W   {"PASS" if q["pass_bus"] else "FAIL"}</text>']
    s += ['<text x="30" y="510" font-family="sans-serif" font-size="14">NOT_RUN: inrush, motor driver compatibility, CVBS, RS485. PHYSICAL_CHECK: thermal, seals, cable.</text>','</svg>']
    return "\n".join(s)+"\n"
def main():
    assert isclose(resistance(1,20),1.4)
    assert isclose(evaluate(1,20,1.3)["robot_v"],21.2)
    assert budget(2.5,60)>budget(1.5,60)>budget(1,60)
    assert not evaluate(1.5,60,3)["pass_bus"]
    assert evaluate(2.5,60,3)["pass_bus"]
    Path(__file__).with_suffix(".svg").write_text(svg(),encoding="utf-8")
    print("PASS arithmetic + SVG; NOT_RUN electrical hardware")
if __name__=="__main__": main()
