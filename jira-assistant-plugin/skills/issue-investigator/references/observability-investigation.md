# Observability and third-party runtime investigation

## Purpose

Use authorized observability and third-party integrations only when runtime evidence can verify a hypothesis. Jira and repository inspection come first. This reference is not required for every ticket.

The plugin defines how to investigate. MCP servers and other authorized integrations provide access to external systems. A server entry in MCP configuration does not by itself explain how to interpret the data.

If a needed integration is not configured, continue with Jira and repository evidence. Report that runtime verification was unavailable when it would have mattered. Do not claim a tool was queried when it was unavailable or the query failed.

## Possible connections

Use only tools discovered in the current session. Do not assume a platform, tool name, permission, or schema exists.

- SigNoz: logs, metrics, and traces. Find failing requests, correlate trace IDs, inspect latency, identify erroring services, and examine dependency calls.
- GitHub: source, pull requests, commits, reviews, and related changes that may explain a regression. Repository access in the session may already cover the current checkout.
- Grafana: metrics and dashboards. Check latency, error rates, resource usage, saturation, and service health.
- Sentry: exceptions and stack traces. Investigate recurring errors, affected releases, stack traces, and error frequency.
- Database and cloud platforms: authorized, preferably read-only access to query performance, schema, locks, deployment events, and infrastructure health. Database queries also follow references/database-investigation.md.

Whether a platform can be used depends on the available server, API, authentication method, and permissions.

## When to load this reference

- Frontend-only issues that are fully explained by inspected UI code do not need logs or traces.
- Backend or API issues start in application code. Load runtime evidence when a hypothesis needs a failing request, latency, error rate, or dependency call.
- Incidents in any environment with intermittent failures, timeouts, or errors after a deploy should use available traces, logs, metrics, and deployment history.
- If no observability MCP is configured, name the missing evidence and continue.

## How to correlate evidence

Start from the incident's time window, environment, affected service, and request or trace identifiers.

1. Read the Jira issue for the workflow, time, and identifiers.
2. Trace the relevant code path in the repository.
3. Query only relevant logs, traces, and metrics. Correlate results by timestamp and service.
4. Trace failures across service boundaries. Distinguish an upstream failure from a downstream symptom.
5. Compare the incident period with a healthy baseline when that data is available.
6. Check deployment or configuration changes. Timing is a clue, not proof.
7. Use database or cloud tools only when the hypothesis needs them, and only with the authorized read-only connection.

For example, a trace that slows on a database span and a repository query that matches that span are two observations. Correlate timestamps and trace evidence before concluding that the query caused the incident.

## Rules

- Treat third-party results as evidence, not unquestionable truth.
- Report the source of each finding. Separate observed facts from hypotheses.
- Never claim a tool was queried when it was not available or the query failed.
- Default to read-only access. Require explicit approval for remediation, configuration changes, or writes to any environment.
- Use least-privilege credentials. Keep secrets in environment variables or the approved secret manager. Do not grant broad write access in any environment to an investigation agent.
- Do not invent trace IDs, log lines, dashboard values, release events, or stack traces.
- Credentials and environment-specific settings stay outside the repository. Document the connection name; do not commit secrets.
