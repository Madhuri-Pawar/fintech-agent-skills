# Payment API Testing Playbook

Use these scenarios to design focused tests for NestJS payment APIs. Adapt the test names and expected results to the application's documented contract.

## 1. Request validation

Test:

* Missing required fields.
* Invalid or unsupported currency.
* Zero, negative, excessively large, or malformed amounts.
* Decimal precision that the currency or API does not support.
* Invalid identifiers and enum values.
* Extra fields that attempt to set internal state or ownership.
* Requests from an unauthorized user or tenant.

Verify that rejected requests do not create payment records or trigger provider calls.

## 2. Idempotency

Test:

* A valid first request creates one logical operation.
* An exact retry returns the documented result without creating a second operation.
* Two simultaneous requests with the same key do not create two logical payments.
* Reusing a key with a different payload follows the API contract and does not silently change the original operation.
* Keys from different scopes do not collide incorrectly.
* A retry after a timeout safely resolves the original operation.
* An in-progress request has a defined response behavior.

Assert both the API response and persisted state. Counting provider mock calls alone may not prove that duplicate financial operations are impossible.

## 3. Provider failures and ambiguous outcomes

Test:

* Provider rejects the request.
* Provider times out before a response arrives.
* Provider processes the request but the response is lost.
* Provider succeeds but local persistence fails.
* A transient provider error triggers only the intended retry policy.
* A permanent validation or business error is not retried indefinitely.
* Provider status lookup returns pending, succeeded, failed, or unknown outcomes where supported.

Verify that an ambiguous result is not automatically treated as a definitive failure and that retrying does not create a second logical payment.

## 4. Transaction boundaries

Test:

* A database error before the commit leaves no partial local state.
* Related records remain consistent when a transaction fails.
* A provider success followed by a local write failure can be recovered.
* An outbox record, when used, commits consistently with the business state.
* A message-publishing failure does not silently lose a required event.
* Deadlock or serialization errors follow the documented retry policy.

Use the actual database engine for tests involving database constraints, transaction isolation, and locking. In-memory mocks alone cannot prove PostgreSQL concurrency behavior.

## 5. Webhooks and asynchronous messages

Test:

* A valid authenticated webhook is accepted.
* An invalid signature is rejected.
* A duplicate event does not repeat the financial side effect.
* An event arrives before the expected preceding event.
* Events arrive out of order.
* The same event identifier is reused with conflicting content.
* Event processing fails midway and is retried.
* An unrelated or unknown provider reference cannot modify another customer's payment.

Verify both state changes and external side effects.

## 6. State transitions

Test:

* Each documented valid transition succeeds.
* Invalid transitions are rejected.
* Repeated terminal events are handled safely.
* A stale event cannot incorrectly revert a newer state.
* Concurrent updates preserve the documented invariants.
* Reconciliation can detect a mismatch between provider and local state.

Do not assume every provider or product uses the same set of states.

## 7. NestJS API behavior

Test:

* DTO validation is actually enabled for the route.
* Guards enforce authentication and authorization.
* Service errors map to the expected HTTP response.
* Internal errors do not expose stack traces or secrets.
* Async errors are propagated and handled.
* Webhook signature verification uses the required request representation.
* Sensitive fields are excluded from response serialization and logs.

## 8. Test quality

Prefer:

* Deterministic mocks for provider failures.
* Integration tests for database constraints and transaction behavior.
* Explicit synchronization for concurrency tests instead of arbitrary sleeps.
* Unique test identifiers and isolated test data.
* Assertions on persisted state and side effects.
* Cleanup that cannot affect non-test environments.

Avoid:

* Tests that only assert HTTP status codes.
* Tests that depend on live payment providers by default.
* Real customer or production payment data.
* Timing assumptions without synchronization.
* Claims that a race is fixed without a test that exercises concurrent requests.

## Suggested test report

For each test scenario, document:

* **Setup:** Initial database and provider state.
* **Action:** Request, event, failure, or concurrent operation.
* **Expected result:** API response and state invariants.
* **Assertions:** Database rows, provider calls, emitted events, and relevant logs.
* **Failure significance:** What financial or operational risk the test protects against.
