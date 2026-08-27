import math
import numpy as np

# PX-1 Rev.DG — manual lift / DN150 camera clearance checker
# This is a deterministic geometry check, not a production drawing.

PIPE_R = 75.0
PIPE_AXIS_Z = 45.0
CAM_R = 26.0
CAM_L = 72.0
TILT_MIN = -105
TILT_MAX = 105
TILT_STEP = 2

# CRP150-style folding manual parallelogram candidate.
BASE_MID_X = 235.0
BASE_Z = 65.0
ARM_L = 135.0
CAM_X_OFFSET = -36.0

POSITIONS = {
    'LOW': 182.0,
    'DN150_SAFE': 178.0,
    'HIGH': 90.0,
}

def camera_axis(theta_deg):
    t = math.radians(theta_deg)
    x = BASE_MID_X + ARM_L * math.cos(t) + CAM_X_OFFSET
    z = BASE_Z + ARM_L * math.sin(t)
    return x, z

def max_pipe_radial(zc, tilt_deg):
    """Numerically sample the complete Ø52x72 camera cylinder.
    Pipe axis is X, so only Y/Z radial distance matters.
    """
    a = math.radians(tilt_deg)
    worst = 0.0
    # cylinder axis d=(cos(a),0,sin(a)); perpendicular basis
    # n1=(0,1,0), n2=(-sin(a),0,cos(a))
    for s in np.linspace(-CAM_L/2.0, CAM_L/2.0, 73):
        for ph in np.linspace(0, 2*math.pi, 181):
            y = CAM_R * math.sin(ph)
            z = zc + s*math.sin(a) + CAM_R*math.cos(ph)*math.cos(a)
            radial = math.hypot(y, z - PIPE_AXIS_Z)
            worst = max(worst, radial)
    return worst

for name, theta in POSITIONS.items():
    x, z = camera_axis(theta)
    if name != 'HIGH':
        worst = max(max_pipe_radial(z, t)
                    for t in range(TILT_MIN, TILT_MAX + 1, TILT_STEP))
        clearance = PIPE_R - worst
        print(name, 'theta', theta,
              'axis X/Z', round(x,2), round(z,2),
              'worst radial', round(worst,3),
              'clearance', round(clearance,3))
        assert clearance >= 3.0
    else:
        print(name, 'theta', theta,
              'axis X/Z', round(x,2), round(z,2),
              'DN150 mechanically blocked')

# Find maximum camera-axis Z that still keeps >=3 mm camera-to-pipe clearance
# across the full TILT sweep.
lo, hi = PIPE_AXIS_Z, 100.0
for _ in range(40):
    mid = (lo + hi) / 2.0
    worst = max(max_pipe_radial(mid, t)
                for t in range(TILT_MIN, TILT_MAX + 1, TILT_STEP))
    if PIPE_R - worst >= 3.0:
        lo = mid
    else:
        hi = mid

print('DN150 max axis Z for >=3 mm clearance:', round(lo,3), 'mm')
print('PASS')
