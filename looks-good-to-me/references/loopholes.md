# Loophole Detection Guide

_Based on Chapter 9 of "Looks Good to Me" by Adrienne Braganza_

## Common Loopholes and How to Spot Them

### 1. Undefined Process

**Symptom:** Reviewers don't know what they're supposed to check. Reviews are inconsistent — one reviewer checks everything, another approves instantly.
**Detection:** No TWA exists. No review checklist. No shared expectations.
**Fix:** Create a TWA (see twa-template.md). Define minimum review criteria.

### 2. Lack of Time

**Symptom:** Reviewers rush through PRs because they're overloaded. Comments are minimal or non-existent. "LGTM" culture.
**Detection:** Review-to-merge time is very short for large PRs. Single reviewer doing most of the reviews.
**Fix:** Review load balancing. PR size limits. Block time for reviews.

### 3. Tool Misconfiguration

**Symptom:** CI checks are passing but not actually checking the right things. Linters configured too leniently. Test coverage thresholds set to 0%.
**Detection:** Teams merging code with failing checks. Tests exist but don't assert anything meaningful.
**Fix:** Audit CI pipeline regularly. Make linter rules explicit. Enforce meaningful test coverage.

### 4. Approval-Driven Metrics

**Symptom:** Teams are measured on "review turnaround time" or "number of reviews completed," leading to rubber-stamping.
**Detection:** High approval rate with low comment count. PRs approved in minutes for complex changes.
**Fix:** Measure what matters: comment quality, knowledge transfer, defect reduction. Not just speed.

### 5. Lack of Feedback Culture

**Symptom:** Team members don't push back on bad code. Constructive criticism is seen as personal attack. Junior devs are afraid to comment on senior code.
**Detection:** Only senior devs leave comments. PRs from certain people are never questioned.
**Fix:** Psychological safety training. Lead models receiving feedback graciously. Explicit encouragement for all team members to participate.

### 6. Emergency Abuse

**Symptom:** "Emergency" label is used routinely for non-urgent changes. Everything is a "hotfix."
**Detection:** >30% of PRs labeled as emergency. Same developers use emergency bypass repeatedly.
**Fix:** Define emergency criteria explicitly in TWA. Audit emergency bypasses in retros. Require lead approval for emergency labels.

## Pattern: The Lazy Review

**Signs:** Approves everything quickly. Comments are vague ("looks good"). Doesn't actually run or test the code.
**Detection:** Reviewer's approval-to-merge ratio is near 100%. Average review time under 2 minutes for complex PRs.

## Pattern: The Mean Review

**Signs:** Comments are personal, condescending, or aggressive. Dismisses author's perspective. Nitpicks everywhere.
**Detection:** Author pushes back frequently. Repeated conflicts involving the same reviewer. High re-review count.

## Pattern: The Shape-Shifting Review

**Signs:** Reviewer keeps adding new requirements in each round. Scope creeps. PR never seems to be "done."
**Detection:** 5+ review rounds. New issues raised in round 3+ that could have been raised in round 1.

## Pattern: The Stringent Review

**Signs:** Demands perfection. Rejects PRs for trivial style choices. Blocks over preferences, not problems.
**Detection:** Low approval rate. High re-review count. Comments are mostly `[NIT]` labeled as blocking.

## What to Do When You Spot a Loophole

1. **Name it** — Identify the specific pattern (use the names above)
2. **Document it** — Note the impact: what risk does this create?
3. **Raise it** — In the review comment or team retro:
   - "I've noticed we're approving a lot of PRs without substantive review. Perhaps we should revisit our TWA on minimum review expectations?"
4. **Fix the root cause** — Is it process, tooling, culture, or people?
   - Process: Update TWA
   - Tooling: Configure better gates
   - Culture: Team discussion + lead modeling
   - People: Coaching or escalation through manager
