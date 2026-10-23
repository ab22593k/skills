#!/usr/bin/env python3
"""Validate the linux-kernel-map package shape, budgets, and eval schema."""

from __future__ import annotations

import argparse
import json
import math
import re
from pathlib import Path

SECRET_PATTERNS = [
    re.compile(r"sk-[A-Za-z0-9]{20,}"),
    re.compile(r"ghp_[A-Za-z0-9]{20,}"),
    re.compile(r"AKIA[0-9A-Z]{16}"),
    re.compile(r"-----BEGIN (?:RSA |EC |OPENSSH |)PRIVATE KEY-----"),
    re.compile(r"(?i)(?:password|api[_-]?key|secret)\s*[:=]\s*\S+"),
]
ABSOLUTE_PATTERNS = [
    re.compile(r"/home/\w"),
    re.compile(r"/usr/(?:local|bin|lib)"),
    re.compile(r"/tmp/"),  # noqa: S108
    re.compile(r"/opt/"),
    re.compile(r"/etc/"),
    re.compile(r"/var/"),
    re.compile(r"/root/"),
    re.compile(r"[A-Za-z]:\\"),
]
FRONTMATTER_RE = re.compile(r"^---\s*\n(.*?)\n---\s*\n", re.DOTALL)
LINK_RE = re.compile(r"\[[^\]]*\]\(([^)]+)\)")
NAME_RE = re.compile(r"^[a-z0-9]+(?:-[a-z0-9]+)*$")
OBSERVATION_COLUMNS = ("mechanism", "config", "availability", "invas", "fallback")


def parse_frontmatter(text: str) -> dict[str, str]:
    match = FRONTMATTER_RE.match(text)
    if not match:
        raise ValueError("SKILL.md is missing YAML frontmatter")
    data: dict[str, str] = {}
    for raw in match.group(1).splitlines():
        if ":" not in raw:
            continue
        key, _, value = raw.partition(":")
        value = value.strip()
        if len(value) >= 2 and value[0] == value[-1] and value[0] in "\"'":
            value = value[1:-1]
        data[key.strip()] = value
    return data


def fail(msg: str) -> None:
    print(f"FAIL: {msg}")


def check_package(package: Path) -> int:
    errors: list[str] = []
    skill_md = package / "SKILL.md"
    if not skill_md.is_file():
        print("FAIL: SKILL.md not found")
        return 1
    text = skill_md.read_text(encoding="utf-8")
    try:
        fm = parse_frontmatter(text)
    except ValueError as exc:
        print(f"FAIL: {exc}")
        return 1

    # Frontmatter
    if fm.get("name") != package.name:
        errors.append(f"name '{fm.get('name')}' does not match directory '{package.name}'")
    name = fm.get("name", "")
    if not (1 <= len(name) <= 64) or not NAME_RE.match(name):
        errors.append("name must be 1-64 lowercase letters, numbers, and hyphens")
    description = fm.get("description", "")
    if not (1 <= len(description) <= 1024):
        errors.append(f"description length {len(description)} outside 1-1024")
    if "license" not in fm:
        errors.append("license is missing from frontmatter")

    # Budgets
    lines = text.splitlines()
    if len(lines) > 500:
        errors.append(f"SKILL.md has {len(lines)} lines, limit 500")
    token_estimate = math.ceil(len(text.encode("utf-8")) / 4)
    if token_estimate >= 5000:
        errors.append(f"SKILL.md estimated tokens {token_estimate}, limit < 5000")

    # Absolute paths and secrets
    for pattern in ABSOLUTE_PATTERNS:
        if pattern.search(text):
            errors.append(f"absolute path pattern found: {pattern.pattern}")
    for pattern in SECRET_PATTERNS:
        if pattern.search(text):
            errors.append(f"secret-like value found: {pattern.pattern}")
    for ref_file in package.rglob("*"):
        if ref_file.is_file() and ref_file.suffix in {".md", ".json", ".py"}:
            content = ref_file.read_text(encoding="utf-8", errors="replace")
            for pattern in SECRET_PATTERNS:
                if pattern.search(content):
                    errors.append(f"secret-like value in {ref_file.relative_to(package)}")

    # References one level deep
    for link in LINK_RE.findall(text):
        if link.startswith(("http://", "https://", "#", "mailto:")):
            continue
        target = (package / link).resolve()
        try:
            target.relative_to(package.resolve())
        except ValueError:
            errors.append(f"reference escapes package: {link}")
            continue
        if not target.exists():
            errors.append(f"referenced file does not exist: {link}")
            continue
        # one level below SKILL.md
        rel = target.relative_to(package.resolve())
        if len(rel.parts) != 2:
            errors.append(f"reference not one level deep: {link}")

    # Attribution
    lower = text.lower()
    if "linux kernel map" not in lower or "inspiration" not in lower:
        errors.append("inspiration credit for the Linux Kernel Map is missing")

    # evals schema
    evals_path = package / "evals" / "evals.json"
    if not evals_path.is_file():
        errors.append("evals/evals.json is missing")
    else:
        try:
            evals = json.loads(evals_path.read_text(encoding="utf-8"))
        except json.JSONDecodeError as exc:
            errors.append(f"evals/evals.json invalid JSON: {exc}")
            evals = {}
        if evals.get("skill_name") != "linux-kernel-map":
            errors.append("evals skill_name must be 'linux-kernel-map'")
        cases = evals.get("evals", [])
        if not isinstance(cases, list) or len(cases) < 12:
            errors.append(f"evals must contain at least 12 cases, found {len(cases) if isinstance(cases, list) else 0}")
        for case in cases if isinstance(cases, list) else []:
            if not isinstance(case.get("id"), int):
                errors.append(f"eval case missing integer id: {case}")
            if not isinstance(case.get("prompt"), str) or len(case.get("prompt", "")) < 20:
                errors.append(f"eval {case.get('id')} has invalid prompt")
            if not isinstance(case.get("expected_output"), str) or len(case.get("expected_output", "")) < 20:
                errors.append(f"eval {case.get('id')} has invalid expected_output")
            exps = case.get("expectations")
            if not isinstance(exps, list) or not exps:
                errors.append(f"eval {case.get('id')} has no expectations")
            for f in case.get("files", []) or []:
                if not isinstance(f, str) or f.startswith("/") or ".." in f.split("/"):
                    errors.append(f"eval {case.get('id')} has invalid file path: {f}")
                elif not (package / f).exists():
                    errors.append(f"eval {case.get('id')} references missing file: {f}")
        # trigger queries
        tq_path = package / "evals" / "trigger_queries.json"
        if tq_path.is_file():
            try:
                tq = json.loads(tq_path.read_text(encoding="utf-8"))
            except json.JSONDecodeError as exc:
                errors.append(f"trigger_queries.json invalid JSON: {exc}")
                tq = []
            if not isinstance(tq, list) or len(tq) < 16:
                errors.append(f"trigger_queries must contain at least 16 entries, found {len(tq) if isinstance(tq, list) else 0}")
            for entry in tq if isinstance(tq, list) else []:
                if not isinstance(entry.get("query"), str) or len(entry.get("query", "")) < 20:
                    errors.append("trigger query missing valid query")
                if not isinstance(entry.get("should_trigger"), bool):
                    errors.append("trigger query missing boolean should_trigger")
                w = entry.get("workflow")
                if entry.get("should_trigger") is True and w not in {"navigation", "triage", "authoring", "security"}:
                    errors.append(f"positive trigger has invalid workflow: {w}")
                if entry.get("should_trigger") is False and w != "out-of-scope":
                    errors.append(f"negative trigger must be out-of-scope, got {w}")

    # observation.md columns
    obs = package / "references" / "observation.md"
    if obs.is_file():
        header_line = ""
        for line in obs.read_text(encoding="utf-8").splitlines():
            if line.strip().startswith("|") and "mechanism" in line.lower():
                header_line = line.lower()
                break
        for col in OBSERVATION_COLUMNS:
            if col not in header_line:
                errors.append(f"observation.md header missing column keyword: {col}")

    # report
    print(f"check_package: {package}")
    print(f"  SKILL.md lines: {len(lines)}, est. tokens: {token_estimate}")
    print(f"  frontmatter: name={fm.get('name')}, description={len(description)} chars")
    if errors:
        for e in errors:
            print(f"  FAIL: {e}")
        print(f"RESULT: FAIL ({len(errors)} findings)")
        return 1
    print("RESULT: PASS")
    return 0


def main() -> int:
    parser = argparse.ArgumentParser(description="Validate the linux-kernel-map package")
    parser.add_argument("package", type=Path, help="Path to the skill package directory")
    args = parser.parse_args()
    if not args.package.is_dir():
        print(f"FAIL: not a directory: {args.package}")
        return 1
    return check_package(args.package)


if __name__ == "__main__":
    raise SystemExit(main())
