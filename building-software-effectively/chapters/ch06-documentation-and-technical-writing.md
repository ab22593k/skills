# Documentation and Technical Writing

## Core concepts

- Documentation is a form of technical debt that doesn't break systems but degrades team performance over time. AI tools can generate 90% of a documentation deliverable in seconds.
- Four types: API/SDK docs, internal specs, user guides, release notes. Different tools excel at different types — Scribe for visual user guides, Swimm for in-repo code docs.
- Best results come from creating prompt templates with predefined sections. This prevents unnecessarily long or unstructured documents.

## Frameworks introduced

**Documentation types matrix** — Match tool to doc type: Swimm (internal code docs, repo-integrated), ChatGPT (general-purpose, best quality), Cursor (IDE-integrated, full codebase context), Scribe (visual user guides from screen recordings).

**Prompt templates for docs** — Create a standard template with sections (overview, technical implementation, test plan, etc.). Use the same template across all prompts to ensure consistency, just as you'd set coding guidelines.

## Key techniques

**Repository-integrated documentation (Swimm):** Connects to the repo and creates/updates docs on each PR. Ensures documentation stays current with code changes. Currently limited to one file per document.

**Screen recording to user guide (Scribe):** Record a browser session → get an annotated step-by-step workflow guide. Best for bug reports, SOPs, and product guides. The AI-generated document output is generic; best used as a visual capture tool.

## Connection to other chapters

Documents the side of development that engineers typically neglect. Follows the same evaluation pattern as Chapters 1-5. The prompt template approach mirrors the coding standards approach from Chapter 1.
