# Chapter 7: How Code Reviews Can Suck

## Core Concepts

- **Review Creep:** Reviewers expanding the scope of the PR by asking for unrelated enhancements, refactoring, or bug fixes outside the original ticket requirements.
- **Review Fatigue:** Reviewers and authors becoming exhausted due to long comment threads, slow cycles, and constant nitpicking, leading to rubber-stamping.
- **Ego Clashes:** Reviews dissolving into battles over who is the smarter developer rather than focuses on what code is best for the product.

## Frameworks Introduced

- **Scope Creep Boundaries:** Defining limits on what a reviewer can request during a single PR review. Unrelated requests must be moved to separate tickets.
- **Ghosting Escalation:** Clear steps to resolve reviews when reviewers don't respond to comment updates.

## Key Techniques

- **Enforcing PR Scope:** Declining out-of-scope requests politely but firmly (e.g., "That is a great suggestion, let's create a separate issue to track it so we don't block this feature").
- **Recognizing Nitpicking Patterns:** Knowing when a comment is about cosmetic details and resolving it quickly.

## Connection to Other Chapters

- Identifying these failure modes provides the justification for implementing **automation (Chapter 5)**, **the 5P process (Chapter 6)**, and **taking reviews offline (Chapter 8)**.

## Technical Code Examples

### How to Politely Reject Review Creep in a PR comment

```markdown
Reviewer comment:
"Since you are in this module modifying `user_auth.py`, could you also refactor
the old database connections in `db_utils.py` and write tests for it?"

❌ BAD REACTION (Aggressive/Defensive):
"No, that's not my ticket. Do it yourself or make another ticket. I'm not blocking my PR for this."

✅ GOOD REACTION (Constructive scope enforcement):
"That's a very good point! The database connections in `db_utils.py` definitely need a refactor.
Since that is outside the scope of this authentication hotfix, I've created a follow-up ticket:
`#INFRA-948: Refactor db_utils connection pool`. I'll link it here so we can tackle it next!"
```

## Reference Tables

### Red Flags of a Toxic Code Review Culture

| Failure Mode     | Symptoms                                                       | Root Cause                                  | Solution                         |
| ---------------- | -------------------------------------------------------------- | ------------------------------------------- | -------------------------------- |
| **Review Creep** | PR scope increases; dozens of requests for unrelated refactors | Reviewer trying to solve everything at once | Create follow-up backlog tickets |
| **Nitpicking**   | Hundreds of comments on styling, naming conventions, spaces    | Lack of automated linting/formatting        | Setup Prettier/ESLint in CI/CD   |
| **PR Ghosting**  | PRs remain open for days with no reviewer responses            | Reviewers overloaded or lack accountability | Establish review SLAs in TWA     |
