---
name: token-efficiency
description: Token optimization best practices for cost-effective Claude Code usage. Automatically applies efficient file reading, command execution, and output handling strategies. Includes model selection guidance (Opus for learning, Sonnet for development/debugging). Prefers bash commands over reading files.
version: 1.7.0
allowed-tools: Read, Grep, Glob, Bash, Edit, Write
---

# Token Efficiency Expert

This skill provides token optimization strategies for cost-effective Claude Code usage across all projects. These guidelines help minimize token consumption while maintaining high-quality assistance.

## Core Principle

**ALWAYS follow these optimization guidelines by default unless the user explicitly requests verbose output or full file contents.**

Default assumption: **Users prefer efficient, cost-effective assistance.**

## Cardinal Rules (Never Violate)

### Rule 1: Answer Exactly What Was Asked — Nothing More

The user asked N specific questions. Your response must answer those N questions and **nothing else**. Do not add:

- Extra analysis sections, ASCII diagrams, flowcharts
- "Security Notes" or "Key Findings" blocks that repeat what you already said
- Summary tables that restate the same data in a different format
- Related-but-unrequested tangents (e.g., token refresh when asked about token creation/verification)
- Example code snippets unless explicitly requested

**Exception**: One short sentence offering to expand on a specific topic is OK. A full extra section is not.

### Rule 2: Always State Your Scope and Assumptions

Before presenting any analysis, explicitly state:

- **Scope**: "Based on the files examined at {paths}..."
- **Assumptions**: "Total revenue is the sum of the `total_revenue` field in the JSON. Growth rates are pre-computed in the data."
- **Confidence**: "These are the ERROR and WARN lines found in the log — no other severity levels were present."

Never present inferences as established facts. Use hedging language: "This suggests...", "This may indicate...", "Possible explanations include...".

### Rule 3: Extract First, Interpret Second

1. First, present exactly what you found (quoted evidence, extracted values)
2. Then, in a clearly separate section, offer interpretation
3. Label interpretation as such: "**Interpretation** (separate from extraction): ..."

This prevents the classic failure mode where speculation is presented as fact.

### Rule 4: Never Repeat Information

Each fact appears exactly once in your response. If you've stated it in one section, reference it ("as noted above") rather than restating it in a table, summary, and recommendations section.

### Rule 5: Prefer Compact Formatting

- For 1-5 items: inline or simple bullet list
- For 5-15 items: compact table or numbered list (one column, not wide multi-column)
- For 15+ items: consider whether all items are necessary
- **No ASCII diagrams** — they consume tokens and add zero informational value
- No Markdown tables with more than 3 columns unless the data genuinely requires it

## Mandatory Pre-Flight: Before EVERY File Read

**This is the single most important rule in this skill.** Before you use the Read tool on any file, you MUST first do ALL of the following:

1. **Check file size with `wc -l <path>`** — this costs near-zero tokens via bash
2. **If it's a log file** (`.log`, no extension): use `grep -i "error\|warn\|exception\|fail" <path>` instead of Read
3. **If it's structured data** (`.json`, `.yaml`, `.yml`, `.csv`): use `jq` or `python3 -c` to extract specific fields instead of Read
4. **If it's code** (`.py`, `.js`, `.ts`, `.rb`, `.go`, `.rs`, etc.): use `grep -rn "function\|class\|def\|const"` to find relevant symbols instead of blind Read

**Exception**: Only Read directly if the file is under 30 lines AND you already verified by `wc -l` that it's that small. Never skip the `wc -l` check.

---

## Model Selection Strategy

**Use the right model for the task to optimize cost and performance:**

### Opus - For Learning and Deep Understanding

**Use Opus when:**

- Learning new codebases - Understanding architecture, code structure, design patterns
- Broad exploration - Identifying key files, understanding repository organization
- Deep analysis - Analyzing complex algorithms, performance optimization
- Reading and understanding - When you need to comprehend existing code before making changes
- Very complex debugging - Only when Sonnet can't solve it or issue is architectural

### Sonnet - For Regular Development Tasks (DEFAULT)

**Use Sonnet (default) for:**

- Writing code, editing and fixing, debugging, testing, documentation, deployment, general questions

**Typical session pattern:**

1. **Start with Opus** - Spend 10-15 minutes understanding the codebase (one-time investment)
2. **Switch to Sonnet** - Use for ALL implementation, debugging, and routine work
3. **Return to Opus** - Only when explicitly needed for deep architectural understanding

**Savings: ~50% token cost vs all-Opus usage.**

---

## Skills and Token Efficiency

**Myth:** Having many skills in `.claude/skills/` increases token usage.

**Reality:** Skills use **progressive disclosure** - Claude sees only skill descriptions at session start (~155 tokens for 4 skills). Full skill content loaded only when activated.

**It's safe to symlink multiple skills to a project.** Token waste comes from reading large files unnecessarily, not from having skills available.

---

## Mandatory Workflows (Follow Exactly)

These are not suggestions — they are the required approach for common tasks. Follow them exactly to minimize token consumption.

### Workflow A: Inspecting a Log File

1. **ALWAYS** start with `grep -i "error\|warn\|exception\|fail" <logfile>` — NEVER read the whole file
2. If the grep is too broad, narrow with `grep -i "error" <logfile>` or `grep -c "error" <logfile>` for counts
3. For time-based filtering: `grep "2026-07-29 08:0[3-5]" <logfile>` for specific windows
4. Only Read individual lines if needed: `grep -n "error" <logfile>` to get line numbers, then Read with offset/limit
5. **Do NOT dump all error lines verbatim** — state the methodology and the count clearly (e.g., "Found 10 ERROR lines via `grep -c '\[ERROR\]'`"). Then offer to show the full list if needed. Dumping all lines costs tokens and adds no value beyond the count.
6. **Extract first, analyze second**: Gather the evidence, then in a clearly separate section provide interpretation. Never merge extraction and analysis.
7. **Count consistently**: If you say "N errors found", the number must exactly match the grep output. No summary-vs-body mismatches.
8. **Respect original severity**: Don't reclassify WARN as ERROR. If the log says "WARN", call it a warning.
9. **Don't cite line numbers you didn't show** — if you reference "line 204", you must have displayed the line's number in your response. Otherwise just reference timestamps.

### Workflow B: Extracting Data from JSON/YAML

1. **ALWAYS** use `python3 -c "import json; d=json.load(open('file.json')); print(d['key'])"` or `jq '.key' file.json`
2. NEVER use the Read tool on a JSON/YAML/CSV file for inspection — this is the #1 token waste. If you need to understand the structure first, use `jq 'keys' file.json` or `head -5 file.json`, never Read the whole file.
3. For complex nested data, extract step by step with `jq` rather than reading and mentally parsing
4. **Answer EXACTLY what was asked with nothing extra**: If the user asks 4 specific questions, give exactly those 4 values. No extra stats (AOV, order counts, percentages), no extra tables, no narrative commentary. Prefer a compact numbered list.
5. **State your methodology in one sentence**: "Total revenue from `summary.total_revenue`. Best category by highest revenue. Low-stock = stock < reorder_point. Growth rate from `regions[].growth`."

### Workflow C: Exploring a Codebase

1. **ALWAYS** start with `find <dir> -name "*.py" | sort` or `ls -R` — not Read on directories with many files
2. Use `grep -rn "class\|function\|def " <dir> --include="*.py"` to find what you need
3. Only Read individual files AFTER identifying them by search
4. Never Read every file in a directory — search first, read selectively
5. **Scope your findings**: "In the files examined ({list})...". Don't claim something doesn't exist unless you've verified every possible location.
6. **Answer exactly the questions — nothing extra**: If asked 3 things, describe exactly those 3 things. No ASCII diagrams. No extra subsections about related-but-unasked topics (e.g., "token refresh" when only "creation and verification" was asked). No "Key Findings" or "Notable Issues" blocks that re-state what you already said.
7. **No code snippets** unless the user explicitly asks to see code.

### Workflow D: File Transformations

| Operation     | Wasteful            | Efficient                    |
| ------------- | ------------------- | ---------------------------- |
| Copy file     | Read + Write        | `cp source dest`             |
| Replace text  | Read + Edit         | `sed -i 's/old/new/g' file`  |
| Append        | Read + Write        | `echo "text" >> file`        |
| Delete lines  | Read + Write        | `sed -i '/pattern/d' file`   |
| Merge files   | Read + Read + Write | `cat file1 file2 > combined` |
| Count lines   | Read file           | `wc -l file`                 |
| Check content | Read file           | `grep -q "term" file`        |

**Use bash for ALL data transformations.** Reading a file to transform it is always wasteful.

### Workflow E: Reading Code for Understanding

1. Start with `grep` to find symbols (functions, classes, imports)
2. Read ONLY the specific functions/classes you identified — use offset/limit
3. Read in this priority: signatures → docstrings → implementation → tests
4. If the file is under 30 lines, Read directly is OK — but verify with `wc -l` first

### Workflow F: Answering Structured Questions

When the user asks N specific questions (numbered or bulleted list):

1. **Extract first** — gather the raw data/evidence for each question (via grep/jq/Read)
2. **Answer N things, and only N things** — respond with exactly N items, directly addressing each question. Do not add related-but-unasked details. If asked about "token creation and verification," do not add a paragraph on token refresh. If asked for revenue and best category, do not add AOV, order counts, or percentages.
3. **Format for minimal tokens**:
   - For N ≤ 5: a compact numbered list, one answer per item. No verbose framing like "The answer to question 1 is..."
   - No separate introduction paragraph, conclusion paragraph, or "here is my analysis" framing
   - No tables unless the data genuinely needs a grid (3+ dimensions)
   - No ASCII diagrams, no flowcharts, no architecture maps unless explicitly requested
4. **Add one line of methodology scope** — e.g., "Scope: JSON fields: total_revenue, top_category, inventory_alerts[].stock, regions[].growth"
5. **Never repeat information** — each fact appears once. If you've described a permission system in section 2, don't describe it again in a "Key Findings" or "Notable Issues" block.

---

## When to Use Read+Edit vs Bash

**Read+Edit ONLY for code modifications** (`.py`, `.js`, `.ts`, `.tsx`, `.go`, `.rs`, `.rb`, `.java`): the user needs a reviewable diff.

**Bash for EVERYTHING else:**

- Inspecting JSON/YAML → `jq` or `python3 -c`
- Inspecting logs → `grep`
- Transforming data → `sed`, `awk`, `python3 -c`
- Copying/moving files → `cp`, `mv`
- Creating new files → Write tool (not bash heredocs)

## Decision Tree

1. **Read-only inspection of data** (JSON, logs, CSV, YAML) → **ALWAYS bash** (grep, jq, python3 -c). Never Read.
2. **Modifying code** → Read + Edit (for reviewable diff)
3. **Modifying data** → bash (sed, awk, python3)
4. **Copying/moving** → bash (cp, mv, cat)
5. **New file** → Write tool
6. **Codebase exploration** → Always grep/find first, never Read the directory

**If you're unsure**, default to bash. The Read tool is only for: (a) code files you're about to edit, (b) files under 30 lines verified by `wc -l`.

---

## When to Override

**Only override efficiency rules when:**

1. **User explicitly requests full output** ("Show me the entire log file")
2. **Filtered output lacks necessary context** for debugging (error references missing line numbers — but still grep first, then Read specific lines)
3. **File is under 30 lines** (verified by `wc -l`)
4. **Learning mode** — Read 2-5 key files to establish understanding, but still use grep to find them

**In cases 1-2, explain token cost to user and offer filtered view first.**

For detailed learning mode strategies, see [learning-mode.md](learning-mode.md).

---

## Quick Reference Card

**Before EVERY file read:**

1. **Run `wc -l <path>` first** — always, without exception
2. **Log file?** → `grep -i "error\|warn" <file>` — never Read
3. **JSON/YAML?** → `jq` or `python3 -c` — never Read
4. **Code for exploring?** → `grep -rn` for symbols — never Read blindly
5. **Code for editing?** → Read + Edit (after wc -l check)
6. **Data transform?** → `sed`, `awk`, `python3 -c` — never Read
7. **New file?** → Write tool
8. **Copy/move?** → `cp`, `mv`, `cat`

**If you're about to use the Read tool and haven't run `wc -l` first, stop and do that now.**

**Before EVERY answer:**

1. Am I answering exactly what was asked and nothing more?
2. Did I separate extraction from interpretation?
3. Did I state my scope and assumptions?
4. Is each fact stated exactly once?
5. Could this be shorter? (No diagrams, no tables where lists work, no extra sections)
6. Did I avoid dumping full data lists? (Just state counts/methodology, offer full data on request)

---

## Cost Impact

| Approach                                  | Tokens/Week | Notes                            |
| ----------------------------------------- | ----------- | -------------------------------- |
| **Wasteful** (Read/Edit/Write everything) | 500K        | Reading files unnecessarily      |
| **Moderate** (filtered reads only)        | 200K        | Grep/head/tail usage             |
| **Efficient** (bash commands + filters)   | 30-50K      | Using cp/sed/awk instead of Read |

**Applying these rules reduces costs by 90-95% on average.**

---

## Implementation

**This skill is ACTIVATED for every file operation.** Before you Read any file:

1. **Stop.** Have you run `wc -l` on it yet? If not, do that first.
2. **Choose your tool** based on the file type and what you need to do:
   - Log → `grep`
   - JSON/YAML → `jq` / `python3 -c`
   - Code exploration → `grep` for symbols
   - Code editing → Read + Edit (after wc -l)
3. **Execute** without further hesitation

**This skill is automatically applied when:**

- Reading log files
- Executing commands with large output
- Navigating codebases
- Debugging errors
- Checking system status

**You can always override by saying:**

- "Show me the full output"
- "Read the entire file"
- "I want verbose mode"
- "Don't worry about tokens"

---

## Supporting Files

| File                                       | Content                                                                                                                                                        | When to load                                                                             |
| ------------------------------------------ | -------------------------------------------------------------------------------------------------------------------------------------------------------------- | ---------------------------------------------------------------------------------------- |
| [strategies.md](strategies.md)             | Detailed bash command strategies, file operation patterns, sed/awk examples, Jupyter notebook manipulation, safe glob patterns, macOS/Linux compatibility      | When implementing specific file operations or need detailed bash patterns                |
| [learning-mode.md](learning-mode.md)       | Strategic file selection, targeted pattern learning workflows, broad repository exploration strategies, repository type identification                         | When entering learning mode or exploring a new codebase                                  |
| [examples.md](examples.md)                 | Extensive token savings examples with before/after comparisons, targeted learning examples (Galaxy wrappers, API patterns), cost calculations                  | When demonstrating token savings or learning from examples                               |
| [project-patterns.md](project-patterns.md) | Analysis file organization, task management with TodoWrite, background process management, repository organization, MANIFEST system, efficient file operations | When organizing projects, managing long-running tasks, or setting up navigation patterns |

---

## Summary

**3 principles: Read efficiently, say only what was asked, never repeat yourself.**

**File operations:** `wc -l` first → bash for inspection → Read+Edit for code edits only.

**Answers:** Answer N questions with exactly N items. No extras. No diagrams. No repeated information. State your scope.

**Extraction vs analysis:** Extract verbatim first. Interpret second. Label assumptions clearly.
