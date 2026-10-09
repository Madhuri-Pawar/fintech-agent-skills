# Data Model

This document defines the reference data model for an ISO 20022 Request-to-Pay service. It is used by `payment-request-assistant` to interpret payment records and choose approved queries.

**Important:** Verify every table, column, relationship, status mapping, and configuration value against the actual application and database before using this document for live investigations. This reference model is not proof that a particular database has these definitions.

## 1. Configuration

Replace every `{{PLACEHOLDER}}` with a verified value before enabling database access.

| Setting                                   | Value                          |
| ----------------------------------------- | ------------------------------ |
| PostgreSQL schema                         | `{{SCHEMA}}`                   |
| User-facing timezone                      | `{{TIMEZONE}}`                 |
| Allowed MCP server names                  | `{{ALLOWED_MCP_SERVERS}}`      |
| Forbidden environments                    | `{{FORBIDDEN_ENVIRONMENTS}}`   |
| Expiry safety margin                      | `{{EXPIRY_MARGIN}}`            |
| Maximum expiry in days                    | `{{MAX_EXPIRY_DAYS}}`          |
| Entity/model source paths                 | `{{ENTITY_SOURCE_PATHS}}`      |
| Status enum and mapping source paths      | `{{STATUS_SOURCE_PATHS}}`      |
| Cancellation and expiry rule source paths | `{{STATUS_GATE_SOURCE_PATHS}}` |

Use exact MCP server identifiers in the allowed-server setting. List production as forbidden if that is your organization's policy. Do not place credentials, passwords, tokens, or connection strings in this file.

If a value is unknown, leave it clearly marked as unresolved and do not use it to make live queries.

All timestamps are expected to use PostgreSQL `timestamptz`. Verify this against the actual schema. Display timestamps in the configured timezone.

## 2. Service overview

The expected Request-to-Pay lifecycle is:

1. **Create:** The client calls the create API with an idempotency key. The platform creates a payment request, builds and signs a `pain.013` message, and attempts to send it.
2. **Submission:** The clearing house or scheme accepts the request and returns a `resource_id`. The application records the corresponding status transition.
3. **Bank response:** A `pain.014` message may indicate that the request was received and provide a redirect URL. The debtor may then approve or reject the request through their bank.
4. **Payment outcome:** A `pacs.002` or another documented scheme event may communicate a processing outcome. The application maps the message status to its internal payment status according to implemented rules.
5. **Cancellation:** Where supported, the client requests cancellation. The platform may send `camt.056` and later receive `camt.029`. The application maps the response according to its implemented rules.
6. **Expiry:** A scheduled job may expire eligible open requests after the configured expiry rules have been satisfied.
7. **Client notification:** The platform may notify the client through an outbound webhook.
8. **Recovery and reconciliation:** Webhook processing, polling, duplicate handling, and reconciliation may update or clarify the recorded outcome.

This is the expected service flow, not a guarantee that every payment follows every stage or that every message is present in the database.

Inbound webhooks and polling are expected to use the application's shared status-application logic. Verify this in the implementation.

## 3. Identifier reference

Confirm the identifier formats and uniqueness rules against the actual application.

| Identifier  | Expected column | Format                     | Origin                         | Purpose                             |
| ----------- | --------------- | -------------------------- | ------------------------------ | ----------------------------------- |
| Internal ID | `id`            | `{{INTERNAL_ID_FORMAT}}`   | Platform database              | Internal joins                      |
| Payment ID  | `payment_id`    | `{{PAYMENT_ID_FORMAT}}`    | Platform                       | Identifier shown to clients         |
| EndToEndId  | `end_to_end_id` | `{{END_TO_END_ID_FORMAT}}` | Platform or originating system | Correlates related ISO messages     |
| ResourceID  | `resource_id`   | `{{RESOURCE_ID_FORMAT}}`   | Clearing house or scheme       | Polling or cancellation correlation |

Identifier shape is a hint, not proof of identity. Use the approved lookup query to verify a supplied value.

If no record matches, report that no match was found in the queried environment. If multiple records match, request additional information rather than choosing one arbitrarily.

Do not assume that `EndToEndId` or `ResourceID` is globally unique unless the application and scheme rules establish that property.

## 4. Table reference

The column lists below describe the expected reference model. Confirm every column and join key against database migrations, ORM entities, or schema introspection before relying on the queries.

### 4.1 `payment_request`

Expected grain: one row per payment request.

| Column                       | Meaning                                                  | Data handling                                  |
| ---------------------------- | -------------------------------------------------------- | ---------------------------------------------- |
| `id`                         | Internal primary identifier                              | Internal use                                   |
| `payment_id`                 | Client-facing payment identifier                         | May be displayed                               |
| `end_to_end_id`              | ISO message correlation identifier                       | Display only when appropriate                  |
| `resource_id`                | Clearing-house or scheme identifier                      | Display only when appropriate                  |
| `client_id`                  | Client identifier                                        | Apply access and disclosure policy             |
| `client_type`                | Client category                                          | Usually suitable for support output            |
| `amount`                     | Requested amount                                         | Financial data; disclose only when appropriate |
| `currency`                   | Currency code                                            | Usually suitable for support output            |
| `purpose`                    | Payment purpose                                          | Verify whether it contains sensitive data      |
| `status`                     | Current internal payment status                          | Interpret using the status reference           |
| `reason_code`                | Latest recorded reason code                              | Interpret using verified mappings              |
| `reason_description`         | Latest recorded reason description                       | Verify that it contains no sensitive data      |
| `http_status`                | Latest relevant HTTP status                              | Operational metadata                           |
| `need_retry`                 | Application retry indicator                              | Not proof that a retry is financially safe     |
| `bank_redirect_url`          | Redirect destination                                     | Do not expose unless required and authorized   |
| `expiry_at`                  | Request expiry timestamp                                 | Display in configured timezone                 |
| `requested_execution_at`     | Requested execution timestamp                            | Display in configured timezone                 |
| `submitted_at`               | Submission timestamp                                     | Display in configured timezone                 |
| `responded_at`               | Latest response timestamp, as defined by the application | Verify its precise meaning                     |
| `cancel_requested_at`        | Cancellation request timestamp                           | Display in configured timezone                 |
| `cancelled_by`               | Actor associated with cancellation                       | Apply disclosure policy                        |
| `debtor_identification_mode` | Identification method, such as `BANK_ACCOUNT` or `PROXY` | Operational metadata                           |
| `created_at`                 | Creation timestamp                                       | Verify in schema                               |
| `updated_at`                 | Last-update timestamp                                    | Verify what updates this field                 |
| `debtor_payload`             | Debtor-related payload                                   | **PII: never select**                          |

Add or remove columns only after checking the real schema. In particular, confirm the primary key, timestamp fields, status type, and correlation identifiers.

### 4.2 `payment_request_status_history`

Expected grain: one row per recorded status transition.

| Column               | Meaning                                                      |
| -------------------- | ------------------------------------------------------------ |
| `payment_request_id` | Reference to the associated payment request                  |
| `from_status`        | Previous status, potentially null for the initial transition |
| `to_status`          | New status                                                   |
| `trigger_source`     | Event or process that triggered the transition               |
| `reason_code`        | Recorded reason code, if present                             |
| `created_at`         | Timestamp of the history record                              |

Verify the foreign key and whether the table has a stable event identifier or sequence column. Use such a column as a secondary sort key if available.

Expected `trigger_source` values:

| Value             | Meaning                            |
| ----------------- | ---------------------------------- |
| `CLIENT_API`      | Client API activity                |
| `CANCEL_API`      | Cancellation API activity          |
| `OUTBOUND_API`    | Platform outbound request activity |
| `INBOUND_WEBHOOK` | Clearing-house webhook processing  |
| `POLL`            | Polling process                    |
| `EXPIRY_JOB`      | Expiry process                     |
| `ADMIN`           | Administrative action              |

Verify the allowed values and their exact semantics in the application.

### 4.3 `iso_message`

Expected grain: one row per recorded ISO message or message-processing record.

| Column               | Meaning                                           | Data handling                           |
| -------------------- | ------------------------------------------------- | --------------------------------------- |
| `payment_request_id` | Associated payment request                        | Verify foreign key                      |
| `msg_family`         | Message family, such as `PAIN`, `PACS`, or `CAMT` | Operational metadata                    |
| `lifecycle_step`     | Application lifecycle stage                       | Operational metadata                    |
| `tx_sts`             | Status recorded inside the ISO message            | Interpret using message-specific rules  |
| `outcome`            | Platform message-processing outcome               | Interpret using the application mapping |
| `error_code`         | Platform-side error, if present                   | Interpret using verified definitions    |
| `created_at`         | Message-record timestamp                          | Verify its exact meaning                |
| `raw_xml`            | Raw ISO XML                                       | **May contain PII: never select**       |
| `extracted_payload`  | Extracted message data                            | **May contain PII: never select**       |

Expected lifecycle steps include `SUBMIT`, `RESEND`, `BANK_RESPONSE`, `PAYMENT_STATUS`, `CANCEL_REQUEST`, and `CANCEL_RESPONSE`. Verify the actual enum and any additional values.

Expected outcomes include `BUILT`, `SENT`, `ACKED`, `RECEIVED`, `PARSED`, `APPLIED`, `FAILED`, `IGNORED_DUP`, and `UNCORRELATED`. Confirm the mapping against the code.

### 4.4 `inbound_webhook`

Expected fields:

| Column           | Meaning                      | Data handling                              |
| ---------------- | ---------------------------- | ------------------------------------------ |
| `event_key`      | Webhook deduplication key    | Do not expose unnecessarily                |
| `end_to_end_id`  | Correlation identifier       | Use according to verified uniqueness rules |
| `process_status` | Webhook processing state     | Operational metadata                       |
| `error_code`     | Processing error, if present | Use documented mappings                    |
| `created_at`     | Record creation timestamp    | Verify in schema                           |
| `processed_at`   | Processing timestamp         | Display in configured timezone             |

Expected processing statuses include `RECEIVED`, `PROCESSING`, `APPLIED`, `IGNORED_DUP`, `FAILED`, and `UNCORRELATED`. Verify actual values.

### 4.5 `client_webhook_outbound`

Expected fields:

| Column               | Meaning                                        | Data handling                       |
| -------------------- | ---------------------------------------------- | ----------------------------------- |
| `payment_request_id` | Associated payment request                     | Verify foreign key                  |
| `event_type`         | Notification type                              | Operational metadata                |
| `status_snapshot`    | Payment status represented by the notification | Not necessarily the current status  |
| `delivery_status`    | Notification delivery state                    | Interpret using application rules   |
| `attempt_count`      | Number of recorded attempts                    | Operational metadata                |
| `last_http_status`   | Most recent recorded HTTP status               | Operational metadata                |
| `last_error_code`    | Most recent notification error                 | Interpret using documented mappings |
| `created_at`         | Notification-record timestamp                  | Verify in schema                    |
| `delivered_at`       | Recorded delivery timestamp                    | Display in configured timezone      |
| `payload`            | Notification payload                           | **May contain PII: never select**   |

Expected delivery statuses include `PENDING`, `IN_FLIGHT`, `DELIVERED`, `FAILED_NO_RETRY`, and `EXHAUSTED`. Verify actual values and delivery semantics.

A recorded `DELIVERED` state does not necessarily prove that the client application processed the notification's business action.

### 4.6 `client_api_idempotency`

Expected fields:

| Column               | Meaning                                                     | Data handling                             |
| -------------------- | ----------------------------------------------------------- | ----------------------------------------- |
| `payment_request_id` | Associated payment request, if the implementation stores it | Verify relationship                       |
| `operation`          | Operation being deduplicated                                | Operational metadata                      |
| `idempotency_key`    | Request deduplication key                                   | Do not expose unnecessarily               |
| `status`             | Idempotency processing state                                | Interpret using application rules         |
| `response_code`      | Recorded response code                                      | Operational metadata                      |
| `retry_count`        | Recorded retry count                                        | Verify exact semantics                    |
| `created_at`         | Record creation timestamp, if present                       | Verify in schema                          |
| `response_data`      | Stored response                                             | Do not select; may contain sensitive data |

Verify the foreign key, uniqueness constraint, and actual column set.

## 5. Payment status reference

The following table is the proposed application-level mapping. Confirm it against the implemented enum and transition logic.

| Status                                | Proposed plain-language meaning                                            | Finality in reference model                         |
| ------------------------------------- | -------------------------------------------------------------------------- | --------------------------------------------------- |
| `PENDING`                             | Saved but not yet sent                                                     | Non-final                                           |
| `PROCESSING`                          | Request is being prepared or sent                                          | Non-final                                           |
| `SUBMITTED`                           | Submission was accepted according to the platform's recorded rule          | Non-final                                           |
| `VALIDATION_FAILED`                   | Submission failed validation                                               | Final in the reference model                        |
| `UPSTREAM_ERROR`                      | An upstream or outbound processing error occurred                          | Depends on verified recovery rules and `need_retry` |
| `INTERNAL_ERROR`                      | An internal platform error occurred                                        | Final in the reference model                        |
| `REDIRECT_READY`                      | A debtor approval step is available                                        | Non-final                                           |
| `BANK_REJECTED`                       | The bank rejected the request                                              | Final in the reference model                        |
| `PAID`                                | The application recorded its defined successful outcome                    | Final in the reference model                        |
| `FAILED`                              | The application recorded a failed outcome                                  | Final in the reference model                        |
| `CANCEL_REQUESTED`                    | A cancellation request was initiated                                       | Non-final                                           |
| `CANCELLED`                           | Cancellation was recorded as confirmed                                     | Final in the reference model                        |
| `CANCEL_REFUSED`                      | Cancellation was refused                                                   | Final in the reference model                        |
| `CANCEL_REJECTED_PAYMENT_IN_PROGRESS` | Cancellation was not accepted because payment is in progress or proceeding | Non-final in the reference model                    |
| `EXPIRED`                             | The request was marked expired by the application                          | Final in the reference model                        |

Do not interpret this table as proof of financial settlement or as a complete description of every possible scheme status. Use the implemented status mapping and scheme rules to determine the meaning of individual messages.

If a status is not documented, report it as an unknown status and request verification.

## 6. Operation gates

Populate this table from the actual application code. Do not infer allowed operations from the status names alone.

| Operation  | Allowed starting states       | Additional checks   | Source of truth          |
| ---------- | ----------------------------- | ------------------- | ------------------------ |
| Cancel     | `{{CANCEL_ALLOWED_STATUSES}}` | `{{CANCEL_GUARDS}}` | `{{CANCEL_RULE_SOURCE}}` |
| Poll       | `{{POLL_ALLOWED_STATUSES}}`   | `{{POLL_GUARDS}}`   | `{{POLL_RULE_SOURCE}}`   |
| Expiry job | `{{EXPIRY_ALLOWED_STATUSES}}` | `{{EXPIRY_GUARDS}}` | `{{EXPIRY_RULE_SOURCE}}` |

Cancellation eligibility is not a guarantee that cancellation will succeed. An expired request, a populated `end_to_end_id`, or a current status alone may not be sufficient to determine whether an operation is safe.

## 7. Reason codes

Use the application's reason-code mapping and the applicable ISO 20022 external code set or scheme rulebook.

Do not infer a code's meaning from its prefix or from a similar code. The same code may have different relevance depending on message type and scheme context.

Reference:

* Application enum or mapping source: `{{REASON_CODE_SOURCE_PATH}}`
* Applicable scheme rulebook: `{{SCHEME_RULEBOOK_REFERENCE}}`

If the mapping cannot be verified, report the raw code and state that its meaning needs confirmation.

## 8. Data interpretation safeguards

* A missing event does not prove that the event never occurred.
* A timeout does not establish whether a payment succeeded or failed.
* `need_retry` does not by itself establish financial retry safety.
* A notification delivery record does not necessarily prove business processing by the client.
* A status-history row records an application event; it may not independently establish the underlying bank or clearing-house outcome.
* Correlate records using verified keys and application rules.
* When records conflict, describe the conflict rather than choosing one without evidence.

## 9. Verification checklist

Before enabling live investigation, verify:

* Every configured value and placeholder.
* All table and column names.
* Primary keys, foreign keys, and uniqueness constraints.
* Identifier formats and correlation rules.
* Timestamp types and timezone behavior.
* Status enums, transition rules, and scheme mappings.
* Cancellation, polling, retry, and expiry gates.
* PII classification for all selected columns.
* The allowed MCP servers and database permissions.
