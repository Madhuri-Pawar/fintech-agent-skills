---
name: payment-code-reviewer
description: Review NestJS payment API code for idempotency, duplicate-payment risks, validation, authorization, transaction boundaries, provider timeouts, webhook handling, error recovery, reconciliation, and missing tests. Use when implementing or reviewing payment creation, capture, refund, cancellation, status updates, or provider callbacks.
---

# Payment Code Reviewer

## Purpose

Find payment-safety problems in NestJS payment code and recommend fixes that can be verified with tests. Prioritize risks that could move money twice, lose money, or leave payment state wrong or unknown.

Base findings on the code and contracts provided. Do not invent provider behavior, database guarantees, or business rules.

## 1. Read the references

Before reviewing:

* Use [references/payment-safety-checklist.md](references/payment-safety-checklist.md) for the review criteria.
* Use [references/testing-playbook.md](references/testing-playbook.md) when identifying missing tests.

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

## 5. Report findings

Order findings by severity:

* **Critical:** Can cause duplicate charges, lost funds, or unauthorized payment actions.
* **High:** Can leave payment state wrong or unrecoverable without manual work.
* **Medium:** Weakens safety, observability, or recovery.
* **Low:** Clarity, maintainability, or minor hardening.

For each finding, include:

* **Location:** File and line or function.
* **Problem:** What is wrong.
* **Failure scenario:** The concrete sequence of events that causes harm.
* **Recommendation:** The smallest change that addresses it.
* **Verification:** The test that proves the fix (see the testing playbook).

Mark anything that depends on an unverified assumption, such as provider idempotency support or database isolation level.

## 6. Recommend tests

List missing tests for the identified risks, using the testing playbook format: setup, action, expected result, assertions, and failure significance.

Prefer integration tests against the real database for constraints, transactions, and concurrency. Do not claim a race condition is fixed without a test that exercises concurrent requests.

## Safety rules

* Do not execute changes or diagnostics against production.
* Do not include secrets, credentials, or real customer payment data in review output.
* Do not impose a universal payment state machine. Review the existing contract first.
* Distinguish verified behavior from assumptions.
