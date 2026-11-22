#!/usr/bin/env python3
"""Post-build integration evidence for PX1 CURRENT master; no surrogate geometry.
Run AFTER: PX1_OUT=current python current/CAD/PX1_Current_Master.py
Consumes exported component_registry.json and PX1_Current_Validation.json.
Only a successful real CAD build can produce the SVG and evidence report.
"""
import json, sys, html
from pathlib import Path

ROOT=Path(__file__).resolve().parents[1]
registry=json.loads((ROOT/"component_registry.json").read_text())
validation=json.loads((ROOT/"PX1_Current_Validation.json").read_text())
step=ROOT/"CAD/PX1_Current_Master.step"
if not step.is_file() or step.stat().st_size<1000:
    raise SystemExit("FAIL: actual STEP export missing or empty")
counts=validation["counts"]; expected=validation["expected_counts"]
if counts!=expected: raise SystemExit("FAIL: drivetrain counts "+repr(counts))
if validation["invalid_shapes"]: raise SystemExit("FAIL: invalid CAD solids")
names=[r["id"] for r in registry]
if len(names)!=len(set(names)): raise SystemExit("FAIL: duplicate CAD component IDs")
# Every rectangle is taken from the CAD-generated 3D bounding box, NOT redrawn by hand.
# X horizontal, Y vertical; both are millimetres. The entire assembly is shown.
boxes=[r["bbox_mm"] for r in registry]
xmin=min(b[0] for b in boxes); xmax=max(b[3] for b in boxes)
ymin=min(b[1] for b in boxes); ymax=max(b[4] for b in boxes)
scale=min(1100/max(xmax-xmin,1),480/max(ymax-ymin,1))
def X(x):return 65+(x-xmin)*scale
def Y(y):return 545-(y-ymin)*scale
palette={"body":"#778899","wheel":"#202c39","gear":"#c89438","bevel":"#e17b36","shaft":"#869cb1","bearing":"#56a7c0","seal":"#b65f9a","electronics":"#5c9b69","lift":"#7d76ae","camera":"#5275ad"}
items=['<svg xmlns="http://www.w3.org/2000/svg" width="1240" height="660" viewBox="0 0 1240 660">',
'<rect width="1240" height="660" fill="#fff"/>',
'<text x="45" y="38" font-size="24" font-family="sans-serif">PX1 — actual CAD component bounding boxes (XY plan)</text>',
'<text x="45" y="63" font-size="14" font-family="sans-serif">CAD-derived boxes; NOT exact projected silhouettes. Unresolved parts remain HOLD.</text>']
for r in registry:
    b=r["bbox_mm"];cat=r["category"]
    items.append('<rect x="%.2f" y="%.2f" width="%.2f" height="%.2f" fill="%s" fill-opacity=".17" stroke="%s" stroke-width=".8"><title>%s</title></rect>'%
        (X(b[0]),Y(b[4]),max(.4,(b[3]-b[0])*scale),max(.4,(b[4]-b[1])*scale),palette.get(cat,"#777"),palette.get(cat,"#777"),html.escape(r["id"])))
items+=['<text x="45" y="596" font-family="monospace" font-size="14">Wheels: %d | Z50: %d | Motors: %d | CAD parts: %d</text>'%(counts["wheel"],counts["Z50"],counts["traction_motor"],len(registry)),
'<text x="45" y="621" font-family="sans-serif" font-size="13">Not manufacturing release. Pressure, physical fits and functional drive unqualified.</text>','</svg>']
preview=ROOT/"CAD/previews/PX1_master_actual_export_plan.svg"
preview.parent.mkdir(parents=True,exist_ok=True)
preview.write_text("\n".join(items))
report={"status":"CAD_EXPORTED_NOT_MANUFACTURING_RELEASE","master_source_sha256":validation["source_sha256"],"step_bytes":step.stat().st_size,
"components":len(registry),"counts":counts,"invalid_shapes":validation["invalid_shapes"],
"rigid_interferences":[p for p in validation["interferences"] if p["classification"]=="RIGID_INTERFERENCE"],
"collision_errors":validation["collision_method"]["errors"],
"pressure":"NEEDS_PHYSICAL_CHECK","motor_driver_compatibility":"NOT_VERIFIED",
"svg":"CAD/previews/PX1_master_actual_export_plan.svg"}
(ROOT/"PX1_Integration_Evidence.json").write_text(json.dumps(report,ensure_ascii=False,indent=2))
print(json.dumps({"step_bytes":report["step_bytes"],"parts":len(registry),"rigid_interferences":len(report["rigid_interferences"]),"collision_errors":len(report["collision_errors"])}))
# CAD can be successfully exported while release remains FAIL: this is intentional.
