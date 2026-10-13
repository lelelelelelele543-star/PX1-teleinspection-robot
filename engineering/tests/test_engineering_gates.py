"""Offline regression and negative/fault injection tests for the PX1 gatekeeper.

Tests passing is NOT proof that the robot is ready for fabrication.
"""
import sys
import unittest
from pathlib import Path

ROOT = Path(__file__).resolve().parents[2]
sys.path.insert(0, str(ROOT / "engineering"))
sys.path.insert(0, str(ROOT / "tools"))

from simulation import dc_feeder, evaluate_model_suite, watchdog_timeline, wheel_speed_m_min
from px1_gate import LOCKED_COUNTS, audit, classify_evidence


class ModelsTest(unittest.TestCase):
    def test_nominal_models(self):
        self.assertEqual(evaluate_model_suite()["status"], "PASS_MODEL_ONLY")

    def test_impossible_low_voltage_cable_case(self):
        self.assertFalse(dc_feeder(24, 96, 40, 0.75)["equilibrium_exists"])

    def test_high_voltage_study_not_energy_release(self):
        s = dc_feeder(110, 150, 40, 0.75, 0.89)
        self.assertTrue(s["equilibrium_exists"])
        self.assertLess(s["power_balance_error_w"], 1e-8)

    def test_reject_rpm_exceeding_candidate_limit(self):
        with self.assertRaises(ValueError):
            wheel_speed_m_min(4001)

    def test_corrupted_command_does_not_keep_motors_alive(self):
        w = watchdog_timeline()
        self.assertTrue(w[100])
        self.assertFalse(w[360])
        self.assertTrue(w[400])

    def test_watchdog_fault_injection_immediate_loss(self):
        w = watchdog_timeline(valid_commands_ms=(0,), corrupted_commands_ms=(250,))
        self.assertTrue(w[250])
        self.assertFalse(w[260])


class GatesTest(unittest.TestCase):
    def val(self, **changes):
        a = {"counts": {**LOCKED_COUNTS}, "counts_match": True,
             "interferences": [], "invalid_shapes": [], "metal_release": False}
        a.update(changes)
        return a

    def test_six_wheels_are_not_optional(self):
        bad = self.val(counts={**LOCKED_COUNTS, "wheel": 4})
        gates, errs = classify_evidence(bad, [], [])
        self.assertEqual(gates[0]["state"], "FAIL")
        self.assertTrue(errs)

    def test_collisions_block_machining(self):
        bad = self.val(interferences=[{"classification": "RIGID_INTERFERENCE"}])
        gates, errs = classify_evidence(bad, [], [])
        self.assertEqual(gates[1]["state"], "BLOCKED")

    def test_holds_cannot_be_forged_into_pass(self):
        bad = self.val(metal_release=True)
        gates, errs = classify_evidence(bad, [{"id": "H01"}], [])
        self.assertTrue(any("contradicts" in e for e in errs))
        self.assertEqual(gates[1]["state"], "BLOCKED")

    def test_real_checkout_never_claims_auto_production_release(self):
        if not (ROOT / "current/PX1_Current_Validation.json").exists():
            self.skipTest("test only runs in full PX1 repo checkout")
        r = audit(ROOT)
        self.assertFalse(r["release_permitted"])
        self.assertNotEqual(r["verdict"], "FAIL_CHECKER", r["integrity_errors"])


if __name__ == "__main__":
    unittest.main()
