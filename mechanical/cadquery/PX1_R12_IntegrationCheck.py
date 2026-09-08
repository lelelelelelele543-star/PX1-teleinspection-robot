"""R12 complete-envelope check against the retained120mm manual lift.
This deliberately checks integration independently of local packing PASS results.
No manufacturing/pressure release is generated.
"""
from pathlib import Path
import json,math
import cadquery as cq
from PX1_R12_SelectedParts import box,cyl,intersect,outside,SEAT
ROOT=Path(__file__).resolve().parents[2]
OUT=ROOT/'build_r12'
def link(p,q,y):
    dx,dz=q[0]-p[0],q[1]-p[1]
    length=math.hypot(dx,dz);ang=-math.degrees(math.atan2(dz,dx))
    sh=box(length,5,18,0,0,0).rotate((0,0,0),(0,1,0),ang).translate(((p[0]+q[0])/2,y,(p[1]+q[1])/2))
    for x,z in (p,q):sh=sh.union(cyl(18,5,(x,y,z),'y')).cut(cyl(8,7,(x,y,z),'y'))
    return sh
def main():
    body=cq.importers.importStep(str(OUT/'PX1_R12_BODY.step')).union(cq.importers.importStep(str(OUT/'PX1_R12_LID.step')))
    camera=cq.importers.importStep(str(OUT/'PX1_R12_CAMERA_CANDIDATE.step'))
    # Source Rev.FN: wheel45, lower92, upper112, camera75/130/205.
    # Transfer using wheel-axis datum: R12 wheel75, deltaZ+30.
    px,lo,hi,L=200.,122.,142.,120.
    report={'status':'UNTESTED','manufacturing_release':False,
      'source_lift':'PX1_LiftCamera_RevFN.py pose120mm; pivot pitch corrected to120mm in capsule geometry',
      'datum_transfer':{'source_wheel_Z':45,'R12_wheel_Z':75,'delta_Z':30},
      'camera_mount_mapping':'Comparison only: fixed rear housing centre localX125 maps to legacy cradle point; adapter is not released.',
      'positions':{},'tail':{},'decision':''}
    for name,z in [('LOW',105.),('MID',160.),('HIGH',235.)]:
        t=math.asin((z-2-(lo+hi)/2)/L)
        dx,dz=-L*math.cos(t),L*math.sin(t)
        q1,q2=(px+dx,lo+dz),(px+dx,hi+dz)
        cam=camera.translate((q1[0]-125,0,z))
        arms={f'{a}_{s}':link((px,p),q,s*26) for s in (-1,1) for a,p,q in [('lower',lo,q1),('upper',hi,q2)]}
        item={'camera_axis_Z_mm':z,'front_pivot_X_mm':q1[0],
              'camera_vs_body_mm3':intersect(cam,body),
              'arm_vs_body_mm3':{n:intersect(p,body) for n,p in arms.items()}}
        if name=='LOW':
            pipe=cyl(150,1000,(150,0,75),'x')
            item['camera_outside_DN150_mm3']=outside(cam.translate((0,0,-SEAT)),pipe)
            item['arms_outside_DN150_mm3']={n:outside(p.translate((0,0,-SEAT)),pipe) for n,p in arms.items()}
            ass=cq.Assembly(name='R12_BASELINE_LIFT_INTERFERENCE_REVIEW')
            ass.add(body,name='Pressure_body',color=cq.Color(.55,.58,.6,.35))
            ass.add(cam,name='Camera_comparison',color=cq.Color(.8,.2,.1,.6))
            for n,p in arms.items():ass.add(p,name=n.replace('-','minus'),color=cq.Color(.9,.55,.1))
            ass.export(str(OUT/'PX1_R12_INTEGRATION_REVIEW.step'))
        report['positions'][name]=item
    pipe=cyl(150,1000,(150,0,75),'x')
    tail=cyl(24,32,(428,0,45),'x').union(cyl(28,30,(459,0,45),'x'))
    report['tail']={'straight_gland_anchor_extent_X_mm':[412,474],
      'outside_DN150_mm3':outside(tail.translate((0,0,-SEAT)),pipe),
      'status':'STRAIGHT_RESERVED_ENVELOPE_ONLY; actual aramid termination and dynamic bend radius remain open'}
    bad=any(p['camera_vs_body_mm3']>1e-3 or any(v>1e-3 for v in p['arm_vs_body_mm3'].values()) for p in report['positions'].values())
    low=report['positions']['LOW']
    bad=bad or low['camera_outside_DN150_mm3']>1e-3 or any(v>1e-3 for v in low['arms_outside_DN150_mm3'].values())
    report['status']='FAIL_BASELINE_LIFT_INTEGRATION' if bad else 'PASS_SCOPED_INTEGRATION'
    report['decision']='Do not freeze412x100x111 as the complete robot or machine the pressure body. Repack the dry volume and recreate the integrated wet deck/lift clearances; do not remove pressure walls just to erase collisions.'
    (OUT/'integration_validation.json').write_text(json.dumps(report,indent=2))
    print(json.dumps(report,indent=2))
if __name__=='__main__':main()
