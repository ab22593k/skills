---
name: booqs
description: "Converts any documentation source — book (PDF/EPUB), URL, git repo, directory, or text file — into a structured, token-efficient knowledge base for LLM consumption. Extracts frameworks, mental models, principles, techniques, anti-patterns, and organized references. Trigger on: 'turn this into a skill', 'create a skill from', 'I want to study', 'study this documentation', 'add this to my skills', 'convert this to a skill', 'make a skill from', 'analyze this book/docs/repo', 'extract frameworks from'. Use when the user provides a path to a PDF/EPUB, a URL to documentation, a git repo URL, a local directory of docs, or any text source, and wants to build a reusable, structured knowledge base from it."
---

# Booqs

Converts any documentation source — book, URL, git repo, directory, or file — into a structured, token-efficient knowledge base for LLM consumption.

## Query routing

| User asks... | Load this section |
|---|---|
| "turn this PDF into a skill" | Detect source type → File path |
| "turn this website into docs" | Detect source type → URL |
| "turn this repo into a skill" | Detect source type → Git repo |
| "study this docs folder" | Detect source type → Directory |
| "what extraction method should I use" | Detect source type → pattern matching |
| "how should I structure the output" | Step 3 (Generate files, templates) |
| "what if the source has no chapters" | Edge cases |
| "this source is huge" | Edge cases (very large sources) |
| extraction / fetch failed | Dependencies |

## Pipeline

0. Detect source type → 1. Extract text → 2. Analyze → 3. Generate files → 4. Install

## Step 0 — Detect source type

Determine what kind of input the user provided:

| Input looks like... | Source type | Extraction strategy |
|---|---|---|
| `https://` or `http://` URL | URL | Firecrawl scrape or webfetch |
| `github.com/owner/repo` or `git@` URL | Git repo | `git clone` → discover docs |
| Local directory path (ends in `/` or no extension) | Directory | Walk `.md`/`.html`/`.rst` files |
| `.pdf` file | File (PDF) | `scripts/extract.py --mode technical` |
| `.epub` file | File (EPUB) | `scripts/extract.py` |
| `.md` or `.txt` file | File (text) | `scripts/extract.py` |
| Other file extension | File (unknown) | Sniff magic bytes or read directly |

Derive the skill slug from the source name: lowercase, replace non-alphanumeric with hyphens, strip leading/trailing hyphens.

## Step 1 — Extract text by source type

### Source: URL

Fetch the page or documentation site content:

```markdown
1. Use firecrawl_scrape or webfetch to get the content
2. Save to /tmp/booqs/full_text.txt
3. Save metadata to /tmp/booqs/metadata.json:
   {"source_type": "url", "url": "...", "estimated_tokens": N, "chapters_detected": M}
```

For multi-page docs (SPAs, doc sites), try:
- `firecrawl_map` to discover sub-page URLs, then scrape each
- Look for a sitemap or table of contents on the main page
- If JavaScript-rendered, use `waitFor` or the firecrawl agent

If firecrawl is unavailable, fall back to `webfetch`.

### Source: Git repo

```bash
git clone --depth 1 <repo-url> /tmp/booqs/repo/
```

Then discover documentation files:

```
Find all .md, .rst, .html, .txt files under /tmp/booqs/repo/
Prioritize: README*, docs/, doc/, wiki/, *.md docs/*.md
```

Read the key doc files and concatenate them into `/tmp/booqs/full_text.txt` with clear file-path markers:

```
[FILE: README.md]
...
[FILE: docs/getting-started.md]
...
```

Skip: `node_modules/`, `.git/`, `__pycache__/`, binary files, vendor directories.

Save metadata:
```json
{"source_type": "git", "repo": "...", "files_discovered": N, "files_read": N, "estimated_tokens": N}
```

### Source: Directory

Walk the directory tree recursively, collect `.md`, `.rst`, `.html`, `.txt` files. Skip hidden dirs (`.`, `__`), build artifacts (`node_modules/`, `target/`, `dist/`, `build/`), and binary files.

Read and concatenate into `/tmp/booqs/full_text.txt` with file-path markers (same format as git repo above).

Save metadata:
```json
{"source_type": "directory", "path": "...", "files_discovered": N, "files_read": N, "estimated_tokens": N}
```

### Source: File (PDF / EPUB / MD / TXT)

Run the extraction script:

```bash
python3 <skill-dir>/scripts/extract.py "<path-to-file>" --mode <technical|text>
```

Read metadata at `/tmp/booqs/metadata.json`. Key fields: `extraction_method`, `estimated_tokens`, `chapters_detected`, `has_toc`.

If the file is a markdown or text file, the script reads it directly. For PDFs also run content-type detection:

Read a ~2K token sample and score these signals:

| Signal | Detected by | High if... | Implies |
|---|---|---|---|
| Code density | Count ` ``` `, indented blocks, `{` `}` `fn` `def` | >5 code blocks per 2K | Technical — use Docling |
| Table density | Count `|` row patterns, aligned columns | >3 row patterns per 2K | Technical — use Docling |
| Framework terms | Named models, theorems, patterns | >3 named frameworks | Text-heavy — fast extraction OK |
| Formula density | Math notation: `=`, `∑`, `∫`, `→` | >5 formulas per 2K | Technical — use Docling |
| Prose ratio | Paragraph-to-heading ratio | >80% paragraph text | Text-heavy — fast extraction OK |

**Decision tree:**
- High code **or** table **or** formula density → `--mode technical`
- High framework terms **or** prose ratio → `--mode text`
- Mixed → show evidence and let user choose
- EPUBs always use ebooklib regardless of mode

If extraction fails, suggest `uv sync` from the skill directory.

## Step 2 — Analyze text

Read `/tmp/booqs/full_text.txt`. If >50K tokens, read the first ~15K tokens plus section markers, then sample strategically.

Identify these six categories per section:

- **Frameworks** — Named conceptual structures (e.g., "CAP theorem", "strangler fig")
- **Mental models** — Ways of thinking the author teaches (e.g., "thinking in streams")
- **Principles** — Rules of thumb (e.g., "prefer composition over inheritance")
- **Techniques** — Specific procedures (e.g., "pipeline pattern with channels")
- **Anti-patterns** — What NOT to do (e.g., "the blob", "god class")
- **Decision trees** — "Use X when Y, use Z when W"

For each section/chapter, produce a 800–1,200 token summary: core idea, frameworks introduced, connections. For technical sources, include key code examples and tables.

## Step 3 — Generate skill files

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
description: "<one-sentence summary focusing on what the source teaches you to do>"
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

Followed by: **Core concepts** → **Frameworks introduced** → **Key techniques** → **Connection to other sections**. For technical content, also add **Code examples** and **Reference tables**.

### Glossary format

```
**term** — definition. (→ chN)
```

Alphabetized. Every key term the source introduces.

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

## Step 4 — Install

```bash
mkdir -p ~/.agents/skills/<slug>
cp -r /tmp/booqs/<slug>/* ~/.agents/skills/<slug>/
```

Tell the user the slug, section count, estimated total tokens, and a usage example.

## Dependencies

- **Any source**: Python 3.10+, `uv`
- **PDF extraction**: PyMuPDF, pdftotext (poppler-utils), PyPDF2, pdfminer.six, docling
- **EPUB extraction**: ebooklib, beautifulsoup4
- **URL fetching**: firecrawl MCP tools, or webfetch
- **Git repo**: `git` CLI
- **Install all**: `uv sync` from the skill directory

## Edge cases

**Very large sources (300+ pages / 150K+ tokens)** — Read only section markers and a ~2K token sample from each section's start. Generate summaries from samples.

**No clear section structure** — If section detection yields 0, scan for markdown headings, numbered sections, all-caps headings. If still nothing, create a single-chapter skill.

**Skill already exists** — Warn and ask before overwriting.

**Partial failures** — Note sections you couldn't extract as "needs review."

**URL behind login** — Note to the user that authentication isn't supported; suggest saving the page content to a file first.

**Very large git repo** — Use `--depth 1` for fast clone. If docs are spread across many files, prioritize top-level README + docs/ directory.

## What NOT to do

- Don't dump raw extracted text into skill files. Every output must be a synthesis.
- Don't guess section content you can't identify — mark as "needs review."
- Don't skip the glossary. It's the most useful file for precise lookups.
- Don't mix content across files (cheatsheet into SKILL.md, patterns into glossary). Each file has a purpose.
- Don't leave orphaned `/tmp/booqs/` directories. Clean up always.

## Design principles

1. **Density over completeness** — 1K token summary beats 10K excerpt. Compress, don't copy.
2. **Practitioner voice** — "Use X when Y" not "The source explains X." Agent thinks in action.
3. **Front-load SKILL.md** — First ~5K tokens are always in context. Lead with mental models and chapter index.
4. **On-demand chapters** — Never inline chapter content into SKILL.md. Load only what's asked for.
5. **Always synthesize** — Every sentence is a step removed from the source: compressed, interpreted, structured.
