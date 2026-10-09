# Testing Playbook

Select tests based on the actual payment flow and implementation.

## General test quality

Check whether tests:

* Cover the relevant business rule and successful behavior.
* Exercise invalid inputs and authorization failures.
* Verify externally observable behavior rather than only private implementation details.
* Assert payment state and financial effects after failure.
* Cover duplicate requests or concurrency when the flow is exposed to them.
* Avoid real credentials, real payments, and customer data.
* Are deterministic and isolated from unrelated services where possible.

## Payment creation

Consider tests for:

* Valid amount and currency
* Invalid or unsupported amount and currency
* Unauthorized payment creation
* Repeated requests with the same idempotency key
* Conflicting requests using the same key
* Provider timeout before a known outcome
* Provider success followed by a local persistence failure
* Safe reconciliation of ambiguous outcomes

## Authorization and capture

Consider tests for:

* Allowed and disallowed state transitions
* Capture amounts beyond the allowed limit
* Repeated capture requests
* Concurrent capture attempts
* Provider rejection and timeout
* Partial capture or authorization expiry if supported

## Refund and cancellation

Consider tests for:

* Refund by an authorized owner
* Attempted refund by an unauthorized caller
* Refund amount exceeding the permitted balance
* Repeated refund request
* Concurrent refund requests
* Cancellation from an invalid state
* Provider timeout after a potentially successful operation
* Internal state consistency after partial failure

## Webhook handling

Consider tests for:

* Valid provider signature
* Invalid or missing signature
* Altered payload
* Malformed event
* Duplicate event delivery
* Replay or timestamp rejection where supported
* Out-of-order event where relevant
* Unknown payment reference
* Invalid state transition
* Persistence failure after successful verification

Test the actual verification boundary. If middleware verifies the signature, tests should cover that middleware or an appropriate integration path rather than assuming the controller owns verification.

## OAuth and API keys

Consider tests for:

* Successful token acquisition
* Invalid client credentials
* Expired access token
* Token refresh failure
* Missing or invalid scope where relevant
* Missing, invalid, or revoked API key
* Safe handling of token endpoint failures
* Absence of secrets from logs and error responses

## TLS and mTLS

Where the test environment supports it, consider:

* Valid server certificate
* Invalid or untrusted server certificate
* Hostname mismatch
* Missing, invalid, or expired client certificate when mTLS is required
* Certificate rotation and configuration change
* No insecure fallback after validation failure

Avoid tests that disable certificate verification as a workaround.

## Exposed APIs and authorization

Consider tests for:

* Missing authentication
* Invalid or expired credentials
* Authenticated caller without permission
* Cross-user or cross-tenant payment access
* Invalid path and query parameters
* Oversized payloads where limits are required
* Safe error responses
* SSRF protections for user-controlled destinations where relevant

## Provider client and outbound calls

Consider tests for:

* Connection timeout
* Provider server error
* Rate limiting
* Invalid or unexpected response
* Redirect to an unintended host
* Bounded retry behavior
* Idempotency across retries
* No credential leakage
* Safe handling of ambiguous payment outcomes

## Reconciliation jobs

Consider tests for:

* Repeated job execution
* Concurrent job instances
* Provider and internal state mismatch
* Partial processing failure
* Retry after restart
* Duplicate event or record processing
* Recovery without duplicate financial side effects

## Test recommendation format

For each relevant finding, suggest:

1. Scenario or precondition
2. Action
3. Expected result
4. Expected payment-state or external-side-effect invariant

Do not recommend every test category for every change. Select tests that exercise the risk identified in the review.
