# AGENTS.md

OpenCode skills collection. Each skill is a directory with `SKILL.md` (frontmatter `name`/`description`, where `name` matches the directory) plus optional `references/` and `evals/`.

## Tooling

Use Bun (latest) for all JS/TS work; there are no npm scripts.

- Install: `bun install`
- Lint: `bunx eslint .`
- Format check/fix: `bun fmt --check` / `bun fmt src test/a.test.ts`
- Bun transpiles but does not type-check; run `bunx tsc --noEmit` separately if a `tsconfig.json` exists.

## Governance

Skill authoring rules live in `.specify/memory/constitution.md` (supersedes this file on conflict). Key constraints: one capability per skill, explicit triggers/non-goals, evidence-based claims with versions, evals covering happy path + a known failure mode, token-efficient content.

## Python tooling

Scripts (e.g. `linux-kernel-map/scripts/*.py`) need Python 3.10+. Packaging validation optionally needs `uvx` and `skills-ref` (Python 3.11+).

## Local-only state

`specs/` and `.specify/feature.json` are machine-local; do not commit them. `.specify/` tracked files are shared scaffold.
