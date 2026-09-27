# Smart Contract Auditor

A Codex skill for evidence-led security reviews of Solidity and EVM smart contracts.

The skill guides an agent through scope discovery, hostile-repository precautions, compilation, testing, static analysis, fuzzing, manual review, exploit validation, business-logic analysis, severity assessment, reporting, and remediation verification.

## What it covers

- Access control, privilege boundaries, and initialization
- Reentrancy, external calls, callbacks, and token edge cases
- Accounting, fees, rounding, value transfer, and withdrawal logic
- Signatures, replay protection, EIP-712, nonces, and cryptographic inputs
- Oracles, bridges, L2 assumptions, MEV, and external integrations
- Proxies, upgrade authorization, and storage-layout risks
- Denial of service, gas-sensitive paths, and state growth
- Business-logic and trust-model failures
- Proof-of-existence and timestamping contract risks
- Fix verification and regression checks

## Design principles

- Treat the audited repository as potentially hostile.
- Prefer reproducible evidence over generic pattern matching.
- Validate automated findings against the source code.
- Use exact `file:line` references when files are available.
- Separate confirmed findings, likely issues, design considerations, and tool false positives.
- Never describe a contract as safe merely because tools or tests pass.
- Never broadcast or sign a live transaction as part of an audit.

## Repository structure

```text
smart-contract-auditor/
├── README.md
└── SKILL.md
```

`SKILL.md` is the Codex skill entrypoint and contains the complete audit workflow, safety controls, review checklist, severity model, and report format.

## Installation

Clone the repository into the Codex skills directory:

```bash
git clone YOUR_REPOSITORY_URL ~/.codex/skills/smart-contract-auditor
```

Alternatively, clone it elsewhere and copy the `smart-contract-auditor` directory into `~/.codex/skills/`.

Restart Codex if the skill is not discovered immediately.

## Usage

Invoke the skill explicitly:

```text
Use $smart-contract-auditor to audit this Foundry project.
```

Example requests:

- `Audit these Solidity contracts and produce a security report.`
- `Review this contract before deployment and validate material findings with tests.`
- `Run Slither and Foundry fuzz tests, then triage the results.`
- `Verify whether the supplied patch resolves the reported reentrancy issue.`
- `Audit this proof-of-existence contract's security and trust assumptions.`

When invoked in a Solidity project, the skill first inspects executable configuration and repository hooks before running project-controlled commands.

## Tooling

The skill can use an existing project toolchain and, where available and authorized:

- Foundry (`forge`, `cast`, and `anvil`)
- Slither and `solc-select`
- Hardhat and project-local Node.js tooling
- Echidna, Medusa, Halmos, Aderyn, or Mythril as secondary tools

These tools are not bundled with this repository. Missing tooling must not be reported as having run, and installation must respect the host environment's approval and network rules.

## Output

The expected audit report includes:

1. Executive summary and frozen scope
2. System overview and trust assumptions
3. Findings table with severity and status
4. Evidence-backed detailed findings
5. Commands, tests, tools, installations, and audit artifacts
6. Business-logic and trust observations
7. Project-specific deployment checklist

The skill does not provide a security certification or guarantee that reviewed contracts are vulnerability-free.

## Validation

Validate the skill with Codex's bundled skill validator:

```bash
python3 /path/to/skill-creator/scripts/quick_validate.py .
```

The validator requires PyYAML in the Python environment.

## Contributing

Contributions should keep findings evidence-led, preserve strict authorization boundaries, and avoid adding checklist items without a concrete Solidity/EVM security use case.

When changing the workflow:

1. Keep the YAML frontmatter valid and the skill name unchanged unless intentionally migrating it.
2. Check that new commands cannot broadcast transactions or expose secrets.
3. Keep chain- and fork-specific statements current.
4. Validate the skill before opening a pull request.

