"""PX1 A38: nominal torsional stress at A37 shaft grooves. All torque values ASSUMED.
Not a fatigue or DIN 471 strength qualification. No stress concentration included.
"""
import math
import csv
from pathlib import Path
D_SHAFT_MM=12.0
D_GROOVE_MM=11.0
GROOVE_WIDTH_MM=1.1
TORQUES_NM=(5.0,10.0,20.0)
OUT=Path(__file__).parent
def tau_mpa(t_nm,d_mm):
    return 16.0*(t_nm*1000.0)/(math.pi*d_mm**3)
def run():
    assert D_GROOVE_MM<D_SHAFT_MM
    assert abs(tau_mpa(10,11)-38.262)<0.01
    rows=[]
    for t in TORQUES_NM:
        a=tau_mpa(t,D_SHAFT_MM)
        g=tau_mpa(t,D_GROOVE_MM)
        assert g>a>0
        rows.append((t,round(a,3),round(g,3),round(g/a,3)))
    with (OUT/"a38_results.csv").open("w",newline="") as f:
        w=csv.writer(f);w.writerow(("assumed_torque_Nm","nominal_tau_D12_MPa","nominal_tau_D11_MPa","ratio"));w.writerows(rows)
    print("PASS",rows)
if __name__=="__main__":run()
