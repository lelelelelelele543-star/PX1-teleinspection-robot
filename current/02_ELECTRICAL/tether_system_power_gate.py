"""PX1 integrated 40 m power screening; design assumptions, not measured specs."""
from math import sqrt
L=40; AREA=1.5; RHO=0.0175; ALPHA=0.00393; TEMP=60
V_BUS=24; I_LOAD=3.7; ETA=.90
R=2*L*RHO*(1+ALPHA*(TEMP-20))/AREA
def constant_current(v,i=I_LOAD):
    return v-i*R, i*i*R
def constant_power(v,p=V_BUS*I_LOAD/ETA):
    d=v*v-4*R*p
    if d<0: return None
    i=2*p/(v+sqrt(d))
    return v-i*R,i,i*i*R
def test():
    assert .99<R<1.1
    a=constant_current(24)
    b=constant_power(36)
    assert a[0]<21 and b[0]>32
    assert abs(36*b[1]-b[2]-24*I_LOAD/ETA)<1e-8
    return a,b
if __name__=="__main__":
    a,b=test()
    print("PASS: arithmetic and energy balance")
    print("24V fixed-current: %.2f V, %.2f W cable loss"%a)
    print("36V conditional constant-power: %.2f V, %.2f A, %.2f W cable loss"%b)
    print("NOT_RUN: startup, converter rating, CVBS, RS485, EMC, pressure")
