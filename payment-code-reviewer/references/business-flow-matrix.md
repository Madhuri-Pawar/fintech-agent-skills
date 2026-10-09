# Business Flow Matrix

Use this matrix to select the relevant review areas. It is a guide, not a requirement to report every item.

| Business flow               | Primary checks                                                           | Conditional checks                                              |
| --------------------------- | ------------------------------------------------------------------------ | --------------------------------------------------------------- |
| Payment creation            | Amount, currency, authorization, idempotency, provider errors            | Webhooks, OAuth, API keys, mTLS depending on architecture       |
| Payment authorization       | State transitions, permissions, authorization amount, duplicate requests | Expiry and incremental authorization if supported               |
| Capture                     | Capture limits, state, idempotency, concurrency                          | Partial or multiple capture rules if supported                  |
| Refund                      | Permissions, refundable balance, state, idempotency                      | Approval workflows or limits if required                        |
| Cancellation or void        | Allowed states, ownership, duplicate operations                          | Provider-specific cancellation window                           |
| Payment status API          | Authentication, object-level authorization, data exposure                | Tenant isolation, pagination, filtering                         |
| Payment history API         | Access controls, query validation, data minimization                     | Rate limiting and export controls                               |
| Webhook handler             | Signature verification, event validation, idempotency                    | Replay controls, ordering, provider IP restrictions if required |
| Outbound provider client    | TLS, credentials, timeouts, retries, response validation                 | OAuth, API keys, mTLS based on contract                         |
| OAuth integration           | Grant flow, client authentication, token lifecycle                       | State, PKCE, redirect URI validation where applicable           |
| API-key integration         | Secure key handling, scope, rotation, revocation                         | Per-key rate limits or IP restrictions where required           |
| mTLS integration            | Server certificate verification, client certificate validation           | Rotation, renewal, certificate identity mapping                 |
| Reconciliation job          | State consistency, concurrency, idempotency, recovery                    | Scheduling, distributed locks, operational alerts               |
| Payment-method management   | Ownership, authorization, sensitive data, tokenization                   | Provider-specific compliance requirements                       |
| Admin or merchant operation | Privileged access, tenant boundaries, audit trail                        | Dual approval or stronger authentication where required         |
| Shared HTTP client          | TLS, credential forwarding, timeout, retry behavior                      | Redirect policy, destination restrictions                       |
| Shared authentication layer | Authentication, authorization, safe failure behavior                     | Rate limits, token revocation, audit logging                    |
| Configuration change        | Secret references, environment separation, secure defaults               | Rotation and deployment rollout                                 |

## How to use this matrix

1. Identify the changed operation and its upstream and downstream dependencies.
2. Select the matching row or rows.
3. Trace where each relevant control is actually enforced.
4. Use the detailed reference checklist for the selected areas.
5. Mark unsupported or irrelevant checks as not applicable during analysis.
6. Ask a focused question if a requirement materially affects the conclusion.

## Important distinctions

* Authentication establishes identity or caller credentials; authorization determines permitted actions and resources.
* TLS validates the server connection when configured correctly. mTLS adds client-certificate authentication when required.
* OAuth and API keys are not interchangeable requirements. The integration contract determines the expected mechanism.
* Webhook signatures authenticate message integrity or origin according to the provider's scheme; they do not automatically prevent replay or duplicate processing.
* A controller may delegate security checks to shared middleware, guards, gateways, or services. Trace these before reporting a missing control.

Do not infer a security defect merely because an optional control is absent. Establish that the control is required or necessary for the observed risk.
