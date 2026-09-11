# PX-1 Rev.B / WB15 — rear camera connector packaging model
# CadQuery envelope model only. Purchased WEIPU drawing/sample controls final machining.

import cadquery as cq

# Controlled project envelopes
HEAD_OD = 52.0
REAR_REGISTER_OD = 36.0
BULKHEAD_T = 3.0
CONNECTOR_PANEL_CUTOUT_D = 13.0
CONNECTOR_FLAT = 11.8
CONNECTOR_FRONT_OD = 19.5
CONNECTOR_PANEL_DEPTH = 19.2
CONNECTOR_FRONT_PROJ = 9.5
PLUG_OD = 18.8
PLUG_LENGTH = 49.0
SERVICE_SOLID_KEEP_OUT = 55.0
SERVICE_EXTRACTION = 60.0

# Derived screens
radial_guard_register_to_connector = (REAR_REGISTER_OD - CONNECTOR_FRONT_OD) / 2.0
radial_ligament_register_to_cutout = (REAR_REGISTER_OD - CONNECTOR_PANEL_CUTOUT_D) / 2.0
panel_thickness_margin = 3.5 - BULKHEAD_T

assert radial_guard_register_to_connector >= 8.0
assert radial_ligament_register_to_cutout >= 11.0
assert panel_thickness_margin >= 0.5 - 1e-9

# Rear bulkhead coupon / register envelope
bulkhead = (
    cq.Workplane("XY")
    .circle(REAR_REGISTER_OD / 2.0)
    .extrude(BULKHEAD_T)
)

# Conservative round cutout. Final drawing must add the two anti-rotation flats
# to WEIPU's 11.8 mm dimension rather than machining a plain round hole.
bulkhead = bulkhead.cut(
    cq.Workplane("XY")
    .circle(CONNECTOR_PANEL_CUTOUT_D / 2.0)
    .extrude(BULKHEAD_T + 1.0)
)

# Panel receptacle gross envelope, wet side negative-Z.
receptacle = (
    cq.Workplane("XY")
    .circle(CONNECTOR_FRONT_OD / 2.0)
    .extrude(-CONNECTOR_FRONT_PROJ)
)

# Rear/internal portion gross envelope.
receptacle_rear = (
    cq.Workplane("XY")
    .workplane(offset=BULKHEAD_T)
    .circle(13.0 / 2.0)
    .extrude(CONNECTOR_PANEL_DEPTH - CONNECTOR_FRONT_PROJ)
)

# Mated straight cable plug external/service envelope.
plug = (
    cq.Workplane("XY")
    .workplane(offset=-CONNECTOR_FRONT_PROJ)
    .circle(PLUG_OD / 2.0)
    .extrude(-PLUG_LENGTH)
)

# Axial service keep-out: must remain free of fixed yoke/bridge geometry.
service_keepout = (
    cq.Workplane("XY")
    .workplane(offset=-CONNECTOR_FRONT_PROJ)
    .circle(max(PLUG_OD, 20.0) / 2.0)
    .extrude(-SERVICE_EXTRACTION)
)

# Head OD reference disk at rear datum only.
head_ref = (
    cq.Workplane("XY")
    .circle(HEAD_OD / 2.0)
    .extrude(0.5)
)

# Named exports when run in a CadQuery environment.
try:
    from cadquery import exporters
    exporters.export(bulkhead, "PX1_WB15_rear_bulkhead_coupon.step")
    exporters.export(receptacle.union(receptacle_rear), "PX1_WB15_SP1312_envelope.step")
    exporters.export(plug, "PX1_WB15_SP1310_plug_envelope.step")
    exporters.export(service_keepout, "PX1_WB15_connector_service_keepout.step")
except Exception:
    pass

print("PX1 WB15 rear connector packaging screen")
print(f"head OD: {HEAD_OD:.1f} mm")
print(f"rear register OD: {REAR_REGISTER_OD:.1f} mm")
print(f"bulkhead thickness: {BULKHEAD_T:.1f} mm")
print(f"SP1312 cutout: Ø{CONNECTOR_PANEL_CUTOUT_D:.1f} with {CONNECTOR_FLAT:.1f} mm anti-rotation flat dimension")
print(f"radial guard to connector OD: {radial_guard_register_to_connector:.2f} mm")
print(f"radial ligament to round cutout: {radial_ligament_register_to_cutout:.2f} mm")
print(f"panel-thickness margin to WEIPU max: {panel_thickness_margin:.2f} mm")
print(f"mated plug length envelope: {PLUG_LENGTH:.1f} mm")
print(f"required practical extraction envelope: {SERVICE_EXTRACTION:.1f} mm")
print("STATUS: local connector/register geometry PASS_SCREEN")
print("HOLD: full yoke/lift/DN150 solid sweep + pressure/video qualification")
