# Glossary

An alphabetized reference guide to key terms and concepts in Adrienne Braganza's _Constructive Code Reviews_.

**Active Reviewer** — A code review participant who actively inspects the proposed pull request changes, runs the code locally when necessary, asks clarifying questions, and leaves constructive feedback. (Chapter 2)

**Asynchronous Review** — A code review workflow conducted offline, where the reviewer leaves comments in a tool (e.g. GitHub) and the author addresses them at a later time, avoiding real-time focus disruptions. (Chapter 2)

**Bypass Merge** — The action of merging a branch directly into a protected branch (e.g. `main`) without completing the required approvals, typically executed using administrative override credentials during emergencies. (Chapter 9)

**Comment Signals** — Explicit Markdown prefixes (`[MUST]`, `[SHOULD]`, `[COULD]`, `[NIT]`) added to the start of review comments to communicate the severity and importance of the feedback to the author. (Chapter 6)

**DICE Rule** — An upstream ticket breakdown rule that stands for **D**efined boundaries, **I**ndependent features, **C**ompact tasks, and **E**stimated efforts. Breaking down tickets using DICE leads to smaller, more reviewable pull requests. (Chapter 8)

**Driver** — In pair and mob programming, the developer who physically sits at the keyboard and focuses on writing syntactically correct code. (Chapter 11)

**Emergency Playbook** — A codified, formal process detailing the steps, authorizations, notifications, and post-merge audits required to bypass the standard code review pipeline during major outages or incidents. (Chapter 10)

**LGTM Rubber-Stamping** — The dangerous practice of typing "Looks Good To Me" and approving a pull request instantly without actually reading or testing the code, defeating the purpose of the review. (Chapter 9)

**Loopholes** — Systematic process gaps or shortcuts (such as ad-hoc self-approvals) that allow code to enter protected branches without being reviewed. (Chapter 9)

**Maintainable Middle Ground (MMG) Exchange** — A 5-step dispute resolution framework designed to resolve conflicting viewpoints on code structure between developers by searching for a maintainable compromise. (Chapter 6)

**Mob Programming** — A software development approach where three or more team members work together at a single workstation (or collaborative IDE) to solve a technical problem collectively. (Chapter 12)

**Navigator** — In pair and mob programming, the developer who does not type, but instead focuses on the strategic architecture, edge cases, and directing the driver's implementation. (Chapter 11)

**Nitpicking** — Leaving cosmetic or non-critical comments (like formatting, style, or personal code preferences) in a pull request. (Chapter 7)

**Passive Reviewer** — A reviewer who simply signs off on a PR or skims it quickly without looking closely at logical correctness, security, or edge cases. (Chapter 2)

**Pull Request (PR)** — A tool-facilitated mechanism in Git platforms where a developer submits a proposed code branch to be reviewed and merged into a protected target branch. (Chapter 2)

**Review Creep** — The anti-pattern of reviewers demanding out-of-scope enhancements, unrelated bug fixes, or minor refactoring before they will approve the current pull request. (Chapter 7)

**Review SLA (Service Level Agreement)** — A team commitment setting clear turnaround times (e.g. "within 24 hours") for completing pull request reviews. (Chapter 4)

**Team Working Agreement (TWA)** — A living, formal markdown document stored in Git that codifies a team's code review norms, style guides, SLAs, and process guidelines. (Chapter 4)

**Three-Exchange Rule** — A rule dictating that if a discussion on a pull request comment exceeds three back-and-forth exchanges, it must be taken offline to a synchronous chat/call to resolve quickly. (Chapter 8)
