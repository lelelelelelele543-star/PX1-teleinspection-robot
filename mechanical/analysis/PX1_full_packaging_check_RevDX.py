#!/usr/bin/env python3
import math

PIPE_R = 75.0
PIPE_Z = 52.0480547
BODY_HALF_W = 46.0
BODY_Z0 = 8.0
BODY_Z1 = 90.0
COVER_Y = 51.0
COVER_Z0 = 5.0
COVER_Z1 = 86.0
MOTOR_R = 18.5
MOTOR_Y = 19.0
BEVEL_R = 68.18/2.0
BEVEL_Z = 45.0
BEVEL_X = 150.0
BODY_X0 = 0.0
BODY_X1 = 307.0
CAM_R = 26.0
CAM_LEN = 72.0
CAM_X = 64.1
CAM_Z = 75.0
TILT_MIN = -105
TILT_MAX = 105
WHEEL_PROFILE = [(51.0,45.0),(54.0,45.0),(67.0,21.0)]


def radial_clearance(y,z):
    return PIPE_R-math.hypot(y,z-PIPE_Z)


def corner_clearance(ymax,z0,z1):
    return min(radial_clearance(y,z) for y in (-ymax,ymax) for z in (z0,z1))


def wheel_noncontact_clearance(samples=10000):
    # Checks the non-contact shoulder against ideal DN150. The traction crown is intentional contact.
    worst=1e9
    where=None
    for (y0,r0),(y1,r1) in zip(WHEEL_PROFILE[:-1],WHEEL_PROFILE[1:]):
        for i in range(samples//2):
            t=i/(samples//2-1)
            y=y0+(y1-y0)*t
            r=r0+(r1-r0)*t
            c=PIPE_R-math.hypot(y,r + 45.0 - PIPE_Z)
            if c<worst:
                worst=c; where=(y,r)
    return worst,where


def camera_sweep(step_deg=1):
    # Sample cylindrical head tilted in X-Z. Cross-section plane remains normal to camera axis.
    worst=1e9; worst_angle=None
    half=CAM_LEN/2
    for deg in range(TILT_MIN,TILT_MAX+1,step_deg):
        a=math.radians(deg)
        sa,ca=math.sin(a),math.cos(a)
        for i in range(73):
            s=-half + CAM_LEN*i/72
            zc=CAM_Z+s*sa
            for j in range(72):
                phi=2*math.pi*j/72
                y=CAM_R*math.sin(phi)
                z=zc+CAM_R*ca*math.cos(phi)
                c=PIPE_R-math.hypot(y,z-PIPE_Z)
                if c<worst:
                    worst=c; worst_angle=deg
    return worst,worst_angle


def main():
    body=corner_clearance(BODY_HALF_W,BODY_Z0,BODY_Z1)
    cover=corner_clearance(COVER_Y,COVER_Z0,COVER_Z1)
    motor_gap=2*MOTOR_Y-2*MOTOR_R
    wall_gap=BODY_HALF_W-(MOTOR_Y+MOTOR_R)
    bevel_bottom=BEVEL_Z-BEVEL_R
    bevel_top=BEVEL_Z+BEVEL_R
    bevel_lower_margin=bevel_bottom-BODY_Z0
    bevel_upper_margin=BODY_Z1-bevel_top
    bevel_x_margin=min(BEVEL_X-BEVEL_R-BODY_X0, BODY_X1-(BEVEL_X+BEVEL_R))
    wc,wpos=wheel_noncontact_clearance()
    cam,ang=camera_sweep()

    print(f'body_corner_clearance_mm={body:.3f}')
    print(f'cover_corner_clearance_mm={cover:.3f}')
    print(f'motor_to_motor_gap_mm={motor_gap:.3f}')
    print(f'motor_to_body_wall_gap_mm={wall_gap:.3f}')
    print(f'large_bevel_lower_body_margin_mm={bevel_lower_margin:.3f}')
    print(f'large_bevel_upper_body_margin_mm={bevel_upper_margin:.3f}')
    print(f'large_bevel_longitudinal_margin_mm={bevel_x_margin:.3f}')
    print(f'wheel_profile_ideal_clearance_mm={wc:.3f} at_y_r={wpos}')
    print(f'camera_sweep_clearance_mm={cam:.3f} at_tilt_deg={ang}')

    ok = body>=5 and cover>=5 and motor_gap>=1 and wall_gap>=5 and bevel_lower_margin>=2.5 and bevel_upper_margin>=5
    print('PACKAGING_BASELINE=' + ('PASS' if ok else 'FAIL'))

if __name__=='__main__':
    main()
