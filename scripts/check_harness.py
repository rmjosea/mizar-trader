"""Validate the agent harness, documentation integrity and code comments.

Checks what agents rely on but cannot see drift in: resolvable links, portable
skills and their tool-specific links, the backlog graph, spec states, decision
records, examples, agent settings and comment rules. Uses only
the standard library so it runs before any project tooling exists.
"""

from __future__ import annotations

import ast
import io
import json
import os
import re
import sys
import tokenize
from collections.abc import Callable, Iterator
from pathlib import Path

SKIP_DIRS = {
    ".git",
    ".work",
    "node_modules",
    ".venv",
    "__pycache__",
    ".pytest_cache",
    ".ruff_cache",
    ".mypy_cache",
}
LINK = re.compile(r"(?<!!)\[[^\]]*\]\(([^)\s]+)\)")
SKILL_NAME = re.compile(r"^[a-z0-9](?:[a-z0-9-]{0,62}[a-z0-9])?$")
PORTABLE_SKILL_KEYS = {
    "name",
    "description",
    "license",
    "compatibility",
    "metadata",
    "allowed-tools",
}
SPEC_STATES = {"draft", "approved", "done"}
BACKLOG_STATES = {"todo", "in-progress", "done"}
BACKLOG_GATES = {"—", "0", "1", "2", "3", "4", "5"}
AGENTS_MAX_LINES = 200
INSTRUCTION_FILES_THAT_DISABLE_AGENTS_MD = ("CLAUDE.md", ".claude/CLAUDE.md")

CODE_SUFFIXES = {
    ".py",
    ".ts",
    ".tsx",
    ".js",
    ".jsx",
    ".sql",
    ".sh",
    ".yml",
    ".yaml",
    ".toml",
}
HASH_COMMENT_SUFFIXES = {".sh", ".yml", ".yaml", ".toml"}
AI_AUTHOR = r"(?:Claude|Codex|ChatGPT|Copilot|GPT[-\w.]*|Gemini|an? (?:AI|LLM|agent|assistant)|AI)\b"
AUTHORSHIP_VERB = (
    r"(?:auto-?)?(?:generated|written|authored|created) (?:by|with|using) "
)
CODE_SUBJECT = r"(?:file|module|code|class|function|script)"
FORBIDDEN_IN_COMMENTS = [
    (re.compile(r"\b(?:SPEC|REQ|PLAN|TASK|OD|AC)-[A-Z0-9]"), "workflow ID"),
    (
        re.compile(
            r"\b(?:issue|pr|pull request|ticket|see|fixes|closes|resolves)\s*#\s*\d+|\bGH-\d+\b",
            re.IGNORECASE,
        ),
        "issue reference",
    ),
    (
        re.compile(
            r"co-authored-by|\bClaude Code\b|\bCodex\b"
            rf"|^\s*(?:#|//|--|/\*|\*)?\s*(?:this (?:{CODE_SUBJECT} )?)?(?:(?:was|is) )?{AUTHORSHIP_VERB}{AI_AUTHOR}"
            rf"|\b{CODE_SUBJECT} (?:was |is )?{AUTHORSHIP_VERB}{AI_AUTHOR}",
            re.IGNORECASE | re.MULTILINE,
        ),
        "agent attribution",
    ),
    (re.compile(r"\b(?:TODO|FIXME|XXX)\b"), "TODO marker (open a backlog item)"),
]
COMMENT_ONLY_FORBIDDEN = [
    (re.compile(r"^(?:#|//|--|/\*|\*)\s*[-=*#~_]{4,}"), "banner or divider comment"),
    (
        re.compile(r"^(?:#|//|--)\s*(?:step\s+)?\d+[.)]\s", re.IGNORECASE),
        "numbered step comment",
    ),
]
MAX_MODULE_DOCSTRING_LINES = 6


def walk_files(root: Path, suffixes: set[str]) -> Iterator[Path]:
    """Yield repository files with the given suffixes, never following symlinks."""
    for directory, dirnames, filenames in os.walk(root, followlinks=False):
        dirnames[:] = [
            d
            for d in dirnames
            if d not in SKIP_DIRS and not (Path(directory) / d).is_symlink()
        ]
        for filename in sorted(filenames):
            path = Path(directory) / filename
            if path.suffix in suffixes and not path.is_symlink():
                yield path


def parse_frontmatter(text: str) -> dict[str, str] | None:
    """Parse top-level `key: value` YAML frontmatter; return None when absent."""
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
    """Report relative Markdown links whose target does not exist."""
    errors: list[str] = []
    for path in walk_files(root, {".md"}):
        text = re.sub(
            r"```.*?```", "", path.read_text(encoding="utf-8"), flags=re.DOTALL
        )
        for target in LINK.findall(text):
            if re.match(r"^[a-z]+:", target) or target.startswith("#"):
                continue
            file_part = target.split("#", 1)[0]
            if "<" in file_part:
                continue  # Template placeholder written in angle brackets.
            if not (path.parent / file_part).exists():
                errors.append(f"{path.relative_to(root)}: broken link -> {target}")
    return errors


def skill_dirs(root: Path) -> list[Path]:
    """Return canonical skill directories under .agents/skills."""
    base = root / ".agents" / "skills"
    return (
        sorted(p for p in base.iterdir() if p.is_dir() and not p.name.startswith("."))
        if base.exists()
        else []
    )


def check_skills(root: Path) -> list[str]:
    """Validate each skill against the portable Agent Skills rules."""
    errors: list[str] = []
    for skill_dir in skill_dirs(root):
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
            errors.append(
                f"{rel}/SKILL.md: name '{name}' must equal the directory name"
            )
        if not SKILL_NAME.match(name) or "--" in name:
            errors.append(f"{rel}/SKILL.md: invalid name '{name}'")
        if not description or len(description) > 1024:
            errors.append(f"{rel}/SKILL.md: description must be 1-1024 characters")
        if re.match(r"^(I|You|We)\b", description):
            errors.append(
                f"{rel}/SKILL.md: description must be written in the third person"
            )
        extra = sorted(set(meta) - PORTABLE_SKILL_KEYS)
        if extra:
            errors.append(f"{rel}/SKILL.md: non-portable frontmatter keys {extra}")
        if len(text.splitlines()) > 500:
            errors.append(f"{rel}/SKILL.md: exceeds 500 lines")
    return errors


def check_skill_links(root: Path) -> list[str]:
    """Require one symlink in .claude/skills per canonical skill, and nothing else."""
    errors: list[str] = []
    claude_dir = root / ".claude" / "skills"
    canonical = {p.name for p in skill_dirs(root)}
    linked: set[str] = (
        {p.name for p in claude_dir.iterdir() if not p.name.startswith(".")}
        if claude_dir.exists()
        else set()
    )
    for name in sorted(canonical - linked):
        errors.append(f".claude/skills/{name}: missing link to .agents/skills/{name}")
    for name in sorted(linked):
        link = claude_dir / name
        target = root / ".agents" / "skills" / name
        if not link.is_symlink():
            errors.append(
                f".claude/skills/{name}: must be a symlink; keep skills in .agents/skills"
            )
        elif name not in canonical or link.resolve() != target.resolve():
            errors.append(
                f".claude/skills/{name}: symlink must point to ../../.agents/skills/{name}"
            )
    return errors


def check_subagents(root: Path) -> list[str]:
    """Validate subagent frontmatter and the skills they preload."""
    errors: list[str] = []
    agents_dir = root / ".claude" / "agents"
    for path in sorted(agents_dir.glob("*.md")) if agents_dir.exists() else []:
        rel = path.relative_to(root)
        text = path.read_text(encoding="utf-8")
        meta = parse_frontmatter(text)
        if meta is None or not meta.get("name") or not meta.get("description"):
            errors.append(f"{rel}: frontmatter needs name and description")
            continue
        header = text.split("\n---", 1)[0]
        block = re.search(
            r"^skills:\s*\n((?:\s+-\s+[\w-]+\s*\n?)+)", header, re.MULTILINE
        )
        for skill in re.findall(r"-\s+([\w-]+)", block.group(1)) if block else []:
            if not (root / ".agents" / "skills" / skill / "SKILL.md").exists():
                errors.append(f"{rel}: preloads unknown skill '{skill}'")
    return errors


def parse_backlog(text: str) -> list[dict[str, str]]:
    """Extract backlog rows from the Markdown task table."""
    rows: list[dict[str, str]] = []
    for line in text.splitlines():
        cells = [cell.strip() for cell in line.strip().strip("|").split("|")]
        if len(cells) == 7 and re.match(r"^[A-Z]\d{2}$", cells[0]):
            rows.append(
                {
                    "id": cells[0],
                    "depends": cells[2],
                    "gate": cells[3],
                    "status": cells[6],
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
    errors: list[str] = []
    ids = [row["id"] for row in rows]
    errors += [
        f"backlog: duplicate task {task}"
        for task in sorted({t for t in ids if ids.count(t) > 1})
    ]
    graph: dict[str, list[str]] = {}
    for row in rows:
        deps = (
            []
            if row["depends"] in {"—", "-", ""}
            else [d.strip() for d in row["depends"].split(",")]
        )
        graph[row["id"]] = deps
        errors += [
            f"backlog: {row['id']} depends on unknown {dep}"
            for dep in deps
            if dep not in ids
        ]
        if row["status"] not in BACKLOG_STATES:
            errors.append(f"backlog: {row['id']} has invalid status '{row['status']}'")
        if row["gate"] not in BACKLOG_GATES:
            errors.append(f"backlog: {row['id']} has invalid gate '{row['gate']}'")

    visiting: set[str] = set()
    finished: set[str] = set()

    def has_cycle(task: str) -> bool:
        if task in finished or task not in graph:
            return False
        if task in visiting:
            return True
        visiting.add(task)
        cyclic = any(has_cycle(dep) for dep in graph[task])
        visiting.discard(task)
        finished.add(task)
        return cyclic

    if any(has_cycle(task) for task in graph):
        errors.append("backlog: dependency cycle detected")
    return errors


def check_specs(root: Path) -> list[str]:
    """Check spec IDs, lifecycle states and their presence in the index."""
    errors: list[str] = []
    specs_dir = root / "specs"
    index_path = specs_dir / "README.md"
    index = index_path.read_text(encoding="utf-8") if index_path.exists() else ""
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
    """Require every decision record to declare its status."""
    errors: list[str] = []
    for adr in sorted((root / "docs" / "decisions").glob("[0-9][0-9][0-9][0-9]-*.md")):
        if not re.search(
            r"^- Status: (proposed|accepted|superseded|deprecated)",
            adr.read_text(encoding="utf-8"),
            re.MULTILINE,
        ):
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
    """Keep AGENTS.md loadable by every agent and agent attribution disabled."""
    errors: list[str] = []
    agents = root / "AGENTS.md"
    if not agents.exists():
        errors.append("AGENTS.md: missing")
    elif len(agents.read_text(encoding="utf-8").splitlines()) > AGENTS_MAX_LINES:
        errors.append(
            f"AGENTS.md: exceeds {AGENTS_MAX_LINES} lines; move detail to docs/ or a skill"
        )
    for name in INSTRUCTION_FILES_THAT_DISABLE_AGENTS_MD:
        if (root / name).exists():
            errors.append(
                f"{name}: remove it; its presence stops Claude Code from loading AGENTS.md"
            )
    settings = root / ".claude" / "settings.json"
    if settings.exists():
        try:
            config = json.loads(settings.read_text(encoding="utf-8"))
        except json.JSONDecodeError as exc:
            return errors + [f".claude/settings.json: invalid JSON ({exc.msg})"]
        attribution = config.get("attribution", {})
        if attribution.get("commit") != "" or attribution.get("pr") != "":
            errors.append(
                ".claude/settings.json: attribution.commit and attribution.pr must be empty strings"
            )
        if config.get("includeGitInstructions") is not False:
            errors.append(
                ".claude/settings.json: includeGitInstructions must be false; AGENTS.md owns git rules"
            )
    return errors


def python_comment_texts(path: Path) -> list[tuple[int, str, bool]]:
    """Return comments and docstrings of a Python file as (line, text, is_comment)."""
    source = path.read_text(encoding="utf-8")
    texts = [
        (token.start[0], token.string, True)
        for token in tokenize.generate_tokens(io.StringIO(source).readline)
        if token.type == tokenize.COMMENT
    ]
    for node in ast.walk(ast.parse(source)):
        if isinstance(
            node, ast.Module | ast.ClassDef | ast.FunctionDef | ast.AsyncFunctionDef
        ):
            docstring = ast.get_docstring(node, clean=False)
            if docstring:
                texts.append((getattr(node, "lineno", 1), docstring, False))
    return texts


def other_comment_texts(path: Path) -> list[tuple[int, str, bool]]:
    """Return comment lines of non-Python source files."""
    if path.suffix in HASH_COMMENT_SUFFIXES:
        markers: tuple[str, ...] = ("#",)
    elif path.suffix == ".sql":
        markers = ("--",)
    else:
        markers = ("//", "/*", "*")
    texts: list[tuple[int, str, bool]] = []
    for number, line in enumerate(
        path.read_text(encoding="utf-8").splitlines(), start=1
    ):
        stripped = line.strip()
        if stripped.startswith(markers) and not stripped.startswith("#!"):
            texts.append((number, stripped, True))
    return texts


def backlog_id_pattern(root: Path) -> re.Pattern[str] | None:
    """Build a pattern matching the backlog task IDs that exist today."""
    path = root / "docs" / "delivery" / "01-backlog.md"
    ids = (
        [row["id"] for row in parse_backlog(path.read_text(encoding="utf-8"))]
        if path.exists()
        else []
    )
    return re.compile(r"\b(?:" + "|".join(ids) + r")\b") if ids else None


def check_code_comments(root: Path) -> list[str]:
    """Enforce the code-documentation prohibitions on comments and docstrings."""
    errors: list[str] = []
    backlog_ids = backlog_id_pattern(root)
    for path in walk_files(root, CODE_SUFFIXES):
        rel = path.relative_to(root)
        try:
            texts = (
                python_comment_texts(path)
                if path.suffix == ".py"
                else other_comment_texts(path)
            )
        except (SyntaxError, UnicodeDecodeError, tokenize.TokenError) as exc:
            errors.append(f"{rel}: cannot parse ({type(exc).__name__})")
            continue
        for line, text, is_comment in texts:
            rules = FORBIDDEN_IN_COMMENTS + (
                COMMENT_ONLY_FORBIDDEN if is_comment else []
            )
            if backlog_ids:
                rules = [*rules, (backlog_ids, "backlog task ID")]
            for pattern, label in rules:
                if pattern.search(text):
                    errors.append(f"{rel}:{line}: {label} in a comment or docstring")
        if path.suffix == ".py":
            module_doc = ast.get_docstring(ast.parse(path.read_text(encoding="utf-8")))
            if (
                module_doc
                and len(module_doc.strip().splitlines()) > MAX_MODULE_DOCSTRING_LINES
            ):
                errors.append(
                    f"{rel}: module docstring exceeds {MAX_MODULE_DOCSTRING_LINES} lines"
                )
    return errors


def check_docs_index(root: Path) -> list[str]:
    """Require every document in docs/ to be listed in docs/README.md."""
    index_path = root / "docs" / "README.md"
    if not index_path.exists():
        return ["docs/README.md: missing documentation index"]
    targets = LINK.findall(index_path.read_text(encoding="utf-8"))
    listed = {
        (index_path.parent / target.split("#", 1)[0]).resolve() for target in targets
    }
    return [
        f"{path.relative_to(root)}: not listed in docs/README.md"
        for path in walk_files(root / "docs", {".md"})
        if path != index_path and path.resolve() not in listed
    ]


CHECKS: tuple[Callable[[Path], list[str]], ...] = (
    check_links,
    check_skills,
    check_skill_links,
    check_subagents,
    check_backlog,
    check_specs,
    check_decisions,
    check_examples,
    check_agent_contract,
    check_code_comments,
    check_docs_index,
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
