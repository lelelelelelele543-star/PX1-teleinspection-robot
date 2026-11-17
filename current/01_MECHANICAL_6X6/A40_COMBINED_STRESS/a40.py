"""PX1 A40 combined bending/torsion sensitivity; assumptions, not qualification."""
import math,csv
from pathlib import Path
D=11.0 # assumed groove root diameter, mm
TORQUES=(5,10,20) # assumed Nm
BENDING=(0,5,10,20) # assumed Nm
KT_B=2.0 # assumed bending stress concentration
KT_T=2.0 # assumed torsion stress concentration
def calc(m,t):
    sigma=KT_B*32000*m/(math.pi*D**3)
    tau=KT_T*16000*t/(math.pi*D**3)
    return sigma,tau,math.hypot(sigma,math.sqrt(3)*tau)
def test():
    assert abs(calc(0,10)[2]-math.sqrt(3)*calc(0,10)[1])<1e-9
    assert calc(20,20)[2]>calc(10,20)[2]>calc(0,20)[2]
    assert calc(10,20)[2]>calc(10,10)[2]
    assert calc(0,0)[2]==0
def svg():
    bars=[]
    for i,m in enumerate(BENDING):
        val=calc(m,10)[2];y=110+i*77
        bars.append(f'<text x="25" y="{y+23}" font-size="16">M={m} Nm</text><rect x="160" y="{y}" width="{val*5.5:.1f}" height="32" rx="4" fill="#3684b7"/><text x="{175+val*5.5:.1f}" y="{y+23}" font-size="16">{val:.1f} MPa</text>')
    return '<svg xmlns="http://www.w3.org/2000/svg" width="1080" height="500" viewBox="0 0 1080 500"><rect width="1080" height="500" fill="#f7f9fc"/><g font-family="Arial,sans-serif" fill="#172c3a"><text x="25" y="43" font-size="25">PX1 A40: bending + torsion, X150 shaft</text><text x="25" y="72" font-size="16">Von Mises equivalent; T=10 Nm; Kt bending=2, Kt torsion=2 (ASSUMED)</text>'+''.join(bars)+'<text x="25" y="445" font-size="15">Groove root diameter 11 mm ASSUMED. No fatigue, axial load or measured torque.</text><text x="25" y="472" font-size="15">Parameter-generated 2D chart, NOT CAD or strength qualification.</text></g></svg>'
if __name__=="__main__":
    test();p=Path(__file__).parent
    with (p/"a40_results.csv").open("w",newline="") as f:
        w=csv.writer(f);w.writerow(["bending_Nm_assumed","torque_Nm_assumed","sigma_MPa","tau_MPa","von_mises_MPa"])
        for m in BENDING:
            for t in TORQUES:w.writerow([m,t,*[round(x,3) for x in calc(m,t)]])
    (p/"a40_preview.svg").write_text(svg(),encoding="utf-8")
    print("PASS 12 cases")
