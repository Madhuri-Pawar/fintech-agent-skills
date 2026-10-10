# Dynamic Layer Investigation

## Principle

Select investigation layers from the symptom, architecture and evidence.
Do not assume every issue is frontend, backend or database related.

Multiple layers may contribute to one failure. A layer can be implicated,
ruled out with evidence, or remain unverified.

## Frontend

Investigate when symptoms involve rendering, user interaction, stale
state, incorrect client-side calculations, navigation, form validation,
request construction or response handling.

Inspect relevant:

- Components and state management
- Hooks, stores and event handlers
- API clients and request/response types
- Client-side validation and calculations
- Routing, caching and error handling
- Browser-specific behavior and frontend tests

Report the component, file, function and verified failure mechanism.
Do not blame the frontend merely because the user sees the symptom there.

## Backend

Investigate when symptoms involve APIs, domain rules, permissions,
validation, orchestration, concurrency, serialization or server-side
error handling.

Inspect relevant:

- Routes, controllers and handlers
- Service and domain layers
- Request/response schemas
- Authentication and authorization
- Transaction boundaries
- Retry and idempotency behavior
- Error translation and exception handling
- Service-level and integration tests

Trace the request and important values through the execution path.

## Database

Investigate when symptoms involve incorrect persisted data, missing
records, duplicate records, transaction behavior, schema mismatch,
deadlocks, locking, query latency or data consistency.

Inspect relevant:

- Schema definitions and migration history
- Queries, ORM mappings and repository code
- Constraints, indexes and transaction boundaries
- Isolation levels and locking patterns
- Data ownership and consistency rules
- Relevant query plans or sanitized runtime evidence, if accessible

Never claim a database defect solely because a backend operation returned
incorrect data. Trace how the query, data, transaction and application
logic interact.

Do not run destructive queries or alter data in any environment.

## APIs and external integrations

Inspect:

- API contracts and version compatibility
- Authentication and request signing
- Timeouts, retries and rate limits
- Error mapping and response parsing
- Idempotency and duplicate delivery
- Provider status and dependency-specific evidence

Separate an external dependency failure from incorrect handling of that
failure inside the application.

## Queues, events and asynchronous work

Inspect:

- Event schemas and producer/consumer contracts
- Ordering, retries, dead-letter handling and duplicate delivery
- Idempotency and eventual consistency
- Worker concurrency and scheduling
- Message loss, lag and poison messages

Do not assume an event was processed just because it was published.

## Cache and distributed state

Inspect:

- Cache key construction and invalidation
- TTL and stale-value behavior
- Cross-instance consistency
- Locking and race conditions
- Cache/database source-of-truth rules

Verify cache involvement with available evidence before recommending a
cache flush or cache bypass.

## Infrastructure, networking and configuration

Inspect when evidence suggests capacity, DNS, TLS, network, resource
limits, deployment, environment variables, feature flags, permissions or
runtime configuration.

Use available deployment records, health checks, metrics and logs. If
those sources are unavailable, say so.

Do not claim that infrastructure is healthy without evidence.

## Business rules and data quality

Compare observed behavior against explicit acceptance criteria, domain
rules, calculation rules, state transitions and data invariants.

If the requirement itself is ambiguous or contradictory, report it as a
business-rule uncertainty instead of inventing the intended behavior.

## Cross-layer tracing

When relevant, trace:

trigger
-> input/state
-> request or event
-> validation
-> business logic
-> persistence/dependency
-> response/side effect
-> user-visible result

Follow only the paths applicable to the architecture.

## Layer reporting

For each layer, use one of:

- Implicated: evidence links it to the failure.
- Ruled out: specific evidence makes it unlikely to explain this symptom.
- Unverified: access or evidence is insufficient.
- Not applicable: the architecture or symptom does not involve it.

Explain the evidence behind the classification.