# Root-Cause Verification

## Objective

Determine what the evidence proves, what it suggests, and what remains
unknown.

## Evidence categories

### Direct evidence

Examples include a reproducible failing test, a relevant stack trace,
a captured incorrect request or response, a query result demonstrating
the inconsistency, or a trace showing the failing operation.

Direct evidence must still be interpreted in context.

### Supporting evidence

Examples include a suspicious recent change, a matching code path,
a related historical incident or a metric that changes around the onset.

Supporting evidence increases or decreases plausibility but may not
prove causation.

### Missing evidence

Examples include unavailable production traces, absent reproduction
steps, inaccessible linked services, or an unverified deployment timeline.

State what is missing and how to obtain it safely.

## Hypothesis table

For each meaningful hypothesis, document:

- Hypothesis
- Supporting evidence
- Contradicting evidence
- Confidence and rationale
- Next discriminating check
- Result of the check, if actually performed

Prefer checks that distinguish between plausible causes rather than
collecting more evidence that all hypotheses predict equally well.

## Confidence labels

CONFIRMED:
The causal mechanism is directly supported by evidence, relevant
alternatives have been sufficiently examined, and validation is strong
enough for the claim being made.

PROBABLE:
Evidence strongly supports the explanation, but an important runtime,
reproduction or dependency check remains outstanding.

UNDETERMINED:
Evidence is incomplete, contradictory or insufficient to select a cause.

Do not assign a numerical probability unless there is a defensible basis.

## Causal chain

Describe:

1. Trigger or precondition
2. Faulty mechanism
3. Resulting incorrect state, response or side effect
4. User-visible symptom or business impact

Identify contributing factors separately from the primary cause.

## Falsification

Ask what observation would disprove the leading hypothesis. Look for
contradictory evidence and test alternatives before concluding.

If a proposed cause cannot explain the full symptom, refine it or retain
multiple hypotheses.

## Code versus runtime evidence

Static source inspection can identify a likely defect, but it cannot
always establish that the defect caused a particular runtime event.

Never claim that logs, traces, tests or monitoring confirm a cause unless
the relevant source was actually inspected and the evidence supports it.

When access to the affected environment is unavailable, provide a verification plan instead
of upgrading a hypothesis to a confirmed root cause.