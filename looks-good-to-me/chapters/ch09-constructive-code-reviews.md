# Chapter 9: Eliminating Process Loopholes

## Core Concepts

- **Process Loopholes:** The shortcuts or pathways through which developers skip or dilute the code review process (e.g., self-approvals, merging without review).
- **Rubber-Stamping (LGTM):** Approving a pull request instantly without actually reading, validating, or running the code, which creates a false sense of security.
- **Tool-Level Enforcement:** Standard workflows should be protected by technology, not just trust, to make sure guidelines are respected under high-stress deadlines.

## Frameworks Introduced

- **Loophole Audit Framework:** A technique for identifying and closing pathways used to bypass reviews.
- **Enforced Workflows:** Configuring repository rules to prevent self-approvals and bypasses.

## Key Techniques

- **Enforcing Two-Approver Rules:** Setting repository branch protection to require at least two approvals.
- **Auditing Bypass Permissions:** Restricting administrator bypass permissions and monitoring bypass events.

## Connection to Other Chapters

- Bypasses should not be done ad-hoc. Closing standard loopholes requires establishing the formal **Emergency Playbook (Chapter 10)** for exceptional bypass scenarios.

## Technical Code Examples

### GitHub Action Config to Prevent LGTM Rubber-Stamping (Checks for changes)

```yaml
# Simple YAML check to block self-approval or enforce review status
name: PR Approval Guards
on:
  pull_request_review:
    types: [submitted]

jobs:
  validate_approvals:
    runs-on: ubuntu-latest
    steps:
      - name: Verify Reviewer is NOT PR Author
        run: |
          AUTHOR="${{ github.event.pull_request.user.login }}"
          REVIEWER="${{ github.event.review.user.login }}"
          if [ "$AUTHOR" = "$REVIEWER" ]; then
            echo "ERROR: You cannot approve your own pull request."
            exit 1
          fi
```

## Reference Tables

### Common Process Loopholes & How to Close Them

| Loophole                 | Operational Risk                                                | Tool/Rule Solution                                                       |
| ------------------------ | --------------------------------------------------------------- | ------------------------------------------------------------------------ |
| **Self-Approval**        | Code goes into main with zero external eyes, risking major bugs | Disable self-approval inside repository branch protection settings       |
| **LGTM Rubber-Stamping** | "Looks Good To Me" is typed with no actual code inspection      | Require positive status checks from automated CI runs; set reviewer SLAs |
| **Admin Bypass Merge**   | Admins bypass review to push features faster under pressure     | Restrict admin bypass, mandate automated logging of bypass actions       |
