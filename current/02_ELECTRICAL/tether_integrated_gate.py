"""PX1 integrated 40m six-core electrical screen. All cable/signal values are DESIGN ASSUMPTIONS.
Run: python tether_integrated_gate.py. No external dependencies. Not a transmission-line simulator.
"""
from math import pi, sqrt
L=40.; V=24.; I=3.7; AREA=2.5; RHO20=.0175; ALPHA=.00393; TEMP=60.
CAP_PF_M=100.; F_VIDEO=5e6; RS_BAUD=115200.; PROP_SPEED=2e8
def evaluate(area=AREA, current=I, temp=TEMP, cap_pf_m=CAP_PF_M):
    rho=RHO20*(1+ALPHA*(temp-20))
    loop=2*L*rho/area
    cap=L*cap_pf_m*1e-12
    # Lumped RC upper-level sensitivity only, not a verified CVBS channel.
    r_thevenin=75*75/(75+75)
    rc=1/sqrt(1+(2*pi*F_VIDEO*r_thevenin*cap)**2)
    delay=L/PROP_SPEED
    return dict(loop_ohm=loop, robot_v=V-current*loop,
                loss_w=current*current*loop, cap_nf=cap*1e9,
                cvbs_rc_ratio=rc, rs_delay_us=delay*1e6,
                rs_bit_us=1e6/RS_BAUD, rs_delay_bit_fraction=delay*RS_BAUD)
if __name__=="__main__":
    x=evaluate()
    assert abs(x["robot_v"]-21.6023)<0.01
    assert abs(x["loss_w"]-8.8716)<0.01
    assert 0<x["cvbs_rc_ratio"]<1
    assert x["rs_delay_bit_fraction"]<0.1
    for k,v in x.items(): print(k,round(v,5))
    print("PASS: arithmetic only; NOT_RUN: RS485 BER, CVBS quality, EMI, motor transients, pressure")
