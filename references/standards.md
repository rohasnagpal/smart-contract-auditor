# Standards and taxonomy mapping

Use this reference when planning standards-based coverage, mapping findings, or describing conformance. Standards supplement adversarial review; they do not replace contract-specific threat modeling or testing.

## Authoritative baselines

Verify the current edition from the primary source when network access is available and permitted by the host's network-approval model. Record the edition, release date, or repository commit used. The following were checked against the linked primary sources on 2026-09-27:

- [OWASP Smart Contract Security Verification Standard (SCSVS)](https://scs.owasp.org/SCSVS/): security requirements and control groups. The OWASP project page describes stable version 0.0.1 (September 2024), while the live SCS site contains a subsequently refactored control set. Pin either an official release or a dated repository commit; do not call an unversioned live page a stable release.
- [OWASP Smart Contract Security Testing Guide (SCSTG)](https://scs.owasp.org/SCSTG/): test procedures supporting SCSVS controls. Some material is marked beta; identify the test ID and snapshot used.
- [OWASP Smart Contract Weakness Enumeration (SCWE)](https://scs.owasp.org/SCWE/): maintained weakness taxonomy for precise finding classification.
- [OWASP Smart Contract Top 10](https://scs.owasp.org/sctop10/): awareness and risk-category mapping. The current edition is 2026; 2025 is archived. Top 10 mapping is not verification coverage.
- [EEA EthTrust Security Levels Specification](https://entethalliance.org/specs/ethtrust-sl/): normative Solidity/EVM review requirements. Version 3 (March 2025) is the current approved specification. A version 4 draft is under review and is not the certification baseline.
- [SWC Registry](https://github.com/SmartContractSecurity/SWC-registry): legacy supplemental taxonomy. The repository states that it has not been significantly updated since 2020 and is no longer actively maintained. Prefer current SCSVS/SCWE and EthTrust requirements.

If a source cannot be verified, say which embedded baseline was used and that currency was not checked.

## Mapping rules

For each finding, include only mappings supported by the finding's actual cause and impact:

```text
Standards mapping (informative):
- OWASP Smart Contract Top 10 2026: SC02 — Business Logic Vulnerabilities
- OWASP SCSVS snapshot <date/commit>: <exact control or requirement ID>
- OWASP SCWE snapshot <date/commit>: SCWE-037 — Insufficient Protection Against Front-Running
- EEA EthTrust v3: [Q] Protect against Ordering Attacks
- SWC Registry: None
```

- Use exact requirement IDs or titles where the source provides them.
- A category-level mapping such as `SCSVS-GOV` must be labeled category-level, not a passed requirement.
- Do not map a finding solely because two labels sound similar.
- Do not force all four frameworks onto every finding.
- Explain any non-obvious mapping in one sentence.
- Prefer SCWE over SWC for current weakness identifiers.
- SWC-105 is specifically Unprotected Ether Withdrawal. It is not a generic missing-access-control identifier.

## Coverage reporting

Use an applicability matrix rather than a list of checked standard names:

| Standard | Edition/snapshot | Requirement | Status | Evidence |
|---|---|---|---|---|
| OWASP SCSVS | commit/date | exact ID/title | Pass / Fail / N/A / Not tested | test, source, trace, or rationale |
| EEA EthTrust | v3 | exact level and title | Pass / Fail / N/A / Not tested | test, source, trace, or rationale |

Definitions:

- `Pass`: evidence supports the requirement within the frozen scope.
- `Fail`: a confirmed finding violates the requirement.
- `Not applicable`: the relevant feature is absent; state why.
- `Not tested`: applicable, but evidence was not obtained; state the limitation.

Do not use a bare checkmark. Do not calculate a compliance percentage unless the chosen standard defines that calculation and the denominator includes every applicable normative requirement.

## Conformance and certification boundary

A cross-reference is not a conformance claim. Say `informative mapping; not a certification or conformance claim` unless the audit:

1. assesses every normative requirement required by the claimed level or profile;
2. records applicability and evidence for each requirement;
3. satisfies the standard's formal claim requirements, including scope, compiler/EVM details, artifacts, dates, and required notices; and
4. is issued by a reviewer entitled and willing to make that claim.

For EEA EthTrust, use `[S]`, `[M]`, and `[Q]` only with their specification meanings. Do not infer level `[Q]` merely because business logic was manually reviewed.

## Version maintenance

At the start of a new audit, check the authoritative pages above for superseding releases when network access is available. Update a local mapping only after verifying the normative source. Drafts may inform additional review but must be labeled draft and must not replace the current approved baseline.
