---
name: looks-good-to-me
description: Applies Adrienne Braganza's Constructive Code Reviews framework to build healthy team practices, write empathetic comments, automate nits, eliminate bottlenecks, and pair reviews with pair/mob programming and AI.
---

# Looks Good to Me: Constructive Code Reviews

## Overview

This skill implements the human-centered code review framework from Adrienne Braganza's _Looks Good to Me: Constructive Code Reviews_. It transforms code review from a dreaded chore into an effective, empathetic team practice.

Use this skill whenever you need to: conduct a code review, review a PR/MR, set up a team review process, write review comments, resolve review bottlenecks, handle review disagreements, create a Team Working Agreement, or automate review checks. Also use when the user mentions code review pain points, LGTM culture, review delays, process loopholes, or improving team review practices — even if they don't explicitly ask for a "framework."

---

## Core Principles

These principles are the foundation. Internalize them — they matter more than the workflow.

1. **Separate code from author** — "This function has a race condition" not "You missed a race condition." Criticism of code is not criticism of the person.

2. **Observe → Impact → Suggest** — Every comment describes what you see, explains why it matters, and offers a path forward.

3. **Assume good intent** — The author worked within their constraints. Your job is to improve the outcome, not assign blame.

4. **Reviews are knowledge transfer** — The goal is shared understanding and a better codebase, not gatekeeping.

5. **Test your advice against falsification** — For process recommendations, ask: "What evidence would tell me this isn't working?" Build in success metrics and checkpoints.

---

## The Review Framework

Think of these as phases, not rigid steps. Apply them fluidly based on context. A 50-line bugfix PR skips straight to feedback; a 500-line refactor needs the full sequence.

### 1. Surface-Level Checks

Verify the basics before diving deep:

- **PR hygiene** — Title describes _what_, description explains _why_, labels match change type, CI has passed
- **PR size** — Flag anything >400 lines as needing justification or splitting. A 1200-line PR is unreviewable.
- **Tests present** — For non-trivial changes, tests should exist. Flag if missing.

If any of these fail, pause and request fixes before proceeding. Use `[BLOCKING]` prefixes.

### 2. Automated-Quality Domain

Check what can be checked objectively:

- **Security** — Hardcoded secrets, injection vectors, XSS, unsafe deserialization, missing input validation. These are always `[BLOCKING]` or `[REQUIRED]`.
- **Error handling** — Are errors caught, logged, and surfaced appropriately? What happens when a dependency fails?
- **Code health** — Dead code, unused imports, consistent patterns, no commented-out code
- **Test quality** — Do tests cover edge cases or just the happy path? Are assertions meaningful?

Security issues are always blocking. For other issues, use `[REQUIRED]` for must-fix and `[SUGGESTION]` for nice-to-have.

### 3. Judgment Domain

This is where human review adds most value. Be explicit about what's subjective.

- **Logic correctness** — Does the implementation do what it claims? Edge cases, off-by-one, race conditions?
- **Design & architecture** — Does it follow project conventions? Is the abstraction appropriate? (YAGNI — is this solving a real problem now?)
- **Maintainability** — Would a new team member understand this in 6 months? Are names meaningful?
- **Test depth** — Do tests cover failure modes, not just the happy path? Are integration tests needed?

Mark subjective opinions explicitly: "In my view..." or "Consider...". Use `[SUGGESTION]` for improvements, `[QUESTION]` for clarifications.

### 4. Policy & Culture Check

- **Team Working Agreement** — If the team has one, verify alignment (response times, approval rules, nit labeling). If none exists, offer the starter template.
- **Bottleneck detection** — Is review load concentrated on one person? Suggest rotation.
- **Emergency label audit** — Is the "emergency" label being used legitimately or abused? Check against team's emergency criteria.
- **Dispute escalation** — After 3+ rounds of async debate on one thread, suggest a sync meeting.
- **Falsifiability check** — For any process recommendation you make, ask: "What would tell us this approach is wrong?" Include a success metric or checkpoint.

Output policy flags with `[POLICY]` referencing the specific rule.

### 5. Compose Feedback

Produce two things:

**Summary (top of review):**

```
**Overall**: approve with suggestions / changes requested / comment

**Strengths**: [1-2 specific things done well — always include these]

**Key areas**: [top 2-3 findings, highest priority first]
```

**Line comments** following this format:

```
[TYPE] Observation → Impact → Suggestion
```

Tag every comment:

- `[BLOCKING]` — Must fix, blocks approval. Use sparingly.
- `[REQUIRED]` — Important, should fix before merge.
- `[SUGGESTION]` — Improvement idea, non-blocking.
- `[QUESTION]` — Clarification needed.
- `[NIT]` — Minor preference, author's call. Always label explicitly.
- `[PRAISE]` — Something well done. Use freely.

Rules:

- One concern per comment — don't bundle issues
- Be specific — reference exact lines and behaviors
- Be specific about why it matters — impact is the most skipped part
- Code suggestions where possible (prefer suggested diff blocks)
- At least one `[PRAISE]` per review unless the code is genuinely problematic

### 6. Escalation

Flag for human decision; never act autonomously.

- Review stalled past response time → Suggest reassignment or nudge
- Single reviewer overloaded → Flag as bottleneck pattern
- Emergency (production outage, security vuln) → Apply Emergency Playbook: bypass, document trade-offs, schedule follow-up
- Irreconcilable disagreement → Suggest sync meeting with a third party

---

## Adapting to Context

**Small teams (2-5):** Focus on phases 3 and 5. Lighter process, more direct communication.

**Medium teams (6-15):** Run all phases. Automate what you can (linting, formatting, CI gates). TWA should be written.

**Large teams (15+):** Full process. Emergency Playbook essential. Multiple reviewers per PR.

**No existing process:** Start with phases 1, 3, 5, 6. Introduce TWA and automation gradually.

---

## Handling Technical Disagreements

When the author pushes back on your feedback:

1. **Acknowledge first** — "That's a fair point."
2. **Clarify your specific concern** — "My concern is specifically about [X], not the overall approach."
3. **Offer a test** — "Can we measure the migration cost on a small slice? If it's under [threshold], I'm convinced."
4. **Know when to escalate** — After 2-3 rounds, suggest a sync or involve a third party.

When the author is a senior dev with strong opinions:

- Recognize that their refactor may have legitimate technical motivations you haven't seen
- Separate "does this break process" from "is this technically better" — address both
- Propose compromise: ship the minimum for now with a tracking issue for follow-up evaluation

## Output Checklist

- [ ] Summary block at the top with Overall / Strengths / Key areas
- [ ] At least one `[PRAISE]` comment
- [ ] All blocking/required comments include impact and suggestion
- [ ] Nits labeled `[NIT]` — no disguised nits
- [ ] Process recommendations include a falsifiability check or success metric
- [ ] Language separates code from author throughout
- [ ] Framework is invisible in the output — focus on clear, natural advice
