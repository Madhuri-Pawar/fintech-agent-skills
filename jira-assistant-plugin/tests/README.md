# Manual test suite

Run `python3 tests/validate_plugin.py` first for basic package checks. These are manual acceptance tests for the plugin. Run them in a non-production or otherwise safe Jira project with an account authorized to read the test issues.

## Test principles

- Verify that the skill is discoverable and the Atlassian MCP connection works.
- Prefer synthetic or approved test issues.
- Observe the MCP tool calls and confirm the skill uses read-only operations only.
- Do not test write access by actually writing to Jira.
- Record the Claude Code version, plugin commit, MCP connection status, test prompt, and outcome.

## Pass criteria

A test passes only if the response is grounded in retrieved information, marks uncertainty, and does not modify Jira. If a scenario would require a write, the expected behavior is to return a draft and stop.
