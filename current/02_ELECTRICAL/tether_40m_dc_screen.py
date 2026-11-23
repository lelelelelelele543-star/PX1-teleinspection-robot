"""PX1 40 m six-core tether DC screening (assumptions; NOT cable qualification)."""
from dataclasses import dataclass
LENGTH_M = 40.0
COPPER_OHM_MM2_PER_M = 0.0175  # assumed copper at 20 C, not a vendor cable spec
SUPPLY_V = 24.0
CORE_ASSIGNMENT = ('DC +', 'DC return', 'RS485 A', 'RS485 B', 'CVBS signal', 'CVBS return')
@dataclass(frozen=True)
class Result:
    area_mm2: float
    current_a: float
    loop_ohm: float
    drop_v: float
    load_v: float
    loss_w: float
def screen(area_mm2, current_a, length_m=LENGTH_M):
    if area_mm2 <= 0 or current_a < 0 or length_m < 0:
        raise ValueError("area>0, current>=0, length>=0 required")
    loop = 2*length_m*COPPER_OHM_MM2_PER_M/area_mm2
    drop = loop*current_a
    return Result(area_mm2,current_a,loop,drop,SUPPLY_V-drop,current_a*drop)
if __name__ == "__main__":
    for a in (0.5,0.75,1,1.5,2.5):
        for i in (1,2,3):
            r=screen(a,i)
            print(f"{a:g} mm2 / {i} A: loop={r.loop_ohm:.3f} ohm, drop={r.drop_v:.2f} V, load={r.load_v:.2f} V, heat={r.loss_w:.2f} W")
    assert abs(screen(1,2).drop_v-2.8)<1e-9
    assert screen(0.5,3).load_v < screen(2.5,3).load_v
    assert len(CORE_ASSIGNMENT)==6
    print("PASS: numeric self-tests")
