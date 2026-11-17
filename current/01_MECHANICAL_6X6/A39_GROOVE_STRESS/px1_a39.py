"""PX1 A39 — sensitivity study, NOT a fatigue qualification.
Kt is a sweep of assumed theoretical stress concentration factors, NOT a DIN lookup.
"""
import math, csv
from pathlib import Path
SHAFT_D=12.0
GROOVE_D=11.0
TORQUES=(5.0,10.0,20.0)
KT=(1.0,1.5,2.0,2.5,3.0)
def nominal_tau(t_nm,d_mm):
    return 16000*t_nm/(math.pi*d_mm**3)
def calculate():
    return [(t,k,round(nominal_tau(t,GROOVE_D),3),round(k*nominal_tau(t,GROOVE_D),3))
            for t in TORQUES for k in KT]
def test():
    assert abs(nominal_tau(10,11)-38.262)<0.01
    assert all(a<=b for _,_,a,b in calculate())
    assert len(calculate())==15
    assert abs(nominal_tau(10,11)/nominal_tau(10,12)-(12/11)**3)<1e-10
if __name__=="__main__":
    test()
    with (Path(__file__).parent/"a39_results.csv").open("w",newline="") as f:
        w=csv.writer(f);w.writerow(["assumed_torque_Nm","assumed_Kt","nominal_tau_MPa","Kt_times_nominal_MPa"]);w.writerows(calculate())
    print("PASS: 15 scenarios; Kt is an assumption, not measured")
