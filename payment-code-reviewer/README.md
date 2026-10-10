# Payment Code Reviewer

A reusable Claude Skill for reviewing payment-related code based on the actual business use case.

It helps identify correctness, security, reliability, concurrency, and testing issues without forcing the same checklist onto every change.

## Capabilities

* Payment creation, authorization, capture, refunds, and cancellations
* Idempotency, duplicate operations, and concurrency
* Payment state transitions and reconciliation
* Webhook signature verification and event processing
* OAuth, access tokens, and API keys
* TLS, mTLS, and certificate lifecycle checks
* Authentication, authorization, and tenant isolation
* Exposed APIs and authenticated outbound requests
* Credential management, sensitive logging, and error handling
* Focused regression-test recommendations

## Repository structure

```text
payment-code-reviewer/
├── SKILL.md
├── README.md
├── references/
│   ├── business-flow-matrix.md
│   ├── payment-safety-checklist.md
│   ├── api-security-checklist.md
│   ├── testing-playbook.md
│   └── finding-format.md
└── test/
    ├── README.md
    ├── test-cases.md
    ├── expected-findings.md
    └── prompt.md
```

## Installation

Follow the Claude Skills installation method supported by your Claude environment.

For a local skill installation, place the `payment-code-reviewer` directory in the supported skills directory, then start or refresh a conversation so the skill can be discovered.

For GitHub publication, keep `SKILL.md` at the skill directory root. Include the referenced files so links and instructions remain complete.

## Example prompts

* Review this payment creation change for duplicate-payment risks.
* Review this refund endpoint for business-rule and authorization defects.
* Review this webhook handler for signature verification and replay risks.
* Review this OAuth client for token expiry, secret handling, and safe retries.
* Review this mTLS integration against the supplied provider contract.
* Review this payment history API for tenant isolation.
* Review this reconciliation job for concurrency and recovery issues.

## Review principles

The skill identifies the use case first, selects relevant checks, traces controls across the actual code path, and reports actionable findings.

It distinguishes confirmed defects from potential risks and unknown requirements. It does not assume that every integration requires OAuth, API keys, mTLS, or webhooks.

## Testing the skill

See `test/README.md` for the manual evaluation workflow.

The test scenarios and expected findings help assess both defect detection and resistance to false positives. They are evaluation fixtures, not a guarantee of complete security coverage.

## Confidentiality

Before sharing code with any model or publishing examples:

* Remove real API keys, client secrets, access tokens, private keys, certificates containing sensitive material, and webhook signing secrets.
* Remove customer information and payment data.
* Replace internal hostnames, company-specific identifiers, and private infrastructure details where necessary.
* Use fictional provider endpoints and placeholder credentials.
* Follow your organization's rules for source-code sharing.

Never use production credentials to run evaluation scenarios.

## Contributions

Contributions should improve use-case selection, evidence-based findings, and test quality without adding provider-specific assumptions to generic guidance.

New test scenarios should include:

1. The business use case.
2. Sanitized input or behavior.
3. Expected findings.
4. False-positive constraints.

## License

MIT. See [LICENSE](LICENSE).
