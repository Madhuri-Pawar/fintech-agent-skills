# Approved Payment Investigation Queries

These queries are templates for the reference data model in `data-model.md`. Verify all table names, columns, foreign keys, data types, and parameter-binding behavior against the actual database before use.

Use only the permitted, read-only database environment configured in `data-model.md`.

## Query rules

* Bind user inputs as query parameters.
* Use the configured schema. Do not accept a schema name from the user.
* Select only the columns required for the investigation.
* Never use `SELECT *`.
* Never select raw XML, debtor payloads, extracted payloads, webhook payloads, or idempotency response data.
* Limit returned rows to 50 or fewer unless an approved bounded query explicitly needs a different limit.
* If the identifier lookup returns multiple records, stop and resolve the ambiguity before running a journey query.
* If a required column or relationship is absent, do not improvise a replacement. Verify the schema and update this reference.
* Do not execute write operations or queries with side effects.

## 1. Resolve a supplied identifier

Purpose: identify a payment when the user supplies an internal ID, Payment ID, EndToEndId, or ResourceID.

Parameter: `:x` — the supplied identifier.

```sql
SELECT
    pr.id,
    pr.payment_id,
    pr.end_to_end_id,
    pr.resource_id,
    pr.status
FROM {{SCHEMA}}.payment_request AS pr
WHERE pr.id::text = :x
   OR pr.payment_id = :x
   OR pr.end_to_end_id = :x
   OR pr.resource_id = :x
LIMIT 2;
```

Interpretation:

* Zero rows: no matching record was found in the queried environment.
* One row: use the verified internal ID for subsequent queries.
* Two rows: the lookup may be ambiguous. Do not select one arbitrarily; ask for another identifier or clarification.

The limit of two rows is intentional: it allows the assistant to detect that more than one record matched without returning a large result set.

Verify the column types and comparison behavior in the actual schema. If the database uses different identifier types or comparison rules, adapt this query using safe parameter binding.

## 2. Look up one payment

Purpose: retrieve the current recorded status and relevant non-PII details.

Parameter: `:payment_id` — a verified Payment ID.

```sql
SELECT
    pr.payment_id,
    pr.status,
    pr.amount,
    pr.currency,
    pr.client_type,
    pr.reason_code,
    pr.reason_description,
    pr.need_retry,
    pr.created_at,
    pr.submitted_at,
    pr.responded_at,
    pr.expiry_at,
    pr.cancelled_by
FROM {{SCHEMA}}.payment_request AS pr
WHERE pr.payment_id = :payment_id
LIMIT 1;
```

Do not use this query until the supplied value has been verified as a Payment ID. Use the identifier-resolution query first when the identifier type is unknown.

## 3. Read payment status history

Purpose: show recorded status transitions for one verified payment.

Parameter: `:payment_request_id` — the verified internal payment ID.

```sql
SELECT
    h.created_at,
    h.from_status,
    h.to_status,
    h.trigger_source,
    h.reason_code
FROM {{SCHEMA}}.payment_request_status_history AS h
WHERE h.payment_request_id = :payment_request_id
ORDER BY h.created_at ASC
LIMIT 50;
```

This returns up to 50 chronological records. If there are more than 50, the query may omit later transitions. Check whether additional records exist before claiming that the final event is known.

If the schema provides a stable history ID or sequence number, use it as a secondary sort key when timestamps are equal.

## 4. Check client notification records

Purpose: inspect the platform's recorded attempts to notify the client.

Parameter: `:payment_request_id` — the verified internal payment ID.

```sql
SELECT
    o.created_at,
    o.event_type,
    o.status_snapshot,
    o.delivery_status,
    o.attempt_count,
    o.last_http_status,
    o.last_error_code,
    o.delivered_at
FROM {{SCHEMA}}.client_webhook_outbound AS o
WHERE o.payment_request_id = :payment_request_id
ORDER BY o.created_at DESC
LIMIT 20;
```

Interpretation:

* `DELIVERED` means the platform recorded successful delivery according to its implementation.
* Failed or exhausted delivery attempts may require investigation by the team responsible for client notifications.
* No matching row means no notification record was found in this table. It does not prove that no notification was sent through any other mechanism.
* A delivery record does not necessarily prove that the client processed the notification successfully.

Verify the actual delivery-state semantics before presenting a definitive conclusion.

## 5. Count requests created on a specified day

Purpose: count payment requests by their current recorded status, grouped by the day on which the requests were created.

Parameters:

* `:day` — the requested calendar date.
* `{{TIMEZONE}}` — the configured timezone.

```sql
SELECT
    pr.status,
    count(*) AS request_count
FROM {{SCHEMA}}.payment_request AS pr
WHERE pr.created_at >= (
    :day::date::timestamp AT TIME ZONE '{{TIMEZONE}}'
)
  AND pr.created_at < (
    (:day::date + 1)::timestamp AT TIME ZONE '{{TIMEZONE}}'
)
GROUP BY pr.status
ORDER BY request_count DESC
LIMIT 50;
```

Describe this metric as "current status of requests created on the specified day." Do not describe it as the number of payments that became paid or failed on that day.

Confirm that `created_at` is `timestamptz` and that the timezone configuration is valid.

## 6. Count status transitions recorded on a specified day

Purpose: count recorded transitions into selected outcome statuses during a calendar day.

Parameters:

* `:day` — the requested calendar date.
* `{{TIMEZONE}}` — the configured timezone.

```sql
SELECT
    h.to_status,
    count(*) AS transition_count
FROM {{SCHEMA}}.payment_request_status_history AS h
WHERE h.created_at >= (
    :day::date::timestamp AT TIME ZONE '{{TIMEZONE}}'
)
  AND h.created_at < (
    (:day::date + 1)::timestamp AT TIME ZONE '{{TIMEZONE}}'
)
  AND h.to_status IN ('PAID', 'FAILED', 'EXPIRED')
GROUP BY h.to_status
ORDER BY transition_count DESC
LIMIT 50;
```

This query counts status-history transitions, not necessarily unique payment requests. Use a distinct-payment metric only when the business definition requires it and the query explicitly implements it.

The selected statuses must be confirmed against the application's status enum.

## 7. Find potentially stalled requests

Purpose: identify open requests that have not been updated recently.

Parameter:

* `:stale_hours` — an approved threshold supplied by the application or operator.

```sql
SELECT
    pr.payment_id,
    pr.status,
    pr.created_at,
    pr.updated_at,
    pr.responded_at,
    pr.expiry_at
FROM {{SCHEMA}}.payment_request AS pr
WHERE pr.status IN (
    'PENDING',
    'PROCESSING',
    'SUBMITTED',
    'REDIRECT_READY',
    'CANCEL_REQUESTED'
)
  AND pr.updated_at < now() - (
      :stale_hours * interval '1 hour'
  )
ORDER BY pr.updated_at ASC
LIMIT 50;
```

Use only a validated, bounded numeric parameter for `:stale_hours`. The application should define an acceptable range.

Describe these as potentially stalled requests, not confirmed failures. Verify that `updated_at` changes reliably for the processing events relevant to the investigation.

Expiry should be assessed separately using the implemented expiry rules, including the configured safety margin.

## 8. Summarize recent failure-related transitions

Purpose: count status transitions into selected failure-related statuses recorded during the last seven days.

```sql
SELECT
    h.to_status,
    h.reason_code,
    count(*) AS transition_count
FROM {{SCHEMA}}.payment_request_status_history AS h
WHERE h.created_at >= now() - interval '7 days'
  AND h.to_status IN (
      'VALIDATION_FAILED',
      'BANK_REJECTED',
      'FAILED',
      'INTERNAL_ERROR'
  )
GROUP BY h.to_status, h.reason_code
ORDER BY transition_count DESC
LIMIT 30;
```

This is a transition report. It is not a count of unique payments unless explicitly changed to count distinct payment IDs.

`UPSTREAM_ERROR` is intentionally excluded from the final-failure category because the reference model says its finality depends on additional recovery rules. If upstream incidents are being measured, report them separately and do not automatically label them final payment failures.

Verify that the selected statuses and reason-code field match the actual history table.

## 9. Find inbound webhook processing problems

Purpose: inspect inbound webhook records that were recorded as failed or uncorrelated.

```sql
SELECT
    w.created_at,
    w.end_to_end_id,
    w.process_status,
    w.error_code,
    w.processed_at
FROM {{SCHEMA}}.inbound_webhook AS w
WHERE w.process_status IN ('FAILED', 'UNCORRELATED')
ORDER BY w.created_at DESC
LIMIT 50;
```

This is an environment-wide operational query. Use it only for an authorized operational investigation. Apply an approved date or identifier filter when the question is about a particular payment or period.

A failed or uncorrelated webhook record does not by itself establish the payment's final financial outcome.

## 10. Investigate ISO message errors

Purpose: inspect non-sensitive ISO message metadata for a verified payment.

Parameter: `:payment_request_id` — the verified internal payment ID.

```sql
SELECT
    m.created_at,
    m.msg_family,
    m.lifecycle_step,
    m.tx_sts,
    m.outcome,
    m.error_code
FROM {{SCHEMA}}.iso_message AS m
WHERE m.payment_request_id = :payment_request_id
  AND (
      m.error_code IS NOT NULL
      OR m.outcome IN ('FAILED', 'UNCORRELATED', 'IGNORED_DUP')
  )
ORDER BY m.created_at DESC
LIMIT 30;
```

Interpret errors using documented platform mappings. Do not infer the meaning of an ISO status from its code alone without checking the message type, scheme rules, and application mapping.

## 11. Full payment journey

Purpose: reconstruct the recorded journey of one verified payment from the client API through platform processing, clearing-house interactions, and client notification.

First run the identifier-resolution query in section 1. If it returns exactly one record, pass that record's internal ID as `:payment_request_id`.

The query below uses only explicit columns. Confirm all listed fields and join relationships against the real schema. In particular, confirm that `client_api_idempotency.payment_request_id` exists and that joining inbound webhooks by `end_to_end_id` cannot incorrectly associate another payment's events.

```sql
WITH pr AS (
    SELECT
        p.id,
        p.payment_id,
        p.end_to_end_id,
        p.amount,
        p.currency,
        p.status,
        p.created_at
    FROM {{SCHEMA}}.payment_request AS p
    WHERE p.id = :payment_request_id
    LIMIT 1
),
all_events AS (
    SELECT
        p.created_at AS event_time,
        '1 Client -> Platform'::text AS stage,
        'Request recorded'::text AS step,
        concat_ws(' ', p.amount::text, p.currency) AS detail
    FROM pr AS p

    UNION ALL

    SELECT
        i.created_at AS event_time,
        '1 Client -> Platform'::text AS stage,
        concat('API operation: ', i.operation::text) AS step,
        concat_ws(
            ' ',
            i.status::text,
            CASE
                WHEN i.response_code IS NOT NULL
                THEN concat('HTTP ', i.response_code::text)
            END
        ) AS detail
    FROM {{SCHEMA}}.client_api_idempotency AS i
    JOIN pr AS p
      ON p.id = i.payment_request_id

    UNION ALL

    SELECT
        h.created_at AS event_time,
        'Status history'::text AS stage,
        concat(
            coalesce(h.from_status::text, '(initial)'),
            ' -> ',
            h.to_status::text
        ) AS step,
        concat_ws(
            ' ',
            h.trigger_source::text,
            CASE
                WHEN h.reason_code IS NOT NULL
                THEN concat('Reason: ', h.reason_code::text)
            END
        ) AS detail
    FROM {{SCHEMA}}.payment_request_status_history AS h
    JOIN pr AS p
      ON p.id = h.payment_request_id

    UNION ALL

    SELECT
        m.created_at AS event_time,
        CASE
            WHEN m.lifecycle_step IN (
                'SUBMIT',
                'RESEND',
                'CANCEL_REQUEST'
            )
            THEN '2 Platform -> Clearing'
            ELSE '3 Clearing -> Platform'
        END::text AS stage,
        concat(
            m.lifecycle_step::text,
            CASE
                WHEN m.tx_sts IS NOT NULL
                THEN concat(' (', m.tx_sts::text, ')')
            END
        ) AS step,
        concat_ws(
            ' ',
            m.outcome::text,
            CASE
                WHEN m.error_code IS NOT NULL
                THEN concat('Error: ', m.error_code::text)
            END
        ) AS detail
    FROM {{SCHEMA}}.iso_message AS m
    JOIN pr AS p
      ON p.id = m.payment_request_id

    UNION ALL

    SELECT
        w.created_at AS event_time,
        '3 Clearing -> Platform'::text AS stage,
        'Inbound webhook'::text AS step,
        concat_ws(
            ' ',
            w.process_status::text,
            CASE
                WHEN w.error_code IS NOT NULL
                THEN concat('Error: ', w.error_code::text)
            END
        ) AS detail
    FROM {{SCHEMA}}.inbound_webhook AS w
    JOIN pr AS p
      ON p.end_to_end_id = w.end_to_end_id

    UNION ALL

    SELECT
        o.created_at AS event_time,
        '4 Platform -> Client'::text AS stage,
        concat('Notify status: ', o.status_snapshot::text) AS step,
        concat_ws(
            ' ',
            o.delivery_status::text,
            concat('Attempts:', o.attempt_count::text),
            CASE
                WHEN o.last_http_status IS NOT NULL
                THEN concat('HTTP ', o.last_http_status::text)
            END,
            CASE
                WHEN o.last_error_code IS NOT NULL
                THEN concat('Error: ', o.last_error_code::text)
            END
        ) AS detail
    FROM {{SCHEMA}}.client_webhook_outbound AS o
    JOIN pr AS p
      ON p.id = o.payment_request_id
),
latest_events AS (
    SELECT
        event_time,
        stage,
        step,
        detail
    FROM all_events
    ORDER BY event_time DESC NULLS LAST
    LIMIT 100
)
SELECT
    to_char(
        e.event_time AT TIME ZONE '{{TIMEZONE}}',
        'YYYY-MM-DD HH24:MI:SS'
    ) AS event_time_local,
    e.stage,
    e.step,
    e.detail
FROM latest_events AS e
ORDER BY e.event_time ASC NULLS LAST, e.stage ASC
LIMIT 100;
```

### Journey-query limitations

* The query returns at most 100 events. If older events were omitted, disclose that fact.
* It orders events by timestamp. Equal timestamps may not reflect the true processing order; use a verified sequence or event identifier when available.
* It does not prove that every stage was recorded or that a missing stage never occurred.
* The inbound webhook join depends on the verified correlation rules for `end_to_end_id`.
* The stage labels are reporting categories. They are not proof that a clearing-house message was successfully processed.
* If the payment cannot be resolved uniquely, do not run this query.

## 12. Query-to-question map

| User question                                              | Approved query or evidence |
| ---------------------------------------------------------- | -------------------------- |
| What is the current status?                                | Sections 1 and 2           |
| What status changes occurred?                              | Section 3                  |
| Was the client notified?                                   | Section 4                  |
| How many requests were created that day by current status? | Section 5                  |
| How many selected status transitions occurred that day?    | Section 6                  |
| Which requests may be stalled?                             | Section 7                  |
| What failure-related transitions were recorded recently?   | Section 8                  |
| Were inbound webhook records unsuccessful?                 | Section 9                  |
| Were ISO message errors recorded?                          | Section 10                 |
| What happened throughout the payment journey?              | Section 11                 |

If a question does not fit an approved query, identify the missing information and request a reviewed query rather than inventing a new schema or unsafe SQL.
