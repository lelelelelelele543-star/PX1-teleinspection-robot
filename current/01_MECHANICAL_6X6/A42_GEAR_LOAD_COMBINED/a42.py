"""PX1 A42: gear-induced bending + torsion, SI units. All dimensions ASSUMED."""
import math, csv
from pathlib import Path
d=11.0; module=1.5; teeth=50; span=24.0; alpha=math.radians(20)
def evaluate(torque_nm, kb=2.0, kt=2.0):
    ft=2000*torque_nm/(module*teeth)
    fr=ft*math.tan(alpha)
    resultant=math.hypot(ft,fr)
    reaction=resultant/2
    moment_nm=reaction*span/2/1000
    sigma=kb*32*moment_nm*1000/(math.pi*d**3)
    tau=kt*16*torque_nm*1000/(math.pi*d**3)
    vm=math.hypot(sigma,math.sqrt(3)*tau)
    return ft,fr,reaction,moment_nm,sigma,tau,vm
def main():
    out=Path(__file__).parent
    rows=[]
    for t in (2,5,10,15,20):
        rows.append((t,*evaluate(t)))
    assert abs(evaluate(10)[0]-266.6666667)<1e-5
    assert abs(evaluate(10)[3]-1.7028)<0.002
    assert all(rows[i][-1]<rows[i+1][-1] for i in range(len(rows)-1))
    with (out/'a42_results.csv').open('w',newline='') as f:
        w=csv.writer(f);w.writerow(['torque_Nm','Ft_N','Fr_N','reaction_each_N','Mmax_Nm','sigma_b_MPa','tau_t_MPa','von_mises_MPa']);w.writerows(rows)
    print('PASS',rows)
if __name__=='__main__': main()
