#!/usr/bin/env python3
"""PX-1 Rev.DL DN150 transverse cross-section sanity checker.

No CAD dependency. Checks body/cover corner envelopes and the current tapered
90 mm wheel profile against an ideal DN150 circle.
"""
import math

PIPE_R = 75.0
PIPE_AXIS_Z = 45.0
BODY_HALF_W = 46.0
BODY_Z_MIN = 14.0
BODY_Z_MAX = 90.0
COVER_OUTER_Y = 51.0
COVER_Z_MIN = 4.0
COVER_Z_MAX = 86.0

# Positive side wheel envelope; opposite side is mirrored.
# Full-diameter crown then tapered outer shoulder.
PROFILE = [
    (51.0, 45.0),
    (54.0, 45.0),
    (67.0, 21.0),
]


def radial(y, z_abs):
    return math.hypot(y, z_abs - PIPE_AXIS_Z)


def pipe_clearance(y, wheel_radius):
    return PIPE_R - math.hypot(y, wheel_radius)


def body_corner_clearance():
    vals = []
    for y in (-BODY_HALF_W, BODY_HALF_W):
        for z in (BODY_Z_MIN, BODY_Z_MAX):
            vals.append(PIPE_R - radial(y, z))
    return min(vals)


def cover_corner_clearance():
    vals = []
    for y in (-COVER_OUTER_Y, COVER_OUTER_Y):
        for z in (COVER_Z_MIN, COVER_Z_MAX):
            vals.append(PIPE_R - radial(y, z))
    return min(vals)


def wheel_profile_clearance(samples=20001):
    worst = (1e9, None, None)
    for (y0, r0), (y1, r1) in zip(PROFILE[:-1], PROFILE[1:]):
        for i in range(samples // (len(PROFILE)-1)):
            t = i / max(1, (samples // (len(PROFILE)-1) - 1))
            y = y0 + (y1-y0)*t
            r = r0 + (r1-r0)*t
            c = pipe_clearance(y, r)
            if c < worst[0]:
                worst = (c, y, r)
    return worst


if __name__ == '__main__':
    bc = body_corner_clearance()
    cc = cover_corner_clearance()
    wc, wy, wr = wheel_profile_clearance()
    print(f'Body corner min clearance: {bc:.3f} mm')
    print(f'Cover corner min clearance: {cc:.3f} mm')
    print(f'Wheel-profile min clearance: {wc:.3f} mm at Y={wy:.3f}, r={wr:.3f}')
    print(f'Overall transverse nominal minimum: {min(bc,cc,wc):.3f} mm')
    if min(bc,cc,wc) >= 4.5:
        print('PASS: current transverse design target >= 4.5 mm')
    elif min(bc,cc,wc) >= 3.0:
        print('MARGINAL PASS: >=3.0 mm but below preferred 4.5 mm')
    else:
        print('FAIL: below 3.0 mm')
