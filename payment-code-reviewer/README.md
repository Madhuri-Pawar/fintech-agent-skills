# Payment code reviewer

A Claude skill for reviewing NestJS payment APIs. It helps developers find payment-safety problems systematically, explain findings clearly, and recommend changes that can be validated with tests.

**Use when:** Implementing or reviewing a NestJS payment API.

The skill checks:

* Idempotency and duplicate-payment risks.
* Input validation and authorization.
* Database transaction boundaries.
* Provider timeouts and ambiguous outcomes.
* Webhook retries and duplicate delivery.
* Error handling, recovery, and reconciliation.
* Tests for concurrency and failure scenarios.

## Structure

```
payment-code-reviewer/
  README.md
  SKILL.md                          # review workflow and safety rules
  references/
    payment-safety-checklist.md     # review criteria
    testing-playbook.md             # test scenarios and report format
  LICENSE
```

## Installation

Copy the `payment-code-reviewer` folder into the skills directory supported by your Claude environment. For Claude Code, project-level skills are stored under:

```
.claude/skills/payment-code-reviewer/SKILL.md
.claude/skills/payment-code-reviewer/references/
```

Keep the `references` directory alongside `SKILL.md`.

## How to use

Describe the task and provide the relevant code.

Examples:

* "Review this NestJS payment endpoint for idempotency and duplicate-payment risks."
* "Check whether this payment service handles provider timeouts safely."
* "Identify missing tests for provider timeouts and repeated webhooks."

Provide the relevant controller, DTO, service, persistence logic, and tests. Include provider and database behavior only when it is safe to share.

## Safety and limitations

* This skill does not replace production change approval or operational procedures.
* Payment safety depends on the actual application architecture and provider contract.
* Recommendations must be tested against the target application and database.
* Never include production credentials, customer payment details, or private infrastructure information in examples.

## Contributing

Contributions are welcome when they improve correctness, clarity, safety, or testability.

Please:

1. Keep examples fictional and provider-neutral unless a specific integration is intentionally documented.
2. Avoid organization-specific schemas, hostnames, internal error codes, and business rules.
3. Explain the reasoning behind important safety recommendations.
4. Include reproducible examples or tests when practical.
5. Distinguish verified behavior from assumptions.

## License

MIT
