"""PX1 integrated M1 source audit; Python 3 stdlib. NOT a FreeCAD or pressure test."""
import ast,json,math,pathlib
root=pathlib.Path(__file__).resolve().parent
src=root/"PX1_Integrated_6x6_M1_interface_repair.py"
text=src.read_text(encoding="utf-8")
tree=ast.parse(text)
P=ast.literal_eval(next(n.value for n in tree.body if isinstance(n,ast.Assign) and any(isinstance(t,ast.Name) and t.id=="P" for t in n.targets)))
checks=[]
def ck(label,ok,note):
    checks.append({"name":label,"status":"PASS" if ok else "FAIL","detail":note})
ck("6 wheel stations / 10 gear stations",len(P["stations"])==3 and len(P["gear_x"])==5 and P["stations"]==P["gear_x"][::2],"source parameters")
ck("Z50 module pitch",P["gear_m"]*50==50 and all(P["gear_x"][i+1]-P["gear_x"][i]==50 for i in range(4)),"pitch only, teeth absent")
clearance=75-math.hypot(46+P["wheel_W"],P["wheel_D"]/2)
ck("DN150 conservative wheel corner",clearance>=2,("%.3f mm nominal clearance"%clearance))
ck("six wheel shaft passages",'for xx in P["stations"]:' in text and 'outer=outer.cut(cyl(11,5' in text,"source loop inspection only")
ck("four internal blind idler carriers",'Idler_carrier_PROXY_' in text and 'if j%2==0:' in text,"attachment NOT_RUN")
ck("six seal cartridge proxies",'Shaft_seal_CARTRIDGE_PROXY_' in text,"pressure rating PHYSICAL_CHECK")
ck("nominal gasket compression",0<P["lid_gasket_compression"]<P["lid_gasket_nominal"],"fasteners and gasket groove NOT_RUN")
ck("STEP roundtrip code present",'Part.read(step_path)' in text and 'volume_error' in text,"execution NOT_RUN")
blockers=["Z50 and bevel teeth are only pitch proxies","Blind idler carriers lack attachment geometry","Shaft seal pressure rating unverified","Lid fasteners and gasket groove absent","3D collision and STEP execution NOT_RUN"]
force=0.7*1e5*.170*.060
report={"classification":"SOURCE_STATIC_ONLY","checks":checks,"lid_force_N_at_0_7_bar":force,"blockers":blockers,"freecad":"NOT_RUN","step":"NOT_RUN","pressure":"PHYSICAL_CHECK"}
(root/"M1_integrated_source_gate.json").write_text(json.dumps(report,ensure_ascii=False,indent=2)+"\n",encoding="utf-8")
# Orthographic schematic, exact placement from parameter positions; no teeth represented.
cx,cy,scale=360,235,1.5
v=['<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 980 620">','<rect width="980" height="620" fill="#f8fafc"/>','<text x="35" y="42" font-family="sans-serif" font-size="24" font-weight="bold">PX1 M1 — integrated 6x6 source audit</text>','<text x="35" y="68" font-family="sans-serif" font-size="15">Design assumptions; orthographic plan; NOT FreeCAD render</text>']
v.append(f'<rect x="{cx-P["body_L"]*scale/2}" y="{cy-P["body_W"]*scale/2}" width="{P["body_L"]*scale}" height="{P["body_W"]*scale}" fill="#cbd5e1" stroke="#334155" stroke-width="3"/>')
for sign in (-1,1):
    y=cy+sign*P["gear_y"]*scale
    for j,x in enumerate(P["gear_x"]):
        px=cx+x*scale
        v.append(f'<circle cx="{px}" cy="{y}" r="{P["gear_m"]*25*scale}" fill="#f59e0b" fill-opacity=".24" stroke="#b45309" stroke-width="2"/>')
        if j%2: v.append(f'<circle cx="{px}" cy="{y}" r="18" fill="none" stroke="#15803d" stroke-width="3" stroke-dasharray="5 3"/>')
    for x in P["stations"]:
        px=cx+x*scale; wy=cy+sign*(46+P["wheel_W"]/2)*scale
        v.append(f'<rect x="{px-P["wheel_D"]*scale/2}" y="{wy-P["wheel_W"]*scale/2}" width="{P["wheel_D"]*scale}" height="{P["wheel_W"]*scale}" rx="6" fill="#334155"/>')
    mx=cx+35*scale; my=cy+sign*P["motor_y"]*scale
    v.append(f'<rect x="{mx}" y="{my-P["motor_D"]*scale/2}" width="{P["motor_L"]*scale}" height="{P["motor_D"]*scale}" rx="10" fill="#2563eb"/>')
v.extend(['<text x="40" y="432" font-family="sans-serif" font-size="16">Amber: Z50 pitch discs (no teeth) | Green: 4 blind idler carriers | Blue: 2 motors | Dark: 6 wheels</text>',f'<text x="40" y="472" font-family="sans-serif" font-size="16">DN150 corner clearance: {clearance:.2f} mm | Lid force at 0.7 bar: {force:.0f} N</text>','<text x="40" y="514" font-family="sans-serif" font-size="16" fill="#b91c1c">UNMODELED: gear teeth, seal lips, idler fasteners, lid bolts, verified motor coupling</text>','<text x="40" y="550" font-family="sans-serif" font-size="15">Static source checks only. FreeCAD / STEP / collision: NOT_RUN; pressure: PHYSICAL_CHECK</text>','</svg>'])
(root/"M1_integrated_source_gate.svg").write_text("\n".join(v)+"\n",encoding="utf-8")
for c in checks: print(c["status"],c["name"],c["detail"])
if any(c["status"]=="FAIL" for c in checks): raise SystemExit(1)
