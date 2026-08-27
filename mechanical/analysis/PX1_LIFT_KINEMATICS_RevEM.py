#!/usr/bin/env python3
import math

PIVOT_X = 200.0
PIVOT_Z = 94.0
LINK_L = 120.0
CAM_AXIS_OFFSET_Z = 10.0
POSITIONS = {
    'LOW_DN150': 75.0,
    'MID': 130.0,
    'HIGH': 205.0,
}


def solve(axis_z):
    s = (axis_z - (PIVOT_Z + CAM_AXIS_OFFSET_Z))/LINK_L
    if abs(s) > 1:
        raise ValueError('Position unreachable')
    th = math.asin(s)
    upper_x = PIVOT_X - LINK_L*math.cos(th)
    upper_z = PIVOT_Z + LINK_L*math.sin(th)
    return math.degrees(th), upper_x, upper_z


if __name__ == '__main__':
    print('PX-1 Rev.EM lift kinematics')
    for name, z in POSITIONS.items():
        a, x, uz = solve(z)
        print(f'{name}: camera_axis_Z={z:.1f} mm, arm_angle={a:.2f} deg, upper_pivot=({x:.2f},{uz:.2f}) mm')
