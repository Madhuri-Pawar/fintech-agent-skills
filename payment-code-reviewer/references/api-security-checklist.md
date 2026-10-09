# API Security Checklist

Use this checklist for the relevant API, webhook, authentication, or provider-integration path.

## 1. Authentication and authorization

* [ ] The endpoint has the intended exposure: public, authenticated, internal, or provider-facing.
* [ ] Protected operations authenticate the caller.
* [ ] Authorization is checked for the requested action and resource.
* [ ] Payment IDs cannot be used to access another customer's or tenant's data.
* [ ] Administrative and merchant operations have appropriate access restrictions.
* [ ] Missing, malformed, expired, and revoked credentials are handled correctly.
* [ ] Shared middleware, guards, gateways, and downstream services have been inspected.
* [ ] Authentication failures do not reveal secrets or sensitive implementation details.

## 2. OAuth and access tokens

* [ ] The grant flow and client authentication method match the integration requirements.
* [ ] Token acquisition and provider errors are handled safely.
* [ ] Expiry and refresh behavior match the token contract.
* [ ] Issuer, audience, signature, algorithm, and scope are validated where the application is responsible for those checks.
* [ ] Redirect URI, state, and PKCE protections are reviewed when relevant to the OAuth flow.
* [ ] Client secrets and access tokens are stored and transmitted securely.
* [ ] Tokens are not sent to unintended hosts or exposed in logs.
* [ ] Refresh failures do not cause unsafe retries or inconsistent payment operations.

Do not require authorization-code-flow protections in a client-credentials flow where they do not apply.

## 3. API keys

* [ ] Keys are sent using the provider's documented mechanism.
* [ ] Keys are not unnecessarily placed in URLs.
* [ ] Keys are stored in approved secret storage or equivalent secure configuration.
* [ ] Scope, revocation, expiry, and rotation are considered where supported.
* [ ] Sandbox and production keys are separated.
* [ ] Keys are not included in logs, responses, source control, or error messages.
* [ ] Invalid keys fail safely.

## 4. TLS and mTLS

* [ ] TLS certificate and hostname verification are enabled for outbound connections.
* [ ] mTLS is used when required by the provider contract or application policy.
* [ ] Required client certificates are presented and validated.
* [ ] Trust configuration is appropriate for the intended endpoint.
* [ ] Private keys are protected and not embedded in source code.
* [ ] Certificate expiry, renewal, and rotation are considered.
* [ ] Invalid certificates and trust failures do not trigger insecure fallback.
* [ ] Development and production certificate configuration is handled appropriately.

Do not confuse presenting a client certificate with validating the remote server's certificate. They serve different purposes.

## 5. Webhook signature verification

* [ ] The provider's documented verification method is used.
* [ ] Signature verification occurs before trusting or applying the event.
* [ ] Raw request bytes are preserved when required by the signing scheme.
* [ ] Algorithm, encoding, canonicalization, and key selection match the provider contract.
* [ ] Timestamp or replay protections are used where supported.
* [ ] Invalid signatures are rejected safely.
* [ ] Duplicate events are handled idempotently.
* [ ] Event type, referenced payment, amount, currency, and allowed state transition are validated where applicable.
* [ ] Signing secrets are protected and not logged.

A valid signature does not automatically guarantee freshness, uniqueness, correct event ordering, or a valid business transition.

## 6. Exposed APIs and request handling

* [ ] Public exposure is intentional and documented where needed.
* [ ] Request bodies, parameters, headers, and content types are validated.
* [ ] Request-size limits and rate limiting are appropriate to the endpoint's risk.
* [ ] Sensitive operations enforce server-side permissions.
* [ ] Error responses avoid leaking internal details.
* [ ] CORS is not treated as a substitute for authentication or authorization.
* [ ] Callback URLs and user-controlled destinations are checked for SSRF risks where applicable.
* [ ] Administrative and diagnostic endpoints are not unintentionally exposed.

## 7. Outbound API calls

* [ ] Credentials are sent only to the intended trusted destination.
* [ ] TLS verification remains enabled.
* [ ] Redirect handling cannot leak credentials to an unintended host.
* [ ] Timeouts and retries are bounded and appropriate to the operation.
* [ ] Retrying a financial operation cannot unintentionally duplicate its effect.
* [ ] Provider responses are validated before changing payment state.
* [ ] Error handling does not expose credentials or sensitive provider responses.
* [ ] Environment and base-URL configuration are validated.

## 8. Secrets and sensitive data

* [ ] No live credentials or private keys are hardcoded.
* [ ] Configuration references an approved secret-management mechanism.
* [ ] Secrets are not logged or returned to callers.
* [ ] Sensitive values are redacted in exceptions and diagnostics.
* [ ] Rotation can occur without unsafe fallback.
* [ ] Secret-bearing files are excluded from publication where appropriate.
* [ ] Tests use synthetic credentials.

## 9. Finding requirements

Report a security issue only when the code, contract, policy, or demonstrated behavior supports it.

For each finding, include:

* Affected endpoint or integration path
* Applicable security requirement
* Evidence and attack or failure scenario
* Impact
* Recommended fix
* Regression test

If the requirement or configuration cannot be verified, label it as a question or potential risk instead of a confirmed vulnerability.
