# Fintech Agent Skills

Claude Code plugins and skills for fintech engineering work: investigating Jira production issues, reviewing payment code, and analyzing payment requests.

| Project | Type | What it does |
| --- | --- | --- |
| [jira-assistant-plugin](jira-assistant-plugin/) | Claude Code plugin | Investigates Jira issues by correlating ticket context, repository code, commit history, and runtime evidence to identify the root cause and recommend a fix. |
| [payment-code-reviewer](payment-code-reviewer/) | Claude skill | Reviews payment-related code for correctness, potential defects, edge cases, and payment-flow risks such as duplicate charges, idempotency, and webhook handling. |
| [payment-request-assistant](payment-request-assistant/) | Claude skill | Answers questions about ISO 20022 Request-to-Pay payments (status, failures, cancellations, journeys, counts) using read-only SQL. |

## Why I built this

Diagnosing a production payment issue usually means jumping between the Jira ticket, the code, git history, logs, and the database. Reviewing payment code means checking for the same costly mistakes every time: duplicate charges, lost idempotency, ambiguous provider timeouts. These projects encode that work as reusable AI workflows so the investigation is faster, consistent, and grounded in evidence.

## Tech stack

Claude Code plugins and Agent Skills · Model Context Protocol (MCP): Jira, PostgreSQL, GitHub, and observability servers · ISO 20022 (pain.013, pain.014, pacs.002, camt.056, camt.029) · NestJS / TypeScript payment APIs · PostgreSQL · Python (plugin validation)

## Key features

- **Evidence over guesses.** Each finding is tied to a file and line, a Jira field, a commit, or a query result, and is labeled as confirmed, likely, or needing verification.
- **Payment-aware.** Checks target fintech failure modes: duplicate charges, idempotency, ambiguous provider timeouts, webhook replay, state transitions, reconciliation, and ISO 20022 reason codes.
- **Read-only by default.** No code, Jira, or database changes during an investigation or review.
- **Works with your existing tools.** Uses the Jira, PostgreSQL, GitHub, and observability MCP connections you already have. It ships no credentials.
- **Tested.** Each project includes test scenarios with expected findings and checks that guard against false positives.

## Install

The Jira plugin installs through this repository's plugin marketplace. Run these inside Claude Code:

```text
/plugin marketplace add Madhuri-Pawar/fintech-agent-skills
/plugin install jira-assistant-plugin@fintech-agent-skills
```

The two payment skills install as standalone skills. Copy the skill directory into your skills folder (for example `~/.claude/skills/` or a project's `.claude/skills/`):

- `payment-code-reviewer/` (the directory that contains `SKILL.md`)
- `payment-request-assistant/payment-request-assistant/` (then follow [SETUP.md](payment-request-assistant/SETUP.md))

## Examples

```text
# Investigate a production issue
/jira-assistant-plugin:issue-investigator PAY-123

# Review a payment change
Review this refund endpoint for authorization, refundable balance, idempotency and concurrent requests.

# Ask about a payment request
Why did payment E2E-20260310-0042 fail, and can it still be cancelled?
```

The Jira plugin's report covers business impact, the execution flow, findings for each affected layer, the root cause with a confidence level, the recommended fix and alternatives, regression tests, and a rollout and rollback plan.

## Running the tests

```bash
# Structural validation of the Jira plugin (manifest, skill metadata, references)
python jira-assistant-plugin/tests/validate_plugin.py

# Load the plugin locally without installing it
claude --plugin-dir ./jira-assistant-plugin
```

Behavioral test scenarios and expected findings are in:

- [jira-assistant-plugin/tests/](jira-assistant-plugin/tests/)
- [payment-code-reviewer/test/](payment-code-reviewer/test/)
- [payment-request-assistant/SETUP.md](payment-request-assistant/SETUP.md) (synthetic-record test cases, section 6)

## Safety

All three are read-only by default. They do not modify code, Jira issues, or payment data, and they report missing evidence instead of guessing. Database and observability access come from your own MCP configuration; no credentials are stored in this repository.

## Author

**Madhuri Pawar** · [github.com/Madhuri-Pawar](https://github.com/Madhuri-Pawar)

## License

MIT. Each project includes its own `LICENSE` file.
