# Cheatsheet & Decision Guides

Quick-reference tables, decision guides, and process checklists.

---

## 🛠️ Choosing Your Review Method

| If the Change is... | And the Team is... | Then Choose... | Why? |
|---------------------|--------------------|----------------|------|
| **Simple / Routine** | distributed or co-located | **Asynchronous PR Review** | Minimizes disruptions, easy to track, instant approval. |
| **Complex Refactor** | co-located in same office | **Synchronous Walkthrough** | Reduces review delays; resolves questions in real-time. |
| **High-Risk Module** | remote or distributed | **Pair Programming** | Driver/Navigator flow catches structural flaws live. |
| **Legacy Migration** | full engineering team | **Mob Programming** | Distributes core migration patterns across all members rapidly. |

---

## ⏱️ The 5P Decision Flow

Use this simple decision matrix during review to determine what to do with a code change suggestion:

```mermaid
graph TD
    A[Reviewer spots potential improvement] --> B[Pause & Ponder: Is this a logic/TWA violation?]
    B -- Yes, Blocker --> C[Propose: Leave [MUST] or [SHOULD] comment]
    B -- Yes, Cosmetic --> D[Propose: Leave [NIT] comment, don't block]
    B -- No, Subjective Preference --> E[Pass: Do not write comment]
    B -- No, Out of Scope but Valid --> F[Postpone: Make backlog ticket or discuss offline]
```

---

## 🕒 TWA Code Review SLA Matrix

Commit to these turnaround windows inside your Team Working Agreement:

| PR Size | Description | SLA (Turnaround) | Escalation Channel |
|---------|-------------|-------------------|-------------------|
| **Small (<100 LOC)** | Typo fix, single variable rename, config edit | **Within 4 hours** | Slack ping to reviewer |
| **Medium (100-300 LOC)** | Standard feature, refactored class, simple bug fix | **Within 24 hours** | Mention in daily standup |
| **Large (>300 LOC)** | Massive schema change, complete module rewrite | **Within 48 hours** | Schedule a synchronous sync-up |
| **Emergency Hotfix** | Blocked production outage, critical CVE patch | **Immediate** | Target in `#dev-emergency` Slack |

---

## 🚨 Emergency Playbook Checklist

Follow these steps when bypassing code review rules for production hotfixes:

1. **Authorize:** Get approval from Tech Lead or Engineering Manager.
2. **Commit:** Branch off `main` with prefix `hotfix/`. Keep changes minimal.
3. **Bypass Merge:** Admin merge the PR directly without approvals.
4. **Notify:** Post the PR URL and outage ticket in the public Slack `#dev-incidents` channel immediately.
5. **Retroactive Review:** Full team conducts a retroactive code review and incident postmortem within **24 hours**.
6. **Realign:** Backport hotfix to developmental branches (e.g. `develop` or active releases).