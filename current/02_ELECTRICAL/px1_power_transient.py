#!/usr/bin/env python3
"""PX1 tether transient power screen. All values are DESIGN ASSUMPTIONS."""
import math, json
from pathlib import Path
VS=24.; L=40.; RHO=.0175; ALPHA=.00393; TEMP=60.; IDLE=48.; PEAK=96.; DURATION=.25; MIN=20.
AREAS=(.5,.75,1.,1.5); CAPS=(0.,.047,.1,.22)
def resistance(a): return 2*L*RHO*(1+ALPHA*(TEMP-20))/a
def equilibrium(a,p):
    d=VS**2-4*resistance(a)*p
    return None if d<0 else (VS+math.sqrt(d))/2
def transient(a,c,dt=.0001):
    v=equilibrium(a,IDLE)
    if v is None:return None
    if c==0:return equilibrium(a,PEAK)
    minimum=v
    for _ in range(round(DURATION/dt)):
        v+=dt*((VS-v)/resistance(a)-PEAK/max(v,.1))/c
        if v<=0:return 0.
        minimum=min(minimum,v)
    return minimum
rows=[dict(area_mm2=a,bulk_cap_F=c,loop_ohm=round(resistance(a),4),min_V=None if transient(a,c) is None else round(transient(a,c),3),status="PASS_SCREEN" if transient(a,c) is not None and transient(a,c)>=MIN else "FAIL_SCREEN") for a in AREAS for c in CAPS]
assert abs(resistance(1.5)-1.08004)<.0001
assert equilibrium(1.5,PEAK)<MIN
assert transient(1.5,.22)>transient(1.5,0)
result=dict(status="CALCULATED_ONLY",assumptions=dict(source_V=VS,idle_W=IDLE,peak_W=PEAK,peak_s=DURATION,hot_C=TEMP,minimum_V=MIN,capacitor="ideal; ESR/ESL and regulator dynamics omitted"),rows=rows,checks=dict(math="PASS",startup="PHYSICAL_CHECK",capacitor_ESR="NOT_RUN",converter_stability="NOT_RUN",wire_ampacity="PHYSICAL_CHECK",CVBS_noise="PHYSICAL_CHECK"))
out=Path(__file__).resolve().parent
(out/"px1_power_transient.json").write_text(json.dumps(result,indent=2)+"\n")
print(json.dumps(result,indent=2))
