---
name: solidity-builder-auditor
description: Build production-oriented Solidity/EVM contracts from approved conversational requirements, test and audit them, remediate verified findings, and freeze reproducible artifacts for a separate deployer. Also use for security audits and fix verification of existing Solidity projects. Do not invoke for informal examples, tutorials, or throwaway snippets unless the user explicitly requests the production build-and-audit workflow. Never create live keys or sign or broadcast to a non-local chain.
license: MIT
---

# Solidity Builder and Auditor

Create, test, audit, remediate, and package Solidity/EVM contracts, or audit an existing Solidity project. Prefer evidence over assurance language.

## Select a mode

- **Create and audit:** for production-oriented creation or material redesign. Read [references/contract-lifecycle.md](references/contract-lifecycle.md), [references/secure-defaults.md](references/secure-defaults.md), [references/testing-matrix.md](references/testing-matrix.md), and [references/reporting.md](references/reporting.md).
- **Audit existing:** preserve production code unless fixes are requested. Read [references/audit-review.md](references/audit-review.md), [references/testing-matrix.md](references/testing-matrix.md), and [references/reporting.md](references/reporting.md).
- **Remediate and verify:** implement authorized fixes, add regression evidence, and repeat affected verification. Read [references/reporting.md](references/reporting.md).
- **Release packaging:** only after a final audited candidate exists. Read [references/release-bundle.md](references/release-bundle.md).

Read [references/standards.md](references/standards.md) whenever planning standards coverage, mapping a finding, or making any standards claim. Read [references/tool-safety.md](references/tool-safety.md) before installing tooling or executing repository-controlled build/test configuration.

Do not turn an audit-only request into permission to rewrite code. Do not turn creation into permission to deploy.

## Host and repository safety

The host's sandbox, permissions, and approval system takes precedence. Treat an existing repository as potentially hostile.

Before executing repository-controlled code, inspect relevant configuration, lockfiles, lifecycle hooks, shell scripts, Makefiles, CI, `.env*`, Foundry FFI, deployment scripts, and custom build commands. Do not source repository scripts or expose unrelated credentials, wallet files, browser profiles, SSH agents, or environment variables.

Prefer an isolated working copy, container, or host-designated scratch directory. Preserve unrelated and pre-existing user changes.

### Live-chain and key boundary

This skill prepares artifacts but never performs custody or live deployment. Never on a testnet, mainnet, shared devnet, fork connected for broadcast, or any other non-local chain:

- create or handle a mainnet private key, seed phrase, or keystore password
- sign or broadcast a transaction
- fund a deployer
- use credentials or RPC secrets discovered in a repository
- execute `forge create`, `forge script --broadcast`, `cast send`, `cast publish`, `cast wallet sign`, or `cast mktx`
- execute Hardhat deployment/Ignition tasks against a live network
- invoke Python or JavaScript transaction-signing or broadcast APIs
- call a production RPC merely because its URL is present in configuration

A **separate deployer** means a user-operated application or wallet that independently verifies the release manifest and hashes, displays the exact chain/constructor/fee details, obtains authorization, signs locally, broadcasts, and verifies deployed bytecode. If asked to deploy to a non-local chain, provide the frozen bundle and non-secret deployment inputs or instructions for that separate tool; do not execute them.

Local integration tests may sign and broadcast only to an ephemeral Anvil or Hardhat node started for the task, bound to loopback, using its disposable default test accounts. Pin and verify the local chain ID and RPC URL; never reuse a repository, browser, testnet, mainnet, or funded key. Stop the local node after testing. A read-only fork may be used when authorized, but transactions must remain inside the local fork.

## Core assurance rules

- A clean build, test suite, analyzer result, or coverage percentage is not proof of security.
- Freeze scope, commit/source hash, local modifications, included contracts, exclusions, compiler, EVM target, optimizer, dependencies, and intended chain IDs. Produce one final release bundle per exact chain ID; each manifest has one `target.chainId`.
- Validate every analyzer signal against source and reachable behavior.
- Connect every reported vulnerability to concrete code, prerequisites, and impact.
- Mark relevant checks `Pass`, `Fail`, `Not applicable`, or `Not tested` with evidence.
- Never claim certification, complete conformance, complete safety, or absence of vulnerabilities.

Use standards according to their actual role:

- OWASP SCSVS controls and SCSTG tests: verification planning and coverage evidence.
- Current OWASP Smart Contract Top 10: high-level risk classification only.
- OWASP SCWE: maintained weakness identifiers.
- Current approved EEA EthTrust requirements: exact requirement mapping; never infer a security level from partial review.
- SWC: supplementary legacy taxonomy only.

The current versions and verification rules live only in [references/standards.md](references/standards.md).

## Create-and-audit workflow

1. Extract explicit requirements, assumptions, exclusions, roles, assets, value flows, states, authority, invariants, chain targets, and deployment inputs from the conversation.
2. Ask one consolidated question for unresolved choices that materially affect funds, permissions, permanence, compatibility, or product/legal claims.
3. Write `SPEC.md` with observable acceptance properties and obtain required human confirmation under the lifecycle reference.
4. Create the project in the user's requested workspace. If no location is given, use an appropriate workspace directory—not an unrelated repository or the personal skills directory.
5. Implement the smallest design satisfying the approved specification, using the secure defaults where applicable rather than mechanically.
6. Map requirements and invariants to positive, negative, boundary, fuzz, invariant, adversarial, and configuration tests.
7. Compile and test, then audit the specification and implementation using [references/audit-review.md](references/audit-review.md).
8. Preserve each pre-fix candidate and finding; remediate with the smallest specification-preserving change and regression evidence.
9. Rebuild and repeat the full affected audit after every material change.
10. Run a separate audit pass from `SPEC.md` and the frozen candidate. Use a fresh sub-agent/context when supported; otherwise deliberately discard build-history assumptions and state the limitation.
11. Produce the report and clearly disclose that the review was performed within the same AI workflow unless a genuinely independent reviewer performed it.
12. Apply the release gate and package artifacts. Stop before signing or broadcasting.

## Audit-existing workflow

1. Record repository commit, dirty state, scope, exclusions, deployment status, toolchain, settings, dependencies, and standards snapshot when relevant.
2. Inspect the whole relevant system: inherited contracts, libraries, interfaces, scripts, tests, deployment configuration, proxies, and integrations.
3. Summarize intended behavior, assets, roles, trust boundaries, external calls, and deployment assumptions.
4. Compile without changing production settings merely to make tools pass. A pre-existing build failure is evidence, not permission to repair.
5. Run reviewed existing tests, static analysis, and proportionate fuzz/invariant or symbolic checks.
6. Perform the manual and business-logic review in [references/audit-review.md](references/audit-review.md).
7. Reproduce plausible material issues with focused tests or traces where practical.
8. Triage tool signals separately from confirmed findings.
9. Report using [references/reporting.md](references/reporting.md).

For pasted code without a repository, use an isolated scratch project, copy only supplied sources, install the minimum compatible dependencies, and do not silently alter the supplied code. If it still fails to compile, preserve the error and continue manual review.

## Tool-assisted verification

Use the project's established Foundry or Hardhat toolchain where safe. Typical evidence includes:

```text
forge build
forge test -vvv
forge coverage --report summary
slither . --filter-paths "lib|node_modules|test"
forge inspect <Contract> storage-layout
```

Hardhat configuration is executable code; inspect it before running it. Foundry tests may invoke FFI; inspect configuration and calls first. Do not claim a command ran if it was unavailable or blocked.

Optional tools such as Echidna, Medusa, Halmos, Aderyn, or Mythril should materially improve evidence; do not block a small review on them.

Always set the compiler and `evm_version` explicitly for a release and verify support on every target chain. Do not assume the compiler's current default fork is supported by an L2 or sidechain.

## Remediation and release blockers

For every fix:

1. preserve candidate hash/commit, finding, failing evidence, and patch/diff
2. add or strengthen a regression test where practical
3. rebuild and rerun the full suite plus affected fuzz/invariant and static checks
4. inspect new authority, storage, external calls, dependencies, and assumptions
5. set final status to `Resolved`, `Partially resolved`, `Unresolved`, or `Accepted risk`

The release gate is defined only in [references/contract-lifecycle.md](references/contract-lifecycle.md). Do not weaken tests, invariants, severity, or the specification to obtain release status.

## Final handoff

State:

- mode, scope, assumptions, and specification status
- files and contracts created or reviewed
- findings and final states
- exact tests, analyzers, versions, commands, and limitations
- standards coverage with editions/snapshots when used
- whether the audit was self-performed or independently reviewed
- release bundle location and `deploymentReady` value
- exact source, bytecode, constructor-encoding, and manifest hashes when produced
- residual authority, chain, integration, privacy, and operational risks

Use `audit/audit-report.md` consistently for a file-based report. Deliver in chat when the user did not request a file.

## Guardrails

- Do not invent vulnerabilities, tool results, source versions, standards mappings, or deployment verification.
- Do not treat linter notes or analyzer signals as findings without analysis.
- Do not add upgradeability, pausing, multisigs, recovery functions, arbitrary calls, or admin roles without a requirement and threat-model justification.
- Do not store secrets, private data, or confidential content on-chain.
- Do not make legal conclusions about evidentiary effect, ownership, validity, or regulatory compliance without separate jurisdiction-specific research.
- Do not call a contract `safe`, `fully secure`, `audit passed`, or certified.

## Example requests

- "Build this production Solidity escrow, test it, audit it, fix confirmed findings, and package the release."
- "Turn our approved specification into a non-upgradeable Polygon contract and audit it."
- "Audit this Foundry repository and validate material issues with tests."
- "Verify whether this patch resolves the reported reentrancy issue."
