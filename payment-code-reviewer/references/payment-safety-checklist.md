# Payment Safety Checklist

Apply only the checks relevant to the reviewed business flow.

## Business rules

* [ ] Amount and currency are validated against trusted server-side data.
* [ ] Payment ownership and customer or tenant boundaries are enforced.
* [ ] Operations are allowed only from valid payment states.
* [ ] Refunds do not exceed the permitted refundable balance.
* [ ] Capture and cancellation rules match the documented business contract.
* [ ] Sensitive operations require the appropriate permission.
* [ ] Client-supplied state or provider status is not trusted without verification.

## Idempotency and duplicate processing

* [ ] Repeated requests cannot unintentionally create duplicate financial effects.
* [ ] Idempotency keys are scoped and stored appropriately.
* [ ] Reusing a key with a different request is handled according to the contract.
* [ ] Concurrent requests are handled safely.
* [ ] Provider-supported idempotency is used where appropriate.
* [ ] A timeout after a possible successful provider operation is treated as ambiguous, not automatically as failure.
* [ ] Recovery can determine the operation's outcome without blindly repeating a financial side effect.

## Transactions and state transitions

* [ ] State transitions are validated and enforced server-side.
* [ ] Database updates preserve required invariants.
* [ ] Transaction boundaries are appropriate to the operation.
* [ ] External API calls are not assumed to participate in local database transactions.
* [ ] Partial failures do not silently leave inconsistent state.
* [ ] Concurrent updates cannot overwrite a newer valid state without detection.
* [ ] Recovery and reconciliation are available for relevant failure modes.

## Provider communication

* [ ] Requests use the intended provider and environment.
* [ ] Response status, schema, and business outcome are validated.
* [ ] Timeouts and network errors are handled.
* [ ] Retries are bounded and safe for the operation.
* [ ] Rate limiting and temporary provider failures are handled appropriately.
* [ ] Ambiguous outcomes are reconciled where necessary.
* [ ] Provider error details are mapped safely without exposing secrets or sensitive information.

## Payment data

* [ ] Only required payment data is collected and retained.
* [ ] Sensitive payment data is not unnecessarily logged or returned.
* [ ] Provider tokens and references are handled according to their intended use.
* [ ] Payment details are not exposed across users, merchants, or tenants.
* [ ] Applicable compliance requirements are established from the actual system context rather than assumed.

## Audit and recovery

* [ ] Important financial state changes can be traced.
* [ ] Audit records avoid secrets and unnecessary sensitive data.
* [ ] Failed and ambiguous operations can be investigated.
* [ ] Reconciliation can identify relevant differences between internal and provider state.
* [ ] Operational recovery does not bypass payment invariants.

## Testing

* [ ] Relevant success paths are tested.
* [ ] Invalid amounts, currencies, states, and permissions are tested where applicable.
* [ ] Duplicate and concurrent operations are tested where relevant.
* [ ] Provider failures and ambiguous outcomes are tested.
* [ ] State consistency is checked after failures.
* [ ] Regression tests cover confirmed defects.

## Review rule

A checkbox is an investigation prompt, not proof of a defect. Trace the relevant code path and requirements before reporting a finding. If a required business rule is not documented, record the uncertainty rather than inventing the rule.
