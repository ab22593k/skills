# Chapter 12: Code Reviews and Mob Programming

## Core Concepts
* **Collective Intelligence:** Mob programming gathers a larger group (3+ developers) to focus on a single computer, using their collective experience to solve a single problem.
* **Knowledge Distribution:** Mob programming is a highly effective tool for rapidly spreading architecture patterns and domain knowledge across the team.
* **Fewer Review Delays:** Because the team writes code together, the output requires minimal asynchronous review, dramatically speeding up the path to production.

## Frameworks Introduced
* **"Agree and Then Split" Approach:** A hybrid framework:
  1. The team mobs together on the complex structural architecture, interfaces, and core patterns.
  2. Developers split to implement routine concrete details asynchronously.
  3. Standard PRs are submitted for routine elements.

## Key Techniques
* **Driver Rotation:** Rotating the driver role every 10-15 minutes to keep all mob participants engaged and focused.
* **Remote Mobbing:** Using dedicated tools, online whiteboard sketchers, and collaborative code spaces to mob virtually.

## Connection to Other Chapters
* Combining mob programming with **automation (Chapter 5)** allows the mob to ignore styling issues, focusing human attention on structural decisions.

## Technical Code Examples
### Simple Mob Timer CLI Command representation
```bash
# Using open-source mobbing CLI tool to rotate drivers in Git
mob start 15      # Start a mobbing session with a 15-minute driver timer
mob next          # Hand over the changes to the next driver via Git
mob status        # Check who is currently driving and navigating
mob done          # Conclude mob session and stage changes for PR review
```

## Reference Tables
### When to Mob vs. When to Review Asynchronously
| Scenario | Mob Programming | Asynchronous PR Review |
|----------|-----------------|------------------------|
| **Legacy Code Migration** | ✅ Excellent (disseminates migration pattern) | ❌ Poor (massive, unreviewable diffs) |
| **Onboarding New Devs** | ✅ Excellent (teaches team conventions live) | ❌ Poor (feedback is delayed) |
| **Routine Bug Fixes** | ❌ Poor (waste of mob time) | ✅ Excellent (fast, straightforward review) |
| **Refactoring Core Core** | ✅ Excellent (ensures team agreement) | ❌ Poor (long subjective PR debates) |