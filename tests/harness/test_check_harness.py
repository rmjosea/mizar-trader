"""Tests for the repository harness validator."""

from __future__ import annotations

import importlib.util
import json
import os
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
VALID_SETTINGS = {"attribution": {"commit": "", "pr": ""}, "includeGitInstructions": False}


def write(root: Path, relative: str, content: str) -> Path:
    """Create a file with parent directories inside a temporary repository."""
    path = root / relative
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(content, encoding="utf-8")
    return path


def add_skill(root: Path, name: str, frontmatter: str | None = None, link: bool = True) -> None:
    """Create a canonical skill and, optionally, its .claude/skills symlink."""
    body = frontmatter if frontmatter is not None else f"name: {name}\ndescription: Does a thing. Use when needed."
    write(root, f".agents/skills/{name}/SKILL.md", f"---\n{body}\n---\n# Title\n")
    if link:
        (root / ".claude" / "skills").mkdir(parents=True, exist_ok=True)
        os.symlink(f"../../.agents/skills/{name}", root / ".claude" / "skills" / name)


class RepositoryTest(unittest.TestCase):
    def test_current_repository_passes(self) -> None:
        self.assertEqual(check_harness.run(REPO), [])


class CheckTest(unittest.TestCase):
    def setUp(self) -> None:
        self._tmp = tempfile.TemporaryDirectory()
        self.root = Path(self._tmp.name)

    def tearDown(self) -> None:
        self._tmp.cleanup()

    def assertReports(self, errors: list[str], fragment: str) -> None:
        self.assertTrue(any(fragment in error for error in errors), f"'{fragment}' not in {errors}")

    def test_broken_relative_link_is_reported(self) -> None:
        write(self.root, "docs/a.md", "[x](missing.md) [ok](https://example.com) [t](<ID>-x/spec.md)")
        errors = check_harness.check_links(self.root)
        self.assertEqual(len(errors), 1)
        self.assertReports(errors, "missing.md")

    def test_links_inside_code_fences_are_ignored(self) -> None:
        write(self.root, "a.md", "```\n[x](missing.md)\n```\n")
        self.assertEqual(check_harness.check_links(self.root), [])

    def test_valid_skill_and_link_pass(self) -> None:
        add_skill(self.root, "good-name")
        self.assertEqual(check_harness.check_skills(self.root), [])
        self.assertEqual(check_harness.check_skill_links(self.root), [])

    def test_skill_name_must_match_directory(self) -> None:
        add_skill(self.root, "good-name", "name: other\ndescription: Does a thing.")
        self.assertReports(check_harness.check_skills(self.root), "directory name")

    def test_skill_without_description_is_reported(self) -> None:
        add_skill(self.root, "a", "name: a")
        self.assertReports(check_harness.check_skills(self.root), "description")

    def test_skill_description_must_be_third_person(self) -> None:
        add_skill(self.root, "a", "name: a\ndescription: You can use this to do things.")
        self.assertReports(check_harness.check_skills(self.root), "third person")

    def test_non_portable_skill_keys_are_reported(self) -> None:
        add_skill(self.root, "a", "name: a\ndescription: Does a thing.\ndisable-model-invocation: true")
        self.assertReports(check_harness.check_skills(self.root), "non-portable")

    def test_missing_claude_skill_link_is_reported(self) -> None:
        add_skill(self.root, "a", link=False)
        self.assertReports(check_harness.check_skill_links(self.root), "missing link")

    def test_real_directory_in_claude_skills_is_reported(self) -> None:
        add_skill(self.root, "a", link=False)
        write(self.root, ".claude/skills/a/SKILL.md", "copy")
        self.assertReports(check_harness.check_skill_links(self.root), "must be a symlink")

    def test_subagent_preloading_unknown_skill_is_reported(self) -> None:
        write(self.root, ".claude/agents/r.md", "---\nname: r\ndescription: d\nskills:\n  - ghost\n---\nbody\n")
        self.assertReports(check_harness.check_subagents(self.root), "ghost")

    def test_subagent_tools_list_is_not_mistaken_for_skills(self) -> None:
        add_skill(self.root, "review")
        agent = "---\nname: r\ndescription: d\ntools:\n  - Read\nskills:\n  - review\n---\nbody\n"
        write(self.root, ".claude/agents/r.md", agent)
        self.assertEqual(check_harness.check_subagents(self.root), [])

    def test_backlog_unknown_dependency_and_cycle(self) -> None:
        rows = (
            "| A01 | a | B01 | 0 | low | x | y | todo |\n"
            "| B01 | b | A01 | 0 | low | x | y | todo |\n"
            "| C01 | c | Z99 | 0 | low | x | y | todo |\n"
        )
        write(self.root, "docs/delivery/01-backlog.md", BACKLOG_HEADER + rows)
        errors = check_harness.check_backlog(self.root)
        self.assertReports(errors, "unknown Z99")
        self.assertReports(errors, "cycle")

    def test_backlog_invalid_status_and_risk(self) -> None:
        write(self.root, "docs/delivery/01-backlog.md", BACKLOG_HEADER + "| A01 | a | — | 0 | extreme | x | y | started |\n")
        errors = check_harness.check_backlog(self.root)
        self.assertReports(errors, "status")
        self.assertReports(errors, "risk")

    def test_spec_must_match_task_and_be_indexed(self) -> None:
        write(self.root, "specs/README.md", "# index\n")
        write(self.root, "specs/F02-schemas/spec.md", "---\nid: SPEC-F03\nstatus: done\n---\n")
        errors = check_harness.check_specs(self.root)
        self.assertReports(errors, "id must be SPEC-F02")
        self.assertReports(errors, "invalid status")
        self.assertReports(errors, "missing from specs/README.md")

    def test_adr_without_status_is_reported(self) -> None:
        write(self.root, "docs/decisions/0001-x.md", "# ADR\n")
        self.assertEqual(len(check_harness.check_decisions(self.root)), 1)

    def test_abstain_with_zero_weight_is_rejected(self) -> None:
        write(self.root, "examples/decision.json", json.dumps({"action": "ABSTAIN", "target_weight": 0}))
        self.assertEqual(len(check_harness.check_examples(self.root)), 1)

    def test_target_without_weight_is_rejected(self) -> None:
        write(self.root, "examples/decision.json", json.dumps({"action": "TARGET", "target_weight": None}))
        self.assertEqual(len(check_harness.check_examples(self.root)), 1)

    def test_valid_agent_contract_passes(self) -> None:
        write(self.root, "AGENTS.md", "# contract\n")
        write(self.root, ".claude/settings.json", json.dumps(VALID_SETTINGS))
        self.assertEqual(check_harness.check_agent_contract(self.root), [])

    def test_claude_md_is_reported_because_it_disables_agents_md(self) -> None:
        write(self.root, "AGENTS.md", "# contract\n")
        write(self.root, "CLAUDE.md", "@AGENTS.md\n")
        self.assertReports(check_harness.check_agent_contract(self.root), "stops Claude Code from loading AGENTS.md")

    def test_agent_attribution_must_be_disabled(self) -> None:
        write(self.root, "AGENTS.md", "# contract\n")
        settings = {"attribution": {"commit": "Co-Authored-By: x", "pr": ""}, "includeGitInstructions": False}
        write(self.root, ".claude/settings.json", json.dumps(settings))
        self.assertReports(check_harness.check_agent_contract(self.root), "attribution")

    def test_builtin_git_instructions_must_be_disabled(self) -> None:
        write(self.root, "AGENTS.md", "# contract\n")
        write(self.root, ".claude/settings.json", json.dumps({"attribution": {"commit": "", "pr": ""}}))
        self.assertReports(check_harness.check_agent_contract(self.root), "includeGitInstructions")

    def test_oversized_agents_md_is_reported(self) -> None:
        write(self.root, "AGENTS.md", "line\n" * (check_harness.AGENTS_MAX_LINES + 1))
        self.assertReports(check_harness.check_agent_contract(self.root), "exceeds")

    def test_workflow_id_in_python_comment_is_reported(self) -> None:
        write(self.root, "src/a.py", '"""Module."""\n\nX = 1  # Implements REQ-001.\n')
        self.assertReports(check_harness.check_code_comments(self.root), "workflow ID")

    def test_attribution_in_docstring_is_reported(self) -> None:
        write(self.root, "src/a.py", '"""Module generated by an agent."""\n')
        self.assertReports(check_harness.check_code_comments(self.root), "agent attribution")

    def test_todo_in_yaml_comment_is_reported(self) -> None:
        write(self.root, "config/a.yaml", "# TODO tune this\nkey: 1\n")
        self.assertReports(check_harness.check_code_comments(self.root), "TODO")

    def test_workflow_id_inside_string_literal_is_allowed(self) -> None:
        write(self.root, "src/a.py", '"""Module."""\n\nPATTERN = "SPEC-F02"\n')
        self.assertEqual(check_harness.check_code_comments(self.root), [])

    def test_model_provider_name_in_adapter_comment_is_allowed(self) -> None:
        write(self.root, "src/adapter.py", '"""Anthropic model adapter."""\n\n# Claude returns a stop reason per message.\n')
        self.assertEqual(check_harness.check_code_comments(self.root), [])

    def test_long_module_docstring_is_reported(self) -> None:
        write(self.root, "src/a.py", '"""Summary.\n\n' + "Line.\n" * 7 + '"""\n')
        self.assertReports(check_harness.check_code_comments(self.root), "module docstring")


if __name__ == "__main__":
    unittest.main()
