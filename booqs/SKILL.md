---
name: booqs
description: "Converts any documentation source — book (PDF/EPUB), URL, git repo, directory, or text file — into a structured, token-efficient knowledge base for LLM consumption. Extracts frameworks, mental models, principles, techniques, anti-patterns, and organized references. Trigger on: 'turn this into a skill', 'create a skill from', 'I want to study', 'study this documentation', 'add this to my skills', 'convert this to a skill', 'make a skill from', 'analyze this book/docs/repo', 'extract frameworks from'. Use when the user provides a path to a PDF/EPUB, a URL to documentation, a git repo URL, a local directory of docs, or any text source, and wants to build a reusable, structured knowledge base from it."
---

## Pipeline

`0. Detect type → 1. Extract → 2. Analyze → 3. Generate files → 4. Install`

## Step 0 — Detect source type

| Input | Type | Strategy |
|---|---|---|
| `https://...` | URL | firecrawl_scrape / webfetch |
| `github.com/...` or `git@` | Git repo | `git clone --depth 1` → walk docs |
| Local dir path | Directory | Walk `.md`/`.rst`/`.html` files |
| `.pdf` file | File | `extract.py --mode technical` |
| `.epub` file | File | `extract.py` |
| `.md` / `.txt` file | File | `extract.py` |
| Other extension | Unknown | Sniff magic bytes |

Slug from source name: lowercase, `[^a-z0-9]+` → `-`, strip edges.

## Step 1 — Extract text by source type

**URL** — `firecrawl_scrape` (or webfetch fallback). Save to `/tmp/booqs/full_text.txt` + `metadata.json` (`{source_type,url,estimated_tokens,chapters_detected}`). For multi-page docs: `firecrawl_map` sub-pages, sitemap, or use `waitFor` for JS-rendered.

**Git repo** — `git clone --depth 1 <url> /tmp/booqs/repo/`. Find `.md`/`.rst`/`.html`/`.txt` (prioritize README, docs/). Concatenate into `full_text.txt` with `[FILE: path]` markers. Skip `node_modules/`, `.git/`, `__pycache__/`, vendor dirs, binary files. Metadata: `{source_type:git, repo, files_discovered, files_read, estimated_tokens}`.

**Directory** — Recursively walk `.md`/`.rst`/`.html`/`.txt` files. Skip hidden dirs (`.`/`__`), build artifacts (`node_modules/`,`target/`,`dist/`,`build/`). Same concat format as git. Same metadata shape.

**File (PDF/EPUB/MD/TXT)** — `python3 <skill-dir>/scripts/extract.py "<path>" --mode <technical|text>`. For PDFs, first read ~2K token sample and signal-detect:

| Signal | Check | High if | → mode |
|---|---|---|---|
| Code density | ` ``` ` `{` `def` `fn` | >5 blocks/2K | technical |
| Table density | `|` rows, columns | >3 patterns/2K | technical |
| Formula density | `=` `∑` `∫` `→` | >5/2K | technical |
| Framework terms | Named models/theorems | >3 | text |
| Prose ratio | Paragraph vs heading | >80% | text |

Decision: high code/table/formula → `technical`; frameworks/prose → `text`. EPUBs always use ebooklib. On failure: suggest `uv sync`.

**Token-efficient extraction rules:**
- Read metadata with `jq` or `python3 -c "import json;..."` — don't Read the full JSON file
- Check file size with `wc -l` / `wc -c` before reading source text
- If >50K tokens, read first ~15K + section markers, then sample
- Use `grep -n "^#\|^Chapter\|^[A-Z ]\{5,\}"` to find section markers without reading full file
- Use `wc -l /tmp/booqs/full_text.txt` to assess size cheaply
- For metadata fields: `python3 -c "import json; m=json.load(open('/tmp/booqs/metadata.json')); print(m['estimated_tokens'], m['chapters_detected'])"`

## Step 2 — Analyze

Read `/tmp/booqs/full_text.txt` (sampled if >50K). Per section identify: **Frameworks**, **Mental models**, **Principles**, **Techniques**, **Anti-patterns**, **Decision trees**. Produce 800–1,200 token summaries with code examples for technical content.

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

Body order: Core mental models (When→Idea→Apply→Pitfalls per model), Query routing table, Chapter index (#,Title,Topic,Best for), Reference file pointers.

Chapter frontmatter: `chapter:N` `topic:"..."` `when:"User needs...", queries:["..."]`. Body: Core concepts→Frameworks→Techniques→Connections (+ Code/Reference tables if technical).

Glossary: `**term** — definition. (→ chN)`. Patterns: `## Name` + Type/Context/Solution/Consequences/Related. Cheatsheet: `## Choosing X` + `If|Then` table.

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
- **Sample strategically**: head 15K + grep section markers for large files
- **Never Read entire JSON/metadata files** — use `python3 -c "import json;..."` to extract one field
- **Batch operations** when possible (e.g., `find ... -exec cat {} +` instead of Read loop)
- **Use Write tool** for new file creation (not bash heredocs)
- **Use Edit tool** for code modifications (reviewability > token cost for code)
- **Summarize, don't dump** — structured summaries of contents, not raw outputs

## Edge cases

- >150K tokens: read only section markers + 2K per section sample
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
- Always clean up `/tmp/booqs/`
- Prefer Write tool for new files over heredocs
- Use `uv sync` for dep installs, not pip

## Design principles

1. **Density over completeness** — 1K token summary beats 10K excerpt. Compress, don't copy.
2. **Practitioner voice** — "Use X when Y" not "The source explains X." Agent thinks in action.
3. **Front-load SKILL.md** — First ~5K tokens are always in context. Lead with mental models and chapter index.
4. **On-demand chapters** — Never inline chapter content into SKILL.md. Load only what's asked for.
5. **Always synthesize** — Every sentence is a step removed from the source: compressed, interpreted, structured.
