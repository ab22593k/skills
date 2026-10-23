#!/usr/bin/env python3
"""Verify every map entry against a Linux kernel source tree."""

from __future__ import annotations

import argparse
import json
import subprocess
from pathlib import Path

VALID_KINDS = {"function", "macro", "struct", "file", "asm"}


def git_available(tree: Path) -> bool:
    try:
        result = subprocess.run(  # noqa: S603
            ["git", "-C", str(tree), "rev-parse", "--is-inside-work-tree"],  # noqa: S603, S607
            capture_output=True,
            text=True,
        )
    except OSError:
        return False
    return result.returncode == 0 and result.stdout.strip() == "true"


def grep_in_file(tree: Path, needle: str, relpath: str, use_git: bool) -> bool:
    full = tree / relpath
    if not full.is_file():
        return False
    if use_git:
        result = subprocess.run(  # noqa: S602, S603, S607
            ["git", "-C", str(tree), "grep", "-F", "-q", needle, "--", relpath],  # noqa: S603, S607
            capture_output=True,
        )  # noqa: S603, S607
        return result.returncode == 0
    result = subprocess.run(  # noqa: S602, S603, S607
        ["grep", "-F", "-q", needle, str(full)], capture_output=True  # noqa: S603, S607
    )
    return result.returncode == 0


def config_gate_present(tree: Path, gate: str, use_git: bool) -> bool:
    if gate == "ALWAYS":
        return True
    bare = gate.removeprefix("CONFIG_")
    # Scan Kconfig files directly. A git-grep shortcut is not used because its
    # pathspec does not reliably reach nested Kconfig files.
    for kf in tree.rglob("Kconfig*"):
        if not kf.is_file():
            continue
        try:
            if bare.encode() in kf.read_bytes():
                return True
        except OSError:
            continue
    return False


def run_command(tree: Path, command: str) -> tuple[bool, str]:
    try:
        result = subprocess.run(  # noqa: S602, S603, S607
            command,
            shell=True,  # noqa: S602
            cwd=str(tree),
            capture_output=True,
            text=True,
            timeout=60,
        )
    except subprocess.TimeoutExpired:
        return False, "timeout after 60s"
    ok = result.returncode == 0
    detail = (result.stdout + result.stderr).strip().splitlines()
    detail = detail[-1] if detail else f"exit {result.returncode}"
    return ok, detail


def main() -> int:
    parser = argparse.ArgumentParser(description="Verify the linux-kernel-map against a kernel tree")
    parser.add_argument("--map", type=Path, required=True, help="Path to references/map.json")
    parser.add_argument("--tree", type=Path, required=True, help="Path to the kernel source tree")
    args = parser.parse_args()

    if not args.map.is_file():
        print(f"FAIL: map file not found: {args.map}")
        return 1
    if not args.tree.is_dir():
        print(f"FAIL: tree not found: {args.tree}")
        return 1

    data = json.loads(args.map.read_text(encoding="utf-8"))
    use_git = git_available(args.tree)
    areas = data.get("areas", [])
    total = len(areas)
    verified = 0
    print(f"check_map: tree={args.tree} git={use_git} areas={total}")
    print(f"{'area':<24}{'roots':<8}{'symbols':<10}{'config':<8}{'commands':<10}")
    for area in areas:
        area_id = area.get("id", "?")
        roots_ok = True
        for root in area.get("roots", []):
            if not (args.tree / root).is_dir():
                roots_ok = False
        symbols_ok = True
        for sym in area.get("symbols", []):
            kind = sym.get("kind")
            name = sym.get("name", "")
            rel = sym.get("file", "")
            if kind == "file":
                if name != rel or not (args.tree / rel).is_file():
                    symbols_ok = False
            else:
                if not grep_in_file(args.tree, name, rel, use_git):
                    symbols_ok = False
        config_ok = True
        for gate in area.get("config_gates", []):
            if not config_gate_present(args.tree, gate, use_git):
                config_ok = False
        commands_ok = True
        for cmd in area.get("verify_commands", []):
            ok, _ = run_command(args.tree, cmd)
            if not ok:
                commands_ok = False
        row_ok = roots_ok and symbols_ok and config_ok and commands_ok
        if row_ok:
            verified += 1
        print(
            f"{area_id:<24}"
            f"{'pass' if roots_ok else 'FAIL':<8}"
            f"{'pass' if symbols_ok else 'FAIL':<10}"
            f"{'pass' if config_ok else 'FAIL':<8}"
            f"{'pass' if commands_ok else 'FAIL':<10}"
        )
        if not row_ok:
            # detail
            for root in area.get("roots", []):
                if not (args.tree / root).is_dir():
                    print(f"   missing root: {root}")
            for sym in area.get("symbols", []):
                name = sym.get("name", "")
                rel = sym.get("file", "")
                kind = sym.get("kind")
                if kind == "file":
                    if not (args.tree / name).is_file():
                        print(f"   missing file symbol: {name}")
                else:
                    if not grep_in_file(args.tree, name, rel, use_git):
                        print(f"   missing symbol: {name} in {rel}")
            for gate in area.get("config_gates", []):
                if gate != "ALWAYS" and not config_gate_present(args.tree, gate, use_git):
                    print(f"   missing config gate: {gate}")
            for cmd in area.get("verify_commands", []):
                ok, detail = run_command(args.tree, cmd)
                if not ok:
                    print(f"   failing command: {cmd} -> {detail}")

    print(f"{verified}/{total} areas verified")
    return 0 if (total > 0 and verified == total) else 1


if __name__ == "__main__":
    raise SystemExit(main())
