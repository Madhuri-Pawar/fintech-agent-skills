# Finding Format

Use a consistent, evidence-based structure for review findings.

## Finding template

### [Severity] Concise title

* **Confidence:** Confirmed / Likely / Needs verification
* **Business flow:** The payment or integration operation affected
* **Location:** File, function, endpoint, or code path when available
* **Evidence:** The observed code or behavior and any relevant requirement
* **Impact:** The realistic consequence
* **Recommendation:** A specific remediation
* **Regression test:** A focused test that prevents recurrence

## Severity guidance

### Critical

A severe, credible risk of major financial compromise, broad unauthorized control, or comparable impact. Reserve this level for situations with strong evidence and substantial impact.

### High

A significant security or correctness defect that could enable unauthorized financial operations, material data exposure, or serious payment inconsistency.

### Medium

A meaningful but more limited defect, such as a narrower authorization gap, unreliable recovery path, or duplicate-operation risk with mitigating controls.

### Low

A limited-impact defect or weakness with constrained consequences.

### Informational

A useful observation, hardening opportunity, or non-defect recommendation. Do not inflate informational advice into a vulnerability.

Severity depends on impact, exploitability, exposure, and existing mitigations. Do not assign severity based solely on the category of the issue.

## Confidence guidance

* **Confirmed:** The defect is directly supported by inspected code, reproducible behavior, or authoritative supplied requirements.
* **Likely:** Evidence strongly suggests the defect, but one material detail remains unverified.
* **Needs verification:** A relevant risk exists, but configuration, shared controls, provider requirements, or runtime behavior cannot be confirmed.

## Evidence rules

* Cite the actual code path or behavior whenever possible.
* Check shared middleware, guards, service layers, and configuration before reporting a missing control.
* Do not invent file names, line numbers, provider requirements, or runtime results.
* If evidence is incomplete, state exactly what is missing.
* Avoid duplicate findings describing the same root cause.

## Recommendation rules

A useful recommendation should explain what control or behavior needs to change. Prefer a focused fix over a broad rewrite.

Suggest a regression test that exercises the failure scenario and verifies the expected business invariant.

## Review summary

At the end, include:

* Business flow reviewed
* Areas inspected
* Findings grouped by severity
* Important assumptions and unverified areas
* Recommended next actions

If no findings are identified, say so without claiming the code is completely secure. State meaningful limitations in the review scope.
