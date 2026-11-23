"""PX1 DC supply alternatives; DESIGN ASSUMPTIONS, not measured specifications."""
from math import sqrt
L=40.; RHO=0.0175; ALPHA=0.00393; TEMP=60.; AREA=2.5
LOAD_I=3.7; LOAD_P=24*LOAD_I; ETA=.90
R=2*L*RHO*(1+ALPHA*(TEMP-20))/AREA
def constant_power(v,p):
    d=v*v-4*R*p
    if d<0: return None
    i=2*p/(v+sqrt(d))
    return (i,v-i*R,i*i*R)
def check():
    i=LOAD_I
    a=(i,24-i*R,i*i*R)
    b=constant_power(36,LOAD_P/ETA)
    assert b is not None
    assert abs(24*i-a[2]-i*a[1])<1e-8
    assert abs(36*b[0]-b[2]-LOAD_P/ETA)<1e-8
    assert 0.647<R<0.650 and 21.5<a[1]<21.7 and 34<b[1]<34.3
    return a,b
if __name__=="__main__":
    a,b=check()
    print("PASS energy balance and numerical regression")
    print("24V constant-current: line %.3f A, robot %.3f V, cable %.3f W; delivered %.3f W"%(a[0],a[1],a[2],a[0]*a[1]))
    print("36V constant-power: line %.3f A, converter input %.3f V, cable %.3f W; assumed converter output %.1f W"%(b[0],b[1],b[2],LOAD_P))
    print("NOT_RUN motor start, converter input/output rating, CVBS, RS485; PHYSICAL_CHECK seals, cable and heating")
