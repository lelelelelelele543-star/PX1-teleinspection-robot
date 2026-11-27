#!/usr/bin/env python3
"""PX1 pressure-boundary interface audit, using constants from the ONLY current CAD master.
Stdlib-only; never imports/executes CadQuery master and never changes its geometry.
python current/CAD/audit_pressure_interfaces.py
"""
import ast, json, math
from pathlib import Path
MASTER=Path(__file__).with_name('PX1_Current_Master.py')
OUT=Path(__file__).with_name('pressure_interface_audit.json')
node=ast.parse(MASTER.read_text(encoding='utf-8'))
wanted={'SERVICE_PLUG_L','SERVICE_OPEN_W','SERVICE_PLUG_R','SERVICE_PLUG_CLR',
        'SERVICE_RGROOVE_D','SERVICE_RGROOVE_W','SERVICE_ORING',
        'SIDE_ORING','SIDE_SEAL_W','SIDE_SEAL_D','FLANGE_ORING',
        'FLANGE_GROOVE_RI','FLANGE_GROOVE_RO','FLANGE_GROOVE_DEPTH',
        'SEAL_18_30_7','WHEEL_X'}
values={}
for item in node.body:
    if not isinstance(item,ast.Assign):continue
    for t in item.targets:
        if isinstance(t,ast.Name) and t.id in wanted:
            values[t.id]=ast.literal_eval(item.value)
missing=wanted-values.keys()
if missing:raise SystemExit('FAIL missing master constants: '+repr(sorted(missing)))
v=values
L=v['SERVICE_PLUG_L'];W=v['SERVICE_OPEN_W'];r=v['SERVICE_PLUG_R']
cl=v['SERVICE_PLUG_CLR'];d=v['SERVICE_RGROOVE_D']
perim=2*((L-2*cl-2*d)+(W-2*cl-2*d))-(8-2*math.pi)*(r-cl-d)
stretch=perim/(math.pi*v['SERVICE_ORING'][0])-1
cs=v['SERVICE_ORING'][1]/math.sqrt(1+stretch)
squeeze=(cs-(d+cl))/cs
side_squeeze=(v['SIDE_ORING'][1]-v['SIDE_SEAL_D'])/v['SIDE_ORING'][1]
flange_squeeze=(v['FLANGE_ORING'][1]-v['FLANGE_GROOVE_DEPTH'])/v['FLANGE_ORING'][1]
pressure=70000.0
shaft_d=v['SEAL_18_30_7'][0]/1000
shaft_force=pressure*math.pi*shaft_d**2/4
# Engineering SCREEN limits, NOT supplier-certified seal acceptance limits.
screen={'service_stretch_le_5pct':stretch<=.05,
        'service_radial_squeeze_15_to_30pct':.15<=squeeze<=.30,
        'side_face_squeeze_15_to_30pct':.15<=side_squeeze<=.30,
        'flange_face_squeeze_15_to_30pct':.15<=flange_squeeze<=.30,
        'dynamic_seal_pressure_rating_confirmed':False}
result={'source':'current/CAD/PX1_Current_Master.py (AST literal constants)',
 'pressure_design_bar_gauge':.7,'pressure_test':'NOT_RUN',
 'service_plug':{'oring_id_mm':v['SERVICE_ORING'][0],'oring_cs_mm':v['SERVICE_ORING'][1],
                 'groove_root_perimeter_mm':perim,'installed_stretch_pct':100*stretch,
                 'installed_cs_mm':cs,'radial_squeeze_pct':100*squeeze,
                 'status':'FAIL_SCREEN: stretch exceeds conservative 5% design screening limit' if stretch>.05 else 'PASS_SCREEN'},
 'side_cover':{'oring_cs_mm':v['SIDE_ORING'][1],'groove_depth_mm':v['SIDE_SEAL_D'],
               'nominal_face_squeeze_pct':100*side_squeeze,'status':'SCREEN_ONLY'},
 'wheel_flange':{'oring_cs_mm':v['FLANGE_ORING'][1],'groove_depth_mm':v['FLANGE_GROOVE_DEPTH'],
                 'nominal_face_squeeze_pct':100*flange_squeeze,'status':'SCREEN_ONLY'},
 'dynamic_shafts':{'quantity':2*len(v['WHEEL_X']),'nominal_seal_mm':v['SEAL_18_30_7'],
                   'pressure_axial_force_per_18mm_bore_N':shaft_force,
                   'pressure_rating':'NOT_VERIFIED; bearing or generic oil seal is not proof of 0.7 bar rating'},
 'screens':screen,'release':'NOT_MANUFACTURING_RELEASE',
 'assumptions':['0.7 bar gauge upper design point','5% service O-ring stretch is a conservative screening threshold, not a vendor specification','15..30% static squeeze is a preliminary screen; gland fill, extrusion, tolerance and material not qualified','18mm shaft pressure area approximated as full shaft bore','no physical pressure or leak test performed'],
 'next_design_action':'Validate candidate 115x1.5 supplier dimensions, tolerances and full CAD collision/pressure checks.'}
OUT.write_text(json.dumps(result,ensure_ascii=False,indent=2)+'\n',encoding='utf-8')
print('FAIL_SCREEN service plug O-ring stretch %.2f%% > 5%%'% (stretch*100) if stretch>.05 else 'PASS_SCREEN service stretch')
print('PASS_SCREEN squeeze service %.2f%% side %.2f%% flange %.2f%%'%(squeeze*100,side_squeeze*100,flange_squeeze*100))
print('NOT_VERIFIED dynamic seals at 0.7 bar; pressure force %.2f N/shaft'%shaft_force)
print('Saved',OUT)
