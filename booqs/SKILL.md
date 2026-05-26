---
name: booqs
description: Converts a technical book (PDF or EPUB) into a structured Agent Code skill — extracting frameworks, mental models, principles, techniques, and anti-patterns the author crystallized. Use when the user wants to study a book through Agent, apply an author's frameworks while working, or build a reusable knowledge base from any PDF or EPUB.
when_to_use: Trigger phrases — "turn this book into a skill", "create a skill from this PDF", "create a skill from this EPUB", "I want to study X book", "add this book to my skills", "convert PDF to skill", "convert EPUB to skill", "analyze this book", "extract frameworks from this book". Accepts a path to a PDF or EPUB and optional skill name slug.
disable-model-invocation: true
context: fork
agent: general-purpose
allowed-tools: Bash(python3 *) Bash(pdftotext *) Bash(mkdir *) Bash(cp *) Bash(find *) Bash(wc *) Bash(echo *) Bash(cat *) Bash(date *) Read Write Glob Grep
argument-hint: <path-to-pdf-or-epub> [skill-name-slug]
arguments: [book_path, skill_name]
effort: high
---

# Booqs

Converts a technical book (PDF or EPUB) into a structured Agent Code skill. The output is a browsable knowledge base of the author's frameworks, mental models, principles, techniques, and anti-patterns — organized so Agent can load only what it needs.

## Pipeline

1. Validate the input file
2. Ask the user whether the book is **technical** (code, tables, formulas) or **text-heavy** (prose)
3. Extract text via `scripts/extract.py`
4. Analyze extracted text — identify structure, frameworks, patterns
5. Generate skill files (SKILL.md, chapters, glossary, patterns, cheatsheet)
6. Install to `~/.agents/skills/<slug>/`

## Step 1 — Validate input

Verify the file exists and has a supported extension (.pdf, .epub, .txt, .md). If no extension, sniff magic bytes: PDF starts with `%PDF`, EPUB starts with ZIP magic `PK`. If unsupported, list the supported formats and stop.

Derive the skill slug from the filename if none was provided: lowercase, replace non-alphanumeric with hyphens, strip leading/trailing hyphens.

## Step 2 — Ask technical or text-heavy

Ask: "Is this a technical book with tables, code blocks, and diagrams? Or text-heavy prose?"

- **technical** → Docling (layout-aware, preserves tables/code as markdown)
- **text-heavy** → PyMuPDF → pdftotext → PyPDF2 → pdfminer (fast fallback chain)
- EPUBs always use ebooklib regardless of mode

If the user is unsure, default to **text-heavy** — it's faster and they can re-run with `--mode technical`.

## Step 3 — Extract text

```bash
python3 <skill-dir>/scripts/extract.py "<path-to-book>" --mode <technical|text>
```

The script writes:

- `/tmp/booqs/full_text.txt` — extracted text
- `/tmp/booqs/metadata.json` — stats (method, pages, tokens, chapters detected, TOC presence)

Read the metadata first. Key fields: `extraction_method`, `estimated_tokens`, `chapters_detected`, `has_toc`.

If extraction fails, show the error and suggest running `uv sync` from the skill directory.

## Step 4 — Analyze the text

Read `/tmp/booqs/full_text.txt`. If it's very large (>50K tokens), read just the first ~15K tokens plus chapter markers, then sample strategically.

Identify:

**Frameworks** — Named conceptual structures the reader applies (e.g., "CAP theorem", "strangler fig pattern")
**Mental models** — Ways of thinking the author teaches (e.g., "thinking in streams")
**Principles** — Rules of thumb (e.g., "prefer composition over inheritance")
**Techniques** — Specific methods or procedures
**Anti-patterns** — What NOT to do (e.g., "the blob", "god class")
**Decision trees** — "Use X when Y, use Z when W" trade-offs

For each chapter, produce a summary of 800–1,200 tokens: the core idea, frameworks introduced, how it connects to other chapters. For technical mode, include key code examples and tables.

## Step 5 — Generate skill files

Create files in `/tmp/booqs/<slug>/`.

### File structure

```
<slug>/
├── SKILL.md            # ~4,000 tokens — core mental models + chapter index
├── chapters/
│   ├── ch01-<slug>.md  # ~1,000 tokens each — one per chapter
│   ├── ch02-<slug>.md
│   └── ...
├── glossary.md         # ~1,500 tokens — all key terms, alphabetized
├── patterns.md         # ~2,000 tokens — techniques, algorithms, patterns
└── cheatsheet.md       # ~1,000 tokens — decision tables, quick-reference
```

### SKILL.md

Frontmatter uses the skill's slug as name and a one-sentence actionable description.

```yaml
---
name: <slug>
description: "<one-sentence summary focusing on what the book teaches you to do>"
effort: medium
---
```

Body sections in order:

**Core mental models** — For each framework/mental model the author builds:

- **Name** — What it's called
- **When to use** — What problem this framework solves (1-2 sentences)
- **The idea** — How it works (2-3 sentences)
- **How to apply** — The practical move (1-2 sentences)
- **Pitfalls** — What goes wrong if misapplied (1 sentence)

**How to use this skill** — Brief usage guide showing the slug commands.

**Chapter index** — Table with #, Title, Topic, Tokens (~1K each). This is critical for on-demand loading: Agent reads the index to decide which chapter file to open.

**Reference files** — Pointers to glossary.md, patterns.md, cheatsheet.md with what each contains.

### Chapter file format

Each chapter must stand alone since Agent reads only one at a time:

```markdown
# Chapter Title

## Core concepts

3-5 key takeaways

## Frameworks introduced

List with brief explanations

## Key techniques

Step-by-step if applicable

## Connection to other chapters

How this fits the book's narrative
```

For technical mode books, also add:

- **Code examples** — Key snippets (not everything, just the illuminating ones)
- **Reference tables** — Tables or formulas the chapter introduces

### Glossary format

```
**term** — definition. (Chapter N)
```

Alphabetized. Every key term the book introduces.

### Patterns format

```markdown
## Pattern Name

**Type:** technique | principle | anti-pattern
**Context:** When to use this
**Solution:** What to do
**Consequences:** What happens as a result
**Related:** Links to other patterns
```

### Cheatsheet format

Decision tables for skimming:

```markdown
## Choosing X

| If          | Then       |
| ----------- | ---------- |
| condition A | approach Y |
| condition B | approach Z |

## Quick reference

- Rule 1: ...
```

## Step 6 — Install

```bash
mkdir -p ~/.agents/skills/<slug>
cp -r /tmp/booqs/<slug>/* ~/.agents/skills/<slug>/
```

Tell the user the slug, number of chapters, estimated total tokens, and a usage example.

## Design principles

1. **Density over completeness.** A 1,000-token summary beats a 10,000-token excerpt. Compress, don't copy.
2. **Practitioner voice.** Write "Use X when Y" not "The book explains X." Agent thinks in action.
3. **Front-load SKILL.md.** The first ~5,000 tokens are always in context. Lead with mental models and chapter index.
4. **On-demand chapters.** Never inline chapter content into SKILL.md. Load only what's asked for.
5. **Always synthesize.** Every sentence should be a step removed from the source — compressed, interpreted, structured.

## Edge cases

**Missing dependencies** — Tell the user exactly which command to run: `uv sync` from the skill directory.

**Very large books (300+ pages / 150K+ tokens)** — Read only chapter markers and a ~2K token sample from each chapter's first page. Generate summaries from samples.

**No clear chapter structure** — If `chapters_detected` is 0, manually scan for patterns like "Chapter N", numbered sections, all-caps headings. If still nothing, create a single-chapter skill.

**Skill already exists** — Warn the user and ask before overwriting.

**Partial failures** — If a chapter was mostly diagrams and you couldn't extract meaning, note it as "needs review" in the chapter file.

## What NOT to do

- Don't dump raw extracted text into skill files. Every output must be a synthesis.
- Don't guess chapter content you can't identify — mark as "needs review."
- Don't skip the glossary. It's the most useful file for precise lookups.
- Don't mix content across files (cheatsheet into SKILL.md, patterns into glossary). Each file has a purpose.
- Don't leave orphaned `/tmp/booqs/` directories. Clean up always.
