"""PX1: 40m six-core signal/power integration screening; assumptions, NOT cable qualification.
Run: python current/02_ELECTRICAL/tether_signal_screen.py
"""
from math import pi
from pathlib import Path
L=40.; RHO=.0175; ALPHA=.00393; TEMP=60.; I=3.7
CORES=("PWR+","PWR-","RS485 A","RS485 B","CVBS","CVBS RETURN")
def loop_r(area,temp=TEMP):
    if area<=0: raise ValueError("area")
    return 2*L*RHO*(1+ALPHA*(temp-20))/area
def dc(area):
    r=loop_r(area)
    return 24-I*r,I*I*r
def rc_corner(cap_pf_m,signal_area=.25,source_ohm=75):
    """Lumped RC sensitivity only; NOT CVBS transmission-line bandwidth."""
    if cap_pf_m<=0: raise ValueError("capacitance")
    return 1/(2*pi*(source_ohm+loop_r(signal_area,20))*L*cap_pf_m*1e-12)
def svg():
    lines=['<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 1200 680">','<rect width="1200" height="680" fill="white"/>','<text x="30" y="40" font-family="sans-serif" font-size="26">PX1 / 40m six-core tether signal screen</text>','<text x="30" y="70" font-family="sans-serif" font-size="15">ENGINEERING SCHEMATIC / ASSUMED DIMENSIONS / NOT A VERIFIED HARNESS</text>','<rect x="30" y="100" width="200" height="370" fill="#eef2f7" stroke="#64748b"/>','<rect x="970" y="100" width="200" height="370" fill="#eef2f7" stroke="#64748b"/>','<text x="48" y="126" font-family="sans-serif" font-size="18">CONSOLE</text>','<text x="990" y="126" font-family="sans-serif" font-size="18">ROBOT</text>']
    for i,(name,color) in enumerate(zip(CORES,("#c2410c","#334155","#2563eb","#0284c7","#15803d","#65a30d"))):
        y=160+53*i
        lines.extend([f'<path d="M230 {y} H970" stroke="{color}" stroke-width="5"/>',f'<text x="350" y="{y-11}" font-family="sans-serif" font-size="16">{name}</text>'])
    v,loss=dc(2.5)
    lines.extend([f'<text x="30" y="520" font-family="monospace" font-size="18">2.5 mm2 power cores, 3.7 A, 60 C: robot {v:.2f} V; cable loss {loss:.2f} W</text>','<text x="30" y="555" font-family="sans-serif" font-size="16">CVBS RETURN is a conductor, NOT coax shielding. Signal conductor 0.25 mm2 assumed.</text>','<text x="30" y="585" font-family="sans-serif" font-size="16">NOT_RUN: CVBS reflections/attenuation, RS485 BER/common-mode, motor-on EMC.</text>','<text x="30" y="615" font-family="sans-serif" font-size="16">PHYSICAL_CHECK: actual cable capacitance/impedance, pressure gland, heat and image.</text>','<text x="30" y="645" font-family="sans-serif" font-size="16">PASS: six-core mapping and arithmetic only. No manufacturing release.</text>','</svg>'])
    return "\n".join(lines)+"\n"
def main():
    assert len(CORES)==6 and len(set(CORES))==6
    assert abs(loop_r(1,20)-1.4)<1e-10
    assert dc(1.5)[0]<21<dc(2.5)[0]
    assert 8<dc(2.5)[1]<10
    assert rc_corner(50)>rc_corner(100)>rc_corner(200)
    Path(__file__).with_suffix(".svg").write_text(svg(),encoding="utf-8")
    print("PASS: DC, pin count and RC arithmetic; NOT_RUN: CVBS/RS485 SI and EMC")
if __name__=="__main__": main()
