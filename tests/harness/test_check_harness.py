"""Tests for the repository harness validator."""

from __future__ import annotations

import importlib.util
import json
import tempfile
import unittest
from pathlib import Path

REPO = Path(__file__).resolve().parents[2]
_spec = importlib.util.spec_from_file_location("check_harness", REPO / "scripts" / "check_harness.py")
check_harness = importlib.util.module_from_spec(_spec)
_spec.loader.exec_module(check_harness)

BACKLOG_HEADER = (
    "| ID | Outcome | Depends | Gate | Risk | Domain | Acceptance | Status |\n"
    "|---|---|---|---|---|---|---|---|\n"
)


def write(root: Path, relative: str, content: str) -> None:
    """Create a file with parent directories inside a temporary repository."""
    path = root / relative
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(content, encoding="utf-8")


class RepositoryTest(unittest.TestCase):
    def test_current_repository_passes(self) -> None:
        self.assertEqual(check_harness.run(REPO), [])


class CheckTest(unittest.TestCase):
    def setUp(self) -> None:
        self._tmp = tempfile.TemporaryDirectory()
        self.root = Path(self._tmp.name)

    def tearDown(self) -> None:
        self._tmp.cleanup()

    def test_broken_relative_link_is_reported(self) -> None:
        write(self.root, "docs/a.md", "[x](missing.md) [ok](https://example.com) [t](<ID>-x/spec.md)")
        errors = check_harness.check_links(self.root)
        self.assertEqual(len(errors), 1)
        self.assertIn("missing.md", errors[0])

    def test_links_inside_code_fences_are_ignored(self) -> None:
        write(self.root, "a.md", "```\n[x](missing.md)\n```\n")
        self.assertEqual(check_harness.check_links(self.root), [])

    def test_skill_name_must_match_directory(self) -> None:
        write(self.root, ".claude/skills/good-name/SKILL.md", "---\nname: other\ndescription: d\n---\n")
        self.assertTrue(any("directory name" in e for e in check_harness.check_skills(self.root)))

    def test_skill_without_description_is_reported(self) -> None:
        write(self.root, ".claude/skills/a/SKILL.md", "---\nname: a\n---\n")
        self.assertTrue(any("description" in e for e in check_harness.check_skills(self.root)))

    def test_agent_preloading_unknown_skill_is_reported(self) -> None:
        write(self.root, ".claude/agents/r.md", "---\nname: r\ndescription: d\nskills:\n  - ghost\n---\nbody\n")
        self.assertTrue(any("ghost" in e for e in check_harness.check_agents(self.root)))

    def test_agent_tools_list_is_not_mistaken_for_skills(self) -> None:
        write(self.root, ".claude/skills/review/SKILL.md", "---\nname: review\ndescription: d\n---\n")
        agent = "---\nname: r\ndescription: d\ntools:\n  - Read\nskills:\n  - review\n---\nbody\n"
        write(self.root, ".claude/agents/r.md", agent)
        self.assertEqual(check_harness.check_agents(self.root), [])

    def test_backlog_unknown_dependency_and_cycle(self) -> None:
        rows = (
            "| A01 | a | B01 | 0 | low | x | y | todo |\n"
            "| B01 | b | A01 | 0 | low | x | y | todo |\n"
            "| C01 | c | Z99 | 0 | low | x | y | todo |\n"
        )
        write(self.root, "docs/delivery/01-backlog.md", BACKLOG_HEADER + rows)
        errors = check_harness.check_backlog(self.root)
        self.assertTrue(any("unknown Z99" in e for e in errors))
        self.assertTrue(any("cycle" in e for e in errors))

    def test_backlog_invalid_status_and_risk(self) -> None:
        write(self.root, "docs/delivery/01-backlog.md", BACKLOG_HEADER + "| A01 | a | — | 0 | extreme | x | y | started |\n")
        errors = check_harness.check_backlog(self.root)
        self.assertTrue(any("status" in e for e in errors))
        self.assertTrue(any("risk" in e for e in errors))

    def test_spec_must_match_task_and_be_indexed(self) -> None:
        write(self.root, "specs/README.md", "# index\n")
        write(self.root, "specs/F02-schemas/spec.md", "---\nid: SPEC-F03\nstatus: done\n---\n")
        errors = check_harness.check_specs(self.root)
        self.assertTrue(any("SPEC-F02" in e and "id" in e for e in errors))
        self.assertTrue(any("invalid status" in e for e in errors))
        self.assertTrue(any("missing from specs/README.md" in e for e in errors))

    def test_adr_without_status_is_reported(self) -> None:
        write(self.root, "docs/decisions/0001-x.md", "# ADR\n")
        self.assertEqual(len(check_harness.check_decisions(self.root)), 1)

    def test_abstain_with_zero_weight_is_rejected(self) -> None:
        write(self.root, "examples/decision.json", json.dumps({"action": "ABSTAIN", "target_weight": 0}))
        self.assertEqual(len(check_harness.check_examples(self.root)), 1)

    def test_target_without_weight_is_rejected(self) -> None:
        write(self.root, "examples/decision.json", json.dumps({"action": "TARGET", "target_weight": None}))
        self.assertEqual(len(check_harness.check_examples(self.root)), 1)

    def test_agent_attribution_must_be_disabled(self) -> None:
        write(self.root, "AGENTS.md", "# contract\n")
        write(self.root, ".claude/settings.json", json.dumps({"attribution": {"commit": "Co-Authored-By: x"}}))
        errors = check_harness.check_agent_contract(self.root)
        self.assertTrue(any("attribution" in e for e in errors))

    def test_oversized_agents_md_is_reported(self) -> None:
        write(self.root, "AGENTS.md", "line\n" * (check_harness.AGENTS_MAX_LINES + 1))
        self.assertTrue(any("exceeds" in e for e in check_harness.check_agent_contract(self.root)))


if __name__ == "__main__":
    unittest.main()
