# Setup: Payment Request Assistant

This guide describes how to configure the payment-request-assistant skill for a PostgreSQL database accessed through an approved MCP server.

The skill files alone do not create a database connection. The host application must support loading skills, and a PostgreSQL MCP server must be separately configured.

## 1. Check the project structure

The project should contain:

```text
payment-request-assistant/          # project root
├── README.md
├── SETUP.md
└── payment-request-assistant/      # the skill directory you install
    ├── SKILL.md
    └── references/
        ├── data-model.md
        └── queries.md
```

Install the inner `payment-request-assistant/` directory as the skill. Confirm that the filenames and directory names match the links and paths in `SKILL.md`.

## 2. Verify the database schema

Before enabling live queries:

1. Compare the documented tables and columns with the actual database schema.
2. Verify primary keys, foreign keys, identifier uniqueness, and timestamp types.
3. Confirm the payment status enum and message-to-status mappings.
4. Confirm the cancellation, polling, retry, and expiry rules from the application code.
5. Identify every PII or sensitive field that the assistant must not query.
6. Confirm the approved parameter-binding syntax for the chosen MCP server.

Update `references/data-model.md` and `references/queries.md` to match the verified implementation.

Do not use example table definitions as a substitute for schema verification.

## 3. Configure the MCP server

Configure a PostgreSQL MCP server using your organization's approved process.

Verify that:

* The server connects to the intended non-production environment.
* The server name exactly matches an entry in `data-model.md`.
* The database account has read-only permissions.
* The account cannot write to tables, execute unsafe functions, or bypass environment restrictions.
* Network and database access controls prevent production access.
* Query execution is parameterized and subject to appropriate timeouts and resource limits.

Do not put passwords, connection strings, tokens, or secrets in the skill files.

A server being connected does not make it an allowed server. The skill must use only an explicitly permitted environment.

## 4. Complete the configuration placeholders

In `references/data-model.md`, replace:

* `{{SCHEMA}}` with the verified PostgreSQL schema.
* `{{TIMEZONE}}` with the timezone used in reports.
* `{{ALLOWED_MCP_SERVERS}}` with the exact permitted MCP server names.
* `{{FORBIDDEN_ENVIRONMENTS}}` with the environments the assistant must never access.
* `{{EXPIRY_MARGIN}}` and `{{MAX_EXPIRY_DAYS}}` with the actual expiry configuration.
* The source-path placeholders with verified paths to the entities, status mappings, and operation rules.
* The identifier-format placeholders with the actual documented formats.
* The operation-gate placeholders with rules confirmed from the code.

Do not invent values to make the configuration look complete.

## 5. Validate the SQL

Before connecting the skill to operational data:

1. Verify that every table and column referenced by a query exists.
2. Verify that every join uses the correct relationship.
3. Confirm that user input is passed as a bound parameter, not concatenated into SQL.
4. Confirm that every query selects only approved fields.
5. Confirm that row limits and date ranges behave as expected.
6. Check timezone boundaries, including daylight-saving changes where relevant.
7. Test ambiguous identifiers and missing records.
8. Verify that journey queries do not silently omit the newest events.
9. Confirm that query execution is restricted to approved read-only operations.

If a query fails because the schema differs from the reference model, fix the documentation or query using the actual schema. Do not guess a replacement column.

## 6. Test with synthetic records

Use a test database with fabricated identifiers and no real customer information.

Test at least these cases:

* A payment that is successfully recorded.
* A request rejected during validation.
* An upstream timeout with an uncertain outcome.
* A delayed inbound webhook.
* A webhook that is uncorrelated or fails processing.
* A client notification that fails delivery.
* A cancellation request awaiting a response.
* An expired payment request.
* An unknown identifier.
* An identifier that matches multiple records.
* A request with more than 100 journey events.

For each case, verify both the SQL result and the assistant's explanation.

The assistant must not invent missing events, treat an uncertain outcome as a confirmed failure, or recommend an unsafe retry.

## 7. Operational acceptance criteria

The skill is ready for a controlled pilot only after the team verifies that:

* The correct skill is loaded for relevant payment questions.
* The permitted database is selected correctly.
* Read-only access is enforced outside the prompt.
* The query references match the actual schema.
* PII and raw payloads are excluded.
* Status and reason-code explanations match the implementation.
* The assistant distinguishes facts, hypotheses, and unknowns.
* Test cases pass consistently.
* Production access remains prohibited.

Record the schema version, application version, test date, and person or team that approved the configuration.

## 8. Troubleshooting

**The assistant cannot find the reference files**

Check the skill directory layout and confirm that the host application loads the skill from the expected location.

**The assistant cannot connect to PostgreSQL**

Verify the MCP server configuration, connection permissions, and server name. Do not ask the assistant to guess connection settings.

**A query fails with a missing-column error**

Compare the query with the real schema and update the documentation. Do not replace the missing column with an assumed equivalent.

**The assistant reports the wrong status meaning**

Check the application's enum, transition logic, message mapping, and scheme-specific rules. Update the reference material and add a regression test.

**The assistant claims a payment failed after a timeout**

Add a test requiring it to distinguish an unknown outcome from a confirmed failure. Check the relevant message, webhook, polling, and reconciliation evidence before recommending further action.
