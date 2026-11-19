"""Conservative GA24 fit study against actual master solids; no manufacturing release."""
import os, sys, types, runpy, json, hashlib, math, shutil
from pathlib import Path
root=Path(__file__).resolve().parents[2]
out=root/'_ga24_fit_study'; out.mkdir(exist_ok=True)
shutil.copytree(root/'current/CAD/vendor',out/'CAD/vendor',dirs_exist_ok=True)
os.environ['PX1_OUT']=str(out)
sys.path.insert(0,str(root/'current/CAD'))
captured={}
stub=types.ModuleType('release_tools')
stub.finish_build=lambda g:captured.update(g)
sys.modules['release_tools']=stub
source=root/'current/CAD/PX1_Current_Master.py'
runpy.run_path(str(source))
g=captured
# Conservative provisional body uses published longer 256-500 ratio drawing.
# It is NOT a confirmed 138:1 outline. Shaft/pilot also remain variant HOLD.
face=189.5
holder=g['boxc'](face+1.5,0,45,3,52.8,30)
for side in (-1,1):
 y=side*13.5
 holder=g['cut'](holder,g['cyl_x'](face-.1,y,45,3.3,3.2))
 for angle in (45,135,225,315):
  a=math.radians(angle)
  holder=g['cut'](holder,g['cyl_x'](face-.1,y+9.5*math.cos(a),45+9.5*math.sin(a),1.35,3.2))
g['components']=[x for x in g['components'] if x[0]!='HOLD_PAIRED_MOTOR_HOLDER_RF25_FIT_CANDIDATE']
g['components'].append(('HOLD_GA24_PROVISIONAL_HOLDER',holder,'metal'))
results=[]
for side in (-1,1):
 y=side*13.5
 candidate=g['fuse_all']([g['cyl_x'](face-67.6,y,45,12.2,67.6),g['cyl_x'](face,y,45,3.2,2),g['cyl_x'](face,y,45,2,17.5)])
 s=candidate.val(); b=s.BoundingBox(); hits=[];errors=[];tested=0
 for name,p,category in g['components']:
  if name.startswith('TRACTION_MOTOR_'):continue
  q=p.val() if hasattr(p,'val') else p; c=q.BoundingBox()
  if not all(min(getattr(b,k+'max'),getattr(c,k+'max'))>max(getattr(b,k+'min'),getattr(c,k+'min'))+1e-7 for k in ('x','y','z')):continue
  tested+=1
  try:
   v=s.intersect(q).Volume()
   if v>1e-4:hits.append({'component':name,'overlap_mm3':v})
  except Exception as e: errors.append({'component':name,'error':str(e)})
 results.append({'side':side,'bbox_candidates_tested':tested,'solid_intersections':hits,'errors':errors,'valid':s.isValid()})
report={'status':'PROVISIONAL_ENVELOPE_STUDY_NOT_INSTALLED','master_sha256':hashlib.sha256(source.read_bytes()).hexdigest(),'assumptions':{'motor_face_x_mm':face,'holder_holes':'ESTIMATED 4 x clearance2.7 on PCD19, depth3; not released','body_diameter_mm':24.4,'body_length_mm':67.6,'shaft_diameter_mm':4,'shaft_projection_mm':17.5,'pilot_diameter_mm':6.4,'pilot_length_mm':2,'dimensions_status':'ESTIMATED conservative envelope from different-ratio family PDF; exact 138:1 outline unresolved'},'results':results,'calculated_force_N':2*(7*.0980665)*2.5*.75/.045,'speed_m_min':52/2.5*math.pi*.09,'qualification':'No seller identity, delivery, thermal endurance or full assembly release implied.'}
(out/'result.json').write_text(json.dumps(report,indent=2))
print(json.dumps(report,indent=2))
