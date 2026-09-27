# Smart Contract Auditor

An agent skill for evidence-led security reviews of Solidity and EVM smart contracts. It works with **Claude Code**, **Codex**, **Cursor**, and other coding agents that support the [Agent Skills](https://agentskills.io) `SKILL.md` format.

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
├── LICENSE
├── README.md
└── SKILL.md
```

`SKILL.md` is the only file an agent needs. It contains the complete audit workflow, safety controls, review checklist, severity model, and report format.

## Installation

### Simplest: ask your agent

Paste this into Codex, Claude Code, Cursor, or any agent with shell access:

```text
Install the skill from https://github.com/rohasnagpal/smart-contract-auditor
```

Codex installs it with its built-in skill installer. Other agents clone the repository into their skills directory. Restart the agent or open a new session if the skill does not show up straight away.

### One command for any agent

The [`skills`](https://github.com/vercel-labs/skills) CLI detects the agents you have installed and installs the skill for each of them:

```bash
npx skills add rohasnagpal/smart-contract-auditor
```

### Manual install

Clone the repository into your agent's skills directory:

| Agent | Personal (all projects) | Project only (commit it to share with a team) |
| --- | --- | --- |
| Claude Code | `~/.claude/skills/smart-contract-auditor` | `.claude/skills/smart-contract-auditor` |
| Codex | `~/.codex/skills/smart-contract-auditor` | `.codex/skills/smart-contract-auditor` |
| Cursor | `~/.cursor/skills/smart-contract-auditor` | `.cursor/skills/smart-contract-auditor` |

For example, for Claude Code:

```bash
git clone https://github.com/rohasnagpal/smart-contract-auditor ~/.claude/skills/smart-contract-auditor
```

Agents without skill support can still use it: point the agent at `SKILL.md` or add it to the agent's instructions file (for example `AGENTS.md`).

### Updating

```bash
git -C <skills-directory>/smart-contract-auditor pull
```

## Usage

The agent loads the skill automatically when you ask for a smart contract audit. To call it explicitly:

| Agent | Explicit invocation |
| --- | --- |
| Claude Code | `/smart-contract-auditor audit this Foundry project` |
| Codex | `Use $smart-contract-auditor to audit this Foundry project.` |
| Cursor | `/smart-contract-auditor audit this Foundry project` |

Example requests:

- `Audit these Solidity contracts and produce a security report.`
- `Review this contract before deployment and validate material findings with tests.`
- `Run Slither and Foundry fuzz tests, then triage the results.`
- `Verify whether the supplied patch resolves the reported reentrancy issue.`
- `Audit this proof-of-existence contract's security and trust assumptions.`

Before running any project-controlled commands in a Solidity project, the skill inspects executable configuration and repository hooks. It follows the host agent's permission and sandbox model: anything that needs network access, installs, or elevated privileges goes through the agent's normal approval prompt.

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

## License

MIT. See [LICENSE](LICENSE).
