#!/usr/bin/env python3
"""Verify the current PX1 CAD export without claiming manufacturing qualification.

Run after build_current.sh. Exit 1 means a failed geometric/reproducibility check;
exit 0 only means the requested CAD screens passed. Unqualified seal, bevel and
thread contacts are retained explicitly as HOLD in the resulting JSON.
"""
from __future__ import annotations
import argparse
import ast
from collections import Counter
import hashlib
import json
import math
from pathlib import Path
import sys

EXPECTED = {'wheel': 6, 'Z50': 10, 'Z40': 2, 'Z16': 2, 'traction_motor': 2,
            '61801_side': 2, '61801_pinion': 2, '61903': 6, '61800': 2,
            'idler_bush': 4, 'camera_harness_cores': 6}
CONTACT_HOLDS = {'SEAL_CONTACT_REQUIRES_GLAND_CHECK', 'TOOTH_CONTACT_HOLD',
                 'THREAD_ENGAGEMENT_HOLD_NO_HELICAL_GEOMETRY',
                 'VALVE_INTERNAL_ENVELOPE_HOLD'}


def digest(path):
    h = hashlib.sha256()
    with path.open('rb') as f:
        for chunk in iter(lambda: f.read(1024 * 1024), b''):
            h.update(chunk)
    return h.hexdigest()


def spur_screen(source, samples=9):
    """Use exactly the master's tooth builder, without executing its assembly."""
    import cadquery as cq
    tree = ast.parse(source.read_text(encoding='utf8'))
    fn = next(n for n in tree.body if isinstance(n, ast.FunctionDef)
              and n.name == 'make_spur_gear')
    namespace = {'cq': cq, 'math': math}
    exec(compile(ast.Module(body=[fn], type_ignores=[]), str(source), 'exec'), namespace)
    gear = namespace['make_spur_gear'](50, 1.0, 4.0, 12.0, 'Y').val()
    results = []
    for k in range(samples):
        angle = 7.2 * k / (samples - 1)
        a = gear.rotate((0, 0, 0), (0, 1, 0), angle).translate((50, 31.8, 45))
        b = gear.rotate((0, 0, 0), (0, 1, 0), 3.6 - angle).translate((100, 31.8, 45))
        volume = a.intersect(b).Volume()
        results.append({'driven_angle_deg': angle, 'other_angle_deg': 3.6 - angle,
                        'intersection_mm3': volume})
    maximum = max(r['intersection_mm3'] for r in results)
    return {'status': 'PASS_DISCRETE_REFERENCE_PROFILE' if maximum <= 1e-4 else 'FAIL_INTERFERENCE',
            'threshold_mm3': 1e-4, 'maximum_intersection_mm3': maximum,
            'centre_distance_mm': 50.0, 'samples': results,
            'scope': 'One adjacent equal-Z50 pair, opposite rotation through one tooth pitch; '
                     'representative of identical alternating gears on both sides.',
            'limitations': 'Discrete sample only; not a continuous sweep, OEM tooth definition, '
                           'backlash/tolerance assessment, bevel test or physical A0 pass.'}


def roundtrip(step, registry):
    import cadquery as cq
    imported = cq.importers.importStep(str(step))
    vals = imported.vals()
    shape = vals[0] if len(vals) == 1 else cq.Compound.makeCompound(vals)
    solids = shape.Solids()
    expected_volume = sum(item['volume_mm3'] for item in registry)
    expected_solids = sum(item['solids'] for item in registry)
    expected_bounds = [min(i['bbox_mm'][k] for i in registry) for k in range(3)] + [
        max(i['bbox_mm'][k] for i in registry) for k in range(3, 6)]
    bb = shape.BoundingBox()
    actual_bounds = [bb.xmin, bb.ymin, bb.zmin, bb.xmax, bb.ymax, bb.zmax]
    actual_volume = shape.Volume()
    checks = {
        'valid_compound': shape.isValid(),
        'valid_solids': all(s.isValid() and s.Volume() > 0 for s in solids),
        'solid_count_matches': len(solids) == expected_solids,
        'volume_matches': abs(actual_volume - expected_volume) <= max(0.01, expected_volume * 1e-6),
        'bounds_match': max(abs(a-b) for a, b in zip(actual_bounds, expected_bounds)) <= 0.001,
    }
    return {'status': 'PASS' if all(checks.values()) else 'FAIL', 'checks': checks,
            'actual_solids': len(solids), 'expected_solids': expected_solids,
            'actual_volume_mm3': actual_volume, 'registry_volume_mm3': expected_volume,
            'actual_bounds_mm': actual_bounds, 'registry_bounds_mm': expected_bounds,
            'tolerance': {'volume_relative': 1e-6, 'volume_absolute_floor_mm3': .01,
                          'bounds_absolute_mm': .001}}


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('output', type=Path, help='Build output directory')
    parser.add_argument('--source', type=Path, default=Path(__file__).resolve().parents[2] / 'current/CAD/PX1_Current_Master.py')
    parser.add_argument('--roundtrip', action='store_true', help='Reimport full STEP and compare geometry to registry')
    parser.add_argument('--skip-spur', action='store_true', help='Record spur screen NOT_RUN, useful for fast diagnostics')
    parser.add_argument('--require-pipe-service', action='store_true', help='Require the current pipe/contact report and continuous motor exit screen')
    args = parser.parse_args()
    out = args.output.resolve()
    val = json.loads((out / 'PX1_Current_Validation.json').read_text())
    registry = json.loads((out / 'component_registry.json').read_text())
    step = out / 'CAD/PX1_Current_Master.step'
    clashes = val.get('interferences', [])
    holds = [p for p in clashes if p.get('classification') in CONTACT_HOLDS]
    blocking = [p for p in clashes if p.get('classification') not in CONTACT_HOLDS]
    def x_centres(category):
        return sorted(round((i['bbox_mm'][0] + i['bbox_mm'][3])/2, 3)
                      for i in registry if i['category'] == category)
    actual_source_hash = digest(args.source)
    checks = {
        'counts_match_frozen_architecture': val.get('counts') == EXPECTED,
        'wheel_stations_preserved': x_centres('wheel') == [50.,50.,150.,150.,250.,250.],
        'gear_stations_preserved': x_centres('gear') == [50.,50.,100.,100.,150.,150.,200.,200.,250.,250.],
        'component_ids_unique': len({i['id'] for i in registry}) == len(registry),
        'source_matches_current_master': val.get('source_sha256') == actual_source_hash,
        'valid_shapes': val.get('invalid_shapes') == [],
        'boolean_errors_absent': val.get('collision_method', {}).get('errors') == [],
        'no_excluded_pairs': val.get('collision_method', {}).get('excluded_pairs') == 0,
        'all_pairs_enumerated': val.get('collision_method', {}).get('all_pairs') == len(registry)*(len(registry)-1)//2,
        'component_count_matches': val.get('component_count') == len(registry),
        'no_rigid_or_wheel_or_unknown_clashes': not blocking,
        'manufacturing_release_remains_false': val.get('metal_release') is False,
        'step_exists': step.is_file() and step.stat().st_size > 1024,
    }
    report = {'status': 'PENDING', 'manufacturing_release': False,
              'source_sha256': actual_source_hash, 'build_source_sha256': val.get('source_sha256'),
              'step_sha256': digest(step) if step.is_file() else None,
              'checks': checks, 'interference_class_counts': dict(Counter(p.get('classification', 'UNKNOWN') for p in clashes)),
              'blocking_interferences': blocking, 'unqualified_contacts_status': 'HOLD' if holds else 'NONE_REPORTED',
              'unqualified_contacts': holds, 'physical_A0_A1_A5_tests': 'NOT_PERFORMED',
              'dn150_status': val.get('dn150', {}).get('global_status'),
              'dn150_protrusions': [i for i in val.get('dn150', {}).get('all_component_results', []) if i.get('clearance_mm', 0) < -.12],
              'scope': 'Export reproducibility, static rigid clearance and requested sampled geometric checks only. '
                       'Does not release pressure sealing, gear tooth manufacture, dynamic lift routing, '
                       'service paths, fatigue, thermal design or purchased-part compatibility.'}
    if args.skip_spur:
        report['spur_screen'] = {'status': 'NOT_RUN'}
    else:
        try:
            report['spur_screen'] = spur_screen(args.source)
            checks['spur_sampled_screen'] = report['spur_screen']['status'] == 'PASS_DISCRETE_REFERENCE_PROFILE'
        except Exception as exc:
            report['spur_screen'] = {'status': 'ERROR', 'error': str(exc)}
            checks['spur_sampled_screen'] = False
    if args.roundtrip:
        try:
            report['step_roundtrip'] = roundtrip(step, registry)
            checks['step_roundtrip'] = report['step_roundtrip']['status'] == 'PASS'
        except Exception as exc:
            report['step_roundtrip'] = {'status': 'ERROR', 'error': str(exc)}
            checks['step_roundtrip'] = False
    else:
        report['step_roundtrip'] = {'status': 'NOT_RUN'}
    if args.require_pipe_service:
        pipe_path=out/'pipe_verification.json'
        pipe=json.loads(pipe_path.read_text()) if pipe_path.is_file() else {}
        service=val.get('service',{}).get('motor_vertical_extraction',{})
        continuous=service.get('continuous_translation_screen',{})
        checks['pipe_contact_profile_and_solid_bounds']=pipe.get('proposed_screen_passes') is True and pipe.get('active_source_sha256')==actual_source_hash
        checks['motor_continuous_exit']=continuous.get('status')=='PASS_CANDIDATE_ENVELOPE' and continuous.get('errors')==[]
        checks['motor_discrete_exit']=service.get('status')=='NO_COLLISION_IN_DISCRETE_SCREEN' and service.get('errors')==[]
        tools=val.get('service',{}).get('service_screw_tools',[])
        checks['four_service_tool_approaches']=len(tools)==4 and all(not i.get('collisions') for i in tools)
        report['pipe_service_scope']='Nominal engineered tyre in perfect straight ID150; active candidate motor exit after explicit preceding disassembly; no physical passage, sealing, traction or complete service-sequence qualification.'
    mt=val.get('service',{}).get('motor_mount_tool_probes')
    if mt is not None:
        checks['ten_motor_mount_bit_access_probes']=len(mt)==10 and all(not i['collisions'] and not i['errors'] for i in mt)
    report['status'] = 'PASS_REQUESTED_CAD_SCREENS_WITH_RELEASE_HOLD' if all(checks.values()) else 'FAIL_CAD_SCREEN'
    (out / 'integrated_checks.json').write_text(json.dumps(report, indent=2, ensure_ascii=False) + '\n')
    print(json.dumps({'status': report['status'], 'checks': checks, 'blocking_interferences': len(blocking),
                      'unqualified_contacts': len(holds), 'report': str(out / 'integrated_checks.json')}, indent=2))
    return 0 if all(checks.values()) else 1


if __name__ == '__main__':
    sys.exit(main())
