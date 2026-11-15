"""PX1 A20 candidate tolerance-driven motor relief revision. All mm ASSUMED."""
from dataclasses import dataclass
@dataclass(frozen=True)
class Dim:
    nominal: float
    tol: float
    @property
    def lo(self): return self.nominal-self.tol
    @property
    def hi(self): return self.nominal+self.tol
old = dict(outer=Dim(28.5,.2),axis=Dim(13.5,.3),relief=Dim(13,.25),motor=Dim(12.5,.25))
new = dict(outer=Dim(29.5,.2),axis=Dim(13.5,.3),relief=Dim(13.4,.25),motor=Dim(12.5,.25))
def check(p):
    return round(p['outer'].lo-p['axis'].hi-p['relief'].hi,4),round(p['relief'].lo-p['motor'].hi,4)
assert check(old)==(1.25,0.0)
assert check(new)==(1.85,0.4)
print('PASS A19 reproduced: minimum web/gap',check(old))
print('PASS A20 candidate: minimum web/gap',check(new))
print('SKIPPED: CAD interference and strength; NEEDS_PHYSICAL_CHECK motor dimensions and machining tolerances')
