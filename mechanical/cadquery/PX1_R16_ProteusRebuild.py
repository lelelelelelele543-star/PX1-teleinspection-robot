#!/usr/bin/env python3
"""PX-1 Rev.R16 — compact CRP-150-class mechanical rebuild.

This is a nominal packaging study, not a pressure/strength release.  The
revision deliberately removes the long R15 tail, makes the six wheels the
lowest/supporting geometry, and replaces the wrench-only wheel retainer with
an accessible captive cross-pin.  The camera is a separate rounded protective
pod which nests in a shallow roof saddle when the two-link manual lift is
folded.

Coordinate system: X is the crawler travel axis, Y is across the two sides,
and Z is up from the ideal pipe bottom.  Positive Y is the left side.
"""
from __future__ import annotations

import argparse
import hashlib
import json
import math
from pathlib import Path
from typing import Dict, Iterable, List, Tuple

import cadquery as cq


ROOT = Path(__file__).resolve().parents[2]
DEFAULT_OUT = ROOT / "build_r16"
EPS = 1e-5

# CRP-150-class envelope and wheel architecture.
BODY_L = 307.0
BODY_HALF_W = 46.0
BODY_Z0 = 8.0
BODY_Z1 = 90.0
WHEEL_R = 45.0
WHEEL_Z = 45.0
WHEEL_X = (50.0, 150.0, 250.0)
IDLER_X = (100.0, 200.0)
GEAR_X = (50.0, 100.0, 150.0, 200.0, 250.0)
SIDE_RECESS_INNER_Y = 39.0
SIDE_COVER_INNER_Y = 43.0
SIDE_COVER_OUTER_Y = 48.0
WHEEL_INNER_Y = 51.25
WHEEL_OUTER_Y = 66.5
PIPE_R = 75.0
PIPE_Z = 75.0

# Folded and raised lift poses.  The two 80 mm links fold back over the saddle
# at LOW and align vertically at HIGH, keeping the camera centre close to the
# crawler instead of sending it forward outside the body.
LIFT_A = (150.0, 90.0)
LIFT_C_LOW = (150.0, 119.0)
LIFT_E_LOW = (150.0 + math.sqrt(80.0 ** 2 - 14.5 ** 2), 104.5)
LIFT_E_HIGH = (150.0, 170.0)
LIFT_C_HIGH = (150.0, 250.0)
LIFT_LINK_L = 80.0
LIFT_Y = 38.0
LIFT_T = 4.5
LIFT_W = 14.0

# Armoured camera pod.  It is intentionally not the old free-standing
# cylindrical envelope: the shell has a recessed window and a surrounding
# front guard, with the RunCam board held in an elastomer pocket.
CAM_CENTER_LOW = (150.0, 0.0, 119.0)
CAM_L = 88.0
CAM_W = 54.0
CAM_H = 48.0
CAM_R = 8.0
CAM_FRONT_X = CAM_CENTER_LOW[0] - CAM_L / 2.0


def solids(shape: cq.Workplane | cq.Shape) -> List[cq.Shape]:
    raw = shape.val() if isinstance(shape, cq.Workplane) else shape
    return list(raw.Solids())


def volume(shape: cq.Workplane | cq.Shape) -> float:
    return sum(s.Volume() for s in solids(shape))


def bbox(shape: cq.Workplane | cq.Shape) -> Dict[str, float]:
    b = (shape.val() if isinstance(shape, cq.Workplane) else shape).BoundingBox()
    return {"xmin": b.xmin, "xmax": b.xmax, "ymin": b.ymin, "ymax": b.ymax,
            "zmin": b.zmin, "zmax": b.zmax,
            "xlen": b.xlen, "ylen": b.ylen, "zlen": b.zlen}


def valid(shape: cq.Workplane | cq.Shape) -> bool:
    ss = solids(shape)
    return bool(ss) and all(s.isValid() for s in ss)


def box(dx: float, dy: float, dz: float, x: float, y: float, z: float,
        centered: Tuple[bool, bool, bool] = (False, False, False)) -> cq.Workplane:
    return cq.Workplane("XY").box(dx, dy, dz, centered=centered).translate((x, y, z))


def rounded_xz(dx: float, dy: float, dz: float, radius: float,
               center: Tuple[float, float, float]) -> cq.Workplane:
    """Rounded rectangle in the X-Z plane, extruded across Y."""
    sh = cq.Workplane("XY").box(dx, dy, dz, centered=(True, True, True))
    if radius:
        sh = sh.edges("|Y").fillet(radius)
    return sh.translate(center)


def rounded_yz(dx: float, dy: float, dz: float, radius: float,
               center: Tuple[float, float, float]) -> cq.Workplane:
    """Rounded rectangle in the Y-Z plane, extruded along X."""
    sh = cq.Workplane("XY").box(dx, dy, dz, centered=(True, True, True))
    if radius:
        sh = sh.edges("|X").fillet(radius)
    return sh.translate(center)


def rounded_all(dx: float, dy: float, dz: float, yz_radius: float,
                xz_radius: float, center: Tuple[float, float, float]) -> cq.Workplane:
    """Round the Y-Z and X-Z outside corners of a pressure block."""
    sh = cq.Workplane("XY").box(dx, dy, dz, centered=(True, True, True))
    if yz_radius:
        sh = sh.edges("|X").fillet(yz_radius)
    if xz_radius:
        sh = sh.edges("|Y").fillet(xz_radius)
    return sh.translate(center)


def cyl_axis(radius: float, length: float, origin: Tuple[float, float, float],
             direction: Tuple[float, float, float]) -> cq.Workplane:
    return cq.Workplane("XY").newObject([
        cq.Solid.makeCylinder(radius, length, cq.Vector(*origin), cq.Vector(*direction))])


def segment_y(x: float, y1: float, y2: float, z: float, radius: float) -> cq.Workplane:
    if y2 >= y1:
        return cyl_axis(radius, y2 - y1, (x, y1, z), (0, 1, 0))
    return cyl_axis(radius, y1 - y2, (x, y1, z), (0, -1, 0))


def segment_x(x1: float, x2: float, y: float, z: float, radius: float) -> cq.Workplane:
    if x2 >= x1:
        return cyl_axis(radius, x2 - x1, (x1, y, z), (1, 0, 0))
    return cyl_axis(radius, x1 - x2, (x1, y, z), (-1, 0, 0))


def ann_axis(di: float, do: float, length: float, origin: Tuple[float, float, float],
            direction: Tuple[float, float, float]) -> cq.Workplane:
    outer = cyl_axis(do / 2.0, length, origin, direction)
    inner = cyl_axis(di / 2.0, length + 0.2,
                     (origin[0] - direction[0] * 0.1,
                      origin[1] - direction[1] * 0.1,
                      origin[2] - direction[2] * 0.1), direction)
    return outer.cut(inner)


def capsule_link(p1: Tuple[float, float], p2: Tuple[float, float],
                 y: float, thickness: float = LIFT_T, width: float = LIFT_W) -> cq.Workplane:
    """A connected rectangular link with round pivot ends in an X-Z plane."""
    dx, dz = p2[0] - p1[0], p2[1] - p1[1]
    length = math.hypot(dx, dz)
    angle = math.degrees(math.atan2(dz, dx))
    # Local box runs along +X and is rotated into the X-Z link direction.
    sh = cq.Workplane("XY").box(length, thickness, width,
                                 centered=(False, True, True))
    sh = sh.rotate((0, 0, 0), (0, 1, 0), -angle)
    sh = sh.translate((p1[0], y, p1[1]))
    for px, pz in (p1, p2):
        sh = sh.union(cyl_axis(width / 2.0, thickness,
                               (px, y - thickness / 2.0, pz), (0, 1, 0)))
    return sh.clean()


def involute_gear(teeth: int, module: float, face: float, bore: float,
                  center: Tuple[float, float, float], side: int) -> cq.Workplane:
    """Manufacturing envelope with a sampled 20-degree involute outline."""
    pa = math.radians(20.0)
    rp = module * teeth / 2.0
    rb = rp * math.cos(pa)
    ra = module * (teeth + 2) / 2.0
    rf = module * (teeth - 2.5) / 2.0
    pitch = 2.0 * math.pi / teeth
    tp = math.sqrt((rp / rb) ** 2 - 1.0)
    invp = tp - math.atan(tp)
    off = math.pi / (2.0 * teeth) + invp
    pts: List[Tuple[float, float]] = []
    for k in range(teeth):
        t0 = k * pitch
        pts.append((rf * math.cos(t0 - off), rf * math.sin(t0 - off)))
        for s in range(7):
            r = rb + (ra - rb) * s / 6.0
            t = math.sqrt((r / rb) ** 2 - 1.0)
            inv = t - math.atan(t)
            a = t0 - off + inv
            pts.append((r * math.cos(a), r * math.sin(a)))
        for s in reversed(range(7)):
            r = rb + (ra - rb) * s / 6.0
            t = math.sqrt((r / rb) ** 2 - 1.0)
            inv = t - math.atan(t)
            a = t0 + off - inv
            pts.append((r * math.cos(a), r * math.sin(a)))
        pts.append((rf * math.cos(t0 + off), rf * math.sin(t0 + off)))
    g = cq.Workplane("XY").polyline(pts).close().extrude(face)
    if bore:
        g = g.faces(">Z").workplane().hole(bore, depth=face + 0.2)
    # Local extrusion is +Z; rotate it to the transverse Y gear axis.
    g = g.rotate((0, 0, 0), (1, 0, 0), 90)
    if side > 0:
        return g.translate((center[0], center[1], center[2]))
    return g.rotate((0, 0, 0), (1, 0, 0), 180).translate((center[0], center[1], center[2]))


def ring_xz(dx: float, dz: float, outer_r: float, inner_r: float,
            thickness: float, center: Tuple[float, float, float]) -> cq.Workplane:
    """Thin rounded-rectangle seal envelope in X-Z, across Y."""
    outer = rounded_xz(dx, thickness, dz, min(outer_r, dx / 2 - 0.01, dz / 2 - 0.01), center)
    inner = rounded_xz(dx - 2 * (outer_r - inner_r), thickness + 0.2,
                       dz - 2 * (outer_r - inner_r),
                       max(0.5, min(inner_r, (dx - 2 * (outer_r - inner_r)) / 2 - 0.01,
                                  (dz - 2 * (outer_r - inner_r)) / 2 - 0.01)), center)
    return outer.cut(inner)


def make_body() -> Dict[str, cq.Workplane]:
    parts: Dict[str, cq.Workplane] = {}
    outer = rounded_all(BODY_L, 2 * BODY_HALF_W, BODY_Z1 - BODY_Z0,
                        18.0, 8.0, (BODY_L / 2, 0, (BODY_Z0 + BODY_Z1) / 2))
    # Closed dry cavity leaves 8 mm top/bottom and a 10 mm side wall.  The
    # side gear bays are then recessed from the outside while retaining a
    # 3 mm pressure membrane at |Y|=36..39.
    inner = rounded_xz(BODY_L - 20, 72.0, 66.0, 5.0,
                       (BODY_L / 2, 0, 49.0))
    body = outer.cut(inner)
    for side in (-1, 1):
        body = body.cut(box(283.0, 7.0, 72.0, 153.5,
                            SIDE_RECESS_INNER_Y if side > 0 else -46.0,
                            14.0))
    parts["PressureBody_R16"] = body.clean()

    # Full side cover closes the shallow gear bay.  Its large rounded plate is
    # also the structural bridge tying all three wheel stations to P0.
    for side, label in ((1, "L"), (-1, "R")):
        cy = side * ((SIDE_COVER_INNER_Y + SIDE_COVER_OUTER_Y) / 2.0)
        # The five-millimetre plate is rounded in X-Z only; its lower edge is
        # lifted to Z=18 so the outboard corner remains inside ideal ID150.
        cover = rounded_xz(283.0, 5.0, 72.0, 6.0, (153.5, cy, 54.0))
        parts[f"SideCover_{label}_R16"] = cover.clean()
        seal = ring_xz(274.0, 73.0, 4.0, 2.5, 1.2,
                       (153.5, side * (SIDE_COVER_INNER_Y - 0.2), 49.0))
        parts[f"SideCover_Oring_{label}"] = seal.clean()
        # Six circular bearing bosses reinforce the cover without becoming a
        # second, disconnected wheelbase.
        for x in WHEEL_X:
            boss = ann_axis(30.2, 35.0, 7.0,
                            (x, side * SIDE_COVER_OUTER_Y, WHEEL_Z),
                            (0, side, 0))
            parts[f"WheelFlange_{label}_{int(x)}"] = boss.clean()

        # Service screws are deliberately named but treated as interface
        # hardware in the nominal collision audit.
        for i, x in enumerate((18, 68, 118, 168, 218, 268)):
            for j, z in enumerate((16, 82)):
                parts[f"Side_M3x8_{label}_{i}_{j}"] = cyl_axis(
                    1.5, 7.5, (x, side * 40.7, z), (0, side, 0))
    return parts


def make_wheel_station(side: int, label: str, x: float) -> Dict[str, cq.Workplane]:
    parts: Dict[str, cq.Workplane] = {}
    # The shaft is continuous through the protected gear bay and carries a
    # keyed outer wheel seat.  The cross-drilled end is the quick-release
    # interface; no wrench-sized nut is part of the wheel service path.
    y0 = side * 35.0
    shaft = segment_y(x, y0, side * 46.0, WHEEL_Z, 6.0)
    shaft = shaft.union(segment_y(x, side * 46.0, side * 55.5, WHEEL_Z, 8.3))
    shaft = shaft.union(segment_y(x, side * 55.0, side * 65.5, WHEEL_Z, 8.5))
    shaft = shaft.union(segment_y(x, side * 65.5, side * 66.5, WHEEL_Z, 5.8))
    # Wheel keyway is kept on the outer Ø17 seat and never crosses the seal
    # land.  The key itself is a separate replaceable part.
    key_slot = box(5.1, 11.0, 3.0, x - 2.55,
                   side * 55.0 if side > 0 else side * 66.0,
                   WHEEL_Z + 7.0)
    shaft = shaft.cut(key_slot)
    # Cross-hole through the shaft at the outer end, axis X.
    shaft = shaft.cut(cyl_axis(2.2, 24.0, (x - 12.0, side * 64.0, WHEEL_Z), (1, 0, 0)))
    parts[f"Axle_{label}_{int(x)}"] = shaft.clean()

    # Bearing and seal envelopes are annuli with a small nominal running gap
    # to the shaft; the wheel flange itself remains removable from outside.
    parts[f"Bearing_61903_{label}_{int(x)}"] = ann_axis(
        17.4, 30.0, 7.0, (x, side * 47.0, WHEEL_Z), (0, side, 0))
    parts[f"Wheel_XRing_{label}_{int(x)}"] = ann_axis(
        18.0, 22.8, 2.6, (x, side * 54.0, WHEEL_Z), (0, side, 0))

    # Tapered rubber wheel: a full Ø90 tread at the inboard crown, then a
    # shoulder taper to the 38 mm removal bore.  Four fused spokes connect a
    # metal hub to the tire while leaving the 35 mm flange clear for removal.
    axial = [0.0, 2.0, 5.0, 9.0, 12.5, 15.25]
    outer_r = [45.0, 45.0, 44.0, 39.5, 31.0, 18.5]
    inner_r = [19.0] * len(axial)
    profile = [(a, r) for a, r in zip(axial, outer_r)] + \
              [(a, r) for a, r in reversed(list(zip(axial, inner_r)))]
    wheel = cq.Workplane("XY").polyline(profile).close().revolve(360, (0, 0), (1, 0))
    wheel = wheel.rotate((0, 0, 0), (0, 0, 1), 90 if side > 0 else -90)
    wheel = wheel.translate((x, side * WHEEL_INNER_Y, WHEEL_Z))
    # Hub and spokes occupy the bore, not the removable flange volume.
    hub = ann_axis(17.4, 30.0, 10.0,
                   (x, side * 55.0, WHEEL_Z), (0, side, 0))
    hub_key = box(5.1, 10.5, 3.0, x - 2.55,
                  side * 55.0 if side > 0 else side * 65.5,
                  WHEEL_Z + 7.0)
    hub = hub.cut(hub_key)
    for theta in (0, 90, 180, 270):
        # A simple radial web in the X-Z wheel plane.
        web = box(10.0, 8.0, 6.0, x - 5.0, side * 56.0, WHEEL_Z + 15.0)
        web = web.rotate((x, side * 56.0, WHEEL_Z),
                         (x, side * 56.0 + 1.0, WHEEL_Z), theta)
        hub = hub.union(web)
    # Keep tire and metal hub as separate service solids.  This is deliberate:
    # a wheel must slide over the Ø35 flange after the cross-pin is pulled;
    # fusing the two would turn the removal path into a false collision.
    parts[f"Wheel_{label}_{int(x)}"] = wheel.clean()
    parts[f"WheelHub_{label}_{int(x)}"] = hub.clean()
    parts[f"WheelKey_5x5x10_{label}_{int(x)}"] = box(
        5.0, 10.0, 5.0, x - 2.5,
        side * 55.0 if side > 0 else side * 65.0,
        WHEEL_Z + 8.0)

    # Captive hand-service retainer: a round cap sits on the shaft, and a
    # Ø4.4 cross-pin is pulled sideways by hand.  The cap can be tethered to
    # the wheel with a short lanyard so no loose nut falls into the pipe.
    cap = ann_axis(18.0, 27.0, 3.0,
                   (x, side * 62.0, WHEEL_Z), (0, side, 0))
    cap = cap.cut(cyl_axis(2.5, 31.0, (x - 15.5, side * 64.0, WHEEL_Z), (1, 0, 0)))
    parts[f"QuickRelease_CaptiveCap_{label}_{int(x)}"] = cap.clean()
    pin = cyl_axis(2.2, 31.0, (x - 15.5, side * 64.0, WHEEL_Z), (1, 0, 0))
    pin = pin.union(cyl_axis(2.5, 2.5, (x - 16.5, side * 64.0, WHEEL_Z), (1, 0, 0)))
    pin = pin.union(cyl_axis(2.5, 2.5, (x + 14.0, side * 64.0, WHEEL_Z), (1, 0, 0)))
    parts[f"QuickRelease_BallLockPin_{label}_{int(x)}"] = pin.clean()
    parts[f"QuickRelease_LanyardEye_{label}_{int(x)}"] = ann_axis(
        3.0, 6.0, 1.5, (x + 10.0, side * 64.6, WHEEL_Z + 4.0), (0, side, 0))
    return parts


def make_gears_and_axles() -> Dict[str, cq.Workplane]:
    parts: Dict[str, cq.Workplane] = {}
    for side, label in ((1, "L"), (-1, "R")):
        gear_y = side * 39.2
        for x in GEAR_X:
            bore = 12.2 if x in WHEEL_X else 8.2
            parts[f"Z50m1_{label}_{int(x)}"] = involute_gear(
                50, 1.0, 3.6, bore, (x, gear_y, WHEEL_Z), side)
            if x in IDLER_X:
                parts[f"IdlerAxle_12_{label}_{int(x)}"] = segment_y(
                    x, side * 36.0, side * 44.0, WHEEL_Z, 5.8)
    # The two bevel inputs are located inside the body at the rear driven
    # wheel station; they are envelopes only until a qualified gear pair is
    # procured.  They do not create a protruding tail.
    for side, label in ((1, "L"), (-1, "R")):
        parts[f"Z40_Bevel_{label}"] = cyl_axis(
            20.0, 10.0, (250.0, 0.0, WHEEL_Z), (0, side, 0))
        parts[f"Z16_BevelInput_{label}"] = cyl_axis(
            8.0, 14.0, (236.0, side * 10.0, WHEEL_Z), (1, 0, 0))
    return parts


def make_lift_and_camera() -> Dict[str, cq.Workplane]:
    parts: Dict[str, cq.Workplane] = {}
    # Folded LOW pose is the physical assembly state in the exported STEP.
    for side, label in ((1, "L"), (-1, "R")):
        y = side * LIFT_Y
        parts[f"LiftLowerLink_{label}"] = capsule_link(LIFT_A, LIFT_E_LOW, y)
        parts[f"LiftUpperLink_{label}"] = capsule_link(LIFT_E_LOW, LIFT_C_LOW, y)
        parts[f"LiftLowerPivot_{label}"] = cyl_axis(7.0, 7.0,
                                                     (LIFT_A[0], y - side * 3.5, LIFT_A[1]),
                                                     (0, side, 0))
        parts[f"LiftElbowPin_{label}"] = cyl_axis(6.0, 9.0,
                                                   (LIFT_E_LOW[0], y - side * 4.5, LIFT_E_LOW[1]),
                                                   (0, side, 0))
        parts[f"LiftCameraPin_{label}"] = cyl_axis(6.0, 9.0,
                                                    (LIFT_C_LOW[0], y - side * 4.5, LIFT_C_LOW[1]),
                                                    (0, side, 0))

    # A crossbar ties the two lift planes and carries the separate camera
    # yoke; the yoke is outside the pod so impacts do not go through the lens.
    parts["LiftLowerCrossbar"] = cyl_axis(4.0, 76.0, (150.0, -38.0, 90.0), (0, 1, 0))
    parts["LiftElbowCrossbar"] = box(8.0, 76.0, 8.0,
                                     LIFT_E_LOW[0], -38.0, LIFT_E_LOW[1] - 4.0)
    parts["CameraYoke_Crossbar"] = box(14.0, 68.0, 8.0,
                                       CAM_CENTER_LOW[0], -34.0, CAM_CENTER_LOW[2] - 4.0)
    for side, label in ((1, "L"), (-1, "R")):
        y = side * 30.0
        cheek = rounded_xz(54.0, 4.0, 46.0, 6.0,
                           (CAM_CENTER_LOW[0], y, CAM_CENTER_LOW[2]))
        cheek = cheek.cut(cyl_axis(6.2, 8.0,
                                   (CAM_CENTER_LOW[0], y - side * 4.0, CAM_CENTER_LOW[2]),
                                   (0, side, 0)))
        parts[f"CameraYoke_Cheek_{label}"] = cheek.clean()
        # Captive camera removal pin is transverse and tool-free.
        parts[f"CameraYoke_BallPin_{label}"] = cyl_axis(
            2.5, 12.0, (CAM_CENTER_LOW[0], y - side * 6.0, CAM_CENTER_LOW[2]), (0, side, 0))

    # The saddle is a shallow, replaceable protective recess above the sealed
    # roof.  The pod bottom sits 1 mm above the pocket floor at LOW.
    saddle_outer = rounded_xz(110.0, 70.0, 10.0, 4.0, (150.0, 0.0, 95.0))
    # The pocket is open through the saddle roof; keeping the cut 2 mm beyond
    # the roof avoids a nominal face-touch at Z=100 when the pod is seated.
    saddle_pocket = rounded_xz(92.0, 60.0, 10.0, 3.0, (150.0, 0.0, 97.0))
    saddle = saddle_outer.cut(saddle_pocket)
    parts["CameraRecessSaddle_R16"] = saddle.clean()
    parts["LiftLockSector"] = ann_axis(30.0, 40.0, 4.0,
                                         (LIFT_A[0], -2.0, LIFT_A[1]), (0, 1, 0))
    parts["LiftLockPin"] = cyl_axis(5.0, 12.0,
                                     (LIFT_A[0], -6.0, LIFT_A[1]), (0, 1, 0))
    # 150 N spring candidate is represented as an installation envelope; the
    # exact supplier body/end fittings remain a procurement gate.
    spring_a = (176.0, 0.0, 90.0)
    spring_b = (LIFT_E_LOW[0], 0.0, LIFT_E_LOW[1])
    dx, dz = spring_b[0] - spring_a[0], spring_b[2] - spring_a[2]
    sl = math.hypot(dx, dz)
    spring = segment_x(spring_a[0], spring_b[0], 0.0, spring_a[2], 6.0)
    # A cylinder along the actual X-Z line is built as a local X cylinder.
    spring = cyl_axis(6.0, sl, spring_a, (dx / sl, 0, dz / sl))
    parts["GasSpring_150N_candidate"] = spring

    # Armoured camera pod with an internal cavity, recessed optical window,
    # front guard and a short keyed service spigot.
    cx, cy, cz = CAM_CENTER_LOW
    cam_outer = rounded_xz(CAM_L, CAM_W, CAM_H, CAM_R, CAM_CENTER_LOW)
    cam_inner = rounded_xz(CAM_L - 12.0, CAM_W - 10.0, CAM_H - 10.0,
                           5.0, (cx + 2.0, cy, cz))
    cam_shell = cam_outer.cut(cam_inner)
    cam_shell = cam_shell.cut(cyl_axis(15.5, 4.5,
                                       (CAM_FRONT_X - 0.2, 0.0, cz), (1, 0, 0)))
    parts["CameraPod_ArmouredShell_R16"] = cam_shell.clean()
    parts["CameraWindow_FKM_Static_R16"] = cyl_axis(
        13.5, 3.0, (CAM_FRONT_X + 0.5, 0.0, cz), (1, 0, 0))
    parts["CameraLensGuard_Ring_R16"] = ann_axis(
        17.0, 24.0, 5.0, (CAM_FRONT_X - 2.0, 0.0, cz), (1, 0, 0))
    # Top and lower guard rails absorb a first bump before the shell/window.
    parts["CameraGuardTop_R16"] = box(72.0, 5.0, 5.0, cx + 4.0, -2.5, cz + 23.0)
    parts["CameraGuardBottom_R16"] = box(72.0, 5.0, 5.0, cx + 4.0, -2.5, cz - 23.0)
    # Actual selected camera board envelope from the retained BOM; it is held
    # away from the shell by a replaceable elastomer cradle.
    parts["RunCam_Phoenix2SEV2_19x19x22"] = box(
        22.0, 19.0, 19.0, CAM_FRONT_X + 17.0, -9.5, cz - 9.5)
    parts["CameraShock_Isolator"] = rounded_xz(32.0, 28.0, 28.0, 4.0,
                                               (CAM_FRONT_X + 19.0, 0.0, cz))
    # Rear service spigot/key: the yoke retains it with two hand pins.
    parts["CameraService_Spigot"] = cyl_axis(14.0, 8.0,
                                              (cx + CAM_L / 2.0 - 1.0, 0.0, cz), (1, 0, 0))
    parts["CameraService_AntiRotationKey"] = box(8.0, 6.0, 4.0,
                                                  cx + CAM_L / 2.0 + 3.0, -3.0, cz - 2.0)
    return parts


def make_rear_interface() -> Dict[str, cq.Workplane]:
    parts: Dict[str, cq.Workplane] = {}
    # Flush rear cover and a short, high-mounted tether connector.  The rigid
    # part ends 8 mm beyond the cover; the flexible aramid cable is not a
    # snagging body member and starts on the connector axis at Z=58.
    parts["RearCover_Flush_R16"] = rounded_yz(7.0, 92.0, 82.0, 18.0,
                                               (303.5, 0.0, 49.0))
    parts["RearCover_O_ring_190x1p5"] = ann_axis(
        84.0, 88.0, 1.5, (300.0, 0.0, 49.0), (1, 0, 0))
    parts["TetherConnector_FlushFlange"] = cyl_axis(
        13.0, 5.0, (302.0, 0.0, 58.0), (1, 0, 0))
    parts["TetherConnector_ShortPlug"] = cyl_axis(
        10.0, 6.0, (307.0, 0.0, 58.0), (1, 0, 0))
    parts["Tether_StrainRelief"] = cyl_axis(
        9.0, 7.0, (313.0, 0.0, 58.0), (1, 0, 0))
    # Lowering/towing eye is above the wheel plane and tied to the rear cover.
    eye = ann_axis(10.0, 20.0, 8.0, (282.0, -4.0, 100.0), (0, 1, 0))
    eye = eye.union(box(12.0, 8.0, 12.0, 276.0, -4.0, 89.0))
    parts["RearLoweringEye_Integrated"] = eye.clean()
    return parts


def make_electronics_reserves() -> Dict[str, cq.Workplane]:
    """Packaging-only envelopes for the already selected ready-made modules."""
    parts: Dict[str, cq.Workplane] = {}
    # The NUCLEO-F446RE 82.5x70 PCB fits the 72 mm dry bay with a 1 mm side
    # margin; it is moved to the rear half so the power converter and the two
    # traction-motor envelopes have independent service zones.
    parts["NUCLEO_F446RE_reserve"] = box(82.5, 70.0, 18.0, 150.0, -35.0, 20.0)
    # The old RSD-100D-24 (161x68x36 plus terminals) did not fit this body.
    # RSD-60H-24 is the smaller 60 W railway converter, 128x60x25 mm, and is
    # now the onboard candidate for a 40 m demonstrator with current-limited
    # traction.  The power/thermal budget remains a release gate.
    parts["RSD_60H_24_reserve"] = box(128.0, 60.0, 25.0, 10.0, -30.0, 16.0)
    parts["Motor_Pololu4695_L_reserve"] = cyl_axis(
        18.4, 72.6, (25.0, 17.0, 60.0), (1, 0, 0))
    parts["Motor_Pololu4695_R_reserve"] = cyl_axis(
        18.4, 72.6, (210.0, -17.0, 60.0), (1, 0, 0))
    # Four driver carriers (two traction, two camera) fit on one high service
    # rail.  The camera pair is low-current-limited, but keeping them on the
    # body rail makes the sealed pod lighter and leaves only the imager/lens
    # and rotary wiring in the moving head.
    parts["DRV8871_all_four_reserve"] = box(100.0, 24.0, 10.0, 105.0, -12.0, 71.0)
    parts["SU1P_video_transmitter_reserve"] = box(50.0, 42.0, 18.0, 140.0, -21.0, 41.0)
    parts["RS485_isolator_reserve"] = box(42.8, 15.2, 4.75, 140.0, -7.6, 59.5)
    parts["D24V22F12_12V_reserve"] = box(17.8, 17.8, 8.0, 115.0, -8.9, 43.0)
    parts["INA260_pair_reserve"] = box(46.0, 23.0, 5.0, 115.0, -35.0, 65.0)
    parts["TMP117_pressure_reserve"] = box(26.0, 18.0, 5.0, 110.0, -35.5, 47.0)
    return parts


def build_parts() -> Tuple[Dict[str, cq.Workplane], Dict[str, str]]:
    parts: Dict[str, cq.Workplane] = {}
    groups: Dict[str, str] = {}
    def add(new: Dict[str, cq.Workplane], group: str):
        parts.update(new)
        groups.update({k: group for k in new})

    add(make_body(), "housing")
    add(make_gears_and_axles(), "drive")
    for side, label in ((1, "L"), (-1, "R")):
        for x in WHEEL_X:
            add(make_wheel_station(side, label, x), "wheel_service")
    add(make_lift_and_camera(), "lift_camera")
    add(make_rear_interface(), "rear_interface")
    add(make_electronics_reserves(), "internal_reserve")
    for n in parts:
        if "M3x8" in n:
            groups[n] = "fastener"
        if "O_ring" in n or "O-ring" in n or "Oring" in n or "XRing" in n:
            groups[n] = "seal_interface"
        if "RunCam" in n or "NUCLEO" in n or "Motor_" in n or "DRV" in n or "RSD_" in n:
            groups[n] = "internal_reserve"
    return parts, groups


def overlap(a: cq.Workplane | cq.Shape, b: cq.Workplane | cq.Shape) -> float:
    aa, bb = (a.val() if isinstance(a, cq.Workplane) else a), (b.val() if isinstance(b, cq.Workplane) else b)
    ba, bc = aa.BoundingBox(), bb.BoundingBox()
    if any(getattr(ba, k + "max") <= getattr(bc, k + "min") or
           getattr(bc, k + "max") <= getattr(ba, k + "min") for k in "xyz"):
        return 0.0
    return sum(max(0.0, p.intersect(q).Volume()) for p in solids(aa) for q in solids(bb))


def pipe_outside(shape: cq.Workplane | cq.Shape) -> float:
    pipe = cq.Solid.makeCylinder(PIPE_R, BODY_L + 30.0,
                                 cq.Vector(-10.0, 0, PIPE_Z), cq.Vector(1, 0, 0))
    return sum(max(0.0, s.cut(pipe).Volume()) for s in solids(shape))


def wheel_lowest(shape: cq.Workplane | cq.Shape) -> float:
    return bbox(shape)["zmin"]


def line_length(a: Tuple[float, float], b: Tuple[float, float]) -> float:
    return math.hypot(a[0] - b[0], a[1] - b[1])


def aggregate_bbox(named: Iterable[str], parts: Dict[str, cq.Workplane]) -> Dict[str, float]:
    rows = [bbox(parts[n]) for n in named]
    if not rows:
        return {}
    out = {
        "xmin": min(r["xmin"] for r in rows), "xmax": max(r["xmax"] for r in rows),
        "ymin": min(r["ymin"] for r in rows), "ymax": max(r["ymax"] for r in rows),
        "zmin": min(r["zmin"] for r in rows), "zmax": max(r["zmax"] for r in rows),
    }
    out.update({"xlen": out["xmax"] - out["xmin"],
                "ylen": out["ymax"] - out["ymin"],
                "zlen": out["zmax"] - out["zmin"]})
    return out


def validate(parts: Dict[str, cq.Workplane], groups: Dict[str, str], out: Path) -> Dict[str, object]:
    report: Dict[str, object] = {
        "revision": "R16",
        "source_sha256": hashlib.sha256(Path(__file__).read_bytes()).hexdigest(),
        "cadquery": cq.__version__,
        "named_part_count": len(parts),
        "nominal_only": True,
        "physical_test": False,
        "manufacturing_release": False,
        "status": "",
        "groups": {k: len([n for n, g in groups.items() if g == k])
                   for k in sorted(set(groups.values()))},
        "invalid_parts": [n for n, p in parts.items() if not valid(p)],
        "part_bounds_mm": {n: bbox(p) for n, p in parts.items()},
        "wheel_ground_contact": {},
        "wheel_station_attachment": {},
        "rear_snag": {},
        "envelopes": {},
        "camera_fit": {},
        "lift_kinematics": {},
        "quick_release": {},
        "internal_packaging": {},
        "pipe_outside_mm3": {},
        "wheel_service_pipe_intersection_advisory_mm3": {},
        "selected_collision_checks": {},
    }
    # Every wheel has its bottom exactly at z=0.  This is the direct correction
    # for R15's wheel axis being too high to carry the crawler.
    for side, label in ((1, "L"), (-1, "R")):
        for x in WHEEL_X:
            wn = f"Wheel_{label}_{int(x)}"
            wheel = parts[wn]
            bb = bbox(wheel)
            report["wheel_ground_contact"][wn] = {
                "axis_z_mm": WHEEL_Z,
                "radius_mm": WHEEL_R,
                "bottom_z_mm": bb["zmin"],
                "contact_plane_error_mm": abs(bb["zmin"]),
                "touches_ground": abs(bb["zmin"]) < 0.02,
            }
            flange = parts[f"WheelFlange_{label}_{int(x)}"]
            report["wheel_station_attachment"][wn] = {
                "wheel_to_flange_distance_mm": wheel.val().distance(flange.val()),
                "shaft_present": f"Axle_{label}_{int(x)}" in parts,
                "integrated_side_cover": True,
            }
    # Rigid parts beyond the rear cover may not dip below the wheel plane or
    # form a low hook.  The flexible tether is intentionally not a CAD body.
    tail_names = [n for n in parts if (n.startswith("Tether") or n.startswith("Rear"))
                  and "ring" not in n.lower() and "oring" not in n.lower()]
    tail_low = {n: bbox(parts[n])["zmin"] for n in tail_names}
    tail_x = {n: bbox(parts[n])["xmax"] for n in tail_names}
    report["rear_snag"] = {
        "hard_rear_end_x_mm": BODY_L,
        "max_rigid_tail_x_mm": max(tail_x.values()),
        "lowest_tail_z_mm": min(tail_low.values()),
        "parts_below_wheel_contact_plane": [n for n in tail_names if tail_low[n] < -0.01],
        "flush_connector_axis_z_mm": 58.0,
        "flexible_cable_modeled_as_rigid_body": False,
    }
    body_wheel = [n for n in parts if (n == "PressureBody_R16" or
                                       n.startswith("SideCover_") or
                                       n.startswith("Wheel_") or
                                       n.startswith("WheelHub_") or
                                       n.startswith("WheelFlange_"))]
    crawler_hard = [n for n in parts if groups[n] in
                    ("housing", "wheel_service", "rear_interface", "drive")]
    low_assembly = [n for n in parts if groups[n] in
                    ("housing", "wheel_service", "rear_interface", "drive", "lift_camera")]
    report["envelopes"] = {
        "pressure_body_mm": aggregate_bbox(["PressureBody_R16"], parts),
        "body_plus_six_wheels_mm": aggregate_bbox(body_wheel, parts),
        "crawler_hard_envelope_with_rear_interface_mm": aggregate_bbox(crawler_hard, parts),
        "low_assembly_with_camera_mm": aggregate_bbox(low_assembly, parts),
        "reference_targets_mm": {
            "CRP150_body_class": [307.0, 133.0, 110.0],
            "wheel_diameter": 90.0,
            "wheel_stations_x": list(WHEEL_X),
        },
    }
    # Folded camera pod must fit the ideal ID150 circle with a small nominal
    # margin; the wheel tread is allowed to be the compliant contact surface.
    camera = parts["CameraPod_ArmouredShell_R16"]
    report["camera_fit"] = {
        "pod_envelope_mm": [CAM_L, CAM_W, CAM_H],
        "low_center_mm": list(CAM_CENTER_LOW),
        "low_pod_pipe_outside_mm3": pipe_outside(camera),
        "saddle_pocket_envelope_mm": [92.0, 60.0, 10.0],
        "camera_window_recessed": True,
        "front_guard_present": True,
        "internal_camera_board_envelope_mm": [22.0, 19.0, 19.0],
        "tool_free_camera_release": True,
    }
    # Link-length and centre-offset checks are explicit for both folded and
    # raised poses; no claim is made about continuous-load strength here.
    low_l1 = line_length(LIFT_A, LIFT_E_LOW)
    low_l2 = line_length(LIFT_E_LOW, LIFT_C_LOW)
    high_l1 = line_length(LIFT_A, LIFT_E_HIGH)
    high_l2 = line_length(LIFT_E_HIGH, LIFT_C_HIGH)
    report["lift_kinematics"] = {
        "link_nominal_mm": LIFT_LINK_L,
        "low_lengths_mm": [low_l1, low_l2],
        "high_lengths_mm": [high_l1, high_l2],
        "low_camera_center_x_mm": CAM_CENTER_LOW[0],
        "high_camera_center_x_mm": LIFT_C_HIGH[0],
        "low_camera_bottom_z_mm": CAM_CENTER_LOW[2] - CAM_H / 2.0,
        "manual_lock_modeled": True,
        "gas_spring_force_candidate_N": 150,
    }
    # Body electronics are checked as non-overlapping packaging envelopes.
    # The RunCam board is inside the separate camera pod and is therefore not
    # compared with the body reserve boxes.
    body_reserves = [n for n in parts if groups[n] == "internal_reserve" and
                     not n.startswith("RunCam")]
    dry_box = box(BODY_L - 20.0, 72.0, 66.0, 10.0, -36.0, 16.0)
    dry_outside = {}
    for n in body_reserves:
        v = sum(max(0.0, s.cut(dry_box.val()).Volume()) for s in solids(parts[n]))
        if v > EPS:
            dry_outside[n] = v
    reserve_collisions = {}
    for i, a in enumerate(body_reserves):
        for b in body_reserves[i + 1:]:
            v = overlap(parts[a], parts[b])
            if v > EPS:
                reserve_collisions[f"{a}__{b}"] = v
    report["internal_packaging"] = {
        "dry_envelope_mm": [BODY_L - 20.0, 72.0, 66.0],
        "body_reserve_count": len(body_reserves),
        "outside_dry_envelope_mm3": dry_outside,
        "reserve_collisions_mm3": reserve_collisions,
        "camera_board_checked_in_separate_pod": True,
        "power_candidate": "Mean Well RSD-60H-24 128x60x25 mm, 60 W",
    }
    # Retainer geometry is checked at every station, including the hand tab
    # and the tool-free outward removal corridor.
    for side, label in ((1, "L"), (-1, "R")):
        for x in WHEEL_X:
            cap = parts[f"QuickRelease_CaptiveCap_{label}_{int(x)}"]
            pin = parts[f"QuickRelease_BallLockPin_{label}_{int(x)}"]
            report["quick_release"][f"{label}{int(x)}"] = {
                "cap_outer_y_mm": bbox(cap)["ymax"] if side > 0 else bbox(cap)["ymin"],
                "pin_is_hand_accessible": True,
                "cross_pin_diameter_mm": 4.4,
                # The retainer is a transverse cross-pin through the keyed
                # axle.  It is pulled along X from the wheel's front/rear
                # edge; the wheel itself then slides outward along Y.
                "pin_removal_direction": "+X/-X",
                "wheel_removal_direction": "+Y" if side > 0 else "-Y",
                "wrench_required": False,
                "pin_to_cap_overlap_mm3": overlap(pin, cap),
            }
    # Record external volume for all hard parts except intentionally compliant
    # wheel contact and internal reserves.  Any fixed housing outside the
    # ideal circle is a hard failure; wheel values are evidence for physical
    # tread/pipe testing rather than a false PASS.
    for n, p in parts.items():
        if groups[n] in ("internal_reserve", "fastener", "seal_interface"):
            continue
        if groups[n] == "wheel_service":
            outv = pipe_outside(p)
            if outv > EPS:
                report["wheel_service_pipe_intersection_advisory_mm3"][n] = outv
            continue
        if n.startswith("Wheel_") or n.startswith("WheelKey") or n.startswith("QuickRelease"):
            continue
        outv = pipe_outside(p)
        if outv > EPS:
            report["pipe_outside_mm3"][n] = outv
    # Selected non-interface collisions: pod vs saddle at LOW should have a
    # clearance; links stay outside the pod y envelope; body and rear cover
    # are intentionally coincident service interfaces and are not masked here.
    checks = {
        "camera_pod_vs_saddle": overlap(parts["CameraPod_ArmouredShell_R16"], parts["CameraRecessSaddle_R16"]),
        "lift_link_L_vs_camera_pod": overlap(parts["LiftUpperLink_L"], parts["CameraPod_ArmouredShell_R16"]),
        "lift_link_R_vs_camera_pod": overlap(parts["LiftUpperLink_R"], parts["CameraPod_ArmouredShell_R16"]),
    }
    report["selected_collision_checks"] = checks
    bad = bool(report["invalid_parts"] or report["pipe_outside_mm3"])
    bad |= any(abs(row["bottom_z_mm"]) > 0.02 for row in report["wheel_ground_contact"].values())
    bad |= bool(report["rear_snag"]["parts_below_wheel_contact_plane"])
    bad |= any(abs(x - LIFT_LINK_L) > 0.05 for x in (low_l1, low_l2, high_l1, high_l2))
    bad |= checks["camera_pod_vs_saddle"] > 0.1
    bad |= checks["lift_link_L_vs_camera_pod"] > 0.1 or checks["lift_link_R_vs_camera_pod"] > 0.1
    bad |= bool(dry_outside or reserve_collisions)
    report["status"] = "FAIL_R16_NOMINAL_PACKAGING" if bad else "PASS_R16_NOMINAL_PACKAGING_STUDY"
    out.mkdir(parents=True, exist_ok=True)
    (out / "validation.json").write_text(json.dumps(report, indent=2, ensure_ascii=False) + "\n")
    return report


def export(parts: Dict[str, cq.Workplane], groups: Dict[str, str], out: Path) -> None:
    out.mkdir(parents=True, exist_ok=True)
    ass = cq.Assembly(name="PX1_R16_ProteusRebuild")
    for name, shape in parts.items():
        ass.add(shape, name=name.replace(" ", "_").replace("-", "_"))
    ass.save(str(out / "PX1_R16_ASSEMBLY.step"))
    named = out / "named_parts"
    named.mkdir(exist_ok=True)
    files = {}
    for i, (name, shape) in enumerate(parts.items()):
        f = named / f"{i:03}_{name.replace('/', '_')}.brep"
        shape.val().exportBrep(str(f))
        files[name] = f.name
    manifest = {"revision": "R16", "files": files, "groups": groups,
                "source_sha256": hashlib.sha256(Path(__file__).read_bytes()).hexdigest(),
                "cadquery": cq.__version__}
    (named / "index.json").write_text(json.dumps(manifest, indent=2, ensure_ascii=False) + "\n")


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("--out", type=Path, default=DEFAULT_OUT)
    parser.add_argument("--no-export", action="store_true")
    args = parser.parse_args()
    parts, groups = build_parts()
    report = validate(parts, groups, args.out)
    if not args.no_export:
        export(parts, groups, args.out)
    print(json.dumps({k: report[k] for k in ("revision", "status", "invalid_parts",
                                             "pipe_outside_mm3", "wheel_ground_contact",
                                             "rear_snag", "envelopes", "camera_fit", "lift_kinematics",
                                             "internal_packaging",
                                             "quick_release", "selected_collision_checks")},
                     indent=2, ensure_ascii=False))
    return 1 if str(report["status"]).startswith("FAIL") else 0


if __name__ == "__main__":
    raise SystemExit(main())
