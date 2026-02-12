# Prospective Testing (Testing Before Code)

Prospective testing is the practice of investigating requirements, designs, and ideas before they are implemented. As outlined in Chapter 8, it's about "looking where you are going" to prevent trouble.

## Why Do Prospective Testing?
- To identify gaps in understanding early.
- To challenge assumptions that would be expensive to fix later.
- To improve the testability of the final product.

## The 11-Question Cheat Sheet for Prospective Testing
Use these questions in meetings with BAs, developers, or product owners:

1. **What exactly are we talking about?** (Define terms and scope).
2. **Is this worth discussing here and now?** (Prioritize valuable discussion).
3. **What exactly are we trying to achieve?** (Identify the core purpose and value).
4. **What influences must we consider?** (Constraints, users, environment, history).
5. **What other features or requirements will be affected?** (Identify side effects and dependencies).
6. **What specific data or conditions must this feature be able to process or work with?** (Edge cases, data types, limits).
7. **What are the merits of different ways of designing or implementing this feature?** (Trade-offs and alternatives).
8. **How will the new feature handle errors or recover from failure?** (Resilience and error reporting).
9. **How will we test the new feature once it exists?** (Advocate for testability: logs, hooks, APIs).
10. **What could go wrong?** (Brainstorm risks and failure modes).
11. **Who else needs to be involved?** (Identify missing stakeholders).

## Handling Resistance
If people resist these questions, use **Safety Language**:
- "I'm asking this to ensure I can design an effective test strategy once the code is ready."
- "I want to make sure we don't have any surprises that slow us down later."
- "My goal is to help us move along at the fastest safe speed."
