#!/usr/bin/env python3
"""PX-1 Rev.DQ camera-cylinder sweep inside corrected DN150 pipe.

Samples a Ø52 x 72 mm cylindrical camera envelope through TILT -105..+105 deg.
This is still an envelope check, not the final detailed-head collision model.
"""
import math

PIPE_R = 75.0
PIPE_Z = 52.04805471869242
CAM_R = 26.0
CAM_L = 72.0


def worst_radial_reach(cam_z, angle_step_deg=1, s_steps=72, phi_steps=180):
    worst = (-1.0, None, None, None)
    for ai in range(int(210/angle_step_deg)+1):
        deg = -105.0 + ai*angle_step_deg
        th = math.radians(deg)
        # camera axis a=(cos th,0,sin th)
        # radial basis e1=(0,1,0), e2=(-sin th,0,cos th)
        for si in range(s_steps+1):
            s = -CAM_L/2 + CAM_L*si/s_steps
            for pi in range(phi_steps):
                ph = 2*math.pi*pi/phi_steps
                y = CAM_R*math.cos(ph)
                z = cam_z + s*math.sin(th) + CAM_R*math.sin(ph)*math.cos(th)
                rho = math.hypot(y, z-PIPE_Z)
                if rho > worst[0]:
                    worst = (rho, deg, s, ph)
    return worst


if __name__ == '__main__':
    for cam_z in (60.3, 69.7, 72.0, 76.0):
        rho, deg, s, ph = worst_radial_reach(cam_z)
        clearance = PIPE_R-rho
        print(f'Zcam={cam_z:5.1f} mm: worst rho={rho:6.3f}, clearance={clearance:6.3f} mm, tilt={deg:6.1f} deg')

    # Closed-form conservative height from cylindrical envelope projection:
    radial_shape = math.hypot(CAM_L/2, CAM_R)
    z_for_5mm = PIPE_Z + (PIPE_R-5.0) - radial_shape
    z_for_3mm = PIPE_Z + (PIPE_R-3.0) - radial_shape
    print(f'Camera-axis height for 5 mm ideal-envelope clearance: {z_for_5mm:.3f} mm')
    print(f'Camera-axis height for 3 mm ideal-envelope clearance: {z_for_3mm:.3f} mm')
