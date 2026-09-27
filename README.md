# Solidity Builder and Auditor

An agent skill that can turn a user conversation into a specified, tested, audited Solidity/EVM contract and freeze deployment-ready artifacts. It also performs evidence-led security reviews of existing contracts. It works with **Claude Code**, **Codex**, **Cursor**, and other coding agents that support the [Agent Skills](https://agentskills.io) `SKILL.md` format.

The skill guides an agent through conversational requirements, specification and threat modeling, implementation, compilation, testing, static analysis, fuzzing, manual review, exploit validation, iterative remediation, release freezing, and standalone audits.

## Creation workflow

For a new contract, the skill:

1. extracts explicit requirements and assumptions from the conversation
2. resolves choices that materially affect funds, authority, permanence, or compatibility
3. writes a reviewable specification and acceptance properties
4. implements the smallest suitable Solidity system and tests
5. audits both the implementation and the product rules
6. records and remediates confirmed findings, adding regression evidence
7. rebuilds and re-audits after every material correction
8. performs a clean-room rebuild and freezes source, ABI, bytecode, compiler input/build artifacts, exact approved constructor encoding, traceability, remediation history, audit report, and checksums for a separate deployment application

The skill never creates live keys, funds deployers, or signs or broadcasts to any non-local chain. It may use disposable default test accounts only on an ephemeral loopback Anvil/Hardhat node.

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
solidity-builder-auditor/
├── LICENSE
├── README.md
├── SKILL.md
├── scripts/
│   └── test_manifest_schema.py
└── references/
    ├── contract-lifecycle.md
    ├── deployment-manifest.example.json
    ├── deployment-manifest.not-ready.example.json
    ├── deployment-manifest.schema.json
    ├── audit-review.md
    ├── release-bundle.md
    ├── reporting.md
    ├── secure-defaults.md
    ├── standards.md
    ├── testing-matrix.md
    └── tool-safety.md
```

`SKILL.md` contains the core workflow and routes the agent to focused references for contract creation, standards mapping, and evidence-led test planning.

## Standards-aware reporting

The skill can map applicable controls and findings to:

- OWASP SCSVS and SCSTG
- OWASP Smart Contract Top 10 and SCWE
- EEA EthTrust Security Levels
- the legacy SWC Registry as supplementary taxonomy only

Mappings use exact editions or dated snapshots, applicability statuses, and evidence. Merely consulting a standard does not produce a checkmark, compliance percentage, certification, or conformance claim.

## Installation

### Simplest: ask your agent

Paste this into Codex, Claude Code, Cursor, or any agent with shell access:

```text
Install the skill from https://github.com/rohasnagpal/solidity-builder-auditor
```

Codex installs it with its built-in skill installer. Other agents clone the repository into their skills directory. Restart the agent or open a new session if the skill does not show up straight away.

### One command for any agent

The [`skills`](https://github.com/vercel-labs/skills) CLI detects the agents you have installed and installs the skill for each of them:

```bash
npx skills add rohasnagpal/solidity-builder-auditor
```

### Manual install

Clone the repository into your agent's skills directory:

| Agent | Personal (all projects) | Project only (commit it to share with a team) |
| --- | --- | --- |
| Claude Code | `~/.claude/skills/solidity-builder-auditor` | `.claude/skills/solidity-builder-auditor` |
| Codex | `~/.codex/skills/solidity-builder-auditor` | `.codex/skills/solidity-builder-auditor` |
| Cursor | `~/.cursor/skills/solidity-builder-auditor` | `.cursor/skills/solidity-builder-auditor` |

For example, for Claude Code:

```bash
git clone https://github.com/rohasnagpal/solidity-builder-auditor ~/.claude/skills/solidity-builder-auditor
```

Agents without skill support can still use it: point the agent at `SKILL.md` or add it to the agent's instructions file (for example `AGENTS.md`).

### Updating

```bash
git -C <skills-directory>/solidity-builder-auditor pull
```

## Usage

The agent loads the skill for production-oriented contract creation and Solidity security audits. Informal examples and tutorials do not trigger the full lifecycle unless requested. To call it explicitly:

| Agent | Explicit invocation |
| --- | --- |
| Claude Code | `/solidity-builder-auditor audit this Foundry project` |
| Codex | `Use $solidity-builder-auditor to audit this Foundry project.` |
| Cursor | `/solidity-builder-auditor audit this Foundry project` |

Example requests:

- `Build a Solidity contract from these requirements, test it, audit it, fix confirmed findings, and freeze the release artifacts.`
- `Turn this conversation into a non-upgradeable escrow contract and prepare it for a separate deployment app.`
- `Audit these Solidity contracts and produce a security report.`
- `Review this contract before deployment and validate material findings with tests.`
- `Run Slither and Foundry fuzz tests, then triage the results.`
- `Verify whether the supplied patch resolves the reported reentrancy issue.`
- `Audit this proof-of-existence contract's security and trust assumptions.`

Before running any project-controlled commands in a Solidity project, the skill inspects executable configuration and repository hooks. It follows the host agent's permission and sandbox model: anything that needs network access, installs, or elevated privileges goes through the agent's normal approval prompt.

A separate deployer is a user-operated application or wallet that verifies the frozen release hashes, displays the exact chain and constructor values, signs locally, broadcasts, and verifies deployed bytecode. This skill prepares that handoff but never creates live keys or signs or broadcasts to a non-local chain.

## Tooling

The skill can use an existing project toolchain and, where available and authorized:

- Foundry (`forge`, `cast`, and `anvil`)
- Slither and `solc-select`
- Hardhat and project-local Node.js tooling
- Echidna, Medusa, Halmos, Aderyn, or Mythril as secondary tools

These tools are not bundled with this repository. Missing tooling must not be reported as having run, and installation must respect the host environment's approval and network rules.

## Output

For creation work, expected outputs include a specification, source, tests, traceability evidence, remediation history, audit report, and—when supported—a checksummed release bundle containing ABI, compiler input/build artifacts, creation/runtime bytecode, exact approved constructor encoding, and a clean-room rebuild result. A parameterized bundle with no approved constructor values is marked `deploymentReady: false`.

The expected audit report includes:

1. Executive summary and frozen scope
2. System overview and trust assumptions
3. Findings table with severity and status
4. Evidence-backed detailed findings
5. Standards coverage with exact versions, applicability, and evidence where useful
6. Commands, tests, tools, installations, and audit artifacts
7. Business-logic and trust observations
8. Project-specific deployment checklist

The skill does not provide a security certification or guarantee that reviewed contracts are vulnerability-free.

## Validation

Install the manifest-test dependency in an isolated development environment and run the targeted schema and cross-field invariant tests:

```bash
python -m pip install 'jsonschema[format]'
python scripts/test_manifest_schema.py
```

Validate the frontmatter with the Agent Skills reference validator:

```bash
npx skills-ref validate .
```

Alternatively, use the `quick_validate.py` script from Anthropic's or Codex's `skill-creator` skill (requires PyYAML):

```bash
python3 /path/to/skill-creator/scripts/quick_validate.py .
```

## Contributing

Contributions should keep findings evidence-led, preserve strict authorization boundaries, and avoid adding checklist items without a concrete Solidity/EVM security use case.

When changing the workflow:

1. Keep the YAML frontmatter valid and the skill name unchanged unless intentionally migrating it.
2. Keep instructions agent-neutral: describe actions, not a particular agent's tool names or approval flow.
3. Check that new commands cannot broadcast transactions or expose secrets.
4. Keep chain- and fork-specific statements current.
5. Validate the skill before opening a pull request.

### Migration from the old name

Installations made under `smart-contract-auditor` do not automatically move. Remove or archive the old installed folder and clone/install `solidity-builder-auditor`, then restart the agent so the new skill identity is discovered.

## License

MIT. See [LICENSE](LICENSE).
