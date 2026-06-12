---
name: booqs
description: "Converts any documentation source — book (PDF/EPUB), URL, git repo, directory, or text file — into a structured, token-efficient knowledge base for LLM consumption. Extracts frameworks, mental models, principles, techniques, anti-patterns, and organized references. Trigger on: 'turn this into a skill', 'create a skill from', 'I want to study', 'study this documentation', 'add this to my skills', 'convert this to a skill', 'make a skill from', 'analyze this book/docs/repo', 'extract frameworks from'. Use when the user provides a path to a PDF/EPUB, a URL to documentation, a git repo URL, a local directory of docs, or any text source, and wants to build a reusable, structured knowledge base from it."
---

## Pipeline

`0. Detect type → 1. Extract → 1b. Chunk (if >50K) → 2. Analyze → 3. Generate files → 4. Install`

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
   - Read the first ~3K tokens (preface, introduction, opening) — captures the book's central argument, intended audience, high-level structure
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

## Step 2 — Analyze

Read `/tmp/booqs/full_text.txt` (or the chunked representation if >50K). Per section extract:

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

## Step 3 — Generate files

Output: `/tmp/booqs/<slug>/`

```
SKILL.md          ~4K tokens — mental models, chapter index, query routing
chapters/chN.md   ~1K each — core ideas, frameworks, techniques, connections
glossary.md       ~1.5K — alphabetized key terms → chN
patterns.md       ~2K — techniques, principles, anti-patterns with context
cheatsheet.md     ~1K — decision tables for quick reference
```

SKILL.md frontmatter: `name:<slug>` + `description:"one-sentence actionable summary"`.

Body order: Core mental models (When→Idea→Apply→Pitfalls per model), Query routing table, Chapter index (#,Title,Topic,Best for,Source chapter), Reference file pointers.

Every concept, pattern, and technique must carry a **source backlink** — the chapter/section it came from — so a practitioner can return to the original for full context. Format: `(→ chN)` for chapter-level, `(→ §Reliability/Hardware Faults)` for section-level.

Chapter frontmatter: `chapter:N` `topic:"..."` `when:"User needs...", queries:["..."]`. Body: Core concepts→Frameworks→Techniques→Trade-off matrices→Connections (+ Code/Reference tables if technical). Every technique section must include **failure conditions** — the specific bounds beyond which the approach degrades.

Glossary: `**term** — definition. (→ chN)`. Source every term to the author's own definition — not a generic one. If the book coins a term (e.g., "two-phase commit"), include the precise way the author frames it since that carries their analytical lens. Patterns: `## Name` + Type/Context/When it fails (boundary conditions)/Solution/Consequences/Related + `(→ §ParentSection)`. Lead with the failure regime — the conditions under which this pattern breaks — then the solution. Cheatsheet: `## Choosing X` + `If|Then` table; prefer comparison matrices (two-axis grids showing which approach wins given X vs Y) over simple If/Then lists. Every entry includes its source section.

**Token-efficient generation:** Apply same density rules to every output file. Never dump raw text. Each file must justify its token budget.

## Step 4 — Install

```bash
mkdir -p ~/.agents/skills/<slug> && cp -r /tmp/booqs/<slug>/* "$_"
```

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

## Constraints

- No raw dumps into output files — always synthesize
- No guessing unreadable content — mark "needs review"
- Never skip glossary — it's the most-used file for lookups
- No cross-file content mixing — each file has a distinct purpose
- Every extracted concept carries a source backlink to its chapter/section — no orphaned knowledge
- Always clean up `/tmp/booqs/`
- Prefer Write tool for new files over heredocs
- Use `uv sync` for dep installs, not pip

## Design principles

1. **Density over completeness** — 1K token summary beats 10K excerpt. Compress, don't copy.
2. **Practitioner voice** — "Use X when Y" not "The source explains X." Agent thinks in action.
3. **Front-load SKILL.md** — First ~5K tokens are always in context. Lead with mental models and chapter index.
4. **On-demand chapters** — Never inline chapter content into SKILL.md. Load only what's asked for.
5. **Always synthesize** — Every sentence is a step removed from the source: compressed, interpreted, structured.
6. **Extract mechanics, not descriptions** — If the source says "Event Sourcing is a pattern where...", skip that sentence. Capture only: what concrete problem it solves, the specific conditions under which it backfires (event schema evolution cost, replay latency), and what trades it forces versus alternatives. A practitioner needs to know _when to choose it and when it burns them_, not what it is.
