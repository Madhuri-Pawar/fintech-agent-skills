# Issue Investigation

## 1. Executive Summary

- Jira issue:
- Summary:
- Business impact:
- Root-cause status: CONFIRMED / PROBABLE / UNDETERMINED
- Main finding:
- Recommended approach:

## 2. Jira Context

- Expected behavior:
- Actual behavior:
- Environment (local / stage / production, from the connected MCP server) and version:
- Reproduction:
- Scope and frequency:
- Relevant comments, history and linked issues:
- Missing or conflicting information:

## 3. System and Execution Flow

Describe only the architecture and path supported by inspected evidence.

Trigger -> relevant components -> dependencies/data -> observed symptom

## 4. Findings by Layer

Include relevant layers only.

### Frontend (FE)

- Status: Implicated / Ruled out / Unverified / Not applicable
- Files and symbols:
- Line ranges, if verified:
- Observed behavior:
- Evidence:
- Required change, if justified:

### Backend (BE)

- Status:
- Service, endpoint and symbols:
- Files and line ranges:
- Observed behavior:
- Evidence:
- Required change:

### Database (DB)

- Status:
- Schema, query, transaction or migration:
- Files and line ranges:
- Observed behavior:
- Evidence:
- Required change:

### Other layers

Use as needed for queues, cache, integrations, authentication,
configuration, infrastructure, networking or business rules.

## 5. Root-Cause Analysis

- Primary cause or leading hypothesis:
- Confidence/status:
- Trigger and preconditions:
- Faulty mechanism:
- Causal chain:
- Contributing factors:
- Evidence supporting the cause:
- Evidence against or not yet available:
- Checks needed to confirm or falsify it:

## 6. Recommended Solution

- Preferred approach:
- Why it is preferred:
- Business correctness:
- Technical design:
- Performance and scale:
- Security and data integrity:
- Reliability and maintainability:
- Alternatives considered:
- Risks and mitigations:

## 7. Implementation Plan

For each step specify:
- Order
- File/module or schema involved
- Intended change
- Reason
- Dependencies
- Verification

Use actual repository paths only when inspected. Mark paths not yet identified.

## 8. Testing and Acceptance Criteria

- Regression tests:
- Unit/integration/contract/E2E tests:
- Negative and boundary cases:
- Performance/concurrency checks:
- Observable success criteria:
- Actual tests run and results, if any:

## 9. Rollout and Recovery

- Deployment considerations:
- Monitoring:
- Rollback trigger:
- Rollback strategy:
- Data recovery concerns:

## 10. Remaining Unknowns

List each unresolved question, why it matters, and the next evidence
needed to resolve it.

## 11. Conclusion

State the best next action. Do not claim a fix is implemented or verified
unless it actually has been.