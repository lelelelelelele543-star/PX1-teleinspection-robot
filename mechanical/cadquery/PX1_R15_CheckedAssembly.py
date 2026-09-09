"""PX1 R15: repair R14 geometry and its false-positive validation coverage.

Millimetres. Nominal CAD study only. No tolerance, pressure or torque release.
Factory motor/camera compounds are checked solid by solid. Every other named
manufactured part, including each screw, must be one connected valid solid.
"""
from pathlib import Path
import argparse
import hashlib
import itertools
import json
import math
import cadquery as cq
import PX1_R12_SelectedParts as r12
import PX1_R13_WetChannels as r13
from PX1_R12_SelectedParts import box, cyl, ann, rr, ring, volume, bounds, SEAT, WHEELS

ROOT = Path(__file__).resolve().parents[2]
EPS = 0.001
SIDE_BOLTS = [(x, z) for x in (35, 75, 112, 150, 188, 225, 265) for z in (41, 109)]
BOTTOM_BOLTS = ([(x, y) for x in (28, 78, 128, 178, 228, 278, 328, 378) for y in (-46, 46)]
                + [(x, y) for x in (6, 406) for y in (-28, 0, 28)])


def sha(path):
    return hashlib.sha256(Path(path).read_bytes()).hexdigest()


def compound_solids(shape):
    return shape.solids().vals()


def overlap(a, b):
    """No internal per-solid rounding; aggregate all solid intersections."""
    aa, bb = a.val().BoundingBox(), b.val().BoundingBox()
    if any(getattr(aa, k + "max") <= getattr(bb, k + "min") or
           getattr(bb, k + "max") <= getattr(aa, k + "min") for k in "xyz"):
        return 0.0
    return sum(max(0.0, p.intersect(q).Volume())
               for p in compound_solids(a) for q in compound_solids(b))


def outside(a, b):
    return sum(max(0.0, p.cut(b.val()).Volume()) for p in compound_solids(a))


def capsule(length, diameter, thickness, x, y, z):
    sh = box(length - diameter, thickness, diameter, x, y, z)
    for xx in (x - (length - diameter) / 2, x + (length - diameter) / 2):
        sh = sh.union(cyl(diameter, thickness, (xx, y, z), "y"))
    return sh


def xz_round(length, height, radius, thickness, x, y, z):
    return rr(length, height, radius, thickness, (0, 0, 0)).rotate(
        (0, 0, 0), (1, 0, 0), 90).translate((x, y, z))


def cone(r1, r2, length, origin, direction):
    return cq.Workplane("XY").newObject([
        cq.Solid.makeCone(r1, r2, length, cq.Vector(*origin), cq.Vector(*direction))])


def side_screw(x, z, side):
    # DIN7991 M3x8: total8 incl head; 6.3 shank +1.5 cone +0.2 rim.
    return cyl(3, 6.3, (x, side * 45.15, z), "y").union(
        cone(1.5, 3, 1.5, (x, side * 48.3, z), (0, side, 0))).union(
        cyl(6, .2, (x, side * 49.9, z), "y")).clean()


def bottom_screw(x, y):
    return cyl(6, .2, (x, y, 21.6)).union(
        cone(3, 1.5, 1.5, (x, y, 21.7), (0, 0, 1))).union(
        cyl(3, 6.3, (x, y, 26.35))).clean()


def host_and_lid(old):
    sh = old
    for side in (-1, 1):
        sh = sh.cut(box(258, 18.9, 64, 150, side * 40.55, 75))
        # Pressure flange ends exactly at46, with a real radial sealing land.
        sh = sh.union(xz_round(272, 78, 6, 6.5, 150, side * 42.75, 75))
        sh = sh.cut(capsule(254, 54, 20, 150, side * 41.1, 75))
        # Restore the full4mm bearing bridge lands after removing old bosses.
        for x in (240, 296):
            sh = sh.union(box(12, 8, 4, x, side * 39, 106))
            sh = sh.cut(cyl(2.5, 3, (x, side * 37, 106.5)))
        for x, z in SIDE_BOLTS:
            sh = sh.cut(cyl(2.5, 5.5, (x, side * 43.25, z), "y"))
    sh = sh.cut(box(500, 200, 40, 206, 0, 5.5))  # trim everything below25.5
    for x in (12, 400):
        sh = sh.union(box(8, 78, 6.5, x, 0, 28.75))
    lid = box(412, 98, 4, 206, 0, 23.5).cut(ring(390, 84, 8, 2.8, 1.5, (206, 0, 24.75)))
    for x, y in BOTTOM_BOLTS:
        sh = sh.cut(cyl(2.5, 5.5, (x, y, 28.25)))
        lid = lid.cut(cyl(3.4, 6, (x, y, 23.5)))
        lid = lid.cut(cyl(6, .3, (x, y, 21.55))).cut(
            cone(3, 1.7, 1.3, (x, y, 21.7), (0, 0, 1)))
    for side in (-1, 1):
        sy = side * 19.5
        lid = lid.union(box(20, 38, 5.5, 335, sy, 28.25))
        for x in (329, 341):
            for y in (sy - 15.4, sy + 15.4):
                lid = lid.cut(cyl(2.5, 5, (x, y, 28.5)))
    return sh.clean(), lid.clean()


def side_plate(side):
    # A rounded rectangle: capsule ends would remove the corner bolt lands.
    sh = xz_round(272, 76, 6, 4, 150, side * 48, 75)
    for x in WHEELS:
        sh = sh.union(cyl(44, 10.45, (x, side * 40.775, 75), "y"))
        for d, a, b in ((25.4, 35.45, 36.65), (30.05, 36.65, 44.5),
                        (34.0, 44.5, 47.8), (35.05, 47.8, 51)):
            sh = sh.cut(cyl(d, b - a, (x, side * (a + b) / 2, 75), "y"))
    for x in (100, 200):
        sh = sh.union(cyl(16, 8, (x, side * 42, 75), "y"))
        sh = sh.cut(cyl(10.05, 9.5, (x, side * 42.75, 75), "y"))
    sh = sh.cut(capsule(264.1, 64.1, 1.1, 150, side * 46.55, 75).cut(
        capsule(259.9, 59.9, 2, 150, side * 46.55, 75)))
    for x, z in SIDE_BOLTS:
        sh = sh.cut(cyl(3.4, 6, (x, side * 48, z), "y"))
        sh = sh.cut(cone(1.7, 3, 1.3, (x, side * 48.5, z), (0, side, 0)))
        sh = sh.cut(cyl(6, .3, (x, side * 49.95, z), "y"))
    return sh.clean()


def seal_holder(x, side):
    sh = cyl(34.9, 5.7, (x, side * 47.35, 75), "y")
    sh = sh.cut(cyl(18.15, 8, (x, side * 47, 75), "y"))
    sh = sh.cut(cyl(22.8, 2.8, (x, side * 48.45, 75), "y"))
    sh = sh.cut(ann(32.85, 36.9, 2, (x, side * 49, 75), "y"))
    for dx in (-13.5, 13.5):
        sh = sh.cut(cyl(2, 1.5, (x + dx, side * 49.45, 75), "y"))
    return sh.clean()


def key_profile(x, side, width=5, length=10, height=5, bottom=80.5):
    # Ganter DIN6885-5-5-10-A-NI size candidate,316Ti, rounded ends in X/Y.
    # Local seller, keyway fits and allowable torque remain unqualified.
    sh = box(width, length - width, height, x, side * 56, bottom + height / 2)
    for y in (56 - (length - width) / 2, 56 + (length - width) / 2):
        sh = sh.union(cyl(width, height, (x, side * y, bottom + height / 2)))
    return sh.clean()


def shaft(x, side):
    start = 29.7 if x == 250 else 31.5
    sh = cyl(17, 44.5 - start, (x, side * (start + 44.5) / 2, 75), "y")
    if x == 250:
        sh = sh.union(cyl(10, 22.7, (x, side * 18.35, 75), "y"))
    sh = sh.union(cyl(18, 6, (x, side * 47.5, 75), "y"))
    sh = sh.union(cyl(17, 10.5, (x, side * 55.75, 75), "y"))
    sh = sh.union(cyl(8, 12.6, (x, side * 67.3, 75), "y"))
    sh = sh.cut(ann(16.2, 18, 1.1, (x, side * 36.1, 75), "y"))
    return sh.cut(key_profile(x, side, width=5, length=10.1, height=10)).clean()


def hub(x, side):
    sh = ann(17.05, 30, 14.5, (x, side * 57.75, 75), "y")
    sh = sh.cut(cyl(24.5, 4.1, (x, side * 63.05, 75), "y"))
    # Hub keyway top is75 +8.525 +2.3 =85.825; candidate nominal relief.
    return sh.cut(box(5.05, 15, 10.825, x, side * 57.75, 80.4125)).clean()


def nut(x, side):
    sh = cq.Workplane("XY").polygon(6, 13 / math.cos(math.pi / 6)).extrude(8)
    sh = sh.translate((0, 0, -4)).rotate((0, 0, 0), (1, 0, 0), 90).translate((x, side * 67, 75))
    return sh.cut(cyl(8.1, 10, (x, side * 67, 75), "y"))


def pinion_support(side):
    sy = side * 19.5
    sh = box(25, 27, 3, 287, sy, 106.5)
    for x in (279.5, 295.5):
        sh = sh.union(box(5, 27, 46.5, x, sy, 84.75).cut(
            cyl(21.02, 7, (x, sy, 75), "x")))
    return sh.clean()


def load_baseline(cache, motor_step):
    data = json.loads((cache / "index.json").read_text())
    expected = {"r13_source_sha256": sha(r13.__file__),
                "motor_step_sha256": sha(motor_step), "cadquery": cq.__version__}
    for k, v in expected.items():
        if data.get(k) != v:
            raise ValueError(f"Baseline provenance mismatch: {k}")
    parts = {n: cq.Workplane("XY").newObject([cq.Shape.importBrep(str(cache / f))])
             for n, f in data["files"].items()}
    # Import and validate all cache entries; hash the exact inputs in R15.
    if any(not p.solids().vals() or not all(s.isValid() for s in p.solids().vals())
           for p in parts.values()):
        raise ValueError("Invalid R13 baseline BREP; rebuild it from R13 sources")
    provenance = expected | {"r12_source_sha256": sha(r12.__file__),
        "r13_cache_brep_sha256": {n: sha(cache / f) for n, f in data["files"].items()},
        "r13_cache_index_sha256": sha(cache / "index.json"),
        "baseline_note": "R13 cache checked against its R13 source, motor and runtime metadata; individual BREP hashes recorded. Historical cache lacks an R12 hash."}
    return parts, dict(data["groups"]), provenance


def geometry(cache, motor_step):
    parts, groups, provenance = load_baseline(cache, motor_step)
    old = parts.pop("BODY_R13"); groups.pop("BODY_R13")
    parts.pop("BOTTOM_LID_R13"); groups.pop("BOTTOM_LID_R13")
    def add(n, p, g):
        parts[n], groups[n] = p, g
    body, lid = host_and_lid(old)
    add("BODY_R15", body, "housing"); add("BOTTOM_LID_R15", lid, "housing")
    threads, mesh, side_units, side_bolts = {}, {}, {}, {}
    for side in (-1, 1):
        label = "L" if side == 1 else "R"
        old_bearing = "61801_" + label + "278.5"
        p = parts.pop(old_bearing); groups.pop(old_bearing)
        add("61801_" + label + "279.5", p.translate((1, 0, 0)), "bearing")
        parts["Pinion_hanging_support_" + label] = pinion_support(side)
        cover = "Side_cover_" + label
        parts[cover] = side_plate(side)
        unit = [cover, "Z40_ENVELOPE_" + label]
        for x in (50., 100., 150., 200., 250.):
            unit.append("Z50_ENVELOPE_" + label + str(x))
        for x in (100, 200):
            unit += ["Idler_pin_" + label + str(x), "6701_" + label + str(x)]
        for x in WHEELS:
            tag = label + str(x)
            parts["Axle_" + tag] = shaft(x, side)
            parts["61903_" + tag] = ann(17, 30, 7, (x, side * 40.15, 75), "y")
            parts["Flange_" + tag] = seal_holder(x, side)
            parts["Crown_" + tag] = parts["Crown_" + tag].cut(cyl(30.05, 18, (x, side * 58.5, 75), "y"))
            add("Wheel_hub_" + tag, hub(x, side), "wheel")
            add("Wheel_key_5x5x10_" + tag, key_profile(x, side), "retainer")
            add("DIN471_17_ENVELOPE_" + tag, ann(16.2, 25, 1, (x, side * 36.1, 75), "y"), "retainer")
            add("Inner_spacer_17p1_20_" + tag, ann(17.1, 20, .85, (x, side * 44.075, 75), "y"), "retainer")
            add("Outer_spacer_25_30_" + tag, ann(25, 30, .75, (x, side * 44.025, 75), "y"), "retainer")
            add("M8_washer_" + tag, ann(8.4, 24, 2, (x, side * 62, 75), "y"), "retainer")
            add("DIN985_M8_ENVELOPE_" + tag, nut(x, side), "fastener")
            unit += [n + tag for n in ("Axle_", "61903_", "Flange_", "Crown_", "Wheel_hub_",
                "Wheel_key_5x5x10_", "DIN471_17_ENVELOPE_", "Inner_spacer_17p1_20_",
                "Outer_spacer_25_30_", "M8_washer_", "DIN985_M8_ENVELOPE_")]
            threads[frozenset(("Flange_" + tag, cover))] = (
                ann(34, 35, 3.3, (x, side * 46.15, 75), "y"), "M35x1 reference annulus only")
        side_bolts[label] = []
        for i, (x, z) in enumerate(SIDE_BOLTS):
            n = f"Side_M3x8_{label}_{i:02}"
            add(n, side_screw(x, z, side), "fastener"); side_bolts[label].append(n)
            threads[frozenset((n, "BODY_R15"))] = (
                ann(2.5, 3, 4, (x, side * 44, z), "y"), "M3 tap engagement |Y|42..46 only")
        side_units[label] = unit
        mesh[frozenset(("Z16_ENVELOPE_" + label, "Z40_ENVELOPE_" + label))] = "Bevel blanks; teeth and disengagement unresolved"
        for x in (50., 100., 150., 200.):
            mesh[frozenset(("Z50_ENVELOPE_" + label + str(x), "Z50_ENVELOPE_" + label + str(x + 50)))] = "Adjacent Z50 tooth blanks only"
    for i, (x, y) in enumerate(BOTTOM_BOLTS):
        n = f"Bottom_M3x8_{i:02}"
        add(n, bottom_screw(x, y), "fastener")
        threads[frozenset((n, "BODY_R15"))] = (
            ann(2.5, 3, 4, (x, y, 27.5)), "M3 tap engagement Z25.5..29.5 only")
    parts["NUCLEO_insulation_tray_RESERVE"] = box(90, 74, 1, 246.25, 0, 26)
    parts["NUCLEO_F446RE"] = box(82.5, 70, 18, 246.25, 0, 38)
    parts["TMP117_4821"] = box(25.5, 4.6, 17.7, 160, -25, 36.35)
    parts["MPRLS_3965"] = box(17.8, 16.7, 7.5, 212, 20, 53.75)
    parts["Waveshare_RS485_C"] = box(42.8, 4.75, 15.2, 251, 0, 56.6)
    # Face-to-face contact at25.5, with2.5mm foot remaining to28.
    parts["RSD_thermal_angle"] = parts["RSD_thermal_angle"].cut(box(180, 50, 20, 108.5, -13.5, 15.5))
    return parts, groups, threads, mesh, side_units, side_bolts, provenance


def residual_overlap(a, b, mask):
    return sum(max(0.0, p.intersect(q).cut(mask.val()).Volume())
               for p in compound_solids(a) for q in compound_solids(b))


def validate(parts, groups, threads, mesh, side_units, side_bolts, camera, quick):
    report = {"revision": "R15", "date": "2026-09-09", "manufacturing_release": False,
        "physical_test": False, "quick": quick, "collision_threshold_mm3": EPS,
        "static_collisions": {}, "routing_collisions": {}, "low_pipe_outside": {},
        "thread_mask_checks": {}, "seal_landing": {}, "side_withdrawal": {},
        "wheel_socket_access": {}, "lift_positions": {}, "contact_checks": {}}
    # Gear blanks remain physical obstacles to all other parts. No housing,
    # mounting, bearing, key, circlip, nut or screw category is exempted.
    physical = {n: p for n, p in parts.items() if groups[n] not in ("route", "external_reserve")}
    report["coverage"] = {"named_static_parts": len(parts), "physical_static_parts": len(physical),
        "physical_pair_count": math.comb(len(physical), 2),
        "excluded_categories": ["route", "external_reserve"],
        "route_note": "Routes checked separately against ALL physical parts, including housings and fasteners.",
        "mesh_pair_exclusions": {"__".join(sorted(k)): v for k, v in mesh.items()},
        "thread_masks": {"__".join(sorted(k)): {"reason": v[1], "bounds_mm": bounds(v[0])} for k, v in threads.items()}}
    print("R15: static pairs including fasteners", flush=True)
    for (n, p), (m, q) in itertools.combinations(physical.items(), 2):
        pair = frozenset((n, m))
        if pair in mesh:
            continue
        v = overlap(p, q)
        if pair in threads:
            residual = residual_overlap(p, q, threads[pair][0]) if v > EPS else 0.0
            report["thread_mask_checks"][n + "__" + m] = {"raw_mm3": v, "outside_mask_mm3": residual}
            v = residual
        if v > EPS:
            report["static_collisions"][n + "__" + m] = v
    for n, p in parts.items():
        if groups[n] == "route":
            for m, q in physical.items():
                v = overlap(p, q)
                if v > EPS:
                    report["routing_collisions"][n + "__" + m] = v
    print(json.dumps({"static_collisions": report["static_collisions"],
                      "routing_collisions": report["routing_collisions"]}), flush=True)
    print("R15: seal backing and support contacts", flush=True)
    body, lid = parts["BODY_R15"], parts["BOTTOM_LID_R15"]
    for side in (-1, 1):
        label = "L" if side == 1 else "R"
        probe = capsule(264.1, 64.1, .1, 150, side * 45.95, 75).cut(capsule(259.9, 59.9, .2, 150, side * 45.95, 75))
        report["seal_landing"][label] = {"unsupported_mm3": outside(probe, body), "probe_mm3": volume(probe)}
        for x in WHEELS:
            tag = label + str(x)
            probe = ann(35.05, 35.25, 2, (x, side * 49, 75), "y")
            report["seal_landing"]["holder_" + tag] = {"unsupported_mm3": outside(probe, parts["Side_cover_" + label]), "probe_mm3": volume(probe)}
            for a, b in (("M8_washer_", "Wheel_hub_"), ("Inner_spacer_17p1_20_", "61903_")):
                report["contact_checks"][a + tag + "__" + b + tag] = parts[a + tag].val().distance(parts[b + tag].val())
    probe = ring(390, 84, 8, 2.8, .1, (206, 0, 25.55))
    report["seal_landing"]["bottom"] = {"unsupported_mm3": outside(probe, body), "probe_mm3": volume(probe)}
    report["contact_checks"]["RSD_thermal_angle__BOTTOM_LID_R15"] = parts["RSD_thermal_angle"].val().distance(lid.val())
    supports = {n: p for n, p in parts.items() if groups[n] in ("housing", "mount", "lift_mount")}
    reached = {"BODY_R15"}
    while True:
        attached = {n for n, p in supports.items() if n not in reached and any(p.val().distance(supports[m].val()) <= 1e-5 for m in reached)}
        if not attached:
            break
        reached.update(attached)
    report["supports_without_contact_path_to_body"] = sorted(set(supports) - reached)
    report["solid_counts"] = {n: len(p.solids().vals()) for n, p in parts.items()}
    report["solid_validity"] = {n: bool(p.solids().vals()) and all(s.isValid() for s in p.solids().vals()) for n, p in parts.items()}
    report["compound_component_allowlist"] = ["Pololu4695_L", "Pololu4695_R"]
    report["unexpected_solid_counts"] = {n: c for n, c in report["solid_counts"].items() if c != 1 and n not in report["compound_component_allowlist"]}
    print("R15: complete side groups, bolts removed before withdrawal", flush=True)
    for side in (-1, 1):
        label = "L" if side == 1 else "R"
        unit = side_units[label]
        stationary = {n: p for n, p in physical.items() if n not in unit and n not in side_bolts[label]}
        offsets = [0, 10, 35] if quick else [0, 2, 5, 10, 20, 35]
        checks = {}
        for offset in offsets:
            print(f"R15: side {label} outward{offset}mm", flush=True)
            hits = {}
            for n in unit:
                moved = parts[n].translate((0, side * offset, 0))
                for m, q in stationary.items():
                    if frozenset((n, m)) in mesh:
                        continue
                    v = overlap(moved, q)
                    if v > EPS:
                        hits[n + "__" + m] = v
            checks[str(offset)] = hits
        report["side_withdrawal"][label] = {"unit_names": unit, "removed_screws": side_bolts[label],
            "offsets_mm": offsets, "collisions": checks,
            "scope": "Discrete non-mesh clearance; gear retention and actual tooth disengagement unresolved."}
    for side in (-1, 1):
        label = "L" if side == 1 else "R"
        for x in WHEELS:
            tag = label + str(x)
            tool = cyl(20, 22, (x, side * 74, 75), "y")
            hits = {}
            for n, q in physical.items():
                if n in ("DIN985_M8_ENVELOPE_" + tag, "M8_washer_" + tag, "Axle_" + tag):
                    continue
                v = overlap(tool, q)
                if v > EPS:
                    hits[n] = v
            report["wheel_socket_access"][tag] = hits
    print("R15: ID150 containment and lift pairs", flush=True)
    pipe = cyl(150, 1600, (100, 0, 75), "x")
    low, _ = r13.pose(100, camera)
    for n, p in (parts | low).items():
        v = outside(p.translate((0, 0, -SEAT)), pipe)
        if v > EPS:
            report["low_pipe_outside"][n] = v
    levels = [100., 160., 235.] if quick else sorted(set(
        [100., 160., 235.] + [128 + 120 * math.sin(math.radians(a)) for a in range(-13, 64, 5)]))
    report["moving_pair_exclusions"] = {"Camera_cradle_REFERENCE__Gas150N_INSTALLATION_RESERVE": "Spring endpoint reserve only; clevis unfinished."}
    for z in levels:
        print(f"R15: lift Z={z:.3f}", flush=True)
        moving, metrics = r13.pose(z, camera)
        hits = {}
        for n, p in moving.items():
            for m, q in physical.items():
                v = overlap(p, q)
                if v > EPS:
                    hits[n + "__" + m] = v
        for (n, p), (m, q) in itertools.combinations(moving.items(), 2):
            if {n, m} == {"Camera_cradle_REFERENCE", "Gas150N_INSTALLATION_RESERVE"}:
                continue
            v = overlap(p, q)
            if v > EPS:
                hits[n + "__" + m] = v
        metrics["collisions"] = hits
        report["lift_positions"][f"{z:.6f}"] = metrics
    report["sweep_pose_count"] = len(levels)
    report["part_bounds_mm"] = {n: bounds(p) for n, p in parts.items()}
    report["LOW_assembly_bounds_mm"] = [
        [min(bounds(p)[0][i] for p in (parts | low).values()) for i in range(3)],
        [max(bounds(p)[1][i] for p in (parts | low).values()) for i in range(3)]]
    report["body_and_lid_aluminum_mass_kg"] = (volume(body) + volume(lid)) * 2.7e-6
    lid_bb = bounds(lid)
    report["bottom_corner_conservative_pipe_clearance_mm"] = 75 - math.hypot(max(abs(lid_bb[0][1]), abs(lid_bb[1][1])), lid_bb[0][2] - SEAT - 75)
    axle_bb = bounds(parts["Axle_L50.0"])
    report["thread_tip_conservative_pipe_clearance_mm"] = 75 - math.hypot(axle_bb[1][1], -4 - SEAT)
    bad = (report["static_collisions"] or report["routing_collisions"] or report["low_pipe_outside"]
        or report["unexpected_solid_counts"] or not all(report["solid_validity"].values())
        or report["supports_without_contact_path_to_body"]
        or any(x["unsupported_mm3"] > EPS for x in report["seal_landing"].values())
        or any(x > 1e-5 for x in report["contact_checks"].values())
        or any(report["wheel_socket_access"].values())
        or any(c for s in report["side_withdrawal"].values() for c in s["collisions"].values())
        or any(p["collisions"] for p in report["lift_positions"].values()))
    report["status"] = "FAIL_R15_NOMINAL_STUDY" if bad else (
        "PASS_R15_QUICK_SCREEN_ONLY" if quick else "PASS_R15_SCOPED_NOMINAL_GEOMETRY")
    report["limitations"] = [
        "No production dimensions: tolerances, pressure, strength, heat and physical tests remain open.",
        "Gears are blanks: tooth manufacture, gear-to-shaft torque joints and axial gear retention remain open.",
        "Wheel key size316Ti DIN6885-5-5-10-A-NI selected from catalog; local supplier, strength and keyway fits remain open.",
        "DIN471 ring and DIN985 nut are conservative envelopes; thread flanks and seating fits unfinished.",
        "M35 holders have only3.3 nominal thread turns, no locking scheme or axial load qualification.",
        "Board standoffs, bracket fasteners, camera clamp/pivots, exact gas spring and moving harness remain open.",
        "Six-core tether unchanged; tail seal/aramid anchor and HV electrical release remain open.",
        "Discrete lift and lateral withdrawal poses; no continuous collision, tooth disengagement or deflection proof.",
        "Only neutral camera, ideal straight ID150; no combined pan/rotate, bends, debris or traction qualification."
    ]
    return report, low


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--out", type=Path, default=ROOT / "build_r15")
    ap.add_argument("--r13-cache", type=Path, default=ROOT / "build_r14/r13_named_cache")
    ap.add_argument("--motor-step", type=Path, required=True)
    ap.add_argument("--quick", action="store_true")
    ap.add_argument("--geometry-only", action="store_true")
    args = ap.parse_args()
    source_digest = sha(__file__)
    args.out.mkdir(parents=True, exist_ok=True)
    print("R15: checked baseline and corrected geometry", flush=True)
    parts, groups, threads, mesh, units, bolts, provenance = geometry(args.r13_cache, args.motor_step)
    camera_path = ROOT / "build_r12/PX1_R12_CAMERA_CANDIDATE.step"
    provenance.update({"r15_source_sha256": source_digest, "camera_step_sha256": sha(camera_path)})
    named = args.out / "named_parts"; named.mkdir(exist_ok=True)
    files = {n: f"{i:03}.brep" for i, n in enumerate(parts)}
    for n, p in parts.items():
        target = named / files[n]
        p.val().exportBrep(str(target))
    roundtrip = {}
    for n, filename in files.items():
        loaded = cq.Shape.importBrep(str(named / filename))
        row = {"solid_count": len(loaded.Solids()),
               "valid": bool(loaded.Solids()) and all(s.isValid() for s in loaded.Solids()),
               "volume_difference_mm3": abs(sum(s.Volume() for s in loaded.Solids()) - volume(parts[n]))}
        if (not row["valid"] or row["solid_count"] != len(parts[n].solids().vals())
                or row["volume_difference_mm3"] > EPS):
            raise ValueError(f"BREP export round-trip failed: {n}: {row}")
        roundtrip[n] = row
    provenance["brep_export_roundtrip"] = roundtrip
    (named / "index.json").write_text(json.dumps({"files": files, "groups": groups,
        "r15_source_sha256": source_digest, "brep_sha256": {n: sha(named / f) for n, f in files.items()}}, indent=2) + "\n")
    (args.out / "provenance.json").write_text(json.dumps(provenance, indent=2) + "\n")
    print(f"R15: saved {len(parts)} named parts", flush=True)
    if args.geometry_only:
        return 0
    camera = cq.importers.importStep(str(camera_path))
    report, low = validate(parts, groups, threads, mesh, units, bolts, camera, args.quick)
    if sha(__file__) != source_digest:
        raise RuntimeError("R15 source changed while checks were running; rerun before publishing a result")
    report["source_sha256"] = source_digest
    report["cadquery"] = cq.__version__
    (args.out / "validation.json").write_text(json.dumps(report, indent=2) + "\n")
    ass = cq.Assembly(name="PX1_R15_NOMINAL_ASSEMBLY")
    for n, p in (parts | low).items():
        ass.add(p, name=n.replace(".", "_").replace("-", "minus"))
    ass.export(str(args.out / "PX1_R15_NOMINAL_ASSEMBLY.step"))
    print(json.dumps({k: report[k] for k in ("status", "static_collisions", "routing_collisions", "unexpected_solid_counts", "supports_without_contact_path_to_body", "low_pipe_outside", "sweep_pose_count")}, indent=2), flush=True)
    return 1 if report["status"].startswith("FAIL") else 0


if __name__ == "__main__":
    raise SystemExit(main())
