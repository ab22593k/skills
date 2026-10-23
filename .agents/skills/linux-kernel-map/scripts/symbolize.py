#!/usr/bin/env python3
"""Optional wrapper around the kernel's own decode scripts."""

from __future__ import annotations

import argparse
import os
import subprocess
import sys
from pathlib import Path


def find_tree(arg: str | None) -> Path | None:
    raw = arg or os.environ.get("KERNEL_SRC")
    if not raw:
        return None
    p = Path(raw).expanduser()
    return p if p.is_dir() else None


def main() -> int:
    parser = argparse.ArgumentParser(
        description="Symbolize a kernel splat using the kernel's own decode scripts"
    )
    parser.add_argument("--tree", help="Kernel source tree (or set KERNEL_SRC)")
    parser.add_argument("--vmlinux", help="Path to vmlinux")
    parser.add_argument("--splat", help="Path to a splat file (read from stdin if omitted)")
    parser.add_argument("--modules", help="Path to modules directory")
    parser.add_argument("--symbol", help="Single symbol in func+0xoff/0xsize form")
    args = parser.parse_args()

    tree = find_tree(args.tree)
    if tree is None:
        print("ERROR: no kernel tree. Set KERNEL_SRC or pass --tree.")
        print("       Without a tree this tool cannot decode; name the missing artifact and stop.")
        return 2

    decode = tree / "scripts" / "decode_stacktrace.sh"
    faddr = tree / "scripts" / "faddr2line"
    if args.symbol:
        if not faddr.is_file():
            print(f"ERROR: {faddr} not found in this tree")
            return 2
        vmlinux = Path(args.vmlinux).expanduser() if args.vmlinux else None
        if vmlinux is None or not vmlinux.is_file():
            print("ERROR: vmlinux is required to decode a symbol. Supply --vmlinux <path>.")
            return 2
        result = subprocess.run(  # noqa: S603
            [str(faddr), str(vmlinux), args.symbol], capture_output=True, text=True
        )
        sys.stdout.write(result.stdout)
        sys.stderr.write(result.stderr)
        return result.returncode
    if not decode.is_file():
        print(f"ERROR: {decode} not found in this tree")
        return 2

    vmlinux = Path(args.vmlinux).expanduser() if args.vmlinux else None
    if vmlinux is None or not vmlinux.is_file():
        print("ERROR: vmlinux is required to decode. Supply --vmlinux <path>.")
        print("       Without it, frames stay unresolved and must be marked reliable: no.")
        return 2

    modules = args.modules or str(tree)
    cmd = [str(decode), str(vmlinux), "auto", modules]
    stdin_data = None
    if args.splat:
        splat_path = Path(args.splat).expanduser()
        if not splat_path.is_file():
            print(f"ERROR: splat not found: {splat_path}")
            return 2
        stdin_data = splat_path.read_bytes()
    else:
        if sys.stdin.isatty():
            print("Reading splat from stdin (Ctrl-D to end)...")
        stdin_data = sys.stdin.buffer.read()

    result = subprocess.run(cmd, input=stdin_data, capture_output=True)  # noqa: S603
    sys.stdout.buffer.write(result.stdout)
    sys.stderr.buffer.write(result.stderr)
    if result.returncode != 0:
        print(f"\nsymbolize: decode_stacktrace.sh exited {result.returncode}", file=sys.stderr)
    print("\nNote: address layout is not presented; only symbolized frames are shown.", file=sys.stderr)
    return result.returncode


if __name__ == "__main__":
    raise SystemExit(main())
