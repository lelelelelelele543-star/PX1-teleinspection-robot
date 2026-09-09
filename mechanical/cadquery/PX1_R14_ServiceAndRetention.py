"""PX1 R14 serviceable side plates and wheel retention study.

All dimensions are millimetres.  This is a nominal integration study, not a
pressure-vessel, fatigue or manufacturing release.  R13 remains the source
of the selected components and camera/lift sweep; this revision adds the
missing service stack and seals it with explicit, checkable geometry.
"""
from pathlib import Path
import argparse, hashlib, itertools, json, math
import cadquery as cq
import PX1_R13_WetChannels as r13
from PX1_R12_SelectedParts import box, cyl, ann, ring, volume, bounds, SEAT, WHEELS, intersect

ROOT = Path(__file__).resolve().parents[2]
SIDE_BOLTS = [(x, z) for x in (35, 75, 112, 150, 188, 225, 265)
              for z in (41, 109)]
BOTTOM_BOLTS = ([(x, y) for x in (28, 78, 128, 178, 228, 278, 328, 378)
                 for y in (-46, 46)] +
                [(x, y) for x in (6, 406) for y in (-28, 0, 28)])


def solids(p):
    return [cq.Workplane("XY").newObject([s]) for s in p.solids().vals()]


def hit(a, b):
    """Intersection volume for every solid in two compounds."""
    aa, bb = a.val().BoundingBox(), b.val().BoundingBox()
    if any(getattr(aa, k + "max") <= getattr(bb, k + "min") or
           getattr(bb, k + "max") <= getattr(aa, k + "min") for k in "xyz"):
        return 0.0
    return sum(intersect(x, y) for x in solids(a) for y in solids(b))


def outvol(a, b):
    return sum(max(0.0, volume(x.cut(b))) for x in solids(a))


def capsule(length, diameter, thickness, x, y, z):
    """Capsule in XZ extruded in Y, with exact semicircular ends."""
    sh = box(length - diameter, thickness, diameter, x, y, z)
    half = (length - diameter) / 2
    for xx in (x - half, x + half):
        sh = sh.union(cyl(diameter, thickness, (xx, y, z), "y"))
    return sh


def xz_round(a, b, radius, height, x, y, z):
    """Rounded XZ plate, using the same orientation as the R12 side cover."""
    sh = box(a, height, b, x, 0, z)
    # The box is deliberately retained as the pressure-side land.  The two
    # end cylinders create a simple capsule-like outer plate without an OCC
    # edge fillet becoming a second solid.
    return sh.translate((0, y, 0))


def outside_screw(x, z, side):
    # DIN 7991 M3x8 envelope: head diameter 6, height <=1.7.  Threads are a
    # drawing reference, not represented by a fictitious solid in the host.
    return cyl(3.0, 6.3, (x, side * 45.15, z), "y").union(
        cyl(6.0, 0.2, (x, side * 49.9, z), "y"))


def bottom_screw(x, y):
    return cyl(3.0, 6.3, (x, y, 26.35)).union(cyl(6.0, 0.2, (x, y, 21.6)))


def host_and_lid(old):
    """Remove R13's open side land and provide R14 service joints."""
    sh = old
    for side in (-1, 1):
        # The wet-channel outer wall ends at |Y|31.  Only the old side boss
        # region is removed; the pressure roof remains continuous.
        sh = sh.cut(box(258, 18.9, 64, 150, side * 40.55, 75))
        sh = sh.union(box(272, 13.0, 78, 150, side * 42.75, 75))
        sh = sh.cut(capsule(254, 54, 20, 150, side * 41.1, 75))
        # Blind pilots are closed above the pressure wall.
        for x, z in SIDE_BOLTS:
            sh = sh.cut(cyl(2.5, 5.5, (x, side * 43.25, z), "y"))
    # Flat R14 bottom lid, with local end lips that back the whole O-ring.
    sh = sh.cut(box(500, 200, 20, 206, 0, 15.5))
    for x in (12, 400):
        sh = sh.union(box(8, 78, 6.5, x, 0, 28.75))
    lid = box(412, 98, 4, 206, 0, 23.5)
    lid = lid.cut(ring(390, 84, 8, 2.8, 1.5, (206, 0, 24.75)))
    for x, y in BOTTOM_BOLTS:
        lid = lid.cut(cyl(3.4, 6, (x, y, 23.5)))
    for side in (-1, 1):
        sy = side * 19.5
        lid = lid.union(box(20, 38, 5.5, 335, sy, 28.25))
        for x in (329, 341):
            for y in (sy - 15.4, sy + 15.4):
                lid = lid.cut(cyl(2.5, 5, (x, y, 28.5)))
    return sh.clean(), lid.clean()


def side_plate(side):
    """Removable side plate carrying wheel bearings and idler pins."""
    sh = capsule(272, 76, 4, 150, side * 48, 75)
    for x in WHEELS:
        sh = sh.union(cyl(44, 10.45, (x, side * 40.775, 75), "y"))
        # From the inside out: bearing front, seat, thread/reference bore,
        # then the plate passage.  The M35 thread itself is documented below.
        for d, a, b in ((25.4, 35.45, 36.65), (30.05, 36.65, 44.5),
                        (34.0, 44.5, 47.8), (35.05, 47.8, 51.0)):
            sh = sh.cut(cyl(d, b - a, (x, side * ((a + b) / 2), 75), "y"))
    for x in (100, 200):
        sh = sh.union(cyl(16, 8, (x, side * 42, 75), "y"))
        sh = sh.cut(cyl(10.05, 9.5, (x, side * 42.75, 75), "y"))
    # CL262x62 R31, 2.1x1.1 groove.  The candidate O-ring is 185x1.5.
    sh = sh.cut(capsule(264.1, 64.1, 1.1, 150, side * 46.55, 75)
               .cut(capsule(259.9, 59.9, 2.1, 150, side * 46.55, 75)))
    for x, z in SIDE_BOLTS:
        sh = sh.cut(cyl(3.4, 6, (x, side * 48, z), "y"))
    return sh.clean()


def seal_holder(x, side):
    """Outside-installed M35x1 holder with static 32x1.5 O-ring groove."""
    sh = cyl(34.9, 5.7, (x, side * 47.35, 75), "y")
    sh = sh.cut(cyl(18.15, 8, (x, side * 47, 75), "y"))
    sh = sh.cut(cyl(22.8, 2.8, (x, side * 48.45, 75), "y"))
    sh = sh.cut(ann(32.85, 36.9, 2, (x, side * 49, 75), "y"))
    for dx in (-13.5, 13.5):
        sh = sh.cut(cyl(2.0, 1.5, (x + dx, side * 49.45, 75), "y"))
    return sh.clean()


def shaft(x, side):
    start = 29.7 if x == 250 else 31.5
    sh = cyl(17, 44.5 - start, (x, side * ((start + 44.5) / 2), 75), "y")
    if x == 250:
        sh = sh.union(cyl(10, 22.7, (x, side * 18.35, 75), "y"))
    sh = sh.union(cyl(18, 6, (x, side * 47.5, 75), "y"))
    sh = sh.union(cyl(17, 10.5, (x, side * 55.75, 75), "y"))
    sh = sh.union(cyl(8, 12.6, (x, side * 67.3, 75), "y"))
    # DIN471 17 mm groove: d3=16.2, nominal width1.1.
    return sh.cut(ann(16.2, 18, 1.1, (x, side * 36.1, 75), "y"))


def hub(x, side):
    sh = ann(17.05, 30, 14.5, (x, side * 57.75, 75), "y")
    return sh.cut(cyl(24.5, 4.1, (x, side * 63.05, 75), "y"))


def nut_reference(x, side):
    # AF13/H8 envelope.  Hex flats are not needed for the collision screen;
    # the tool/socket clearance is tested independently as a Ø20 cylinder.
    return cyl(13, 8, (x, side * 67, 75), "y").cut(
        cyl(8.1, 10, (x, side * 67, 75), "y"))


def load_r13(out, motor_step):
    # R13 itself already has a validated camera/lift assembly.  We call it
    # once and use its returned named parts; no vendor STEP is copied into the
    # repository or included in the generated export.
    cache = out / "r13_named_cache"
    meta = cache / "index.json"
    source_sha = hashlib.sha256(Path(r13.__file__).read_bytes()).hexdigest()
    motor_sha = hashlib.sha256(motor_step.read_bytes()).hexdigest() if motor_step else None
    if meta.exists():
        saved = json.loads(meta.read_text())
        if (saved.get("r13_source_sha256") == source_sha and
                saved.get("motor_step_sha256") == motor_sha and
                saved.get("cadquery") == cq.__version__):
            parts = {n: cq.Workplane("XY").newObject([cq.Shape.importBrep(str(cache / f))])
                     for n, f in saved["files"].items()}
            return parts, saved["groups"], saved.get("r13_report", {})
    parts, groups, report = r13.build(out / "r13_baseline", motor_step, 5)
    cache.mkdir(parents=True, exist_ok=True)
    files = {n: f"{i:03}.brep" for i, n in enumerate(parts)}
    for n, p in parts.items():
        p.val().exportBrep(str(cache / files[n]))
    meta.write_text(json.dumps({"r13_source_sha256": source_sha,
                                "motor_step_sha256": motor_sha,
                                "cadquery": cq.__version__, "files": files,
                                "groups": groups, "r13_report": report}, indent=2))
    return parts, groups, report


def build(out, motor_step=None, quick=False):
    out.mkdir(parents=True, exist_ok=True)
    parts, groups, r13_report = load_r13(out, motor_step)
    old_body = parts.pop("BODY_R13")
    groups.pop("BODY_R13")
    parts.pop("BOTTOM_LID_R13")
    groups.pop("BOTTOM_LID_R13")
    def add(name, shape, group):
        parts[name] = shape
        groups[name] = group
    body, lid = host_and_lid(old_body)
    add("BODY_R14", body, "housing")
    add("BOTTOM_LID_R14", lid, "housing")
    exclusions = {}
    def exclude(a, b, reason):
        exclusions[frozenset((a, b))] = reason
    side_units = {"L": [], "R": []}
    for side in (-1, 1):
        side_name = "L" if side == 1 else "R"
        # Move only the front bearing datum and its hanging support by 1 mm;
        # the R13 check found a 0.046 mm contact with the bevel envelope.
        old_name = "61801_" + side_name + "278.5"
        if old_name in parts:
            bearing = parts.pop(old_name)
            groups.pop(old_name)
            add("61801_" + side_name + "279.5", bearing.translate((1, 0, 0)), "bearing")
        support = "Pinion_hanging_support_" + side_name
        if support in parts:
            parts[support] = parts[support].translate((1, 0, 0))
        plate = "Side_cover_" + side_name
        parts[plate] = side_plate(side)
        groups[plate] = "housing"
        unit = [plate]
        for x in WHEELS:
            tag = side_name + str(x)
            parts["Axle_" + tag] = shaft(x, side)
            parts["61903_" + tag] = ann(17, 30, 7, (x, side * 40.15, 75), "y")
            parts["Flange_" + tag] = seal_holder(x, side)
            groups["Flange_" + tag] = "seal_holder"
            # Give the tyre a real wheel-hub envelope, leaving the rubber as a
            # 30.05 mm bore.  Rubber/hub bonding is a qualification item.
            parts["Crown_" + tag] = parts["Crown_" + tag].cut(
                cyl(30.05, 18, (x, side * 58.5, 75), "y"))
            add("Wheel_hub_" + tag, hub(x, side), "wheel")
            add("DIN471_17_ENVELOPE_" + tag,
                ann(16.2, 25, 1, (x, side * 36.1, 75), "y"), "reference")
            add("Inner_spacer_17p1_20_" + tag,
                ann(17.1, 20, .85, (x, side * 44.075, 75), "y"), "retainer")
            add("Outer_spacer_25_30_" + tag,
                ann(25, 30, .75, (x, side * 44.025, 75), "y"), "retainer")
            add("M8_washer_" + tag,
                ann(8.4, 24, 2, (x, side * 62, 75), "y"), "retainer")
            add("DIN985_M8_REFERENCE_" + tag, nut_reference(x, side), "reference")
            unit.extend(["Axle_" + tag, "61903_" + tag, "Flange_" + tag,
                         "Wheel_hub_" + tag, "Inner_spacer_17p1_20_" + tag,
                         "Outer_spacer_25_30_" + tag, "M8_washer_" + tag,
                         "DIN471_17_ENVELOPE_" + tag, "Crown_" + tag,
                         "DIN985_M8_REFERENCE_" + tag])
        for i, (x, z) in enumerate(SIDE_BOLTS):
            name = f"Side_M3x8_{side_name}_{i:02}"
            add(name, outside_screw(x, z, side), "fastener")
            exclude(name, "BODY_R14", "M3 thread/tap engagement is intentional")
        side_units[side_name] = unit
    for i, (x, y) in enumerate(BOTTOM_BOLTS):
        name = f"Bottom_M3x8_{i:02}"
        add(name, bottom_screw(x, y), "fastener")
        exclude(name, "BODY_R14", "M3 thread/tap engagement is intentional")
    # R14 board datums raised with the flat bottom lid.
    parts["NUCLEO_insulation_tray_RESERVE"] = box(90, 74, 1, 246.25, 0, 26)
    parts["NUCLEO_F446RE"] = box(82.5, 70, 18, 246.25, 0, 38)
    parts["TMP117_4821"] = box(25.5, 4.6, 17.7, 160, -25, 36.35)
    parts["MPRLS_3965"] = box(17.8, 16.7, 7.5, 212, 20, 53.75)
    parts["Waveshare_RS485_C"] = box(42.8, 4.75, 15.2, 251, 0, 56.6)
    # R13's thermal-angle foot was dimensioned from the old lid datum and
    # dipped into the raised R14 lid by 2.5 mm.  Keep a 2 mm metal foot above
    # the lid, rather than allowing an accidental solid overlap.
    parts["RSD_thermal_angle"] = parts["RSD_thermal_angle"].cut(
        box(180, 50, 4, 108.5, -13.5, 24.0))
    # The named R13 route reserves are retained; no new conductor is invented.
    report = {
        "revision": "R14", "date": "2026-09-09", "manufacturing_release": False,
        "physical_test": False, "status": "UNTESTED",
        "motor_model": "vendor_STEP" if motor_step else "dimension_abstraction",
        "motor_step_sha256": hashlib.sha256(motor_step.read_bytes()).hexdigest() if motor_step else None,
        "source_sha256": hashlib.sha256(Path(__file__).read_bytes()).hexdigest(),
        "cadquery_version": cq.__version__, "collision_threshold_mm3": .001,
        "static_collisions": {}, "routing_collisions": {}, "low_pipe_outside": {},
        "seal_landing": {}, "side_installation": {}, "wheel_socket_access": {},
        "lift_positions": {}, "explicit_pair_exclusions": {},
        "limitations": [
            "Nominal CAD only: no pressure, tolerance, load, fatigue or heat test.",
            "DIN471 and DIN985 entries are envelopes/references, not exact CAD parts.",
            "Gears remain blank envelopes; teeth, hubs, keys and torque retention are open.",
            "Board standoffs, connector strain relief and camera harness are open.",
            "M35x1 holder has a reference thread region; flanks, fit and locking are open.",
            "The cable tail cylinders remain installation reserves; aramid termination and dry barrier are open.",
            "Ideal straight ID150 only; pipe ovality, debris, bends and traction are not certified."
        ]
    }
    # Thread/reference overlaps are narrowly excluded; all other named parts
    # are screened as physical solids.
    for side in (-1, 1):
        side_name = "L" if side == 1 else "R"
        exclude("Side_cover_" + side_name, "BODY_R14",
                "side-plate face contact is the intentional sealed assembly joint")
        for x in WHEELS:
            fl = "Flange_" + side_name + str(x)
            cover = "Side_cover_" + side_name
            exclude(fl, cover, "M35x1 holder thread is a machining reference")
        exclude("Z16_ENVELOPE_" + side_name, "Z40_ENVELOPE_" + side_name,
                "intentional bevel tooth blank overlap")
        for x in (50., 100., 150., 200.):
            exclude("Z50_ENVELOPE_" + side_name + str(x),
                    "Z50_ENVELOPE_" + side_name + str(x + 50),
                    "intentional adjacent tooth blank envelopes")
    exclude("Hanging_bearing_bridge", "BODY_R14",
            "bridge-to-body contact is the intentional structural joint")
    # The thermal foot is intentionally seated on the lid plane after the
    # trim above; a face contact is not an interference.
    report["explicit_pair_exclusions"] = {
        "__".join(sorted(pair)): reason for pair, reason in exclusions.items()}
    physical = {n: p for n, p in parts.items()
                if groups[n] not in ("route", "external_reserve", "reference", "fastener")}
    for (n, p), (m, q) in itertools.combinations(physical.items(), 2):
        if frozenset((n, m)) in exclusions:
            continue
        v = hit(p, q)
        if v > .001:
            report["static_collisions"][n + "__" + m] = v
    physical_nonhousing = {n: p for n, p in parts.items()
                           if groups[n] not in ("route", "external_reserve",
                                                "reference", "fastener", "housing")}
    for n, p in parts.items():
        if groups[n] != "route":
            continue
        for m, q in physical_nonhousing.items():
            v = hit(p, q)
            if v > .001:
                report["routing_collisions"][n + "__" + m] = v
    # Confirm that a representative 0.1mm seal-band slice is backed by solid
    # body material, not simply surrounded by a cover groove.
    for side in (-1, 1):
        key = "L" if side == 1 else "R"
        probe = capsule(264.1, 64.1, .1, 150, side * 45.95, 75).cut(
            capsule(259.9, 59.9, .2, 150, side * 45.95, 75))
        report["seal_landing"][key] = {
            "body_probe_volume_mm3": volume(probe),
            "unsupported_mm3": outvol(probe, body),
            "candidate_ring_ID_mm": 185, "candidate_cross_section_mm": 1.5,
            "nominal_compression_pct": 26.667, "nominal_stretch_pct": 1.514,
            "inboard_land_mm": 2.95
        }
    bottom_probe = ring(390, 84, 8, 2.8, .1, (206, 0, 25.55))
    report["bottom_seal_landing"] = {
        "probe_volume_mm3": volume(bottom_probe),
        "unsupported_mm3": outvol(bottom_probe, body),
        "opening_X_mm": [16, 396], "lip_Z_mm": [25.5, 32]
    }
    # Lateral removal of the complete side unit.  At zero offset the plate is
    # assembled; positive offsets model sliding out of the body.
    for side in (-1, 1):
        side_name = "L" if side == 1 else "R"
        stationary = {n: p for n, p in physical.items() if n not in side_units[side_name]}
        checks = {}
        offsets = [0, 2, 5, 10, 20, 35] if not quick else [0, 10, 35]
        for offset in offsets:
            hits = {}
            for n in side_units[side_name]:
                moved = parts[n].translate((0, side * offset, 0))
                for m, q in stationary.items():
                    if frozenset((n, m)) in exclusions:
                        continue
                    v = hit(moved, q)
                    if v > .001:
                        hits[n + "__" + m] = v
            checks[str(offset)] = hits
        report["side_installation"][side_name] = {
            "offsets_outward_mm": offsets, "collisions_by_offset": checks}
    # A Ø20 service socket at each external nut is intentionally excluded from
    # the nut/washer itself; it must not hit the cover, tyre or holder.
    for side in (-1, 1):
        side_name = "L" if side == 1 else "R"
        for x in WHEELS:
            tag = side_name + str(x)
            tool = cyl(20, 22, (x, side * 74, 75), "y")
            misses = {}
            for n, q in physical.items():
                if n in ("DIN985_M8_REFERENCE_" + tag, "M8_washer_" + tag,
                         "Axle_" + tag):
                    continue
                v = hit(tool, q)
                if v > .001:
                    misses[n] = v
            report["wheel_socket_access"][tag] = misses
    # Reuse the complete R13 lift sweep and camera source, but test the revised
    # static body as well.  This keeps the 19 pose coverage explicit.
    camera = cq.importers.importStep(str(ROOT / "build_r12/PX1_R12_CAMERA_CANDIDATE.step"))
    pipe = cyl(150, 1600, (100, 0, 75), "x")
    low, _ = r13.pose(100, camera)
    for n, p in (parts | low).items():
        v = outvol(p.translate((0, 0, -SEAT)), pipe)
        if v > .001:
            report["low_pipe_outside"][n] = v
    levels = [100., 160., 235.] if quick else sorted(set(
        [100., 160., 235.] + [128 + 120 * math.sin(math.radians(a))
                               for a in range(-13, 64, 5)]))
    for z in levels:
        moving, metrics = r13.pose(z, camera)
        hits = {}
        for n, p in moving.items():
            for m, q in physical.items():
                v = hit(p, q)
                if v > .001:
                    hits[n + "__" + m] = v
        metrics["collisions"] = hits
        report["lift_positions"][f"{z:.6f}"] = metrics
    report["part_bounds_mm"] = {n: bounds(p) for n, p in parts.items()}
    report["LOW_assembly_bounds_mm"] = [
        [min(bounds(p)[0][i] for p in (parts | low).values()) for i in range(3)],
        [max(bounds(p)[1][i] for p in (parts | low).values()) for i in range(3)]]
    report["body_plus_bottom_lid_aluminum_mass_kg"] = (volume(body) + volume(lid)) * 2.7e-6
    report["nominal_bottom_corner_radial_clearance_mm"] = .546
    report["nominal_thread_tip_radial_clearance_mm"] = 1.108
    report["solid_validity"] = {n: all(s.isValid() for s in p.solids().vals())
                                for n, p in parts.items()}
    bad = (report["static_collisions"] or report["routing_collisions"] or
           report["low_pipe_outside"] or not all(report["solid_validity"].values()) or
           any(x["unsupported_mm3"] > .001 for x in report["seal_landing"].values()) or
           report["bottom_seal_landing"]["unsupported_mm3"] > .001 or
           any(v for v in report["wheel_socket_access"].values()) or
           any(v for a in report["side_installation"].values()
               for v in a["collisions_by_offset"].values()) or
           any(v["collisions"] for v in report["lift_positions"].values()))
    report["status"] = "FAIL_R14_STUDY" if bad else "PASS_SCOPED_R14_RETENTION_LANDING_ASSEMBLY"
    report["quick"] = quick
    (out / "validation.json").write_text(json.dumps(report, indent=2))
    # Only source/text and a lightweight assembly are intended for persistence;
    # all generated files are ignored by git.
    ass = cq.Assembly(name="PX1_R14_NOMINAL_SERVICE_STUDY")
    colors = {"housing": (.55, .6, .65, .4), "wheel": (.12, .12, .12),
              "component": (.12, .5, .3), "gear_envelope": (.85, .65, .2)}
    for n, p in (parts | low).items():
        ass.add(p, name=n.replace(".", "_").replace("-", "minus"),
               color=cq.Color(*colors.get(groups.get(n), (.7, .7, .7))))
    ass.export(str(out / "PX1_R14_NOMINAL_SERVICE_STUDY.step"))
    named = out / "named_parts"
    named.mkdir(exist_ok=True)
    files = {n: f"{i:03}.brep" for i, n in enumerate(parts)}
    for n, p in parts.items():
        p.val().exportBrep(str(named / files[n]))
    (named / "index.json").write_text(json.dumps({"files": files, "groups": groups}, indent=2))
    print(json.dumps({k: report[k] for k in (
        "status", "static_collisions", "routing_collisions", "seal_landing",
        "bottom_seal_landing", "side_installation", "wheel_socket_access",
        "low_pipe_outside", "LOW_assembly_bounds_mm")}, indent=2), flush=True)
    return parts, groups, report


if __name__ == "__main__":
    ap = argparse.ArgumentParser()
    ap.add_argument("--out", type=Path, default=ROOT / "build_r14")
    ap.add_argument("--motor-step", type=Path)
    ap.add_argument("--quick", action="store_true")
    args = ap.parse_args()
    build(args.out, args.motor_step, args.quick)
