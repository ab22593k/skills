# Comment Patterns

Reference of comment patterns from Chapter 6 of *Looks Good to Me*.

## The Core Pattern: Observation → Impact → Suggestion

Every review comment has three parts:
1. **Observation** — What you see (objective, factual)
2. **Impact** — Why it matters (the consequence)
3. **Suggestion** — What to do instead (actionable)

## Comment Templates by Scenario

### Requesting a Change
```
The [specific code element] on line [N] [does X].
[Impact]: This [causes problem / creates risk / reduces maintainability].
[Suggest]: [Specific alternative or approach].
```

**Example:**
> The `fetchUserData` function on line 42 catches all exceptions with a generic handler. Impact: This silently swallows network errors and auth failures alike, making debugging difficult. Suggestion: Catch specific exception types separately, or at minimum log the error before re-throwing.

### Asking a Clarifying Question
```
I'm not sure I understand [specific element] on line [N]. Could you help me understand [what it does / why this approach]?
```

**Example:**
> I'm not sure I understand the `transformData` call on line 88. Could you help me understand what format the input data is in here? I want to make sure we're not losing precision.

### Making a Suggestion (Non-blocking)
```
Consider [alternative approach] instead of [current approach].
Why: [reason based on outcome, not preference].
```

**Example:**
> Consider using `Optional` here instead of returning null. Why: It makes the "no result" case explicit in the type signature, so callers can't forget to handle it.

### Labeling a Nitpick
> [NIT] Consider renaming `processData` to something more specific, like `processInvoice`. Entirely your call.

### Giving Praise
```
Nice work on [specific element]. [Specific reason why it's good].
```

**Example:**
> Nice work on the test coverage for `PaymentProcessor`. The edge cases for failed payments and timeouts are thorough — that's exactly the kind of robustness this module needs.

## Anti-patterns to Avoid

| Anti-pattern | Instead |
|---|---|
| "You should…" (personal) | "Consider…" or "This could…" |
| "This is wrong/bad" (judgment) | "This [does X], which causes [Y]" (observation) |
| "Why didn't you…" (blame) | "Have you considered…" (curiosity) |
| Multiple issues in one comment | One concern per comment |
| Vague: "This could be better" | Specific: "Line 42 doesn't handle null input" |
| "LGTM" with no substance | "LGTM" + one thing you appreciated |

## Handling Disagreement

**If the author pushes back:**
1. Acknowledge their perspective: "That's a fair point."
2. Clarify your reasoning: "My concern is specifically about [X]."
3. Offer a **testable compromise**: "Can we measure the impact of each approach? If [condition], I'm convinced."
4. Know when to escalate: If after 2-3 rounds there's no resolution, suggest a sync meeting or ask a third reviewer.

**When the author is a senior/experienced dev:**
- Their refactor may have legitimate technical motivations you haven't seen. Ask: "What problem with the current approach led you to this?"
- Separate "process violation" from "technical merit" — address both independently
- Propose empirical validation: "Let's measure the migration cost on one module first, then decide as a team"

**Falsifiability check for process recommendations:**
When suggesting a process change, include a way to verify it's working:
- "If review times don't improve in 4 weeks, revisit the rotation"
- "Track [metric] and check at the next retro"
- "What would tell us this approach isn't working?"

**If you're uncertain about your feedback:**
- Frame it as a question, not a demand
- Say "I might be missing context — what do you think?"
- Use `[QUESTION]` prefix explicitly

## Code Compliments (Chapter 6.3)

Always include positive feedback. It:
- Reinforces good practices
- Builds psychological safety
- Makes constructive feedback more palatable

Good compliments are specific:
- "The way you extracted the validation logic into a separate module makes the controller much cleaner."
- "This test covers exactly the edge case I would have missed — great catch."
- "The error messages here are excellent — clear, actionable, and user-friendly."
