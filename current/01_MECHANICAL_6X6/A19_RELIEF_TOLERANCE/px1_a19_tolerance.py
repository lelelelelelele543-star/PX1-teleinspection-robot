"""A19: worst-case tolerance stack for A17/A18 motor relief; all values ASSUMED, mm."""
from dataclasses import dataclass
@dataclass(frozen=True)
class Dim:
    nominal: float
    tol: float
    def lo(self): return self.nominal-self.tol
    def hi(self): return self.nominal+self.tol
outer=Dim(28.5,0.2)
axis=Dim(13.5,0.3)
relief_r=Dim(13.0,0.25)
motor_r=Dim(12.5,0.25)
web_nom=outer.nominal-axis.nominal-relief_r.nominal
web_min=outer.lo()-axis.hi()-relief_r.hi()
web_max=outer.hi()-axis.lo()-relief_r.lo()
radial_clearance_nom=relief_r.nominal-motor_r.nominal
radial_clearance_min=relief_r.lo()-motor_r.hi()
assert abs(web_nom-2.0)<1e-9
assert abs(web_min-1.25)<1e-9
assert abs(web_max-2.75)<1e-9
assert abs(radial_clearance_min)<1e-9
print(f"PASS nominal web={web_nom:.2f}; worst web=[{web_min:.2f},{web_max:.2f}] mm")
print(f"PASS arithmetic radial clearance nominal={radial_clearance_nom:.2f}; worst={radial_clearance_min:.2f} mm")
print("FAIL clearance reserve: zero worst-case radial clearance before mounting misalignment")
print("NEEDS_PHYSICAL_CHECK dimensions, motor alignment, material strength; SKIPPED FreeCAD solid validation")
