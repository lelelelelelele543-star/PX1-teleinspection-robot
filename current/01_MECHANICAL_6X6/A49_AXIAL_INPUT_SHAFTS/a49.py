"""A49: assumed axial input shaft packaging; no physical validation."""
from pathlib import Path
import csv
P=Path(__file__).parent
rear=250.0
motors={"L":(55.,120.),"R":(150.,215.)}
coupling=12.0
bearing_width=7.0
bearing_offset=16.0
end_clearance=4.0
rows=[]
for side,(start,end) in motors.items():
    reach=rear-end
    bearing_center=rear-bearing_offset
    budget=reach-coupling-bearing_width/2-end_clearance
    assert start<end<rear and budget>=0,(side,budget)
    rows.append((side,reach,bearing_center,budget))
assert rows==[("L",130.,234.,110.5),("R",35.,234.,15.5)]
with (P/"results.csv").open("w",newline="") as f:
    w=csv.writer(f)
    w.writerow(["side","motor_end_to_rear_mm","support_center_x_mm","remaining_axial_budget_mm"])
    w.writerows(rows)
print("PASS: axial budget; SKIPPED: 3D interference; NEEDS_PHYSICAL_CHECK")
