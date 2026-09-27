# Findings and reporting

## Severity

Assess impact and likelihood together, considering prerequisites, attacker capability, affected value/users, reversibility and detectability.

- **Critical:** realistic catastrophic loss, protocol takeover, arbitrary asset theft or irreversible systemic corruption.
- **High:** serious exploit or privilege bypass with major financial, integrity or availability impact.
- **Medium:** material security/correctness failure with meaningful impact or plausible prerequisites.
- **Low:** limited-impact weakness, edge case or defense-in-depth/operational issue.
- **Informational:** improvement without concrete security impact.

Owner centralization is not automatically High; rate the actual power, disclosure, intended trust model and compromise impact.

## Finding state model

Keep three independent fields:

- **Classification:** `Confirmed finding`, `Potential issue`, `Design consideration`, or `Analyzer false positive`.
- **Verification:** `Code review`, `Confirmed by test/trace`, `Needs confirmation`, or `Not applicable`.
- **Resolution:** `Open`, `Resolved`, `Partially resolved`, `Unresolved`, or `Accepted risk`.

Only `Confirmed finding` entries are security findings. Analyzer false positives belong in a separate tool-triage section, not the findings count. `Accepted risk` requires the human acceptance evidence defined by the release gate.

## Finding format

```text
ID and title:
Severity:
Classification:
Verification:
Resolution:
Location:
Standards mapping (informative):
Description:
Attack or failure scenario:
Impact:
Evidence:
Recommendation:
Patch or remediation evidence:
```

Use exact `file:line` references when files exist. Connect theoretical patterns to reachable code and impact.

## Report structure

Use `audit/audit-report.md` for a file report:

1. Executive summary: frozen scope/hash, toolchain, tests, reviewer independence, and finding counts.
2. System overview: behavior, assets, roles and trust assumptions.
3. Findings table.
4. Standards coverage: edition/snapshot, requirement, applicability status and evidence; not a certification claim.
5. Detailed findings.
6. Analyzer and linter triage, including false positives.
7. Commands, tool versions, installations, tests and artifacts.
8. Business-logic and trust observations.
9. Limitations and checks not performed.
10. Project-specific release/deployment checklist.

Do not issue numeric safety scores or say `audit passed`, `fully secure`, or `100% safe`. A suitable conclusion is: `No Critical or High findings were identified within the reviewed scope; this does not guarantee the absence of vulnerabilities.`
