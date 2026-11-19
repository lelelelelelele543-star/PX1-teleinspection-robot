#!/usr/bin/env python3
"""Analytic DN150 wheel-profile/ground-contact screen plus exact-assembly mesh scan.

A geometric design study, not verification of a real QRW90 tyre or pipe test.
The profile arguments are explicit radius/local-axial-coordinate polygon pairs.
All distances mm; wheel axes parallel Y, pipe axis X; left/right symmetric.
"""
from __future__ import annotations
import argparse
import ast
import gzip
import hashlib
import json
import math
from pathlib import Path

ROOT = Path(__file__).resolve().parents[2]
BASELINE = [(26.,-12.),(32.,-12.),(42.,-8.),(45.,0.),(42.,8.),(32.,12.),(8.,12.),(8.,-2.),(26.,-2.)]
PROPOSED = [(26.,-12.),(32.,-12.),(42.,-8.),(45.,0.),(28.5,8.),(20.5,12.),(8.,12.),(8.,-2.),(26.,-2.)]
MIN_NONCONTACT_GAP = 3.0  # F04 requirement, mm


def profile_screen(points, pipe_radius, wheel_y, wheel_z, pipe_z):
    """Exact bound for every point of the polygon's solid of revolution.

    For a fixed radius/axial station, revolution gives z=wheel_z+r*sin(theta).
    The worst radial distance is hypot(Y, r+abs(wheel_z-pipe_z)). On each
    polygon segment this is a convex norm of an affine function, so its maximum
    is attained at an endpoint. Checking all vertices is therefore sufficient;
    unlike a tessellation this does not miss between-vertex tyre bulges.
    """
    delta = abs(pipe_z-wheel_z)
    vertices = []
    for radius, local_y in points:
        global_y = wheel_y + local_y
        distance = math.hypot(global_y, radius+delta)
        vertices.append({'radius_mm': radius, 'local_y_mm': local_y,
                         'global_y_mm': global_y, 'max_pipe_radial_mm': distance,
                         'radial_clearance_mm': pipe_radius-distance})
    limit = min(math.sqrt(max(0., pipe_radius**2-(wheel_y+y)**2))-r for r,y in points)
    worst = max(vertices, key=lambda p: p['max_pipe_radial_mm'])
    # F04: every vertex except the grounded crown contact (r=crown, local y=0)
    # must keep the required radial gap. Segment maxima lie at endpoints (see above).
    non_contact = [v for v in vertices if not (v['local_y_mm'] == 0 and v['radius_mm'] == max(r for r, _ in points))]
    non_contact_min = min(v['radial_clearance_mm'] for v in non_contact)
    return {'minimum_radial_clearance_mm': worst['radial_clearance_mm'],
            'worst_vertex': worst, 'vertices': vertices,
            'feasible_pipe_center_delta_interval_mm': [-limit, limit] if limit >= 0 else None,
            'maximum_permitted_absolute_center_delta_mm': limit,
            'all_rigid_revolved_geometry_inside': worst['radial_clearance_mm'] >= -1e-9,
            'minimum_noncontact_vertex_clearance_mm': non_contact_min,
            'noncontact_gap_requirement_mm': MIN_NONCONTACT_GAP,
            'noncontact_gap_ok': non_contact_min >= MIN_NONCONTACT_GAP - 1e-9}


def scan_mesh(path, pipe_r, pipe_z):
    with gzip.open(path, 'rt') as f:
        components = json.load(f)
    results = []
    for component in components:
        radial = max(math.hypot(p[1], p[2]-pipe_z) for p in component['vertices'])
        results.append({'id': component['id'], 'category': component['category'],
                        'radial_clearance_mm': pipe_r-radial})
    non_wheels = [r for r in results if r['category'] != 'wheel']
    return {'source': str(path.relative_to(ROOT)) if path.is_relative_to(ROOT) else str(path),
            'sha256': hashlib.sha256(path.read_bytes()).hexdigest(),
            'method': 'All vertices of the archived assembly mesh; no surrogate boxes.',
            'mesh_limit': 'Master tessellation tolerance .25 mm; a discrete surface screen, not exact BRep containment.',
            'proposed_wheels_not_substituted_in_mesh': True,
            'minimum_nonwheel_clearance_mm': min(r['radial_clearance_mm'] for r in non_wheels),
            'nonwheel_protrusions': [r for r in non_wheels if r['radial_clearance_mm'] < 0],
            'component_results': results}


def main():
    ap = argparse.ArgumentParser(description=__doc__)
    ap.add_argument('--mesh', type=Path, default=ROOT/'current/09_RELEASE/integrated_20261117/images/assembly_mesh.json.gz')
    ap.add_argument('--out', type=Path, default=ROOT/'current/09_RELEASE/pipe_service_20261118/pipe_pose_analysis.json')
    ap.add_argument('--active', action='store_true', help='Verify active master profile and matching rebuilt mesh, not the historical study')
    args = ap.parse_args()
    pipe_r, wheel_y, wheel_z, crown_r = 75., 54.5, 45., 45.
    # Highest pipe centre that does not penetrate fixed wheels equals lowest
    # gravity-supported chassis pose; the crown at z=0 touches the lower wall.
    delta = math.sqrt(pipe_r**2-wheel_y**2)-crown_r
    pipe_z = wheel_z+delta
    baseline_at_axis = profile_screen(BASELINE,pipe_r,wheel_y,wheel_z,wheel_z)
    old = profile_screen(BASELINE,pipe_r,wheel_y,wheel_z,52.0480547)
    candidate = profile_screen(PROPOSED,pipe_r,wheel_y,wheel_z,pipe_z)
    report = {'status': 'PROPOSED_GEOMETRY_SCREEN_ONLY', 'manufacturing_release': False,
              'dimensions_mm': {'pipe_inner_radius':pipe_r,'wheel_axis_z':wheel_z,'wheel_center_abs_y':wheel_y,
                                'crown_radius':crown_r,'outer_width':2*(wheel_y+12),'wheel_diameter':2*crown_r},
              'baseline_profile_radius_local_y_mm': BASELINE,
              'proposed_profile_radius_local_y_mm': PROPOSED,
              'inherited_pose': {'pipe_center_z_mm':52.0480547,'exact_profile_screen':old},
              'baseline_best_centered_pose': {'pipe_center_z_mm':wheel_z,'exact_profile_screen':baseline_at_axis,
                  'conclusion':'No rigid centred level pose fits the inherited wheel meridian: outer shoulder already exceeds R75 with zero centre offset.'},
              'derived_supported_pose': {'pipe_center_z_mm':pipe_z,'wheel_below_pipe_axis_mm':delta,
                  'crown_contact_points_yz_mm':[[-wheel_y,wheel_z-crown_r],[wheel_y,wheel_z-crown_r]],
                  'normal_vertical_fraction':math.sqrt(pipe_r**2-wheel_y**2)/pipe_r,
                  'derivation':'pipe_z = wheel_z - crown_radius + sqrt(pipe_radius^2-wheel_center_y^2); paired lower-wall crown contacts support gravity with symmetric lateral reactions.'},
              'proposed_exact_profile_screen':candidate,
              'nonwheel_integrated_mesh_screen':scan_mesh(args.mesh.resolve(),pipe_r,pipe_z),
              'limits':['Nominal rigid, straight circular ID150 pipe, level crawler, static lift LOW only.',
                        'Wheel outer contour is an engineering estimate, not a recovered OEM QRW90 profile.',
                        'Tyre deformation, loading/contact stress, wear, traction and tolerances not qualified.',
                        'No curved-pipe, joint/obstacle, full-lift or endurance/pressure test claimed.',
                        'Rebuild full CAD with proposed profile and contact-derived pose, rerun all-pair collision and STEP checks before adopting.']}
    if args.active:
        master=ROOT/'current/CAD/PX1_Current_Master.py'
        tree=ast.parse(master.read_text()); values={}
        for node in tree.body:
            if isinstance(node,ast.Assign):
                try:value=ast.literal_eval(node.value)
                except (ValueError,TypeError):continue
                for target in node.targets:
                    if isinstance(target,ast.Name):values[target.id]=value
        actual_profile=[tuple(pair) for pair in values['WHEEL_PROFILE']]
        active_source_hash=hashlib.sha256(master.read_bytes()).hexdigest()
        validation=json.loads((args.mesh.parent.parent/'PX1_Current_Validation.json').read_text())
        report['active_master_checks']={
            'profile_matches':actual_profile==PROPOSED,
            'wheel_y_matches':values['WHEEL_CENTRE_Y']==wheel_y,
            'wheel_z_matches':values['WHEEL_Z']==wheel_z,
            'crown_matches':values['WHEEL_CROWN_R']==crown_r,
            'noncontact_gap_requirement_matches':values.get('WHEEL_MIN_NONCONTACT_GAP')==MIN_NONCONTACT_GAP,
            'pipe_radius_matches':values['PIPE_R']==pipe_r,
            'contact_pose_matches':abs(validation['dn150']['assumed_pipe_center_z_mm']-pipe_z)<1e-9,
            'source_hash_matches':validation['source_sha256']==active_source_hash}
        registry=json.loads((args.mesh.parent.parent/'component_registry.json').read_text())
        box_proof=[]
        for item in registry:
            if item['category']=='wheel':continue
            b=item['bbox_mm']
            bound=max(math.hypot(y,z-pipe_z) for y in (b[1]-.00001,b[4]+.00001) for z in (b[2]-.00001,b[5]+.00001))
            box_proof.append({'id':item['id'],'conservative_clearance_mm':pipe_r-bound})
        report['nonwheel_bounding_box_containment']={'method':'Every YZ corner of each kernel bounding box, expanded by0.00001mm for registry rounding. Cylinder cross-section is convex, so contained corners prove the entire box and solid are contained.',
            'minimum_clearance_mm':min(i['conservative_clearance_mm'] for i in box_proof),
            'results':box_proof}
        report['active_master_checks']['nonwheel_boxes_inside']=all(i['conservative_clearance_mm']>=0 for i in box_proof)
        report['active_source_sha256']=active_source_hash
        report['status']='ACTIVE_NOMINAL_CAD_SCREEN_WITH_RELEASE_HOLD'
        report['nonwheel_integrated_mesh_screen']['proposed_wheels_not_substituted_in_mesh']=False
        report['active_all_component_mesh_protrusions']=[i for i in report['nonwheel_integrated_mesh_screen']['component_results'] if i['radial_clearance_mm'] < -.12]
    report['proposed_screen_passes'] = candidate['all_rigid_revolved_geometry_inside'] and candidate['noncontact_gap_ok'] and not report['nonwheel_integrated_mesh_screen']['nonwheel_protrusions']
    if args.active:
        report['proposed_screen_passes'] = report['proposed_screen_passes'] and all(report['active_master_checks'].values()) and not report['active_all_component_mesh_protrusions']
    args.out.parent.mkdir(parents=True,exist_ok=True)
    args.out.write_text(json.dumps(report,ensure_ascii=False,indent=2)+'\n')
    print(json.dumps({'report':str(args.out),'pipe_center_z_mm':pipe_z,
                      'old_best_possible_clearance_mm':baseline_at_axis['minimum_radial_clearance_mm'],
                      'candidate_clearance_mm':candidate['minimum_radial_clearance_mm'],
                      'candidate_outer_shoulder_clearance_mm':candidate['vertices'][4]['radial_clearance_mm'],
                      'candidate_outer_edge_clearance_mm':candidate['vertices'][5]['radial_clearance_mm'],
                      'candidate_min_noncontact_clearance_mm':candidate['minimum_noncontact_vertex_clearance_mm'],
                      'nonwheel_mesh_min_clearance_mm':report['nonwheel_integrated_mesh_screen']['minimum_nonwheel_clearance_mm'],
                      'proposed_screen_passes':report['proposed_screen_passes']},indent=2))
    return 0 if report['proposed_screen_passes'] else 1

if __name__ == '__main__':
    raise SystemExit(main())
