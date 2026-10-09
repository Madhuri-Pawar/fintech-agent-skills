# Evaluation Prompts

Run these prompts in a fresh conversation with the skill enabled. Pair each prompt with its matching scenario in `test-cases.md`.

## Prompt 1 — General review

Review this payment-related change. Identify the business use case first, trace the relevant code path, and select only applicable correctness, security, reliability, and testing checks.

Report actionable findings with evidence, severity, impact, remediation, and suggested regression tests. Separate confirmed defects from risks and unanswered questions. Avoid a generic checklist.

## Prompt 2 — Payment creation

Review this payment creation flow for amount and currency validation, authorization, idempotency, provider timeouts, retries, and ambiguous outcomes.

Prioritize payment-initiation risks. Do not add unrelated webhook or certificate findings unless the reviewed path makes them relevant.

## Prompt 3 — Refund API

Review this refund endpoint for caller permissions, payment ownership, refundable balance, currency and amount validation, idempotency, concurrent requests, provider failures, and state consistency.

Trace shared controls before reporting missing protections.

## Prompt 4 — Webhook security

Review this provider webhook handler for signature verification, raw-body requirements, replay protections, event validation, duplicate delivery, event ordering, and payment-state transitions.

Use the supplied provider contract. Do not assume all providers use the same signature scheme.

## Prompt 5 — OAuth client

Review this outbound OAuth provider client for the applicable grant flow, client authentication, token acquisition, expiry and refresh, scopes, TLS verification, secret handling, timeouts, and safe retries.

Distinguish requirements for this flow from controls applicable only to other OAuth flows.

## Prompt 6 — mTLS integration

Review this integration for TLS and mTLS security. Determine whether mTLS is required from the supplied contract.

Check server certificate and hostname verification, client-certificate presentation and validation, private-key handling, expiry, rotation, and failure behavior.

Do not recommend disabling certificate verification.

## Prompt 7 — Payment history API

Review this API for authentication, object-level authorization, tenant isolation, sensitive data exposure, pagination, filtering, and relevant input validation.

Trace shared authorization before reporting a gap.

## Prompt 8 — Reconciliation job

Review this reconciliation job for concurrency, duplicate processing, inconsistent internal and provider state, retry safety, partial failures, and recovery.

Recommend controls appropriate to the actual execution model.

## Prompt 9 — Security-focused review

Perform a security-focused review of this payment integration. Select applicable checks for authentication, authorization, OAuth, API keys, TLS/mTLS, webhook signatures, exposed endpoints, SSRF, secrets, sensitive logging, and outbound requests.

Do not assume every control is mandatory. Explain which requirements are supported by the evidence.

## Prompt 10 — False-positive resistance

Review this implementation and report only actionable findings supported by the code and supplied requirements.

Shared middleware verifies webhook signatures, and the provider contract does not require mTLS. Trace these controls and do not report them as missing. Identify any separate, evidenced defects.

## Prompt 11 — Missing context

Review this provider integration. The code is available, but the provider's authentication requirements are not supplied.

Identify what can be established from the implementation. Ask only focused questions needed to resolve material uncertainty. Do not invent requirements or request real credentials.

## Prompt 12 — Regression-test planning

Based on the review, propose focused regression tests for the findings. Include success cases, authorization failures, malformed input, provider failures, duplicate requests, and concurrency where relevant.

Do not recommend tests for controls unrelated to this business flow.
