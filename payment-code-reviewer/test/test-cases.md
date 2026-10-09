# Payment Code Reviewer Test Cases

All scenarios are fictional evaluation fixtures.

## TC-01 — Duplicate payment creation

**Scenario**

A payment endpoint sends a create-payment request to a provider. The client may retry after a timeout. The application does not use an idempotency key or reconcile ambiguous outcomes.

**Expected behavior**

* Identify the risk of duplicate payment creation.
* Recommend provider-supported idempotency or an equivalent safe deduplication design.
* Explain why a timeout does not prove the provider operation failed.
* Suggest a test for a retry after an ambiguous outcome.

**False-positive guard**

Do not report missing webhook signature verification unless webhook processing is part of the reviewed path.

## TC-02 — Refund authorization

**Scenario**

A refund endpoint accepts a payment identifier and amount. It verifies that the payment exists, but the inspected execution path contains no ownership check or refundable-balance validation.

**Expected behavior**

* Report missing authorization if no shared layer enforces it.
* Report the missing refund validation when supported by the supplied business rules.
* Recommend tests for unauthorized access and excessive refunds.

**False-positive guard**

Do not assume mTLS is required for this endpoint.

## TC-03 — Webhook signature verification

**Scenario**

A provider-facing handler processes a payment-success event. The supplied code path contains no signature verification, and the provider contract requires signed webhooks.

**Expected behavior**

* Report the missing required verification.
* Explain the risk of untrusted events changing payment state.
* Recommend verification before processing, state validation, and invalid-signature tests.

**False-positive guard**

Do not report missing verification if trusted shared middleware performs it and that path is evidenced.

## TC-04 — OAuth token expiry

**Scenario**

A provider client retrieves an access token once at application startup and caches it indefinitely. Requests begin failing when the token expires.

**Expected behavior**

* Identify the missing token-lifecycle handling.
* Recommend expiry-aware refresh or reacquisition according to the provider contract.
* Suggest tests for expiry and refresh failure.

**False-positive guard**

Do not demand an additional API key if the provider contract specifies OAuth.

## TC-05 — Disabled TLS verification

**Scenario**

An outbound client presents an mTLS client certificate but disables verification of the provider server's certificate.

**Expected behavior**

* Report disabled server certificate verification.
* Explain the risk of connecting to an impersonated endpoint.
* Recommend normal certificate and hostname verification and appropriate tests.

**False-positive guard**

Do not confuse server certificate verification with client-certificate presentation.

## TC-06 — Cross-tenant payment access

**Scenario**

An authenticated caller can request a payment by identifier. The service retrieves it by identifier alone. The supplied code and surrounding path show no ownership or tenant authorization check.

**Expected behavior**

* Report the object-level authorization defect.
* Explain the possibility of unauthorized payment-data access.
* Recommend server-side access enforcement and cross-tenant tests.

**False-positive guard**

Do not report a missing check if an inspected shared authorization layer demonstrably enforces it.

## TC-07 — Concurrent reconciliation

**Scenario**

Two job instances can process the same pending payment. Each can call the provider before either instance records its result.

**Expected behavior**

* Identify the concurrent-processing and duplicate-side-effect risk.
* Recommend an approach appropriate to the architecture, such as provider idempotency, concurrency-safe state transitions, or coordination.
* Suggest a concurrent execution test.

**False-positive guard**

Do not prescribe distributed locks automatically if another proven mechanism safely enforces the invariant.

## TC-08 — Secure webhook implementation

**Scenario**

Shared middleware verifies webhook signatures using the documented provider scheme. The handler validates events, deduplicates deliveries, and applies allowed state transitions. The provider contract does not require mTLS.

**Expected behavior**

* Recognize the evidenced controls.
* Report only independent, evidence-supported defects.

**False-positive guard**

Do not report missing mTLS or missing signature verification merely because those checks are on a generic checklist.

## TC-09 — Missing provider contract

**Scenario**

The code calls an external payment API using a configured credential. No provider documentation or security contract is supplied.

**Expected behavior**

* Review visible credential handling, TLS configuration, request construction, error handling, and retry behavior.
* Identify requirements that cannot be verified.
* Ask a focused question about the provider's required authentication mechanism if it materially affects the review.

**False-positive guard**

Do not claim OAuth, API keys, or mTLS is mandatory without evidence.

## TC-10 — Secret leakage

**Scenario**

An outbound provider client includes an access token in an exception message that is written to application logs.

**Expected behavior**

* Report sensitive credential exposure.
* Recommend redaction and safe error handling.
* Suggest a test ensuring credentials do not appear in logs.

**False-positive guard**

Do not reproduce the secret in the finding.

## TC-11 — Unsafe callback URL

**Scenario**

A service accepts a user-configurable callback URL and sends an authenticated outbound request to it. The code does not restrict the destination.

**Expected behavior**

* Assess the risk of server-side request forgery and credential forwarding.
* Recommend destination restrictions and safe outbound-request handling appropriate to the use case.
* Suggest tests for disallowed internal or unexpected destinations.

**False-positive guard**

Do not claim exploitability beyond what the code and environment support.

## TC-12 — Irrelevant checklist controls

**Scenario**

A local refund calculation validates amounts and state transitions. It does not make network requests or process webhooks. Relevant authorization is enforced by the calling service.

**Expected behavior**

* Focus on the calculation, relevant business rules, and tests.
* Trace authorization enforcement if needed.
* Avoid irrelevant findings about OAuth, mTLS, or webhook signatures.

## Evaluation criteria

A case passes when the skill identifies relevant defects, grounds findings in evidence, proposes focused remediation, and avoids the listed false positives.

If the supplied scenario is insufficient to confirm a defect, the skill should state the uncertainty instead of inventing evidence.
