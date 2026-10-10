# Testing and Rollout

## Objective

Define how the proposed fix will be shown to correct the defect without
creating regressions.

## Tests by level

Choose the relevant levels rather than requiring every level for every bug.

- Unit: the faulty decision or calculation.
- Integration: interactions between services, database and dependencies.
- Contract: API, event and schema compatibility.
- End-to-end: the user-visible business workflow.
- Regression: the original failure and related edge cases.
- Load/concurrency: contention, duplicate requests and capacity-sensitive
  behavior, when relevant.
- Security: authorization, tenant isolation and input-handling cases.

## Test design

Include:

- Original reproduction scenario
- Expected successful behavior
- Negative and invalid inputs
- Boundary values
- Empty or missing data
- Duplicate requests and retries, if applicable
- Concurrent operations, if applicable
- Downstream dependency failure
- Backward compatibility
- Existing regression tests

Each proposed test should state its setup, action and expected outcome.

## Evidence discipline

Clearly distinguish:

- Test proposed
- Test written
- Test executed
- Test passed
- Test failed
- Test blocked

Never claim execution or success based only on reading test code.

If tests are run, report the actual command and result. Do not hide
failures or unrelated pre-existing failures.

## Rollout plan

When deployment is in scope, recommend a safe rollout appropriate to
the system:

- Feature flag or staged rollout, where available
- Migration ordering and backward compatibility
- Monitoring and alert thresholds
- Verification window
- Rollback triggers and rollback procedure
- Data recovery considerations, if applicable

Do not execute a deployment, alter environment configuration, or modify
data in any environment during a plan-only investigation.

## Acceptance criteria

Define observable conditions that demonstrate:
- The original issue no longer occurs.
- Expected business behavior is preserved.
- Relevant regression tests pass.
- Error rates, latency or data invariants remain within agreed limits.
- Monitoring can detect recurrence.

Do not invent numerical service-level targets. Use documented targets or
identify the need for an agreed threshold.