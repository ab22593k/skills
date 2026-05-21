# Chapter 8: Decreasing Code Review Delays

## Core Concepts
* **Review Turnaround Bottlenecks:** When a single team member (often the lead developer) reviews all PRs, they become a bottleneck, stalling the delivery pipeline.
* **Taking Discussions Offline:** Long back-and-forth comments indicate misaligned viewpoints. When a thread passes 3 cycles, shift to a synchronous discussion.
* **Upstream Gaps:** Massive, unreviewable PRs are usually caused by bad task/ticket sizing during planning.

## Frameworks Introduced
* **The Three-Exchange Rule:** A simple rule stating that if a discussion on a PR comment exceeds 3 back-and-forth exchanges, it must be taken offline (call, video chat, or in-person discussion) to resolve quickly.
* **PR Sizing Rules:** Techniques for dividing massive features into minor, reviewable PRs (e.g. branch stacking).

## Key Techniques
* **Reviewer Rotations:** Sharing review responsibilities across the entire team to distribute knowledge and prevent lead developer overload.
* **PR Stacking:** Developing features in minor, dependent increments, merging smaller branches into an active feature branch.

## Connection to Other Chapters
* Resolving delays uses the SLAs codified in the **TWA (Chapter 4)** and is facilitated by the **pair/mob programming workflows (Chapters 11 and 12)**.

## Technical Code Examples
### Transitioning an Infinite Thread Offline
```markdown
Thread Exchange 1:
Reviewer: "I think we should use a strategy pattern here."
Author: "A simple factory is much simpler and fits our needs."

Thread Exchange 2:
Reviewer: "But strategy will allow us to easily extend in the future."
Author: "That is over-engineering. We don't have future strategies planned yet."

Thread Exchange 3:
Reviewer: "It keeps code cleaner. Check Chapter 8 in design books."
Author: "I still feel it's too much boilerplate."

✅ APPLYING THREE-EXCHANGE RULE:
Reviewer: "Hey! We've hit our 3-exchange limit for async discussion. 
I'll ping you on Slack to hop on a quick 5-minute call so we can align 
and update this PR with the outcome! 📞"
```

## Reference Tables
### Causes and Solutions of Code Review Delays
| Cause | Effect | Strategic Solution |
|-------|--------|--------------------|
| **Reviewer King/Queen Bottleneck** | PRs wait days for the senior lead; junior devs feel disempowered | Implement reviewer rotations, pair juniors with seniors |
| **Gargantuan PRs (>500 LOC)** | Reviewers procrastinate reading due to fatigue | Break down tickets upstream, utilize PR Stacking |
| **Async Communication Ping-Pong** | Comment threads go on for 20+ cycles with no resolution | Enforce the **Three-Exchange Rule** to sync offline |