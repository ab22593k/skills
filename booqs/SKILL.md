---
name: booqs
description: "Converts any documentation source — book (PDF/EPUB), URL, git repo, directory, or text file — into a structured, token-efficient knowledge base for LLM consumption. Extracts frameworks, mental models, principles, techniques, anti-patterns, and organized references. Trigger on: 'turn this into a skill', 'create a skill from', 'I want to study', 'study this documentation', 'add this to my skills', 'convert this to a skill', 'make a skill from', 'analyze this book/docs/repo', 'extract frameworks from'. Use when the user provides a path to a PDF/EPUB, a URL to documentation, a git repo URL, a local directory of docs, or any text source, and wants to build a reusable, structured knowledge base from it."
---

## Pipeline

`0. Detect type → 0.5. Classify content → 1. Extract → 1b. Chunk (if >50K) → 2. Analyze (Conceptual +/or Procedural) → 3. Generate files → 4. Install`

## Step 0 — Detect source type

| Input                      | Type      | Strategy                          |
| -------------------------- | --------- | --------------------------------- |
| `https://...`              | URL       | firecrawl_scrape / webfetch       |
| `github.com/...` or `git@` | Git repo  | `git clone --depth 1` → walk docs |
| Local dir path             | Directory | Walk `.md`/`.rst`/`.html` files   |
| `.pdf` file                | File      | `extract.py --mode technical`     |
| `.epub` file               | File      | `extract.py`                      |
| `.md` / `.txt` file        | File      | `extract.py`                      |
| Other extension            | Unknown   | Sniff magic bytes                 |

Slug from source name: lowercase, `[^a-z0-9]+` → `-`, strip edges.

## Pre-flight check

Before starting the pipeline, verify the environment:

```bash
# Check core dependency
which uv >/dev/null 2>&1 || { echo "Need uv — install at https://docs.astral.sh/uv/"; exit 1; }

# Check that this skill's script is present
test -f <skill-dir>/scripts/extract.py || { echo "Missing extract.py — is the skill installed correctly?"; exit 1; }

# Check firecrawl/webfetch for URL sources
test -n "$FIRECRAWL_API_KEY" || echo "Warning: no FIRECRAWL_API_KEY — will fall back to webfetch"

# Verify output directory is writable
mkdir -p /tmp/booqs || { echo "Cannot write to /tmp/booqs"; exit 1; }
```

If any check fails, stop and explain the missing dependency. Do not proceed with a broken environment.

## Step 1 — Extract text by source type

**URL** — `firecrawl_scrape` (or webfetch fallback). Save to `/tmp/booqs/full_text.txt` + `metadata.json` (`{source_type,url,estimated_tokens,chapters_detected}`). For multi-page docs: `firecrawl_map` sub-pages, sitemap, or use `waitFor` for JS-rendered.

**Git repo** — `git clone --depth 1 <url> /tmp/booqs/repo/`. Find `.md`/`.rst`/`.html`/`.txt` (prioritize README, docs/). Concatenate into `full_text.txt` with `[FILE: path]` markers. Skip `node_modules/`, `.git/`, `__pycache__/`, vendor dirs, binary files. Metadata: `{source_type:git, repo, files_discovered, files_read, estimated_tokens}`.

**Directory** — Recursively walk `.md`/`.rst`/`.html`/`.txt` files. Skip hidden dirs (`.`/`__`), build artifacts (`node_modules/`,`target/`,`dist/`,`build/`). Same concat format as git. Same metadata shape.

**File (PDF/EPUB/MD/TXT)** — `python3 <skill-dir>/scripts/extract.py "<path>" --mode <technical|text>`. For PDFs, first read ~2K token sample and signal-detect:

| Signal          | Check                  | High if         | → mode         |
| --------------- | ---------------------- | --------------- | -------------- | --------- |
| Code density    | ` ``` ` `{` `def` `fn` | >5 blocks/2K    | technical      |
| Table density   | `                      | ` rows, columns | >3 patterns/2K | technical |
| Formula density | `=` `∑` `∫` `→`        | >5/2K           | technical      |
| Framework terms | Named models/theorems  | >3              | text           |
| Prose ratio     | Paragraph vs heading   | >80%            | text           |

Decision: high code/table/formula → `technical`; frameworks/prose → `text`. EPUBs always use ebooklib. On failure: suggest `uv sync`.

**Token-efficient extraction rules:**

- Read metadata with `jq` or `python3 -c "import json;..."` — don't Read the full JSON file
- Check file size with `wc -l` / `wc -c` before reading source text
- Use `wc -l /tmp/booqs/full_text.txt` to assess size cheaply
- For metadata fields: `python3 -c "import json; m=json.load(open('/tmp/booqs/metadata.json')); print(m['estimated_tokens'], m['chapters_detected'])"`
- If >50K tokens, use the **rolling-window chunking** strategy below instead of reading the full text

### Rolling-window chunking (for sources >50K tokens)

For sources exceeding ~50K tokens, the full text is too large to process in one pass. Build a chunked representation:

1. **Extract global thesis (200–300 tokens):**
   - Read the first ~3K tokens (preface, introduction, opening) — captures the central argument, intended audience, high-level structure
   - Read the last ~2K tokens (conclusion, summary chapter, closing remarks) — captures the author's synthesis and final framing
   - Synthesize into a **global thesis** payload: one-sentence thesis, intended audience, overarching argument, high-level chapter map
   - This payload is prepended to every chunk so the model never loses sight of the whole while analyzing a part

2. **Build section header index:**
   - Run `grep -n "^#\|^Chapter\|^[A-Z ]\{5,\}"` to extract all structural markers with line numbers
   - Also capture the chain of parent headers (e.g., for an H3 "Two-Phase Commit" under H2 "Atomic Commit" under H1 "Chapter 9: Consistency", record the full breadcrumb `Ch9 > Atomic Commit > Two-Phase Commit`)

3. **Divide into overlapping rolling windows:**
   - Window size: **8K tokens** per chunk
   - Overlap: **2K tokens** (25%) between adjacent windows — no concept falls between the cracks
   - For each window, record:
     - `start_line`, `end_line` in the source
     - **Structural breadcrumb** — the nearest preceding parent-section headings at each level (H1→H2→H3) for this window. Derived from the section header index: find the most recent H1, H2, H3 before the window's start
     - **Global thesis** (from step 1) — prepended as system context

4. **Chunk data structure (stored as `/tmp/booqs/chunks.json`):**

   ```json
   [
     {
       "window": 0,
       "start_line": 1,
       "end_line": 312,
       "breadcrumb": "Chapter 1: Reliability > Hardware Faults > Disk Redundancy",
       "global_thesis": "This book teaches...",
       "text": "<extracted text for this window>"
     }
   ]
   ```

5. **For sources >150K tokens:** Apply the same rolling-window strategy, but sample strategically — process every Nth window (e.g., every other window) rather than all of them, prioritizing windows whose breadcrumb contains key chapter boundaries or introduces new topics.

When Step 2 says "read the source", use the chunked representation: analyze each chunk independently, then synthesize across chunks.

## Step 0.5 — Classify content type (Conceptual vs Procedural)

Before analysis, sample ~2K tokens and classify the content into one or more of:

| Type           | Hallmarks                                                                         | Extraction strategy                                                    |
| -------------- | --------------------------------------------------------------------------------- | ---------------------------------------------------------------------- |
| **Conceptual** | Frameworks, principles, mental models, theories, trade-offs, architecture         | Existing pipeline (categories below)                                   |
| **Procedural** | Step-by-step instructions, how-to guides, tutorials, recipes, maintenance manuals | Two-stage CoT procedural extraction (see "Procedural extraction mode") |
| **Mixed**      | Both conceptual material AND step-by-step instructions                            | Run both pipelines; output merges both analysis types                  |

Detection signals per ~2K sample:

| Signal                   | Examples                                                   | High if      |
| ------------------------ | ---------------------------------------------------------- | ------------ |
| Imperative sentences     | "Remove the cover", "Click Save", "Mix until combined"     | >5 sentences |
| Ordered lists            | "1. ", "Step ", "First, " then "Next, "                    | >3 instances |
| Sequential markers       | "then", "after that", "before proceeding", "once complete" | >5 instances |
| Equipment/tool mentions  | "using a wrench", "with a screwdriver", "in a bowl"        | >3 instances |
| Action verbs in commands | "insert", "rotate", "configure", "run", "pour", "fold"     | >5 instances |
| Temporal constraints     | "for 30 minutes", "until golden", "wait 5 seconds"         | >2 instances |

Decision:

- **Conceptual**: <2 procedural signals
- **Procedural**: ≥4 procedural signals AND procedures are the main content (>50% of text)
- **Mixed**: ≥4 procedural signals but significant conceptual content too (>25% each)

Record as `content_type: "conceptual" | "procedural" | "mixed"` in `metadata.json`.

## Step 2 — Analyze

Read `/tmp/booqs/full_text.txt` (or the chunked representation if >50K). Run the analysis pipeline(s) determined by Step 0.5 content type.

### Step 2a — Conceptual extraction (for Conceptual and Mixed sources)

Per section extract:

| Category          | What to capture                                                            |
| ----------------- | -------------------------------------------------------------------------- |
| **Frameworks**    | Structured approaches, step-by-step methodologies, decision trees          |
| **Mental models** | Heuristics, simplifying lenses, rules of thumb                             |
| **Principles**    | Invariant guidelines, laws, axioms                                         |
| **Techniques**    | Specific procedures, algorithms, code patterns                             |
| **Anti-patterns** | Design mistakes, architectural traps, security risks, performance pitfalls |
| **Terminology**   | Author-defined terms, coined names, precise definitions                    |
| **Trade-offs**    | Comparison matrices, boundary conditions, failure regimes                  |

**Critical extraction rule:** Do NOT capture descriptions of patterns. Capture their **mechanics** and **trade-offs**. Target:

- Comparison tables (A vs B, columns, trade-off axes)
- Structural diagrams / decision matrices
- Boundary conditions — exactly when a pattern or approach fails
- Specific criteria that dictate architectural or algorithmic choices (e.g., consistency model selection under high latency, split-brain handling in read-heavy systems)
- **Failure conditions** — the specific setup that makes something a risk (e.g., "JWT without refresh rotation → no revocation capability", "N+1 query under 100ms SLAs → 10x p99 latency")

If a passage describes _what_ a thing is but doesn't state _when to use it, when to avoid it, or what breaks_, skip it or surface it only as a brief anchor. The output should let a practitioner make concrete engineering trade-off decisions.

Map every extracted term back to its source chapter — the practitioner needs a path back to the original.

Produce 800–1,200 token summaries with code examples for technical content.

### Step 2b — Procedural extraction (for Procedural and Mixed sources)

Use a **two-stage Chain-of-Thought extraction** inspired by the Procedural Knowledge Graph (PKG) approach (Carriero et al. 2024, arXiv:2412.03589).

**Stage 1 — Extract procedural elements:**

Read the source and extract, for each step, the following dimensions:

| Dimension         | What to capture                                 | Example                                                     |
| ----------------- | ----------------------------------------------- | ----------------------------------------------------------- |
| **Step**          | A discrete unit of action in the procedure      | "Mount the bracket to the wall"                             |
| **Action**        | The verb / phrasal verb / idiomatic expression  | "mount"                                                     |
| **Direct object** | The noun being acted upon                       | "the bracket"                                               |
| **Equipment**     | Objects/tools needed (including implicit ones)  | "drill, screwdriver, wall anchors"                          |
| **Temporal info** | Duration, ordering constraints, waiting periods | "for 30 seconds", "until golden brown", "before proceeding" |

One-shot example to guide extraction:

```
Procedure: How to clean a flat panel monitor
Step 1: Turn off the monitor and unplug it.
Step 2: Dampen a microfiber cloth with distilled water.
Step 3: Wipe the screen gently in circular motions.
Step 4: Wait for the screen to dry completely.
Step 5: Plug the monitor back in and turn it on.

Extraction:
- Step 1: "Turn off the monitor and unplug it"
  → Action: "turn off", Objects: ["the monitor"]
  → Action: "unplug", Objects: ["it" (the monitor)]
  → Equipment: [] (implicit: hands)
  → Temporal: []
- Step 2: "Dampen a microfiber cloth with distilled water"
  → Action: "dampen", Objects: ["a microfiber cloth"]
  → Equipment: ["distilled water"]
  → Temporal: []
- Step 3: "Wipe the screen gently in circular motions"
  → Action: "wipe", Objects: ["the screen"]
  → Equipment: ["microfiber cloth"] (implicit — mentioned in Step 2)
  → Temporal: []
- Step 4: "Wait for the screen to dry completely"
  → Action: "wait", Objects: ["the screen" (to dry)]
  → Equipment: []
  → Temporal: ["until the screen is completely dry"]
- Step 5: "Plug the monitor back in and turn it on"
  → Action: "plug in", Objects: ["the monitor"]
  → Action: "turn on", Objects: ["it" (the monitor)]
  → Equipment: []
  → Temporal: []
```

Extraction guidelines:

- A single step sentence may contain **multiple actions** — split them
- **Implicit equipment** (tools from earlier steps, obvious prerequisites) should be included — if the step says "wipe the screen" and Step 2 mentions a microfiber cloth, the extraction for Step 3 should include `Equipment: [microfiber cloth]`
- **Temporal info** includes durations ("for 30 minutes"), endpoints ("until dry"), ordering ("before connecting"), and conditions ("once the light turns green")
- **Flexible rephrasing** is OK — strict verbatim extraction is less important than capturing the right action-object relationship. The goal is consistent semantic extraction, not exact string matching.
- If a step has **conditional branching** ("if X, do Y; otherwise do Z"), capture both branches as alternatives with their conditions

**Stage 2 — Structure into procedural graph:**

From the extracted elements (Stage 1), build a step-relationship graph. For each step, record:

```json
{
  "step_number": 1,
  "label": "Turn off the monitor and unplug it",
  "actions": [
    { "verb": "turn off", "object": "monitor" },
    { "verb": "unplug", "object": "monitor" }
  ],
  "equipment": [],
  "temporal": [],
  "preceded_by": null,
  "followed_by": 2,
  "conditional": null,
  "source_section": "§Setup/Monitor Cleaning"
}
```

The graph captures:

- **Sequencing**: `step_number`, `preceded_by` / `followed_by` — the ordering of steps
- **Action-object-equipment triples**: What action is performed on what object, using what tool
- **Temporal constraints**: Durations, waiting periods, ordering requirements
- **Conditional branches**: Decision points in the procedure
- **Source backlinks**: Every step maps to the section/chapter it came from

**Cross-document step merging:** When the source is a git repo, directory, or multiple files, steps from different documents that describe the same procedure should be merged into a unified step sequence. Signal same-procedure by matching on action+object pairs or shared equipment mentions. When merging, note the document source for each step.

**Stage 1 and Stage 2 as separate prompts:** Execute these as two sequential reasoning passes, not one. The extraction pass produces raw intermediate data (saved to `/tmp/booqs/procedural_raw.json`). The structuring pass reads that intermediate data and produces the final graph. This two-pass architecture is the core insight from the PKG paper — it prevents the model from conflating extraction accuracy with format conformance.

**When chunked (>50K):** Run Stage 1 on each chunk independently, then run Stage 2 over all merged extractions to build the unified graph. Each chunk's extraction payload carries its source breadcrumb so the final graph has accurate section backlinks.

## Step 3 — Generate files

Output: `/tmp/booqs/<slug>/`

```
SKILL.md          ~4K tokens — mental models, chapter index, query routing
chapters/chN.md   ~1K each — core ideas, frameworks, techniques, connections
glossary.md       ~1.5K — alphabetized key terms → chN
patterns.md       ~2K — techniques, principles, anti-patterns with context
cheatsheet.md     ~1K — decision tables for quick reference
```

**For Procedural-mode sources, add:**

```
steps.md           ~2K — step sequences with actions, objects, equipment, temporal info
procedural-graph.md ~1.5K — step-relationship graph (sequencing, branching, dependencies)
```

SKILL.md frontmatter: `name:<slug>` + `description:"one-sentence actionable summary"`.

Body order: Core mental models (When→Idea→Apply→Pitfalls per model), Query routing table, Chapter index (#,Title,Topic,Best for,Source chapter), Reference file pointers.

Every concept, pattern, and technique must carry a **source backlink** — the chapter/section it came from — so a practitioner can return to the original for full context. Format: `(→ chN)` for chapter-level, `(→ §Reliability/Hardware Faults)` for section-level.

Chapter frontmatter: `chapter:N` `topic:"..."` `when:"User needs...", queries:["..."]`. Body: Core concepts→Frameworks→Techniques→Trade-off matrices→Connections (+ Code/Reference tables if technical). Every technique section must include **failure conditions** — the specific bounds beyond which the approach degrades.

Glossary: `**term** — definition. (→ chN)`. Source every term to the author's own definition — not a generic one. If the book coins a term (e.g., "two-phase commit"), include the precise way the author frames it since that carries their analytical lens. Patterns: `## Name` + Type/Context/When it fails (boundary conditions)/Solution/Consequences/Related + `(→ §ParentSection)`. Lead with the failure regime — the conditions under which this pattern breaks — then the solution. Cheatsheet: `## Choosing X` + `If|Then` table; prefer comparison matrices (two-axis grids showing which approach wins given X vs Y) over simple If/Then lists. Every entry includes its source section.

### steps.md format (for Procedural sources)

```markdown
## How to <Goal>

| Step | Action   | Object  | Equipment        | Timing               | Preceded by |
| ---- | -------- | ------- | ---------------- | -------------------- | ----------- |
| 1    | turn off | monitor | —                | —                    | —           |
| 2    | unplug   | monitor | —                | —                    | 1           |
| 3    | dampen   | cloth   | distilled water  | —                    | 2           |
| 4    | wipe     | screen  | microfiber cloth | gently, circular     | 3           |
| 5    | wait     | —       | —                | until completely dry | 4           |
| 6    | plug in  | monitor | —                | —                    | 5           |
| 7    | turn on  | monitor | —                | —                    | 6           |
```

Include a row for every action (not every sentence). A single sentence like "Turn off the monitor and unplug it" produces two rows (one for "turn off", one for "unplug"). The action is always an imperative verb; the object is the thing acted upon; equipment is any tool needed (including implicit tools inherited from earlier steps); timing captures duration, endpoint conditions, or ordering constraints.

If the source has **conditional branches**, represent them as:

| Step | Condition              | Action | Object                  | ... |
| ---- | ---------------------- | ------ | ----------------------- | --- |
| 4a   | If screen is smudged   | apply  | screen cleaner solution | ... |
| 4b   | If screen is dust-only | skip   | —                       | ... |

For long procedures (>20 steps), group steps into **phases** with section headers:

```
### Phase 1: Preparation
### Phase 2: Main procedure
### Phase 3: Cleanup
```

### procedural-graph.md format (for Procedural sources)

````markdown
## Step Graph

```mermaid
flowchart LR
  1[Turn off monitor] --> 2[Unplug monitor]
  2 --> 3[Dampen cloth]
  3 --> 4[Wipe screen]
  4 --> 5[Wait for drying]
  5 --> 6[Plug in monitor]
  6 --> 7[Turn on monitor]
```
````

## Branching & Dependencies

| Decision point | Condition                 | Next step |
| -------------- | ------------------------- | --------- |
| Step 4: wipe   | If still dirty → repeat 4 | Step 4    |
| Step 4: wipe   | If clean → proceed        | Step 5    |

## Equipment Summary

| Tool             | Used in steps | Introduced in |
| ---------------- | ------------- | ------------- |
| microfiber cloth | 3, 4          | Step 3        |
| distilled water  | 3             | Step 3        |

````

**Token-efficient generation:** Apply same density rules to every output file. Never dump raw text. Each file must justify its token budget.

## Step 4 — Install

```bash
mkdir -p ~/.agents/skills/<slug> && cp -r /tmp/booqs/<slug>/* "$_"
````

Report slug, section count, total tokens, usage example. Clean up `/tmp/booqs/`.

## Dependencies

Python 3.10+, `uv`. PDF: PyMuPDF/pdftotext/PyPDF2/pdfminer/docling. EPUB: ebooklib+bs4. URL: firecrawl/webfetch. Git: `git` CLI. All via `uv sync`.

## Efficiency guidelines during execution

- **Prefer bash over Read** for file operations: `cp`, `mv`, `mkdir`, `python3 -c` for JSON, `jq` for metadata
- **Check size first**: `wc -l /tmp/booqs/full_text.txt` — Read only if needed
- **Use rolling-window chunking** for files >50K (see section above) instead of ad-hoc sampling
- **Never Read entire JSON/metadata files** — use `python3 -c "import json;..."` to extract one field
- **Batch operations** when possible (e.g., `find ... -exec cat {} +` instead of Read loop)
- **Use Write tool** for new file creation (not bash heredocs)
- **Use Edit tool** for code modifications (reviewability > token cost for code)
- **Summarize, don't dump** — structured summaries of contents, not raw outputs

## Edge cases

- > 150K tokens: apply rolling-window chunking (8K windows, 2K overlap), then sample strategically — every Nth window prioritizing chapter-boundary windows. Each sampled window still carries the global thesis payload and breadcrumb.
- No sections detected: scan for `^#`, `^Chapter`, `^[A-Z ]{5,}`; otherwise single-chapter
- Skill exists: warn + ask before overwrite
- Partial failure: mark "needs review"
- Login-gated URL: explain limitation, suggest saving to file
- Large git repo: `--depth 1`, prioritize README + docs/
- **No procedural signals detected from procedural-type content**: Document the content accurately. Mark `content_type: "procedural"` but note "inferred — no sequential structure found." Fall back to conceptual-only extraction.
- **Conflicting step order across documents**: When merging steps from multiple files, use the document's own ordering as authoritative. If two documents disagree on step order, include both as alternatives with `(source: docA)` / `(source: docB)` annotations.
- **Procedure with no distinct actions**: Some guides ("best practices", "guidelines") use imperative sentences but aren't sequential procedures. Classify these as Conceptual, not Procedural. The key test: can you number the steps and get a natural sequence?

## Constraints

- No raw dumps into output files — always synthesize
- No guessing unreadable content — mark "needs review"
- Never skip glossary — it's the most-used file for lookups
- No cross-file content mixing — each file has a distinct purpose
- Every extracted concept carries a source backlink to its chapter/section — no orphaned knowledge
- Always clean up `/tmp/booqs/`
- Prefer Write tool for new files over heredocs
- Use `uv sync` for dep installs, not pip
- **For procedural extraction, Stage 1 and Stage 2 must run as separate passes.** Do not skip Stage 1 intermediate data. The two-stage architecture prevents extraction errors from propagating into the graph structure.

## Design principles

1. **Density over completeness** — 1K token summary beats 10K excerpt. Compress, don't copy.
2. **Practitioner voice** — "Use X when Y" not "The source explains X." Agent thinks in action.
3. **Front-load SKILL.md** — First ~5K tokens are always in context. Lead with mental models and chapter index.
4. **On-demand chapters** — Never inline chapter content into SKILL.md. Load only what's asked for.
5. **Always synthesize** — Every sentence is a step removed from the source: compressed, interpreted, structured.
6. **Extract mechanics, not descriptions** — If the source says "Event Sourcing is a pattern where...", skip that sentence. Capture only: what concrete problem it solves, the specific conditions under which it backfires (event schema evolution cost, replay latency), and what trades it forces versus alternatives. A practitioner needs to know _when to choose it and when it burns them_, not what it is.
7. **Two-stage procedural extraction** — Separate the concerns: Stage 1 extracts raw action-object-equipment-temporal data; Stage 2 structures it into a graph. This separation (from Carriero et al. 2024) is what makes LLM procedural extraction reliable at scale.
8. **Implicit equipment is real equipment** — If a step says "wipe the screen" and an earlier step mentions "microfiber cloth", the cloth is equipment for the wipe step. The model should carry tools forward through the procedure. Missing implicit equipment is the most common procedural extraction failure — be aggressive about including it.
