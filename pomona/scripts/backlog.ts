#!/usr/bin/env bun
/**
 * Pomona backlog lifecycle manager (bunsh-native).
 *
 * Manages `pomona.md` at the repo root — create/list/add/complete/dedupe
 * prioritized entries (P1–P4) — without scanning. Scanning stays with
 * agents; this script is the deterministic backlog mutation layer.
 *
 * Zero dependencies. Uses Bun APIs (Bun.file / Bun.write) so it runs
 * with `bun run pomona/scripts/backlog.ts` in any Bun project.
 *
 * Usage:
 *   bun run pomona/scripts/backlog.ts init [--backlog pomona.md]
 *   bun run pomona/scripts/backlog.ts status [--backlog pomona.md] [--json]
 *   bun run pomona/scripts/backlog.ts list [--priority P1] [--open|--all] [--json]
 *   bun run pomona/scripts/backlog.ts add --priority P1 --title "Fix X" --file "src/a.ts" --source "ruff F401" --details "..." [--subtask "..."]
 *   bun run pomona/scripts/backlog.ts done --id 3 | --match "substring"
 *   bun run pomona/scripts/backlog.ts remove --id 1 | --match "..."
 *   bun run pomona/scripts/backlog.ts dedupe
 *   bun run pomona/scripts/backlog.ts move --id 2 --to P2
 *   bun run pomona/scripts/backlog.ts next [--json]
 *
 * Semantics follow pomona/SKILL.md + paper §2.3:
 * - Completed tasks are DELETED (audit = `git log -- pomona.md`), never marked - [x].
 * - Dedupe is against open `- [ ]` entries only.
 * - Priorities: P1 Do first → P2 Quick wins → P3 Plan the split → P4 Parking lot.
 */

import { existsSync } from "node:fs";

type Priority = "P1" | "P2" | "P3" | "P4";

interface Task {
  /** 1-based global open index in file order. */
  id: number;
  priority: Priority | null;
  title: string;
  file: string;
  source: string;
  details: string;
  subtasks: string[];
  /** 0-based inclusive start line index (the `- [ ]` line). */
  start: number;
  /** 0-based exclusive end line index (line before next task/heading). */
  end: number;
}

const HEADINGS: Record<Priority, string> = {
  P1: "## P1 — Do First",
  P2: "## P2 — Quick wins",
  P3: "## P3 — Worth doing, plan the split",
  P4: "## P4 — Parking lot (don't pick)",
};

const PRIORITY_ORDER: Priority[] = ["P1", "P2", "P3", "P4"];

const INIT_CONTENT = `${HEADINGS.P1}

${HEADINGS.P2}

${HEADINGS.P3}

${HEADINGS.P4}
`;

const headingRe = /^##\s*P([1-4])\b/;
const taskRe = /^- \[ \] \*\*(.+)\*\*/;
const fileRe = /^\s*-\s*\*\*File\*\*:\s*(.+)$/;
const sourceRe = /^\s*-\s*\*\*Source\*\*:\s*(.+)$/;
const detailsRe = /^\s*-\s*\*\*Details\*\*:\s*(.+)$/;
// Nested only — the task title line `- [ ] **Title**` must not match.
const subtaskRe = /^\s+-\s*\[ \] (.+)$/;

function stripBackticks(s: string): string {
  const t = s.trim();
  return t.startsWith("`") && t.endsWith("`") && t.length >= 2
    ? t.slice(1, -1)
    : t;
}

export function dedupeKey(t: { title: string; file: string }): string {
  return `${t.title.trim().toLowerCase()}|${t.file.trim().toLowerCase()}`;
}

function parsePriority(line: string): Priority | null {
  const m = headingRe.exec(line);
  if (!m) return null;
  return (`P${m[1]}` as Priority) || null;
}

export function parseTasks(lines: string[]): Task[] {
  const tasks: Task[] = [];
  let current: Priority | null = null;
  let open: {
    start: number;
    priority: Priority | null;
    title: string;
    lines: string[];
  } | null = null;

  const flush = (end: number) => {
    if (!open) return;
    let file = "";
    let source = "";
    let details = "";
    const subtasks: string[] = [];
    for (const l of open.lines) {
      const fm = fileRe.exec(l);
      if (fm && !file) file = stripBackticks(fm[1]);
      const sm = sourceRe.exec(l);
      if (sm && !source) source = sm[1].trim();
      const dm = detailsRe.exec(l);
      if (dm && !details) details = dm[1].trim();
      const stm = subtaskRe.exec(l);
      // Sub-task lines are nested under "- **Sub-tasks**" — any `- [ ]` child counts.
      if (stm && l.trim().startsWith("- [ ]")) subtasks.push(stm[1].trim());
    }
    tasks.push({
      id: tasks.length + 1,
      priority: open.priority,
      title: open.title,
      file,
      source,
      details,
      subtasks,
      start: open.start,
      end,
    });
    open = null;
  };

  for (let i = 0; i < lines.length; i++) {
    const line = lines[i];
    const p = parsePriority(line);
    if (p) {
      flush(i);
      current = p;
      continue;
    }
    // Any other `##` heading ends the current priority section.
    if (line.startsWith("## ")) {
      flush(i);
      current = null;
      continue;
    }
    const tm = taskRe.exec(line);
    if (tm) {
      flush(i);
      open = {
        start: i,
        priority: current,
        title: tm[1].trim(),
        lines: [line],
      };
      continue;
    }
    if (open) open.lines.push(line);
  }
  flush(lines.length);
  return tasks;
}

export function renderTask(
  priority: Priority,
  title: string,
  file: string,
  source: string,
  details: string,
  subtasks: string[],
): string[] {
  const out: string[] = [];
  out.push(`- [ ] **${title.trim()}**`);
  if (file) out.push(`  - **File**: \`${file.trim()}\``);
  if (source) out.push(`  - **Source**: ${source.trim()}`);
  if (details) out.push(`  - **Details**: ${details.trim()}`);
  if (subtasks.length) {
    out.push(`  - **Sub-tasks**:`);
    for (const s of subtasks) out.push(`    - [ ] ${s.trim()}`);
  }
  return out;
}

async function readLines(backlog: string): Promise<string[]> {
  if (!existsSync(backlog)) return [];
  const text = await Bun.file(backlog).text();
  // Normalize CRLF, keep trailing empty entries from final newline.
  return text.replace(/\r\n/g, "\n").split("\n");
}

async function writeLines(backlog: string, lines: string[]) {
  await Bun.write(backlog, lines.join("\n"));
}

function ensureHeadings(lines: string[]): string[] {
  const out = [...lines];
  const present = new Set<Priority>();
  for (const l of out) {
    const p = parsePriority(l);
    if (p) present.add(p);
  }
  for (const p of PRIORITY_ORDER) {
    if (!present.has(p)) {
      // Append at end, separated by one blank line.
      if (out.length && out[out.length - 1].trim() !== "") out.push("");
      out.push(HEADINGS[p], "");
    }
  }
  return out;
}

/** 0-based insertion index: first line after the priority section's last task/body. */
function sectionEnd(lines: string[], priority: Priority): number {
  let inSection = false;
  let end = lines.length;
  for (let i = 0; i < lines.length; i++) {
    const p = parsePriority(lines[i]);
    if (lines[i].startsWith("## ")) {
      if (inSection) {
        end = i;
        break;
      }
      inSection = p === priority;
      continue;
    }
    if (inSection) end = i + 1;
  }
  // Trim trailing blank lines of the section for insertion point.
  while (
    end > 0 &&
    lines[end - 1]?.startsWith("## ") === false &&
    lines[end - 1]?.trim() === ""
  ) {
    // Keep one blank line before next heading; return position before blanks.
    if (end + 1 < lines.length && lines[end]?.startsWith("## ")) break;
    end--;
    if (end === 0) break;
    // Stop at last non-blank content inside section.
    break;
  }
  return end;
}

function parseFlags(argv: string[]): {
  cmd: string;
  flags: Record<string, string | boolean>;
  values: Record<string, string[]>;
} {
  const flags: Record<string, string | boolean> = {};
  const values: Record<string, string[]> = {};
  const positional: string[] = [];
  let i = 0;
  while (i < argv.length) {
    const a = argv[i];
    if (a.startsWith("--")) {
      const eq = a.indexOf("=");
      const name = eq === -1 ? a.slice(2) : a.slice(2, eq);
      const inline = eq === -1 ? undefined : a.slice(eq + 1);
      if (inline !== undefined) {
        flags[name] = inline;
        (values[name] ??= []).push(inline);
        i++;
      } else if (i + 1 < argv.length && !argv[i + 1].startsWith("--")) {
        flags[name] = argv[i + 1];
        (values[name] ??= []).push(argv[i + 1]);
        i += 2;
      } else {
        flags[name] = true;
        i++;
      }
    } else {
      positional.push(a);
      i++;
    }
  }
  return { cmd: positional[0] ?? "", flags, values };
}

function usage() {
  console.log(`pomona backlog — lifecycle manager for pomona.md (Bun, zero deps)

Usage:
  bun run pomona/scripts/backlog.ts <command> [options] [--backlog pomona.md]

Commands:
  init     Create pomona.md with P1–P4 headings (no-op if exists)
  status   Counts per priority + open total [--json]
  list     List open tasks [--priority P1] [--all] [--json]
  add      Add task: --priority P1 --title "..." --file "path" [--source "..."] [--details "..."] [--subtask "..." ...]
  done     Delete a completed task (audit = git log): --id N | --match "substring"
  remove   Alias of done (delete by --id/--match)
  dedupe   Remove duplicate open entries (keep first)
  move     Reprioritize: --id N --to P2
  next     First open task in P1→P4 order [--json]

Flags:
  --backlog <path>   Backlog file (default: pomona.md)
  --json             Machine-readable output
  --help             This help
`);
}

function normalizePriority(raw: string | boolean): Priority | null {
  if (typeof raw !== "string") return null;
  const m = /^p([1-4])$/i.exec(raw.trim());
  return m ? (`P${m[1]}` as Priority) : null;
}

/** Typed never-exit helper — narrows after calls even without @types/node. */
function fail(message: string, code = 2): never {
  console.error(message);
  // process.exit is typed `never` with @types/node; without it, throw keeps
  // control-flow narrowing correct while still exiting via process when typed.
  process.exit(code);
  throw new Error(message);
}

async function main() {
  const { cmd, flags, values } = parseFlags(Bun.argv.slice(2));

  if (cmd === "--help" || cmd === "-h" || cmd === "help" || !cmd) {
    usage();
    process.exit(cmd ? 0 : 2);
  }

  const backlog =
    typeof flags.backlog === "string" ? flags.backlog : "pomona.md";
  const asJson = flags.json === true;

  switch (cmd) {
    case "init": {
      if (existsSync(backlog)) {
        console.log(`exists: ${backlog} (no-op)`);
        return;
      }
      await Bun.write(backlog, INIT_CONTENT);
      console.log(`created: ${backlog}`);
      return;
    }

    case "status": {
      if (!existsSync(backlog)) {
        console.log(`missing: ${backlog} (run init)`);
        process.exit(1);
      }
      const lines = await readLines(backlog);
      const tasks = parseTasks(lines);
      const counts: Record<Priority, number> = { P1: 0, P2: 0, P3: 0, P4: 0 };
      for (const t of tasks) if (t.priority) counts[t.priority]++;
      if (asJson) {
        console.log(
          JSON.stringify({ backlog, counts, total: tasks.length }, null, 2),
        );
      } else {
        for (const p of PRIORITY_ORDER) console.log(`${p}: ${counts[p]}`);
        console.log(`total open: ${tasks.length}`);
      }
      return;
    }

    case "list": {
      if (!existsSync(backlog)) {
        console.log(`missing: ${backlog} (run init)`);
        process.exit(1);
      }
      const lines = await readLines(backlog);
      let tasks = parseTasks(lines);
      const want = normalizePriority(flags.priority ?? "");
      if (want) tasks = tasks.filter((t) => t.priority === want);
      else if (flags.all !== true) {
        // Default: show all open with their priorities, ordered P1→P4 then file order.
        tasks = [...tasks].sort((a, b) => {
          const pa = a.priority ? PRIORITY_ORDER.indexOf(a.priority) : 99;
          const pb = b.priority ? PRIORITY_ORDER.indexOf(b.priority) : 99;
          return pa - pb || a.id - b.id;
        });
      }
      if (asJson) {
        console.log(
          JSON.stringify(
            tasks.map((t) => ({
              id: t.id,
              priority: t.priority,
              title: t.title,
              file: t.file,
              source: t.source,
              details: t.details,
              subtasks: t.subtasks,
            })),
            null,
            2,
          ),
        );
      } else if (tasks.length === 0) {
        console.log("no open tasks");
      } else {
        // --id in `list` output is the global open id (stable for done/remove). Re-number after filter sort.
        for (const t of tasks) {
          console.log(
            `#${t.id} [${t.priority ?? "—"}] ${t.title}${t.file ? ` (${t.file})` : ""}`,
          );
        }
      }
      return;
    }

    case "add": {
      const priority = normalizePriority(flags.priority ?? "");
      const title = typeof flags.title === "string" ? flags.title : "";
      if (!priority) fail('add requires --priority P1..P4 and --title "..."');
      if (!title) fail('add requires --priority P1..P4 and --title "..."');
      const file = typeof flags.file === "string" ? flags.file : "";
      const source = typeof flags.source === "string" ? flags.source : "";
      const details = typeof flags.details === "string" ? flags.details : "";
      const subtasks = values.subtask ?? [];

      let lines = await readLines(backlog);
      if (!existsSync(backlog))
        lines = INIT_CONTENT.replace(/\r\n/g, "\n").split("\n");
      lines = ensureHeadings(lines);

      const existing = parseTasks(lines);
      const key = dedupeKey({ title, file });
      const dup = existing.find((t) => dedupeKey(t) === key);
      if (dup) {
        console.error(
          `duplicate: open task #${dup.id} [${dup.priority}] "${dup.title}" already exists (dedupe against open entries)`,
        );
        process.exit(0); // Idempotent: not an error, just already present.
      }

      const entry = renderTask(
        priority,
        title,
        file,
        source,
        details,
        subtasks,
      );
      const insertAt = sectionEnd(lines, priority);
      // Insert blank line before entry if previous line is non-blank and not a heading end.
      const needsBlank = insertAt > 0 && lines[insertAt - 1]?.trim() !== "";
      const block = needsBlank ? ["", ...entry] : entry;
      lines.splice(insertAt, 0, ...block);
      // Keep one blank line between the new entry and a following heading.
      const after = insertAt + block.length;
      if (lines[after]?.startsWith("## ")) lines.splice(after, 0, "");
      await writeLines(backlog, lines);
      console.log(`added [${priority}] ${title}${file ? ` (${file})` : ""}`);
      return;
    }

    case "done":
    case "remove": {
      if (!existsSync(backlog)) fail(`missing: ${backlog}`, 1);
      const lines = await readLines(backlog);
      const tasks = parseTasks(lines);
      let target: Task | undefined;
      if (typeof flags.id === "string") {
        const n = Number(flags.id);
        target = tasks.find((t) => t.id === n);
      } else if (typeof flags.match === "string") {
        const needle = flags.match.toLowerCase();
        target = tasks.find((t) => t.title.toLowerCase().includes(needle));
      }
      if (!target)
        fail(
          'done requires --id N or --match "substring" (use `list` to see ids)',
        );
      // Delete task lines. Consume one trailing blank line if present to avoid blank pile-up.
      let end = target.end;
      if (lines[end]?.trim() === "" && end + 1 < lines.length) end += 1;
      lines.splice(target.start, end - target.start);
      await writeLines(backlog, lines);
      // Per paper §2.3: deleted, not - [x] — audit is git log.
      console.log(
        `deleted (done) #${target.id} [${target.priority}] ${target.title} — audit = git log -- ${backlog}`,
      );
      return;
    }

    case "dedupe": {
      if (!existsSync(backlog)) fail(`missing: ${backlog}`, 1);
      const lines = await readLines(backlog);
      const tasks = parseTasks(lines);
      const seen = new Set<string>();
      const dups: Task[] = [];
      for (const t of tasks) {
        const k = dedupeKey(t);
        if (seen.has(k)) dups.push(t);
        else seen.add(k);
      }
      if (dups.length === 0) {
        console.log("no duplicates");
        return;
      }
      // Delete from last to first so earlier indices stay valid.
      for (const d of [...dups].sort((a, b) => b.start - a.start)) {
        let end = d.end;
        if (lines[end]?.trim() === "" && end + 1 < lines.length) end += 1;
        lines.splice(d.start, end - d.start);
      }
      await writeLines(backlog, lines);
      for (const d of dups)
        console.log(`removed duplicate #${d.id} [${d.priority}] ${d.title}`);
      console.log(`removed ${dups.length} duplicate(s)`);
      return;
    }

    case "move": {
      const to = normalizePriority(flags.to ?? "");
      if (!to) fail("move requires --to P1..P4");
      if (!existsSync(backlog)) fail(`missing: ${backlog}`, 1);
      const lines = await readLines(backlog);
      const tasks = parseTasks(lines);
      const n = Number(flags.id);
      const target = tasks.find((t) => t.id === n);
      if (!target) fail(`move: no task --id ${flags.id ?? ""} (use list)`);
      const block = lines.slice(target.start, target.end);
      // Trim trailing blanks from block.
      while (block.length && block[block.length - 1].trim() === "") block.pop();
      let end = target.end;
      if (lines[end]?.trim() === "" && end + 1 < lines.length) end += 1;
      lines.splice(target.start, end - target.start);
      // Predict inserted position (before the removed range, so offset shrinks if moving forward).
      const insertAt = sectionEnd(lines, to);
      const needsBlank =
        insertAt > 0 &&
        lines[insertAt - 1]?.trim() !== "" &&
        !lines[insertAt - 1]?.startsWith("##");
      lines.splice(insertAt, 0, ...(needsBlank ? ["", ...block] : block));
      await writeLines(backlog, lines);
      console.log(`moved #${target.id} → ${to}: ${target.title}`);
      return;
    }

    case "next": {
      if (!existsSync(backlog)) {
        console.log(`missing: ${backlog} (run init)`);
        process.exit(1);
      }
      const lines = await readLines(backlog);
      const tasks = parseTasks(lines);
      const sorted = [...tasks].sort((a, b) => {
        const pa = a.priority ? PRIORITY_ORDER.indexOf(a.priority) : 99;
        const pb = b.priority ? PRIORITY_ORDER.indexOf(b.priority) : 99;
        return pa - pb || a.id - b.id;
      });
      const top = sorted[0];
      if (!top) {
        if (asJson) console.log(JSON.stringify(null));
        else
          console.log(
            "no open tasks (run scanning to refill P1/P2 per Pomona Step 2)",
          );
        return;
      }
      if (asJson) {
        console.log(
          JSON.stringify(
            {
              id: top.id,
              priority: top.priority,
              title: top.title,
              file: top.file,
              source: top.source,
              details: top.details,
              subtasks: top.subtasks,
            },
            null,
            2,
          ),
        );
      } else {
        console.log(
          `#${top.id} [${top.priority}] ${top.title}${top.file ? ` (${top.file})` : ""}`,
        );
        if (top.details) console.log(top.details);
      }
      return;
    }

    default:
      console.error(`unknown command: ${cmd}`);
      usage();
      process.exit(2);
  }
}

if (import.meta.main) {
  main().catch((e) => {
    console.error(e instanceof Error ? e.message : String(e));
    process.exit(1);
  });
}
