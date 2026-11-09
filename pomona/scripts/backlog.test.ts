#!/usr/bin/env bun
/**
 * sectionEnd trailing-blank trim: black-box coverage via the CLI.
 *
 * Zero-dependency (Bun built-ins only). Run: `bun test pomona/scripts/`
 * Covers the multi-blank section bug: add/move into a section ending in
 * multiple blank lines must collapse to a single separator blank.
 */
import { describe, expect, test } from "bun:test";
import { mkdtempSync, readFileSync, writeFileSync } from "node:fs";
import { tmpdir } from "node:os";
import { join } from "node:path";

const SCRIPT = new URL("./backlog.ts", import.meta.url).pathname;

function run(cwd: string, ...args: string[]) {
  const proc = Bun.spawnSync(["bun", "run", SCRIPT, ...args], {
    cwd,
    stdout: "pipe",
    stderr: "pipe",
  });
  return {
    exit: proc.exitCode ?? 0,
    stdout: proc.stdout.toString(),
    stderr: proc.stderr.toString(),
  };
}

function freshDir(): string {
  return mkdtempSync(join(tmpdir(), "pomona-sectionend-"));
}

function maxBlankRun(text: string): number {
  let max = 0;
  let cur = 0;
  for (const line of text.split("\n")) {
    if (line.trim() === "") {
      cur++;
      max = Math.max(max, cur);
    } else {
      cur = 0;
    }
  }
  return max;
}

describe("sectionEnd multi-blank trim", () => {
  test("add into multi-blank P1 collapses to single separators", () => {
    const dir = freshDir();
    writeFileSync(
      join(dir, "pomona.md"),
      [
        "## P1 — Do First",
        "",
        "- [ ] **Existing P1**",
        "  - **File**: `src/a.ts`",
        "  - **Source**: ruff F401",
        "",
        "",
        "",
        "## P2 — Quick wins",
        "",
        "## P3 — Worth doing, plan the split",
        "",
        "## P4 — Parking lot (don't pick)",
        "",
      ].join("\n"),
    );

    const res = run(
      dir,
      "add",
      "--priority",
      "P1",
      "--title",
      "New P1",
      "--file",
      "src/b.ts",
      "--source",
      "ruff F841",
    );
    expect(res.exit).toBe(0);
    expect(res.stdout).toContain("added [P1] New P1");

    const text = readFileSync(join(dir, "pomona.md"), "utf-8");
    // No triple-blank run survives; one separator on each side of the new entry.
    expect(maxBlankRun(text)).toBeLessThanOrEqual(1);
    expect(text).toContain("- [ ] **New P1**");
    // Tasks still parse.
    const list = run(dir, "list");
    expect(list.stdout).toContain("Existing P1");
    expect(list.stdout).toContain("New P1");
  });

  test("add into trailing-blank EOF section leaves no blank run", () => {
    const dir = freshDir();
    writeFileSync(
      join(dir, "pomona.md"),
      [
        "## P1 — Do First",
        "",
        "## P2 — Quick wins",
        "",
        "## P3 — Worth doing, plan the split",
        "",
        "## P4 — Parking lot (don't pick)",
        "",
        "",
        "",
      ].join("\n"),
    );

    const res = run(
      dir,
      "add",
      "--priority",
      "P4",
      "--title",
      "Parked",
      "--file",
      "src/c.ts",
      "--source",
      "TODO",
    );
    expect(res.exit).toBe(0);

    const text = readFileSync(join(dir, "pomona.md"), "utf-8");
    expect(text).toContain("- [ ] **Parked**");
    expect(maxBlankRun(text)).toBeLessThanOrEqual(1);
  });

  test("move into multi-blank destination collapses separators", () => {
    const dir = freshDir();
    writeFileSync(
      join(dir, "pomona.md"),
      [
        "## P1 — Do First",
        "",
        "- [ ] **Existing P1**",
        "  - **File**: `src/a.ts`",
        "  - **Source**: ruff F401",
        "",
        "",
        "## P2 — Quick wins",
        "",
        "",
        "",
        "## P3 — Worth doing, plan the split",
        "",
        "## P4 — Parking lot (don't pick)",
        "",
      ].join("\n"),
    );

    const res = run(dir, "move", "--id", "1", "--to", "P2");
    expect(res.exit).toBe(0);
    expect(res.stdout).toContain("moved");

    const text = readFileSync(join(dir, "pomona.md"), "utf-8");
    expect(maxBlankRun(text)).toBeLessThanOrEqual(1);
    expect(run(dir, "list").stdout).toContain("Existing P1");
  });

  test("eval4 golden path on clean file is unchanged", () => {
    const dir = freshDir();
    expect(run(dir, "init").exit).toBe(0);
    expect(
      run(
        dir,
        "add",
        "--priority",
        "P1",
        "--title",
        "Fix failing test in checkout",
        "--file",
        "src/checkout.ts",
        "--source",
        "bun test",
      ).exit,
    ).toBe(0);
    expect(
      run(
        dir,
        "add",
        "--priority",
        "P2",
        "--title",
        "Format checkout.ts",
        "--file",
        "src/checkout.ts",
        "--source",
        "bun fmt",
      ).exit,
    ).toBe(0);
    // Duplicate add is idempotent, exit 0, single copy.
    const dup = run(
      dir,
      "add",
      "--priority",
      "P1",
      "--title",
      "Fix failing test in checkout",
      "--file",
      "src/checkout.ts",
      "--source",
      "bun test",
    );
    expect(dup.exit).toBe(0);
    expect(dup.stderr).toContain("duplicate:");
    expect(
      run(dir, "list")
        .stdout.split("\n")
        .filter((l) => l.includes("Fix failing")).length,
    ).toBe(1);
    // done deletes (audit = git log), no -[x] marker, next returns P2.
    expect(run(dir, "done", "--id", "1").stdout).toContain("deleted (done)");
    const text = readFileSync(join(dir, "pomona.md"), "utf-8");
    expect(text).not.toContain("- [x]");
    expect(run(dir, "next").stdout).toContain("Format checkout.ts");
  });

  test("list keeps global ids after filter; done --id targets displayed task", () => {
    const dir = freshDir();
    expect(run(dir, "init").exit).toBe(0);
    expect(
      run(
        dir,
        "add",
        "--priority",
        "P1",
        "--title",
        "A",
        "--file",
        "a.ts",
        "--source",
        "r",
      ).exit,
    ).toBe(0);
    expect(
      run(
        dir,
        "add",
        "--priority",
        "P2",
        "--title",
        "B",
        "--file",
        "b.ts",
        "--source",
        "r",
      ).exit,
    ).toBe(0);
    expect(
      run(
        dir,
        "add",
        "--priority",
        "P2",
        "--title",
        "C",
        "--file",
        "c.ts",
        "--source",
        "r",
      ).exit,
    ).toBe(0);
    // Filtered list must NOT renumber: P2 shows #2/#3, not #1/#2.
    const filtered = run(dir, "list", "--priority", "P2").stdout;
    expect(filtered).toContain("#2 [P2] B");
    expect(filtered).toContain("#3 [P2] C");
    expect(filtered).not.toContain("#1 [P2]");
    // Global id 3 still targets C.
    expect(run(dir, "done", "--id", "3").stdout).toContain("deleted (done)");
    const after = run(dir, "list").stdout;
    expect(after).toContain("A");
    expect(after).toContain("B");
    expect(after).not.toContain("C");
  });
});
