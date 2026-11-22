"""PX1 combined 40m traction + auxiliary voltage screen. All values DESIGN ASSUMPTIONS.
Run: python current/02_ELECTRICAL/tether_transient_envelope.py
Constant-current copper resistance screen, NOT a motor-start transient simulation.
"""
from pathlib import Path
L=40.0; V=24.0; RHO=0.0175; ALPHA=0.00393; VMIN=21.0
AUX=0.70  # camera .18, lighting .32, controller .12, reserve .08 A (assumed)
AREAS=(1.0,1.5,2.5); TEMPS=(20.0,60.0)
MOTOR_TOTAL=(0.0,1.3,2.0,3.0,4.0,6.0)
def resistance(area,temp):
    if area<=0 or not -40<=temp<=120: raise ValueError("invalid area/temp")
    return 2*L*RHO*(1+ALPHA*(temp-20))/area
def robot_voltage(area,temp,motors):
    if motors<0: raise ValueError("negative current")
    return V-(AUX+motors)*resistance(area,temp)
def current_limit(area,temp):
    return (V-VMIN)/resistance(area,temp)
def svg():
    s=['<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 1100 650">',
       '<rect width="1100" height="650" fill="#f8fafc"/>',
       '<text x="30" y="45" font-family="sans-serif" font-size="26" font-weight="bold">PX1 / 40m / 24V: traction + auxiliary current envelope</text>',
       '<text x="30" y="76" font-family="sans-serif" font-size="15">DESIGN ASSUMPTIONS: 21V minimum, 0.70A auxiliaries, copper properties, 20/60C</text>',
       '<text x="30" y="107" font-family="sans-serif" font-size="15">Two power cores; four remaining cores: RS485 A/B, CVBS signal/return. Not a start-current simulation.</text>',
       '<text x="30" y="155" font-family="sans-serif" font-size="19" font-weight="bold">60C current limits at 21V robot input</text>']
    for i,a in enumerate(AREAS):
        y=195+i*46
        s += [f'<rect x="30" y="{y-28}" width="1030" height="35" fill="{("#dbeafe" if a==1.5 else "#e2e8f0")}"/>',
              f'<text x="48" y="{y}" font-family="monospace" font-size="17">{a:.1f} mm2     total {current_limit(a,60):.2f} A     traction budget {current_limit(a,60)-AUX:.2f} A     (20C total {current_limit(a,20):.2f} A)</text>']
    s += ['<text x="30" y="360" font-family="sans-serif" font-size="19" font-weight="bold">Robot input voltage at 60C for combined motor currents</text>',
          '<text x="40" y="395" font-family="monospace" font-size="16">Motor sum     Total w/aux      1.0mm2      1.5mm2      2.5mm2</text>']
    for i,m in enumerate(MOTOR_TOTAL):
        y=430+i*34
        values=[robot_voltage(a,60,m) for a in AREAS]
        s += [f'<rect x="30" y="{y-23}" width="1030" height="29" fill="{("#f1f5f9" if i%2==0 else "#e2e8f0")}"/>',
              f'<text x="45" y="{y}" font-family="monospace" font-size="16">{m:5.2f} A          {m+AUX:5.2f} A         {values[0]:6.2f} V     {values[1]:6.2f} V     {values[2]:6.2f} V</text>']
    s += ['<text x="30" y="639" font-family="sans-serif" font-size="13">PASS arithmetic; NOT_RUN inrush, UVLO, RS485/CVBS; PHYSICAL_CHECK cable and motor current</text>','</svg>']
    return "\n".join(s)+"\n"
def main():
    assert abs(resistance(1,20)-1.4)<1e-10
    assert abs(robot_voltage(1,20,1.3)-21.2)<1e-10
    assert abs(robot_voltage(1.5,60,1.3)-21.84)<0.02
    assert robot_voltage(1.5,60,3)<VMIN
    assert robot_voltage(2.5,60,2)>VMIN
    assert current_limit(2.5,60)>current_limit(1.5,60)>current_limit(1,60)
    target=Path(__file__).with_suffix(".svg"); target.write_text(svg(),encoding="utf-8")
    for a in AREAS: print(f"{a:.1f}mm2 / 60C: total limit {current_limit(a,60):.3f}A; motors {current_limit(a,60)-AUX:.3f}A")
    print("PASS arithmetic and SVG generated")
if __name__=="__main__": main()
