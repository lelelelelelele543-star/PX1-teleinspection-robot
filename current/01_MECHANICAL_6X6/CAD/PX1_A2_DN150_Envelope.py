#!/usr/bin/env python3
"""PX1 A2 independent DN150 envelope, no OEM geometry implied.

STD library verifies geometry. Optional cadquery exports STEP and STL.
Dimensions are design assumptions except archived A0/A1 topology and motor candidate.
"""
import argparse
import json
from dataclasses import dataclass, asdict
from math import sqrt, hypot
from pathlib import Path

@dataclass(frozen=True)
class A2:
    pipe_id: float = 150.0
    wheel_d: float = 70.0
    wheel_width: float = 16.0
    wheel_inner_y: float = 45.0
    body_half_y: float = 33.0
    cavity_half_y: float = 28.0
    shell_half_z: float = 28.0
    cavity_half_z: float = 23.0
    gearbox_d: float = 26.0
    gearbox_l: float = 44.4
    motor_d: float = 22.0
    motor_l: float = 51.8
    motor_center_y: float = 13.5
    motor_x_start: float = 116.2
    cavity_xmin: float = 105.0
    cavity_xmax: float = 245.0
    shell_xcenter: float = 150.0
    shell_length: float = 264.0
    gear_module: float = 1.0
    gear_teeth: int = 50
    gear_centers: tuple = (50.,100.,150.,200.,250.)
    wheel_centers: tuple = (50.,150.,250.)

    @property
    def outside_y(self):
        return self.wheel_inner_y + self.wheel_width

    @property
    def tube_z(self):
        return self.pipe_id / 2

    @property
    def axle_z(self):
        # Conservative corner contact: NOT a rounded-tread or traction model
        return self.tube_z - sqrt(self.tube_z**2 - self.outside_y**2) + self.wheel_d/2


def validate(d=A2()):
    errors=[]
    if d.outside_y>=d.tube_z:
        return {'pass':False,'errors':['wheel Y outside tube radius']}
    gap_center=2*d.motor_center_y-d.gearbox_d
    gap_wall=d.cavity_half_y-d.motor_center_y-d.gearbox_d/2
    motor_right=d.motor_x_start+d.motor_l+d.gearbox_l
    gap_x=min(d.motor_x_start-d.cavity_xmin,d.cavity_xmax-motor_right)
    gap_z=d.cavity_half_z-d.gearbox_d/2
    wheel_radius=d.wheel_d/2
    wheel_radial=hypot(d.outside_y,max(abs(d.axle_z-wheel_radius-d.tube_z),
                                        abs(d.axle_z+wheel_radius-d.tube_z)))
    body_radial=hypot(d.body_half_y,abs(d.axle_z-d.tube_z)+d.shell_half_z)
    gear_pitch=d.gear_module*d.gear_teeth
    if min(gap_center,gap_wall,gap_x,gap_z)<=0:
        errors.append('motor / gearbox collision')
    if wheel_radial>d.tube_z+1e-6 or body_radial>d.tube_z:
        errors.append('DN150 radial envelope crossed')
    if d.body_half_y>=d.wheel_inner_y:
        errors.append('wheel lane overlaps shell')
    if len(d.wheel_centers)!=3 or len(d.gear_centers)!=5:
        errors.append('6-wheel/five-gear topology invalid')
    if any(abs(d.gear_centers[i+1]-d.gear_centers[i]-gear_pitch)>1e-6 for i in range(4)):
        errors.append('gear pitch spacing invalid')
    return {'pass':not errors,'errors':errors,
            'motor_wall_gap_mm':round(gap_wall,3),
            'motor_to_motor_gap_mm':round(gap_center,3),
            'motor_x_gap_mm':round(gap_x,3),
            'wheel_radial_wall_penetration_mm':round(wheel_radial-d.tube_z,6),
            'body_max_radial_mm':round(body_radial,3),
            'axle_z_from_pipe_bottom_mm':round(d.axle_z,3),
            'overall_width_mm':2*d.outside_y,
            'motor_count':2,'wheel_count':len(d.wheel_centers)*2,
            'gear_pitch_d_mm':gear_pitch,'side_gear_count':len(d.gear_centers)}


def export_step(d,outdir):
    import cadquery as cq
    z=d.axle_z
    outer=cq.Workplane('XY').box(d.shell_length,2*d.body_half_y,
                                 2*d.shell_half_z).translate((d.shell_xcenter,0,z))
    cavity=cq.Workplane('XY').box(d.cavity_xmax-d.cavity_xmin,2*d.cavity_half_y,
                                  2*d.cavity_half_z).translate(((d.cavity_xmin+d.cavity_xmax)/2,0,z))
    shell=outer.cut(cavity).val()
    a=cq.Assembly(name='PX1_A2_ENVELOPE_ONLY')
    a.add(shell,name='conceptual_dry_housing')
    for side in (-1,1):
        yc=side*d.motor_center_y
        mot=cq.Solid.makeCylinder(d.motor_d/2,d.motor_l,
                                  cq.Vector(d.motor_x_start,yc,z),cq.Vector(1,0,0))
        reducer=cq.Solid.makeCylinder(d.gearbox_d/2,d.gearbox_l,
                                      cq.Vector(d.motor_x_start+d.motor_l,yc,z),
                                      cq.Vector(1,0,0))
        a.add(mot,name=f'motor_{side}')
        a.add(reducer,name=f'gearbox_{side}')
        for x in d.gear_centers:
            # pitch disks, not teeth, bearings, or true gear meshes
            disk=cq.Solid.makeCylinder(d.gear_teeth*d.gear_module/2,5,
                                       cq.Vector(x,side*38,z),cq.Vector(0,side,0))
            a.add(disk,name=f'pitch_disk_{side}_{int(x)}')
        for x in d.wheel_centers:
            tire=cq.Solid.makeCylinder(d.wheel_d/2,d.wheel_width,
                                       cq.Vector(x,side*d.wheel_inner_y,z),
                                       cq.Vector(0,side,0))
            a.add(tire,name=f'wheel_envelope_{side}_{int(x)}')
    a.save(str(outdir/'PX1_A2_Envelope_Assembly.step'),exportType='STEP')
    cq.exporters.export(shell,str(outdir/'PX1_A2_Shell_Envelope.stl'))


def run():
    p=argparse.ArgumentParser()
    p.add_argument('--out',default='PX1_A2_outputs')
    p.add_argument('--cad',action='store_true')
    opt=p.parse_args()
    d=A2()
    r=validate(d)
    assert r['pass'],r
    # Negative controls ensure actual failure detection rather than hardcoded PASS
    from dataclasses import replace
    assert not validate(replace(d,gearbox_d=32))['pass']
    assert not validate(replace(d,wheel_width=32))['pass']
    assert not validate(replace(d,gear_centers=(50,99,150,200,250)))['pass']
    path=Path(opt.out); path.mkdir(parents=True,exist_ok=True)
    (path/'PX1_A2_Validation.json').write_text(
        json.dumps({'design_parameters':asdict(d),'result':r},indent=2)+'\n',encoding='utf-8')
    if opt.cad:
        export_step(d,path)
    print(json.dumps(r,indent=2))

if __name__=='__main__':
    run()
