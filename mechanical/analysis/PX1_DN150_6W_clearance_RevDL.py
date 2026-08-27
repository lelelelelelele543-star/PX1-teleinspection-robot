#!/usr/bin/env python3
"""PX-1 Rev.DL DN150 cross-section checker.

The crawler settles until the lower wheel crowns contact the pipe. The script
therefore solves the pipe-axis height from the wheel profile first, then checks
body/cover clearance. Wheel contact is expected and is not treated as a failure.
"""
import math

PIPE_R = 75.0
WHEEL_AXIS_Z = 45.0
BODY_HALF_W = 46.0
BODY_Z_MIN = 14.0
BODY_Z_MAX = 90.0
COVER_OUTER_Y = 51.0
COVER_Z_MIN = 4.0
COVER_Z_MAX = 86.0

# Positive-side external wheel profile, mirrored on the other side.
# (Y, local radius from wheel axis)
PROFILE = [
    (51.0, 45.0),
    (54.0, 45.0),
    (67.0, 21.0),
]


def profile_samples(n_per_segment=10000):
    for (y0, r0), (y1, r1) in zip(PROFILE[:-1], PROFILE[1:]):
        for i in range(n_per_segment + 1):
            t = i / n_per_segment
            yield y0 + (y1-y0)*t, r0 + (r1-r0)*t


def solve_pipe_axis_z():
    """Highest pipe center compatible with all lower wheel points.

    At equilibrium one or more tread points contact the lower wall.
    """
    best = (float('inf'), None, None)
    for y, r in profile_samples():
        if abs(y) >= PIPE_R:
            continue
        zp_limit = WHEEL_AXIS_Z - r + math.sqrt(PIPE_R**2 - y**2)
        if zp_limit < best[0]:
            best = (zp_limit, y, r)
    return best


def radial_clearance(y, z_abs, pipe_z):
    return PIPE_R - math.hypot(y, z_abs - pipe_z)


def rectangular_envelope_clearance(y_abs, zmin, zmax, pipe_z):
    return min(
        radial_clearance(y, z, pipe_z)
        for y in (-y_abs, y_abs)
        for z in (zmin, zmax)
    )


if __name__ == '__main__':
    pipe_z, contact_y, contact_r = solve_pipe_axis_z()
    body_c = rectangular_envelope_clearance(BODY_HALF_W, BODY_Z_MIN, BODY_Z_MAX, pipe_z)
    cover_c = rectangular_envelope_clearance(COVER_OUTER_Y, COVER_Z_MIN, COVER_Z_MAX, pipe_z)

    print(f'Solved DN150 pipe-axis Z: {pipe_z:.3f} mm')
    print(f'Wheel contact: |Y|={contact_y:.3f} mm, local radius={contact_r:.3f} mm')
    print(f'Body rectangular-envelope min radial clearance: {body_c:.3f} mm')
    print(f'Side-cover rectangular-envelope min radial clearance: {cover_c:.3f} mm')

    min_nonwheel = min(body_c, cover_c)
    if min_nonwheel >= 4.5:
        print(f'PASS: non-wheel nominal clearance {min_nonwheel:.3f} mm >= 4.5 mm')
    elif min_nonwheel >= 3.0:
        print(f'MARGINAL PASS: {min_nonwheel:.3f} mm >=3.0 mm but below preferred 4.5 mm')
    else:
        print(f'FAIL: non-wheel clearance {min_nonwheel:.3f} mm <3.0 mm')
