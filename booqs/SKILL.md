---
name: booqs
description: "Converts a technical book (PDF or EPUB) into a structured Agent Code skill — extracting frameworks, mental models, principles, techniques, and anti-patterns. Trigger on: 'turn this book into a skill', 'create a skill from this PDF/EPUB', 'I want to study [book]', 'add this book to my skills', 'convert PDF/EPUB to skill', 'analyze this book', 'extract frameworks from this book'. Use when the user provides a path to a PDF or EPUB and wants to build a reusable knowledge base from it, or wants to study a book through an AI agent."
---

# Booqs

Converts a PDF/EPUB technical book into a structured Agent Code skill — a browsable knowledge base of frameworks, mental models, principles, techniques, and anti-patterns.

## Query routing

| User asks... | Load this section |
|---|---|
| "turn this PDF into a skill" | Pipeline → Steps 1–6 |
| "what extraction method should I use" | Step 2 (Pattern matching) → Step 3 |
| "how should I structure the output" | Step 5 (Generate files, templates) |
| "what if the book has no chapters" | Edge cases |
| "this book is 500 pages" | Edge cases (very large books) |
| extraction script failed | Step 3 (dependency install) |

## Pipeline

1. Validate input → 2. Detect book type → 3. Extract text → 4. Analyze → 5. Generate files → 6. Install

## Step 1 — Validate input

Verify the file exists and has a supported extension (.pdf, .epub, .txt, .md). If no extension, sniff magic bytes: PDF starts with `%PDF`, EPUB starts with ZIP magic `PK`. If unsupported, list supported formats and stop.

Derive the skill slug from the filename if none was provided: lowercase, replace non-alphanumeric with hyphens, strip leading/trailing hyphens.

## Step 2 — Detect book type with pattern matching

Read a ~2K token sample from the start of the book and score these signals to auto-detect extraction strategy:

| Signal | Detected by | High if... | Implies |
|---|---|---|---|
| Code density | Count ` ``` `, indented blocks `    `, `{` `}` `fn` `def` `class` | >5 code blocks per 2K tokens | Technical — tables, code structure matter |
| Table density | Count `|` row patterns, aligned columns | >3 row patterns per 2K tokens | Technical — layout matters |
| Framework terms | Named models, theorems, patterns (e.g., "CAP theorem", "observer pattern") | >3 named frameworks | Text-heavy — concepts matter more than code |
| Formula density | Math notation: `=`, `∑`, `∫`, `→`, superscript patterns | >5 formulas per 2K tokens | Technical — Docling preserves formulas |
| Prose ratio | Paragraph-to-heading ratio | >80% paragraph text | Text-heavy — fast extraction OK |

**Decision tree:**
- High code **or** table **or** formula density → `--mode technical` (Docling preserves structure)
- High framework terms **or** prose ratio → `--mode text` (PyMuPDF fast fallback chain)
- Mixed signals → show the evidence to the user and let them choose
- If the user explicitly provided `--mode`, skip detection and use their choice
- EPUBs always use ebooklib regardless of mode

## Step 3 — Extract text

```bash
python3 <skill-dir>/scripts/extract.py "<path-to-book>" --mode <technical|text>
```

The script writes:

- `/tmp/booqs/full_text.txt` — extracted text
- `/tmp/booqs/metadata.json` — stats (method, pages, tokens, chapters, ToC)

Read the metadata first. Key fields: `extraction_method`, `estimated_tokens`, `chapters_detected`, `has_toc`.

If extraction fails, show the error and suggest running `uv sync` from the skill directory.

## Step 4 — Analyze text

Read `/tmp/booqs/full_text.txt`. If >50K tokens, read the first ~15K tokens plus chapter markers, then sample strategically.

Identify these six categories per chapter:

- **Frameworks** — Named conceptual structures (e.g., "CAP theorem", "strangler fig")
- **Mental models** — Ways of thinking the author teaches (e.g., "thinking in streams")
- **Principles** — Rules of thumb (e.g., "prefer composition over inheritance")
- **Techniques** — Specific procedures (e.g., "pipeline pattern with channels")
- **Anti-patterns** — What NOT to do (e.g., "the blob", "god class")
- **Decision trees** — "Use X when Y, use Z when W"

For each chapter, produce a 800–1,200 token summary: core idea, frameworks introduced, connections. For technical mode, include key code examples and tables.

## Step 5 — Generate skill files

Create files in `/tmp/booqs/<slug>/`.

### File structure

```
<slug>/
├── SKILL.md            # ~4,000 tokens — core mental models + chapter index
├── chapters/
│   ├── ch01-<slug>.md  # ~1,000 tokens each
│   ├── ch02-<slug>.md
│   └── ...
├── glossary.md         # ~1,500 tokens — key terms, alphabetized
├── patterns.md         # ~2,000 tokens — techniques, algorithms, patterns
└── cheatsheet.md       # ~1,000 tokens — decision tables, quick-reference
```

### SKILL.md template

```yaml
---
name: <slug>
description: "<one-sentence summary focusing on what the book teaches you to do>"
---
```

Body sections in order:

**Core mental models** — Per model: **When to use** → **The idea** → **How to apply** → **Pitfalls**

**Query routing** — Map user questions to chapters. Same format as this page.

**Chapter index** — Table with #, Title, Topic, Best for (critical for on-demand loading).

**Reference files** — Pointers to glossary.md, patterns.md, cheatsheet.md.

### Chapter file template

```yaml
---
chapter: N
topic: "..."
when: "User needs...", queries: ["...", "..."]
---
```

Followed by: **Core concepts** → **Frameworks introduced** → **Key techniques** → **Connection to other chapters**. For technical mode, also add **Code examples** and **Reference tables**.

### Glossary format

```
**term** — definition. (→ chN)
```

Alphabetized. Every key term the book introduces.

### Patterns format

```markdown
## Pattern Name

**Type:** technique | principle | anti-pattern
**Context:** When to use this
**Solution:** What to do
**Consequences:** What happens
**Related:** (→ skill.md), (→ chN)
```

### Cheatsheet format

Decision tables for skimming:

```markdown
## Choosing X

| If          | Then       |
| ----------- | ---------- |
| condition A | approach Y |
| condition B | approach Z |
```

## Step 6 — Install

```bash
mkdir -p ~/.agents/skills/<slug>
cp -r /tmp/booqs/<slug>/* ~/.agents/skills/<slug>/
```

Tell the user the slug, chapter count, estimated total tokens, and a usage example.

## Edge cases

**Missing dependencies** — Run `uv sync` from the skill directory.

**Very large books (300+ pages / 150K+ tokens)** — Read only chapter markers and a ~2K token sample from each chapter's first page. Generate summaries from samples.

**No clear chapter structure** — If `chapters_detected` is 0, scan for "Chapter N", numbered sections, all-caps headings. If still nothing, create a single-chapter skill.

**Skill already exists** — Warn and ask before overwriting.

**Partial failures** — Note diagram-heavy pages as "needs review."

## What NOT to do

- Don't dump raw extracted text into skill files. Every output must be a synthesis.
- Don't guess chapter content you can't identify — mark as "needs review."
- Don't skip the glossary. It's the most useful file for precise lookups.
- Don't mix content across files (cheatsheet into SKILL.md, patterns into glossary). Each file has a purpose.
- Don't leave orphaned `/tmp/booqs/` directories. Clean up always.

## Design principles

1. **Density over completeness** — 1K token summary beats 10K excerpt. Compress, don't copy.
2. **Practitioner voice** — "Use X when Y" not "The book explains X." Agent thinks in action.
3. **Front-load SKILL.md** — First ~5K tokens are always in context. Lead with mental models and chapter index.
4. **On-demand chapters** — Never inline chapter content into SKILL.md. Load only what's asked for.
5. **Always synthesize** — Every sentence is a step removed from the source: compressed, interpreted, structured.
