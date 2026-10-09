# Payment Safety Checklist

Use this checklist when reviewing payment creation, capture, authorization, cancellation, refund, status updates, and provider callbacks.

Not every application implements every operation. Verify the actual architecture before treating an item as required.

## 1. Payment invariants

* [ ] Amounts are validated and represented using an exact, documented monetary format.
* [ ] Currency is validated against the operation's supported currencies.
* [ ] The authenticated caller is authorized to perform the operation.
* [ ] Client input cannot directly set trusted internal state or ownership fields.
* [ ] The system has a clear source of truth for payment state.
* [ ] Invalid state transitions are rejected.
* [ ] Responses distinguish accepted, pending, successful, failed, and unknown outcomes where the domain requires them.
* [ ] Sensitive data is not unnecessarily returned or logged.

## 2. Idempotency

Verify the behavior for:

* [ ] The first request with a new key.
* [ ] An exact retry with the same key and payload.
* [ ] Concurrent requests using the same key.
* [ ] Reuse of the same key with a different payload.
* [ ] The same key used by a different customer or operation.
* [ ] An application restart between processing steps.
* [ ] A provider timeout after the provider may have processed the request.
* [ ] A provider success followed by a local persistence failure.
* [ ] A repeated webhook or message delivery.
* [ ] Expiration or cleanup of stored idempotency records.

An idempotency key should be scoped according to the domain and protected by an atomic mechanism. A prior lookup alone is not sufficient when concurrent requests are possible.

The application must define what happens when an existing operation is still in progress or its outcome is unknown.

## 3. External side effects

* [ ] External calls have explicit timeout behavior.
* [ ] Retry rules distinguish transient errors from permanent errors.
* [ ] Retries do not unintentionally create a second logical payment.
* [ ] Provider idempotency is used when supported and appropriate.
* [ ] Provider success can be recovered if local state recording fails.
* [ ] Unknown outcomes can be queried, reconciled, or safely retried.
* [ ] Webhook authenticity is verified using the provider's documented mechanism.
* [ ] Duplicate and out-of-order callbacks are handled.
* [ ] Durable event publication is considered when database writes and message publication must remain consistent.

A database rollback cannot undo an external payment-provider action.

## 4. Transactions and concurrency

* [ ] Related database changes use the appropriate transaction boundary.
* [ ] The transaction includes the necessary state changes, but does not unnecessarily hold locks across slow network calls.
* [ ] Uniqueness and consistency invariants are enforced at the database level where appropriate.
* [ ] Concurrent updates cannot silently overwrite important payment state.
* [ ] Lock ordering and isolation assumptions are understood.
* [ ] Deadlock and serialization failures have deliberate retry behavior.
* [ ] Event or outbox records are committed consistently with the state they represent.
* [ ] Compensation and reconciliation are defined for cross-system failures.

## 5. Validation and authorization

* [ ] DTO validation runs at the API boundary.
* [ ] Amounts, currencies, identifiers, and enums are validated.
* [ ] Ownership and tenant boundaries are checked server-side.
* [ ] Provider identifiers are not treated as proof of authorization.
* [ ] State-changing operations require appropriate permissions.
* [ ] Untrusted webhook fields cannot override authoritative internal values.
* [ ] Secrets and signature verification material are handled safely.

## 6. Errors and observability

* [ ] Internal exceptions do not leak stack traces or sensitive implementation details to clients.
* [ ] Logs contain enough correlation information to investigate failures without exposing secrets or full payment payloads.
* [ ] Unknown provider outcomes are not reported as definitive failures or successes without evidence.
* [ ] Retry attempts and final outcomes are distinguishable.
* [ ] Alerts cover relevant failure rates, stuck states, and reconciliation discrepancies.
* [ ] Operational recovery procedures are documented for ambiguous or inconsistent outcomes.

## 7. State machine

Check whether the implementation defines and enforces allowed transitions.

For example, an application might model transitions from `pending` to `succeeded` or `failed`, but the actual states and rules depend on its domain and provider. Do not impose a universal state machine without reviewing the existing contract.

* [ ] Terminal states cannot be overwritten by stale events without a deliberate rule.
* [ ] Repeated events do not repeat financial side effects.
* [ ] Out-of-order events are handled.
* [ ] State changes have a traceable source and timestamp.
* [ ] The system can recover from a local/provider state mismatch.

## 8. Before approving

* [ ] Findings are evidence-based and include locations.
* [ ] The most serious plausible financial risks are addressed.
* [ ] Tests cover the identified failure paths.
* [ ] Remaining assumptions and risks are explicit.
* [ ] No secrets or real customer data are included in the review output.
