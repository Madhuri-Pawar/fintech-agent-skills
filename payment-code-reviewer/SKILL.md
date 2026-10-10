---
name: payment-code-reviewer
description: Review payment-related code (examples assume NestJS, but the checks apply to any backend) for correctness, potential defects, edge cases, and payment-flow risks - idempotency, duplicate payments, amount and currency validation, authorization, transaction boundaries, provider timeouts, webhook handling, OAuth/API-key/mTLS integrations, error recovery, reconciliation, and missing tests. Use when implementing or reviewing payment creation, authorization, capture, refund, cancellation, status updates, payment APIs, or provider callbacks.
---

# Payment Code Reviewer

## Purpose

Find correctness defects, edge cases, and payment-flow risks in payment code and recommend fixes that can be verified with tests. Prioritize risks that could move money twice, lose money, or leave payment state wrong or unknown.

Base findings on the code and contracts provided. Do not invent provider behavior, database guarantees, or business rules.

## 1. Read the references

Before reviewing:

* Use [references/business-flow-matrix.md](references/business-flow-matrix.md) to identify the business flow and select the relevant checks.
* Use [references/payment-safety-checklist.md](references/payment-safety-checklist.md) for payment correctness and safety criteria.
* Use [references/api-security-checklist.md](references/api-security-checklist.md) when the change touches API exposure, authentication, authorization, webhooks, OAuth, API keys, TLS/mTLS, or outbound provider calls.
* Use [references/testing-playbook.md](references/testing-playbook.md) when identifying missing tests.
* Use [references/finding-format.md](references/finding-format.md) to write findings.

Not every application implements every operation. Check the actual architecture before treating a checklist item as required.

## 2. Establish the scope

Identify:

* The operation under review (create, authorize, capture, refund, cancel, status update, webhook).
* The entry points: controllers, DTOs, guards, pipes, and message handlers.
* The services, repositories, and provider clients involved.
* The source of truth for payment state.
* The documented API and provider contract, if available.

If important code is missing, such as the persistence layer or the provider client, say so and limit conclusions to what was supplied.

## 3. Trace the request path

Follow one request from the API boundary to the final persisted state:

1. Validation and authorization at the boundary.
2. Idempotency check and how it is stored.
3. Database writes and transaction boundaries.
4. External provider calls, timeouts, and retries.
5. Persisting the provider result.
6. Events, messages, or webhooks emitted or consumed.
7. The response returned to the client.

At each step, ask what happens if the process crashes, the request is repeated, or a concurrent request arrives.

## 4. Review the high-risk areas

Work through the checklist sections, focusing on:

* **Idempotency:** Atomic key handling, concurrent duplicates, key reuse with a different payload, in-progress and unknown outcomes.
* **External side effects:** A database rollback cannot undo a provider action. Check timeouts, ambiguous outcomes, provider idempotency, and recovery when local persistence fails after provider success.
* **Transactions and concurrency:** No locks held across slow network calls, database-level uniqueness, no silent overwrites of payment state.
* **Validation and authorization:** Exact monetary representation, currency checks, server-side ownership, no client control of internal state.
* **Webhooks:** Signature verification, duplicate and out-of-order delivery, stale events that could revert a terminal state.
* **Errors and observability:** No leaked internals or secrets, unknown outcomes not reported as success or failure, enough correlation data for reconciliation.

Also check edge cases: zero, negative, and maximum amounts; rounding and minor units; currency mismatches; partial captures and refunds; retries after partial failure; expired or already-terminal payments; and null or missing provider fields.

## 5. Report findings

Use the template and severity guidance in [references/finding-format.md](references/finding-format.md). Order findings by severity (Critical, High, Medium, Low, Informational). As a rule of thumb:

* **Critical:** Can cause duplicate charges, lost funds, or unauthorized payment actions.
* **High:** Can leave payment state wrong or unrecoverable without manual work.
* **Medium:** Weakens safety, observability, or recovery.
* **Low:** Limited-impact defect or minor hardening.
* **Informational:** Useful observation that is not a defect.

For every finding, state the concrete failure scenario: the sequence of events that causes harm. Mark confidence as Confirmed, Likely, or Needs verification, and flag anything that depends on an unverified assumption, such as provider idempotency support or database isolation level.

Separate confirmed defects from potential risks and open questions. Do not report a missing control until you have traced the shared guards, middleware, and downstream services where it might be enforced.

## 6. Recommend tests

List missing tests for the identified risks, using the testing playbook format: setup, action, expected result, assertions, and failure significance.

Prefer integration tests against the real database for constraints, transactions, and concurrency. Do not claim a race condition is fixed without a test that exercises concurrent requests.

## Safety rules

* Do not execute changes or diagnostics against production.
* Do not include secrets, credentials, or real customer payment data in review output.
* Do not impose a universal payment state machine. Review the existing contract first.
* Distinguish verified behavior from assumptions.
