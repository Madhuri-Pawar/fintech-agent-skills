# Solution Trade-Off Analysis

## Objective

Recommend the best practical fix for the verified problem, not merely
the quickest patch or the most elaborate redesign.

## Establish the constraints

Identify:

- Business requirements and acceptance criteria
- Existing architectural boundaries and contracts
- Data correctness and security requirements
- Performance and availability requirements
- Compatibility constraints
- Delivery urgency and implementation cost
- Operational support and rollback capabilities

If a requirement is unknown, state the assumption and explain its effect.

## Generate candidate solutions

Consider at least one focused fix. Consider alternatives when they offer
a meaningful improvement in correctness, reliability, scale or cost.

Do not invent alternatives just to make the report longer.

For each candidate explain:

- What changes
- Why it addresses the cause
- Benefits
- Risks and trade-offs
- Compatibility and migration impact
- Tests required
- Rollback approach

## Evaluation criteria

### Business correctness
Does the change implement the intended rule and acceptance criteria?
Could it alter pricing, permissions, workflow state, or other business
outcomes unexpectedly?

### Root-cause coverage
Does it eliminate the verified cause or only suppress the symptom?
Does it introduce a compensating workaround that could hide failures?

### Architecture and maintainability
Does the solution preserve clear ownership and existing contracts?
Does it add unnecessary coupling, duplication or complexity?

### Performance and scalability
Consider:
- Expected and peak request volume
- Query count and query complexity
- CPU, memory and network overhead
- Concurrency and contention
- Cache effectiveness and invalidation
- Queue throughput and backpressure
- Horizontal scaling and shared state
- Latency targets and tail latency

Use measured data where available. Do not invent performance gains.

### Data correctness
Consider:
- Atomicity and transaction boundaries
- Constraints and invariants
- Duplicate requests and idempotency
- Retries and partial failures
- Concurrent updates and lost writes
- Migration, backfill and rollback compatibility

### Security and privacy
Preserve authentication, authorization, input validation, tenant isolation,
secret handling, and least privilege. Avoid logging sensitive information.

### Reliability and operability
Consider:
- Timeouts and bounded retries
- Failure isolation
- Degraded-mode behavior
- Monitoring and actionable alerts
- Diagnostics and trace correlation
- Safe rollout and recovery

### Compatibility
Consider clients, APIs, events, schemas, old and new application versions,
and external consumers.

### Cost and delivery
Compare engineering effort, operational cost, maintenance burden and
risk of delaying an urgent mitigation.

## Decision method

1. Eliminate candidates that violate business correctness or security.
2. Eliminate candidates that fail to address the verified cause unless
   explicitly presented as temporary containment.
3. Compare remaining options against the constraints and criteria.
4. Recommend the option with the best justified overall trade-off.
5. Explain why meaningful alternatives were rejected.
6. Identify assumptions that could change the recommendation.

Do not present an arbitrary weighted score as objective truth. If scoring
is requested, show the weights and assumptions.

## Required recommendation

State:

- Preferred solution
- Why it addresses the cause
- Files, modules, contracts or schema elements involved
- Ordered implementation steps
- Alternative and its trade-offs
- Risks and mitigations
- Tests and acceptance criteria
- Rollout and rollback plan

Prefer the smallest complete, safe change. Avoid unrelated refactoring.