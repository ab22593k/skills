<!--
Sync Impact Report
- Version change: (none) → 1.0.0 (initial ratification)
- Modified principles: none (all 5 principles newly defined from scaffold placeholders)
- Added sections:
  - Core Principles: I. Skill Atomicity, II. Explicit Triggering, III. Evidence Over Recall, IV. Evaluated Capability (NON-NEGOTIABLE), V. Token-Efficient Simplicity
  - Additional Constraints: SKILL.md schema, quality gates, external sourcing
  - Development Workflow: propose → implement → evaluate → review lifecycle
  - Governance: ratified with amendment procedure, versioning policy, compliance review
- Removed sections: none (scaffold placeholders instantiated, not removed)
- Follow-up TODOs: none — all placeholders resolved
-->

# Skills Constitution

## Core Principles

### I. Skill Atomicity

Every skill MUST represent exactly one capability with a single, verifiable
purpose. A skill directory MUST contain a `SKILL.md` with valid `name` and
`description` frontmatter; supporting files (`references/`, `evals/`) MUST be
referenced from `SKILL.md` and MUST NOT duplicate its normative guidance.
No organizational-only skills: if two skills cannot be distinguished by
trigger or outcome, they MUST be merged.

### II. Explicit Triggering

Every skill description MUST state precisely when the skill applies and when
it does not. It MUST list trigger phrases, file patterns, or task signals
that activate it, plus explicit non-goals. Vague applicability language
("useful for various tasks") is forbidden; an agent reading only the
description MUST be able to decide correctly whether to load the skill.

### III. Evidence Over Recall

Skills MUST ground behavioral claims in verifiable sources, never in model
recall. Commands, flags, config keys, and API shapes MUST be checked against
current upstream docs before being written. Version-sensitive claims MUST
carry the verified version (e.g., "checked against Bun 1.4.2"). Claims
carried from docs without local verification MUST be labeled as unverified.
Any setting that fails silently (unknown config keys, invisible test
discovery) MUST be documented with its symptom and verification step.

### IV. Evaluated Capability (NON-NEGOTIABLE)

Every behavior a skill promises MUST be backed by an automated check that
fails if the behavior regresses. Procedural skills MUST ship `evals/` cases
covering the happy path and at least one known failure mode or gotcha.
Reference-only skills MUST include a verification section with exact commands
and expected observable outcomes. No skill lands without its checks passing;
no check is allowed to pass vacuously (e.g., a test run that discovers zero
tests or an eval with no assertions).

### V. Token-Efficient Simplicity

Skills MUST be the smallest complete statement of their capability. Authors
MUST prefer decision tables, command references, and gotcha lists over prose;
prose that restates the obvious MUST be deleted. Content MUST be structured
for progressive disclosure: frontmatter for routing, `SKILL.md` body for the
fast path, `references/` for depth. Marketing claims, unverifiable
performance assertions, and generic advice available elsewhere MUST NOT ship.

## Additional Constraints

Technology and format requirements for this repository. Every `SKILL.md`
MUST use Markdown with `name`/`description` frontmatter where `name` matches
its directory name. Markdown, JSON/JSONC, and JS/TS files MUST pass the repo
`eslint` and `prettier` configuration (`npm run fmt` MUST produce no diff).
External skills vendored from other repositories MUST be pinned in
`skills-lock.json` with source, sourceType, skillPath, and computedHash; hash
mismatches MUST block acceptance. Skills MUST NOT embed secrets, API keys,
or environment-specific endpoints; environment differences MUST be expressed
as variables with defaults. License for contributed content is MIT unless a
skill directory explicitly states otherwise.

## Development Workflow

Skill lifecycle is propose → implement → evaluate → review. Authors MUST
scope the skill first (name, triggers, non-goals, and planned evals) before
writing reference content. Changes MUST be small and atomic: one skill added,
updated, or removed per change set. Reviewers MUST verify the constitution
checklist for every change: atomicity, trigger precision, evidence citations,
evals passing, and token efficiency. Fixes to incorrect skill guidance MUST
first add or update the failing eval or verification step (red), then correct
the content (green), then simplify (refactor). Breaking changes to a skill's
triggers, frontmatter contract, or documented commands REQUIRE a minor
version note in the change summary and migration guidance for consumers.

## Governance

This constitution supersedes all other practices in this repository.
Amendments REQUIRE a documented proposal, maintainer approval, and a Sync
Impact Report recorded as an HTML comment at the top of the amended file
during review (removed before commit). Versioning follows semantic versioning:
MAJOR for backward-incompatible principle removals or redefinitions, MINOR
for new principles or materially expanded guidance, PATCH for clarifications
and wording fixes. All reviews MUST explicitly verify constitution compliance;
unjustified complexity or scope expansion MUST be rejected. Runtime
development guidance lives in `AGENTS.md`; in case of conflict, this
constitution governs.

**Version**: 1.0.0 | **Ratified**: 2026-10-04 | **Last Amended**: 2026-10-04
