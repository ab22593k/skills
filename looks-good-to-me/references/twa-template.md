# Team Working Agreement (TWA) — Starter Template

*Based on Appendix A of "Looks Good to Me" by Adrienne Braganza*

## Purpose
A TWA defines shared expectations for how this team conducts code reviews. It prevents mismatched assumptions, reduces friction, and creates a predictable review experience for everyone.

---

## Section 1: Response & Review Times

- **Target first-response time:** [e.g., 1 business day]
- **Target review completion:** [e.g., 2 business days for <400 line PRs]
- **Max PR size before mandatory split:** [e.g., 400 lines]
- **Weekend/holiday policy:** [e.g., reviews are not expected outside business hours]

## Section 2: PR Requirements

- **Title format:** [e.g., `type(scope): description` — `feat(auth): add JWT login`]
- **Description minimum:** [e.g., must include "what" and "why" — context, motivation, trade-offs]
- **Required labels:** [e.g., bugfix, feature, refactor, docs, chore]
- **Tests required for:** [e.g., all new logic, bug fixes]
- **CI must pass before review:** [Yes / No]

## Section 3: Review Focus Areas

The team agrees to review for (rank or check all that apply):
- [ ] Correctness — does the code do what it claims?
- [ ] Security — are there vulnerabilities?
- [ ] Maintainability — is the code readable and well-structured?
- [ ] Performance — are there obvious performance issues?
- [ ] Test quality — are the right tests in place?
- [ ] Architecture — does the code follow our design patterns?

## Section 4: Comment Guidelines

- **Blocking issues** are labeled `BLOCKING`: [e.g., security vulnerability, data loss, broken functionality]
- **Required fixes** are labeled `REQUIRED`: [e.g., correctness issues, test gaps]
- **Nitpicks** are labeled `NIT`: [e.g., style preferences, minor naming suggestions]
- **Positive feedback** is encouraged: [at least one praise comment per review is the team norm]

## Section 5: Approval Rules

- **Minimum reviewers:** [e.g., 1 for trivial, 2 for significant changes]
- **Self-approval allowed?** [Yes / No — if yes, for what changes?]
- **Who can approve:** [e.g., any team member, senior devs only]
- **Merge requirements:** [e.g., at least one approval + all CI passing]

## Section 6: Violations & Escalation

- **Missed response time:** [e.g., reassign reviewer, ping on chat]
- **Persistent disagreement:** [e.g., schedule a sync meeting, involve lead]
- **Emergency bypass:** [e.g., lead can approve with documented trade-offs; follow-up fix scheduled]

## Section 7: Review Culture

- **Assume good intent** — Authors aren't trying to write bad code
- **Be specific** — "Line 42 doesn't handle null" not "This is wrong"
- **Be timely** — Respect the author's need to move forward
- **Share knowledge** — Explain *why* as much as *what*

---

## How to Use This Template

1. **Discuss as a team** — Go through each section in a team meeting
2. **Fill in defaults** — Start with simple defaults (e.g., 1 day response, 400 lines, 2 reviewers)
3. **Try it for 2-4 weeks** — Don't try to get it perfect upfront
4. **Review and iterate** — After the trial, adjust based on what's working
5. **Store it** — Keep the TWA in a shared location the team can reference

The best TWA is the one your team actually uses. Start simple and refine.
