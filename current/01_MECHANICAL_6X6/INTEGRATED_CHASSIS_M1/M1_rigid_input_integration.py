"""FreeCADCmd macro extending existing M1 generator, not factory geometry.
Creates a rigid coupling proxy between coaxial rear Z40 and Z50 on each side,
then exports FCStd/STEP and reopens STEP. Real teeth/seals remain NOT_RUN.
"""
from pathlib import Path
import runpy, json
root=Path(__file__).resolve().parent
ns=runpy.run_path(str(root/'PX1_Integrated_6x6_M1_interface_repair.py'))
App,Part,V,D,parts=(ns[k] for k in ('App','Part','V','D','parts'))
checks=[]
for side,sgn in [('L',-1),('R',1)]:
    # Shared shaft/hub: 19..33 mm from mid-plane, Z40 19..27, Z50 27..33.
    y0=19 if sgn==1 else -33
    hub=Part.makeCylinder(7,14,V(100,y0,0),V(0,1,0))
    obj=D.addObject('PartDesign::Feature','Rigid_Z40_Z50_hub_'+side+'_ASSUMED')
    obj.Shape=hub;obj.ViewObject.ShapeColor=(0.3,0.75,0.85);parts.append(obj)
    z40=next(o for o in parts if o.Name=='Bevel_Z40_PROXY_'+side)
    z50=next(o for o in parts if o.Name=='Z50_pitch_PROXY_'+side+'_5')
    assert abs(hub.BoundBox.XCenter-z40.Shape.BoundBox.XCenter)<1e-6
    assert abs(hub.BoundBox.XCenter-z50.Shape.BoundBox.XCenter)<1e-6
    checks.append({'side':side,'status':'PASS','check':'hub nominally spans Z40/Z50 axial interface',
                   'note':'Geometric proxy; real key/spline, bearing, stress and torque NOT_RUN'})
    nodes=['motor','Z16','Z40','hub','Z50_5','Z50_4','Z50_3','Z50_2','Z50_1',
           'rear_wheel','center_wheel','front_wheel']
    edges=[('motor','Z16'),('Z16','Z40'),('Z40','hub'),('hub','Z50_5'),
           ('Z50_5','Z50_4'),('Z50_4','Z50_3'),('Z50_3','Z50_2'),
           ('Z50_2','Z50_1'),('Z50_5','rear_wheel'),
           ('Z50_3','center_wheel'),('Z50_1','front_wheel')]
    seen={'motor'}
    for _ in range(len(nodes)):
        for a,b in edges:
            if a in seen:seen.add(b)
            if b in seen:seen.add(a)
    assert set(nodes)==seen
    checks.append({'side':side,'status':'PASS','check':'nominal graph connects motor to all three wheels',
                   'note':'Gear ratios and actual involute/bevel tooth contact NOT_RUN'})
D.recompute()
D.saveAs(str(root/'PX1_Integrated_6x6_M1_rigid_input.FCStd'))
step=root/'PX1_Integrated_6x6_M1_rigid_input.step'
Part.export(parts,str(step))
reopened=App.newDocument('PX1_M1_STEP_reopen')
Part.insert(str(step),reopened.Name)
reopened.recompute()
shapes=[o.Shape for o in reopened.Objects if hasattr(o,'Shape') and not o.Shape.isNull()]
assert shapes and all(s.isValid() for s in shapes)
checks.append({'status':'PASS','check':'STEP reopened, valid non-null shapes','count':len(shapes)})
checks.append({'status':'NOT_RUN','check':'true gear tooth mesh, pressure seal, torque capacity, all collision exclusions'})
(root/'M1_rigid_input_checks.json').write_text(json.dumps(checks,indent=2),encoding='utf8')
print('PX1 M1: nominal rigid torque coupling; STEP reopened; manufacturing NOT approved')
