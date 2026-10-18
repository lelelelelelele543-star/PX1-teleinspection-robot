"""Offline checks for the PX1 Codex runner. No real agents are started."""
import json
import sys
import tempfile
import unittest
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parents[1] / "tools"))
import px1_team_autorun as team


class TeamRunnerTests(unittest.TestCase):
    def test_status_reads_only_explicit_marker(self):
        with tempfile.TemporaryDirectory() as tmp:
            path = Path(tmp) / "checkpoint.md"
            self.assertEqual(team.status(path), "MISSING")
            path.write_text("# Report\nSTATUS: IN_PROGRESS\n", encoding="utf-8")
            self.assertEqual(team.status(path), "IN_PROGRESS")

    def test_command_enables_native_multiagent(self):
        cmd = team.command("codex", Path("last.txt"))
        self.assertEqual(cmd[0:4], ["codex", "exec", "--enable", "multi_agent"])
        self.assertIn("agents.max_threads=4", cmd)
        self.assertIn("agents.max_depth=1", cmd)
        self.assertIn("--json", cmd)
        self.assertIn("workspace-write", cmd)
        self.assertNotIn("danger-full-access", cmd)
        self.assertNotIn("--yolo", cmd)

    def test_count_only_observed_tool_call_items(self):
        events = [
            {"type": "item.started", "item": {"id": "s1", "type": "collab_tool_call", "tool": "spawn_agent"}},
            {"type": "item.completed", "item": {"id": "s1", "type": "collab_tool_call", "tool": "spawn_agent"}},
            {"type": "item.completed", "item": {"id": "s2", "type": "collab_tool_call", "tool": "send_message"}},
            {"type": "item.completed", "item": {"id": "s3", "type": "agent_message", "text": "spawn_agent"}},
        ]
        self.assertEqual(team.spawn_event_count("\n".join(map(json.dumps, events))), 1)

    def test_invalid_logs_do_not_crash(self):
        self.assertEqual(team.spawn_event_count("not json\n{}\n[]\nnull"), 0)

    def test_prompt_contains_active_project_constraints(self):
        text = team.prompt(1)
        for token in ("HOLD", "six-core", "SUBAGENTS_UNAVAILABLE", "PX1_TEAM_BRIEF.md"):
            self.assertIn(token, text)


if __name__ == "__main__":
    unittest.main()
