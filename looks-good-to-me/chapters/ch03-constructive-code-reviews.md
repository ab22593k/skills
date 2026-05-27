# Chapter 3: Building Your Team's First Code Review Process

## Core Concepts
* **Phase-Based Implementation:** Trying to adopt code reviews all at once causes friction. A gradual, phase-based adoption yields better long-term alignment.
* **Objective-Driven Processes:** The process should serve the team's goals, not the other way around. Enforcing rules without understanding *why* leads to resentment.
* **Process Iteration:** The review process must be periodically adjusted during team retrospectives as the codebase and team size change.

## Frameworks Introduced
* **Three-Phase Review Setup:**
  - **Phase 1: Alignment & Goals:** Get the team to agree on the core purpose (e.g. sharing knowledge, avoiding bugs).
  - **Phase 2: Workflow & Tools:** Select the platform, branch protection rules, and setup templates.
  - **Phase 3: Guidelines & Style:** Establish agreements on PR size, review times, and coding conventions.

## Key Techniques
* **PR Sizing Constraints:** Establishing that a standard PR should represent less than 300-500 lines of code to maintain review high quality.
* **Retrospective Adjustments:** Using retrospectives to refine review guidelines (e.g., if reviews take too long, adjust the SLA or required approvals).

## Connection to Other Chapters
* The guidelines and guidelines formulated in Phase 3 are formally codified into the **Team Working Agreement (Chapter 4)** and optimized using CI/CD in **Chapter 5**.

## Technical Code Examples
### Draft Configuration for Git Branch Protection (YAML representation)
```yaml
# Conceptual branch protection configurations
branch_protection:
  target_branch: main
  rules:
    require_pull_request: true
    required_approvals: 1
    dismiss_stale_reviews: true
    require_status_checks:
      - unit-tests-ci
      - code-linter-ci
    block_admin_bypass: false # Bypasses audited via Emergency Playbook (Ch 10)
```

## Reference Tables
### Three-Phase Implementation Checklist
| Phase | Action Items | Deliverables |
|-------|--------------|--------------|
| **Phase 1: Alignment** | Discuss review values, identify pain points, align on shared team objectives | Written list of code review goals |
| **Phase 2: Setup** | Select GitHub/GitLab, configure branch protection, add PR templates | Branch rules active, template in `.github/` |
| **Phase 3: Rules** | Set PR size limits, review SLAs, styling rules | Draft of guidelines (precursor to TWA) |