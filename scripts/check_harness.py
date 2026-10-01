"""Validate the agentic-delivery harness and documentation integrity.

Checks the invariants that agents rely on but cannot see drift in: resolvable
links, well-formed skills and subagents, a consistent backlog graph, spec
lifecycle states, ADR status, example contracts and human-only attribution.
Uses only the standard library so it runs before any project tooling exists.
"""

from __future__ import annotations

import json
import re
import sys
from pathlib import Path

SKIP_DIRS = {".git", ".work", "node_modules", ".venv", "__pycache__"}
LINK = re.compile(r"(?<!!)\[[^\]]*\]\(([^)\s]+)\)")
SKILL_NAME = re.compile(r"^[a-z0-9](?:[a-z0-9-]{0,62}[a-z0-9])?$")
SPEC_STATES = {"draft", "approved", "planned", "implemented", "verified"}
BACKLOG_STATES = {"todo", "in-progress", "done"}
BACKLOG_RISKS = {"low", "medium", "high"}
AGENTS_MAX_LINES = 200


def markdown_files(root: Path) -> list[Path]:
    """Return repository Markdown files outside ignored directories."""
    return sorted(
        path
        for path in root.rglob("*.md")
        if not SKIP_DIRS.intersection(path.relative_to(root).parts)
    )


def parse_frontmatter(text: str) -> dict[str, str] | None:
    """Parse flat `key: value` YAML frontmatter; return None when absent."""
    if not text.startswith("---\n"):
        return None
    end = text.find("\n---", 4)
    if end == -1:
        return None
    fields: dict[str, str] = {}
    for line in text[4:end].splitlines():
        match = re.match(r"^([A-Za-z_][\w-]*):\s*(.*)$", line)
        if match:
            fields[match.group(1)] = match.group(2).strip()
    return fields


def check_links(root: Path) -> list[str]:
    """Report relative Markdown links whose target file does not exist."""
    errors = []
    for path in markdown_files(root):
        text = re.sub(r"```.*?```", "", path.read_text(encoding="utf-8"), flags=re.DOTALL)
        for target in LINK.findall(text):
            if re.match(r"^[a-z]+:", target) or target.startswith("#"):
                continue
            file_part = target.split("#", 1)[0]
            if "<" in file_part:
                continue  # Template placeholder, e.g. <TASK-ID>-<slug>/spec.md.
            if not (path.parent / file_part).exists():
                errors.append(f"{path.relative_to(root)}: broken link -> {target}")
    return errors


def check_skills(root: Path) -> list[str]:
    """Validate each skill against the Agent Skills metadata rules."""
    errors = []
    skills_dir = root / ".claude" / "skills"
    for skill_dir in sorted(p for p in skills_dir.iterdir() if p.is_dir()) if skills_dir.exists() else []:
        rel = skill_dir.relative_to(root)
        skill_file = skill_dir / "SKILL.md"
        if not skill_file.exists():
            errors.append(f"{rel}: missing SKILL.md")
            continue
        text = skill_file.read_text(encoding="utf-8")
        meta = parse_frontmatter(text)
        if meta is None:
            errors.append(f"{rel}/SKILL.md: missing frontmatter")
            continue
        name, description = meta.get("name", ""), meta.get("description", "")
        if name != skill_dir.name:
            errors.append(f"{rel}/SKILL.md: name '{name}' must equal directory name")
        if not SKILL_NAME.match(name) or "--" in name:
            errors.append(f"{rel}/SKILL.md: invalid name '{name}'")
        if not description or len(description) > 1024:
            errors.append(f"{rel}/SKILL.md: description must be 1-1024 characters")
        if len(text.splitlines()) > 500:
            errors.append(f"{rel}/SKILL.md: exceeds 500 lines")
    return errors


def check_agents(root: Path) -> list[str]:
    """Validate subagent frontmatter and the skills they preload."""
    errors = []
    agents_dir = root / ".claude" / "agents"
    for path in sorted(agents_dir.glob("*.md")) if agents_dir.exists() else []:
        rel = path.relative_to(root)
        text = path.read_text(encoding="utf-8")
        meta = parse_frontmatter(text)
        if meta is None or not meta.get("name") or not meta.get("description"):
            errors.append(f"{rel}: frontmatter needs name and description")
            continue
        header = text.split("\n---", 1)[0]
        block = re.search(r"^skills:\s*\n((?:\s+-\s+[\w-]+\s*\n?)+)", header, re.MULTILINE)
        for skill in re.findall(r"-\s+([\w-]+)", block.group(1)) if block else []:
            if not (root / ".claude" / "skills" / skill / "SKILL.md").exists():
                errors.append(f"{rel}: preloads unknown skill '{skill}'")
    return errors


def parse_backlog(text: str) -> list[dict[str, str]]:
    """Extract backlog rows from the Markdown task table."""
    rows = []
    for line in text.splitlines():
        cells = [cell.strip() for cell in line.strip().strip("|").split("|")]
        if len(cells) == 8 and re.match(r"^[A-Z]\d{2}$", cells[0]):
            rows.append(
                {
                    "id": cells[0],
                    "depends": cells[2],
                    "gate": cells[3],
                    "risk": cells[4],
                    "status": cells[7],
                }
            )
    return rows


def check_backlog(root: Path) -> list[str]:
    """Check backlog IDs, dependencies, states and the absence of cycles."""
    path = root / "docs" / "delivery" / "01-backlog.md"
    if not path.exists():
        return ["docs/delivery/01-backlog.md: missing"]
    rows = parse_backlog(path.read_text(encoding="utf-8"))
    if not rows:
        return ["docs/delivery/01-backlog.md: no tasks found"]
    errors = []
    ids = [row["id"] for row in rows]
    duplicates = {task for task in ids if ids.count(task) > 1}
    errors += [f"backlog: duplicate task {task}" for task in sorted(duplicates)]
    graph: dict[str, list[str]] = {}
    for row in rows:
        deps = [] if row["depends"] in {"—", "-", ""} else [d.strip() for d in row["depends"].split(",")]
        graph[row["id"]] = deps
        errors += [f"backlog: {row['id']} depends on unknown {dep}" for dep in deps if dep not in ids]
        if row["status"] not in BACKLOG_STATES:
            errors.append(f"backlog: {row['id']} has invalid status '{row['status']}'")
        if row["risk"] not in BACKLOG_RISKS:
            errors.append(f"backlog: {row['id']} has invalid risk '{row['risk']}'")
        if row["gate"] not in {"—", "0", "1", "2", "3", "4", "5"}:
            errors.append(f"backlog: {row['id']} has invalid gate '{row['gate']}'")

    visiting, done = set(), set()

    def visit(task: str) -> bool:
        if task in done or task not in graph:
            return False
        if task in visiting:
            return True
        visiting.add(task)
        cyclic = any(visit(dep) for dep in graph[task])
        visiting.discard(task)
        done.add(task)
        return cyclic

    if any(visit(task) for task in graph):
        errors.append("backlog: dependency cycle detected")
    return errors


def check_specs(root: Path) -> list[str]:
    """Check spec IDs, lifecycle states and their presence in the index."""
    errors = []
    specs_dir = root / "specs"
    index = (specs_dir / "README.md").read_text(encoding="utf-8") if (specs_dir / "README.md").exists() else ""
    for spec in sorted(specs_dir.glob("*/spec.md")) if specs_dir.exists() else []:
        rel = spec.relative_to(root)
        task_id = spec.parent.name.split("-", 1)[0]
        meta = parse_frontmatter(spec.read_text(encoding="utf-8")) or {}
        if meta.get("id") != f"SPEC-{task_id}":
            errors.append(f"{rel}: id must be SPEC-{task_id}")
        if meta.get("status") not in SPEC_STATES:
            errors.append(f"{rel}: invalid status '{meta.get('status')}'")
        if f"SPEC-{task_id}" not in index:
            errors.append(f"{rel}: missing from specs/README.md")
    return errors


def check_decisions(root: Path) -> list[str]:
    """Require every ADR to declare its status."""
    errors = []
    for adr in sorted((root / "docs" / "decisions").glob("[0-9][0-9][0-9][0-9]-*.md")):
        if not re.search(r"^- Status: (proposed|accepted|superseded|deprecated)", adr.read_text(encoding="utf-8"), re.MULTILINE):
            errors.append(f"{adr.relative_to(root)}: missing '- Status:' line")
    return errors


def check_examples(root: Path) -> list[str]:
    """Check the example decision against the Decision contract rules."""
    path = root / "examples" / "decision.json"
    if not path.exists():
        return []
    try:
        decision = json.loads(path.read_text(encoding="utf-8"))
    except json.JSONDecodeError as exc:
        return [f"examples/decision.json: invalid JSON ({exc.msg})"]
    action, weight = decision.get("action"), decision.get("target_weight")
    if action not in {"TARGET", "HOLD", "ABSTAIN"}:
        return [f"examples/decision.json: invalid action '{action}'"]
    if action == "TARGET" and weight is None:
        return ["examples/decision.json: TARGET requires target_weight"]
    if action != "TARGET" and weight is not None:
        return [f"examples/decision.json: {action} must have target_weight null"]
    return []


def check_agent_contract(root: Path) -> list[str]:
    """Keep AGENTS.md within budget and attribution disabled for agents."""
    errors = []
    agents = root / "AGENTS.md"
    if not agents.exists():
        errors.append("AGENTS.md: missing")
    elif len(agents.read_text(encoding="utf-8").splitlines()) > AGENTS_MAX_LINES:
        errors.append(f"AGENTS.md: exceeds {AGENTS_MAX_LINES} lines; move detail to docs/")
    settings = root / ".claude" / "settings.json"
    if settings.exists():
        try:
            attribution = json.loads(settings.read_text(encoding="utf-8")).get("attribution", {})
        except json.JSONDecodeError as exc:
            return errors + [f".claude/settings.json: invalid JSON ({exc.msg})"]
        if attribution.get("commit") != "" or attribution.get("pr") != "":
            errors.append(".claude/settings.json: attribution.commit and attribution.pr must be empty strings")
    return errors


CHECKS = (
    check_links,
    check_skills,
    check_agents,
    check_backlog,
    check_specs,
    check_decisions,
    check_examples,
    check_agent_contract,
)


def run(root: Path) -> list[str]:
    """Run every check against a repository root and collect the errors."""
    return [error for check in CHECKS for error in check(root)]


def main() -> int:
    """Print harness errors and return a process exit code."""
    root = Path(__file__).resolve().parent.parent
    errors = run(root)
    for error in errors:
        print(f"ERROR {error}")
    print(f"check_harness: {len(errors)} error(s) across {len(CHECKS)} checks")
    return 1 if errors else 0


if __name__ == "__main__":
    sys.exit(main())
