"""Integrated master architecture gate; Python stdlib; no CAD execution or STEP claim."""
import ast,json,math
from pathlib import Path
P=Path(__file__).with_name("PX1_Current_Master.py")
def read():
 d={}
 for n in ast.parse(P.read_text(encoding="utf8")).body:
  if isinstance(n,ast.Assign):
   for t in n.targets:
    if isinstance(t,ast.Name):
     try:d[t.id]=ast.literal_eval(n.value)
     except (ValueError,TypeError):pass
 return d
def check(p):
 req=["WHEEL_X","GEAR_X","Z50_TEETH","Z50_MOD","Z50_PD","Z50_OD","WHEEL_Z","PIPE_R","WHEEL_CENTRE_Y","WHEEL_CROWN_R","BODY_HALF_W_SCREEN","BODY_Z0","BODY_TOP","SERVICE_ORING","SIDE_ORING","SERVICE_PLUG_L","SERVICE_OPEN_W","SERVICE_PLUG_R","SERVICE_PLUG_CLR","SERVICE_RGROOVE_D","MOTOR_OD","MOTOR_LEN","GEARHEAD_OD","GEARHEAD_LEN"]
 missing=set(req)-p.keys()
 if missing:raise ValueError("Missing master constants: "+str(sorted(missing)))
 x,g=p["WHEEL_X"],p["GEAR_X"]
 L,W,r,c,d=[p[k] for k in ("SERVICE_PLUG_L","SERVICE_OPEN_W","SERVICE_PLUG_R","SERVICE_PLUG_CLR","SERVICE_RGROOVE_D")]
 root=2*((L-2*c-2*d)+(W-2*c-2*d))-(8-2*math.pi)*(r-c-d)
 stretch=lambda ID:100*(root/(math.pi*ID)-1)
 cz=p["WHEEL_Z"]-p["WHEEL_CROWN_R"]+math.sqrt(p["PIPE_R"]**2-p["WHEEL_CENTRE_Y"]**2)
 gap=p["PIPE_R"]-max(math.hypot(p["BODY_HALF_W_SCREEN"],z-cz) for z in (p["BODY_Z0"],p["BODY_TOP"]))
 return {"checks":{"six_wheels":"PASS" if len(x)==3 else "FAIL","ten_Z50":"PASS" if len(g)==5 and p["Z50_TEETH"]==50 else "FAIL","wheel_gear_alignment":"PASS" if set(x)<=set(g) else "FAIL","involute_nominal_dimensions":"PASS" if p["Z50_PD"]==p["Z50_TEETH"]*p["Z50_MOD"] and p["Z50_OD"]==(p["Z50_TEETH"]+2)*p["Z50_MOD"] else "FAIL","two_distinct_seals":"PASS" if p["SERVICE_ORING"]!=p["SIDE_ORING"] else "FAIL","service_110_stretch":"FAIL" if stretch(110)>5 else "PASS","service_115_stretch":"PASS" if 0<=stretch(115)<=5 else "FAIL","motor_driver_compatibility":"FAIL_UNRESOLVED_ISSUE_15","SP13_shell_interference":"FAIL_UNRESOLVED_ISSUE_14","3d_collisions":"NOT_RUN","STEP_reopen":"NOT_RUN","pressure_seals":"PHYSICAL_CHECK"},"body_dn150_nominal_gap_mm":round(gap,3),"service_root_perimeter_mm":round(root,3),"service_110_stretch_pct":round(stretch(110),2),"service_115_stretch_pct":round(stretch(115),2),"motor_od_mm":p["MOTOR_OD"],"motor_len_mm":p["MOTOR_LEN"],"gearhead_od_mm":p["GEARHEAD_OD"],"gearhead_len_mm":p["GEARHEAD_LEN"],"wheel_x_mm":x,"gear_x_mm":g,"assumptions":["DN150 treated as 150mm inner diameter","rectangular body envelope, not 3D shell","115x1.5 O-ring candidate not stock or pressure verified"]}
if __name__=="__main__":
 result=check(read())
 (P.parent/"previews"/"PX1_integrated_release_gate.json").write_text(json.dumps(result,indent=2),encoding="utf8")
 print(json.dumps(result,indent=2))
 assert result["checks"]["six_wheels"]=="PASS"
