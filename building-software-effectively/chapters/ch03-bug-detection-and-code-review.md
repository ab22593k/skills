# Bug Detection and Code Review

## Core concepts

- AI code-review tools detect security vulnerabilities (SQL injection, XSS) more reliably than performance issues (memory leaks, inefficient loops).
- Three integration types: **IDE-based** (real-time feedback on save), **Git-based** (triggers on PR/push), **Browser-based** (external platform reviews PRs). Only IDE tools catch issues before code leaves the developer's machine.
- AI reviews augment but never replace human reviews. Human reviewers catch context-specific issues and business logic gaps that AI misses.

## Frameworks introduced

**Linters → Static analysis → AI-powered analysis** — Three layers of code quality automation. Linters enforce style. Static analysis detects bugs and vulnerabilities with rules. AI-powered analysis learns patterns across millions of repos to find deeper issues and suggest fixes.

**PR blocking strategies** — Codacy blocks merges until issues are fixed (enforcement). DeepCode doesn't block but flags issues (awareness). CodeRabbit only posts comments (advisory). Choose based on team maturity.

## Key techniques

**Test snippet with injected bugs:** Introduce SQL injection, XSS, memory leaks, and inefficient loops into a sample codebase. Run through each tool to compare what they catch and miss.

**Commit suggestion workflow:** Codacy and CodeRabbit offer one-click fix commits directly in the PR. DeepCode provides reference fixes from open source repos (more cognitive load).

## Reference tables

| Tool | Security issues found | Performance issues found | Score |
|------|---------------------|------------------------|-------|
| Codacy | 2/2 (SQLi, XSS) | 0/2 | 8/10 |
| DeepCode | 1/2 (SQLi only) | 0/2 | 6/10 |
| CodeRabbit | 2/2 (SQLi, XSS) | 0/2 | 7/10 |

## Connection to other chapters

Extends the AI + Human review principle from Chapter 1 with specific tool comparisons. Sets up the QA/testing discussion in Chapter 4 — code review is the gate before QA.
