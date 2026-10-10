# PostgreSQL database investigation

## Purpose

Use the configured PostgreSQL MCP server only when database evidence can verify a hypothesis. This reference is not required for frontend-only investigations, and it is not required for a backend investigation until the code shows that database evidence is needed.

The environment is not fixed in this plugin. It is the server the user's MCP configuration connected: local, stage, or production. Discover that from the available server, then report it. Do not prefer or reject an environment because of its name.

If no PostgreSQL MCP connection is configured, continue with Jira and repository evidence. Report database verification as unavailable when it would have mattered.

Database access supplements Jira and repository investigation. Do not assume database evidence alone proves an incident's cause. Read-only access must be enforced by the database account. Do not rely only on these instructions to prevent writes.

## 1. Discover and verify access

- Discover the database MCP tools actually available in the current session.
- Confirm the connected database and environment using the available connection metadata or safe, read-only queries.
- Identify the connected server and the environment it represents. Record that in the report.
- If the environment cannot be identified, state that it is unknown. Do not label it local, stage, or production from guesswork.
- Never assume tool names, permissions, schemas, tables, or columns.
- Use only the connected database server. Do not create a new connection or switch to another environment.

## 2. Enforce read-only access

- Use a database account that has SELECT-only access to the minimum required schemas and tables on the connected server.
- Never execute INSERT, UPDATE, DELETE, MERGE, TRUNCATE, DDL, stored procedures with side effects, migrations, or other write-capable operations.
- Do not change database settings, permissions, roles, extensions, or connection configuration.
- Do not assume that starting a read-only transaction makes an otherwise privileged connection safe.
- If a tool can execute arbitrary SQL, restrict usage to reviewed, read-only queries and verify that the server and database permissions enforce the intended restrictions.

## 3. Investigate only relevant data

- First inspect the relevant schema, table definitions, indexes, constraints, and relationships.
- Derive candidate queries from inspected application code, ORM mappings, SQL statements, migrations, and business rules.
- Use narrowly scoped SELECT queries with explicit columns and restrictive predicates.
- Apply row limits and reasonable query timeouts where supported.
- Avoid SELECT *, unbounded scans, sensitive columns, and unnecessary access to personal or financial data.
- Do not expose credentials, tokens, secrets, or unnecessary customer data in the report.
- Do not treat rows from the connected environment as proof of a different environment.

## 4. Verify database hypotheses

- Check whether relevant rows, relationships, status values, null values, or duplicates support the current hypothesis.
- Inspect constraints, indexes, transaction boundaries, and query behavior when relevant to the issue.
- Consider concurrent writes, isolation, retries, and idempotency where the evidence suggests these risks.
- Compare database observations with the application code and Jira's expected behavior.
- Treat missing rows as inconclusive when the affected scenario cannot be reproduced on the connected server.
- Do not infer another environment's row state, performance, or incident cause from this connection.

## 5. Handle query failures safely

- If access is denied, a query times out, or required data is unavailable, report the limitation.
- Do not bypass permissions, broaden access, or switch servers to complete the investigation.
- Do not repeatedly execute expensive queries.
- If a query could be costly or its behavior is uncertain, inspect the query and available schema information before proceeding.

## 6. Report findings

- Include database findings only when they materially affect the investigation.
- In the DB section, state the required schema, constraint, index, or data change—or `none` if no database change is needed.
- In Code, include only database-related source or migration files that were actually opened and require changes.
- Put necessary migrations, backfills, data prerequisites, and dependent files under Depends on.
- Name the MCP server and environment the observations came from. Separate those observations from assumptions about any other environment.
- Do not claim a query ran unless it actually ran, and do not claim the proposed fix is verified unless the relevant validation was performed.

## 7. Maintain the investigation boundary

- Investigation is read-only by default.
- Do not modify application code, database rows, schemas, permissions, Jira, infrastructure, or deployments.
- A request to investigate or recommend a fix does not authorize implementation.
- If a write operation is needed for remediation, describe the proposed action and leave execution to an explicitly authorized workflow.