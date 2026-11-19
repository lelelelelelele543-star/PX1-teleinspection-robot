"""Screen Z22 candidate against released component bounds; NOT a collision pass."""
import hashlib, json, math
from pathlib import Path
root = Path(__file__).resolve().parents[2]
registry = root / 'current/09_RELEASE/pipe_service_20261118/component_registry.json'
rows = json.loads(registry.read_text())
face, length, radius = 195.5, 85 + 40.6, 11
screens = []
for side in (-1, 1):
    y = side * 13.5
    bounds = [face-length, y-radius, 34, face, y+radius, 56]
    hits = []
    for row in rows:
        b = row['bbox_mm']
        if all(min(bounds[i+3], b[i+3])-max(bounds[i], b[i]) > 1e-5 for i in range(3)):
            hits.append(row['id'])
    screens.append({'side': side, 'body_bounds_mm': bounds, 'bbox_candidates_not_confirmed_collisions': hits})
result = {
    'status': 'TECHNICAL_SELECTION_PENDING_SUPPLIER_CONFIRMATION_AND_CAD_INTEGRATION',
    'candidate': '2 x Z22DP2410-60S / 22PM105 (K bearing suffix to confirm)',
    'registry_sha256': hashlib.sha256(registry.read_bytes()).hexdigest(),
    'catalogue_output_torque_Nm': 0.8,
    'catalogue_loaded_output_rpm': 57,
    'assumed_downstream_efficiency': 0.75,
    'required_motor_output_torque_for_50N_Nm': 50*.045/(2*2.5*.75),
    'calculated_total_force_N_not_measured': 2*.8*2.5*.75/.045,
    'calculated_speed_m_min_not_measured': 57/2.5*math.pi*.09,
    'minimum_downstream_efficiency_for_50N': 50*.045/(2*.8*2.5),
    'motor_pair_body_width_mm': 27+22,
    'existing_cavity_width_mm': 53,
    'body_rear_x_mm': face-length,
    'existing_service_opening_front_x_mm': 128,
    'screens': screens,
    'limitations': ['Bounds overlap is not a solid intersection test.',
                    'Pilot, shaft, wire bend envelope and replacement mounts need integration.',
                    'Previous STEP validation applies only to the unchanged JGA25 assembly.',
                    'No stock, thermal, traction, extraction or manufacturing qualification.']
}
print(json.dumps(result, indent=2, ensure_ascii=False))
