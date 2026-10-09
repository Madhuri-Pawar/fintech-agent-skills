# Skill Evaluation Tests

These tests evaluate whether `payment-code-reviewer` selects relevant checks dynamically, detects real defects, and avoids unsupported findings.

## Files

- `test-cases.md`: fictional scenarios to review
- `expected-findings.md`: expected results and false-positive constraints
- `prompt.md`: reusable evaluation prompts

## Manual evaluation

1. Load the skill into your Claude environment.
2. Start a fresh conversation.
3. Choose a test case from `test-cases.md`.
4. Use a matching prompt from `prompt.md`.
5. Provide the scenario without revealing the expected answer first.
6. Record the skill's findings.
7. Compare the results with `expected-findings.md`.
8. Repeat with a valid implementation to test false-positive resistance.



## Scoring

Score each criterion from 0 to 2:

- Correct business-flow selection
- Detection of the expected defect
- Evidence and impact quality
- Actionable remediation and test advice
- Avoidance of unsupported findings

Maximum score: 10 per scenario.

Record missed defects and false positives separately. A high numerical score does not compensate for a critical missed finding.

## Limitations

These are manual evaluation fixtures, not an automated test suite. Model responses can vary. Evaluate the correctness of the reasoning and findings rather than requiring exact wording.

Do not use live payment environments, real credentials, or production customer data for these evaluations.