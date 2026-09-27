---
name: smart-contract-auditor
description: Audit Solidity/EVM smart contracts for security, correctness, access-control, economic, integration, deployment, and trust-model risks. Use for Solidity contract audits, pre-deployment security reviews, exploit validation, and remediation verification. Prefer evidence from compilation, tests, static analysis, fuzzing, and exact file:line references. Treat audited repositories as potentially hostile, and never equate clean tool output with safety. Vyper is outside the automated-tooling scope unless the environment explicitly supports it.
license: MIT
---

# Smart Contract Auditor

Perform a practical security audit of Solidity/EVM smart contracts.

The objective is to identify exploitable vulnerabilities, correctness failures, dangerous trust assumptions, integration risks, and deployment hazards, then produce a concise report that a developer can act on.

## Host agent compatibility

This skill is agent-neutral. It works in Claude Code, Codex, Cursor, and any other coding agent that supports the Agent Skills `SKILL.md` format or can be pointed at this file as instructions.

- Use whatever shell, file-reading, file-editing, and search tools the host agent provides. Tool names differ between agents; the workflow does not.
- The host's permission, sandbox, and approval model always takes precedence. Where this skill says to "obtain authorization" or "request approval", use the host's native mechanism (permission prompt, approval mode, or asking the user directly).
- If the host has no shell access, perform the manual review and report every tool-dependent check as not run.
- If the host supports sub-agents or parallel tasks, they may be used for independent review areas, but every finding must still be validated against the source before it is reported.
- Deliver the report in chat unless the user asks for a file. If writing a file, place it outside tracked contract sources (for example `audit/REPORT.md`) and say where it was written.

## Threat model for the audit environment

Treat the repository being audited as potentially hostile.

Before executing repository-controlled code:

- inspect `package.json`, package-manager lockfiles, `hardhat.config.*`, `foundry.toml`, `.env*`, shell scripts, Makefiles, CI scripts, and custom install/build scripts
- inspect whether Foundry FFI is enabled (`ffi = true`)
- inspect npm lifecycle scripts such as `preinstall`, `install`, `postinstall`, `prepare`, and custom build hooks
- do not source repository-provided shell files
- do not execute arbitrary repo scripts until they have been read and are necessary to the audit
- prefer a sandbox, container, disposable workspace, or isolated working copy when one is available
- never expose host secrets, SSH agents, cloud credentials, wallet files, browser profiles, or unrelated environment variables to audit commands

### Hard prohibitions

Never:

- broadcast a transaction
- sign a transaction with a real private key
- run `forge script --broadcast`
- run `cast send`
- run Hardhat deployment or execution tasks against a live network unless the user explicitly requests a deployment operation
- use private keys, mnemonics, keystore passwords, API secrets, or RPC credentials discovered in the repository
- call a production RPC endpoint merely because it appears in `.env`
- modify `foundry.toml`, remappings, compiler pragma, lockfiles, or production source merely to make a tool run
- run destructive repository scripts without explicit inspection and necessity

For integration testing, prefer local Anvil/Hardhat nodes or explicitly provided safe test/fork RPC endpoints.

## Core rule

Never treat a clean automated scan as proof that a contract is secure.

Use multiple layers where the environment allows:

1. Manual adversarial review
2. Compilation
3. Existing unit tests
4. Static analysis
5. Targeted tests written during the audit
6. Fuzzing / invariant testing
7. Dependency and configuration review

If a required audit tool is unavailable, use an already-approved, isolated installation path when one exists. Otherwise request any authorization required by the environment before installing it. If installation is not possible, continue manually and clearly state which checks could not be run.

## Tool bootstrap and safe installation

Before starting the audit, detect the available toolchain and inspect the repository before executing it.

Check for:

```bash
git status --short
git rev-parse HEAD
forge --version
cast --version
anvil --version
slither --version
solc-select --version
echidna --version
medusa --version
halmos --version
node --version
npm --version
python3 --version
pipx --version
```

Also inspect the repository for:

```text
foundry.toml
hardhat.config.*
package.json
package-lock.json
yarn.lock
pnpm-lock.yaml
.env*
requirements.txt
pyproject.toml
.gitmodules
Makefile
scripts/
```

### Installation principles

When a useful audit tool is missing:

1. Prefer an existing project-local toolchain.
2. Prefer project-local or isolated installs over modifying the global environment.
3. Use established official installation methods.
4. Do not use `sudo` unless the environment explicitly requires it and the user has already authorized privileged changes.
5. Never uninstall, downgrade, or replace unrelated user tooling merely to satisfy the audit.
6. Never change application dependencies, lockfiles, compiler pragma, `foundry.toml`, or remappings merely to make analysis work.
7. Obtain any approval required for network access, user-level or global changes, or privileged installation before acting.
8. Record every installation command in the final report.
9. Try each network-dependent installation path once. If it is blocked, use a documented fallback once, then proceed with remaining tooling.
10. If installation fails, continue with the remaining available tools.

### Foundry

If Foundry is required and missing, inspect the current official installation instructions and obtain any authorization required by the environment. Prefer a verifiable release artifact or package-manager route over piping a remote script directly to a shell.

After installation, verify:

```bash
forge --version
cast --version
anvil --version
```

Do not reinstall or upgrade Foundry merely to obtain a newer version unless the project requires it.

Keep any PATH adjustment scoped to the audit shell unless the user asks for a persistent configuration change.

### Slither and solc-select

Prefer an isolated Python installation using `pipx`:

```bash
pipx install slither-analyzer
pipx install solc-select
```

If `pipx` is unavailable, create the Python environment outside the audited repository, for example:

```bash
python3 -m venv /tmp/smart-contract-audit-venv
. /tmp/smart-contract-audit-venv/bin/activate
python -m pip install --upgrade pip
python -m pip install slither-analyzer solc-select
```

Avoid `sudo pip install`.

For a single Solidity file, select the matching compiler:

```bash
solc-select install <version>
solc-select use <version>
```

For Foundry or Hardhat projects, let Slither use the framework via crytic-compile where possible.

Reduce dependency/test noise when appropriate:

```bash
slither . --filter-paths "lib|node_modules|test"
```

### Hardhat / Node tooling

Read `hardhat.config.*` before any `npx hardhat` command because the config itself is executable code.

If dependencies are missing and a lockfile exists, prefer:

```bash
npm ci --ignore-scripts
```

Inspect lifecycle scripts before running them. Only rerun without `--ignore-scripts` when a required script has been reviewed and is necessary.

Do not globally install Hardhat if the project already declares it.

### Foundry safety checks

Before `forge test`:

- inspect `foundry.toml`
- if `ffi = true`, inspect the tests and scripts that invoke FFI before execution
- inspect `.env*` without printing secrets into the audit report
- do not run scripts that broadcast, sign, deploy, or call live networks
- do not use repository RPC URLs unless they are explicitly safe for testing

### Optional advanced tooling

Use these only when installed or safely installable and when they materially improve confidence:

- Echidna for property-based fuzzing
- Medusa for fuzzing
- Halmos for symbolic execution of small, well-defined properties
- `forge coverage` for test-path visibility

Do not block a small audit on optional tooling.

### Ephemeral audit artifacts

Create audit environments outside the repository when practical, in the system temporary directory or the scratch directory the host agent designates:

```text
<system-temp-dir>/smart-contract-audit-venv
<system-temp-dir>/smart-contract-audit-work
```

If audit tests must be added inside the repo, use a clearly named path such as:

```text
test/audit/
```

Record whether these files are left in place, delivered as a patch, or removed after the audit. Avoid polluting tracked files.

### Network-restricted environments

If an install path fails due to network restrictions:

- try one documented fallback if available
- do not repeatedly retry
- do not claim the tool was run
- continue with installed tooling and manual review
- state exactly which tools were unavailable

### Installation verification

After installing any tool, verify it before relying on it:

```bash
<tool> --version
```

A successful installer exit code alone is not sufficient.

## Scope discovery

Before analyzing findings, freeze and record the scope:

- `git rev-parse HEAD` when a Git repository is available
- `git status --short`
- files/contracts included in scope
- files/contracts explicitly out of scope
- whether local modifications are present

Then determine:

- Solidity version and compiler settings
- Target EVM chain(s)
- Whether the contract is already deployed
- Whether it is upgradeable
- Whether it holds or transfers ETH/tokens
- Privileged/admin roles
- External contracts, oracles, bridges, callbacks, hooks, proxies, libraries, or delegatecalls
- Expected invariants and business rules
- Whether fees, balances, ownership, timestamps, signatures, hashes, or user identities have special meaning
- Existing tests and deployment scripts

Inspect the whole relevant repository where available, not only the contract named by the user, because security assumptions often live in inherited contracts, libraries, scripts, tests, or configuration.

Do not force an intake questionnaire if these facts can be inferred from the codebase.

## Pasted code with no repository

If the user provides one or more Solidity files directly in chat with no project:

1. create a disposable scratch directory outside any existing project
2. initialize the smallest suitable Foundry project
3. copy only the supplied source into that workspace
4. inspect declared imports
5. install only the minimum required dependencies at versions compatible with the supplied pragma/imports
6. compile and audit from that scratch workspace
7. do not silently alter the supplied source to make it compile

If compilation still fails, report the exact failure and continue with manual review.

## Build-failure rule

If the target does not compile:

- capture the compiler error
- do not "repair" production code merely to proceed
- distinguish pre-existing build failure from security findings
- continue with manual/static review where possible
- clearly mark tests or analyzers that could not run

## Audit workflow

### 1. Build and map the system

Compile the project first.

Prefer Foundry where present:

```bash
forge build
forge test
```

For Hardhat projects use the project's configured commands, commonly:

```bash
npx hardhat compile
npx hardhat test
```

Identify:

- externally callable functions
- state-changing functions
- value transfers
- privileged functions
- trust boundaries
- external calls
- storage layout
- inheritance
- events
- signature verification
- user-controlled inputs
- initialization and deployment flow

Summarize the contract's intended behavior in plain English before judging implementation.

### 2. Run static analysis

If Slither is installed:

```bash
slither .
```

For a single file where appropriate:

```bash
slither path/to/Contract.sol
```

If additional analyzers are installed, use them as secondary signals rather than as substitutes for manual review.

Examples:

```bash
aderyn .
myth analyze path/to/Contract.sol
```

Do not reproduce tool output blindly. Validate each reported issue against the actual code and discard false positives.

### 3. Review manually, line by line

Check at minimum:

#### Access control
- missing authorization
- privilege escalation
- unsafe ownership transfer
- unprotected initialization
- dangerous admin powers
- compromised-owner blast radius
- renounce-ownership consequences
- role misconfiguration

#### Reentrancy and external interaction
- ETH transfers
- token callbacks
- ERC777/ERC721/ERC1155 hooks
- arbitrary external calls
- checks-effects-interactions violations
- cross-function reentrancy
- read-only reentrancy where relevant

#### Value and accounting
- incorrect `msg.value` validation
- push-vs-pull payment design
- `transfer` / `send` 2300-gas stipend assumptions
- external-call gas griefing, including 63/64 forwarding behavior
- return-data bombs or unexpectedly large returndata
- blacklistable/freezeable token behavior causing payout DoS
- USDT-style allowance reset requirements
- no-return-value ERC20s and unsafe direct token calls; prefer SafeERC20 where appropriate
- flash-loan-enabled manipulation of accounting or spot prices
- ERC-4626 first-depositor/share-inflation attacks where applicable
- missing slippage bounds or transaction deadlines
- MEV / sandwich exposure where ordering affects value
- trapped ETH
- overpayment handling
- rounding
- precision loss
- fee calculation
- withdrawal logic
- double-spend / double-claim conditions
- incorrect balance assumptions

#### State integrity
- duplicate records
- overwrite conditions
- stale state
- missing state transition
- race conditions
- front-running
- griefing
- denial of service
- unbounded loops
- storage collisions

#### Inputs and cryptography
- zero values
- EIP-712 domain separation and inclusion of `chainId` where replay matters
- fork / cross-chain signature replay
- `ecrecover` returning `address(0)`
- ERC-1271 contract-wallet signatures
- permit / approval front-running or griefing
- nonce management and signature expiry
- malformed hashes
- replay attacks
- signature malleability
- missing nonces
- incorrect domain separation
- `abi.encodePacked` collision risks
- weak assumptions about `block.timestamp`
- predictable randomness
- unsafe `tx.origin`
- misuse of `blockhash`

#### External integrations
- unchecked return values
- Chainlink sequencer-uptime handling on L2 where relevant
- L2-specific block/timestamp semantics, including `block.number` differences where relevant
- compiler/EVM-version compatibility such as `PUSH0` on chains that have not adopted Shanghai
- governance, timelocks, emergency roles, and execution delays where present
- non-standard ERC20 behavior
- fee-on-transfer tokens
- rebasing tokens
- decimals assumptions
- oracle manipulation
- stale oracle data
- bridge trust
- callback assumptions
- malicious external contracts

#### Proxy / upgradeability
If upgradeable:
- initializer protection
- implementation initialization
- storage layout compatibility
- upgrade authorization
- proxy admin assumptions
- UUPS authorization
- delegatecall hazards

If not upgradeable, mark these checks N/A rather than inventing findings.

#### Solidity / EVM hazards
- `delegatecall`
- `selfdestruct`, interpreted according to the target chain's fork rules; on Cancun-compatible Ethereum, EIP-6780 means ordinary `SELFDESTRUCT` no longer deletes code/storage except when called in the same transaction as creation
- `tx.origin == msg.sender`, `extcodesize == 0`, and similar EOA-only assumptions; on EIP-7702-capable chains an EOA may execute delegated code, so these checks do not reliably imply "no contract logic"
- inline assembly
- transient storage (`TSTORE` / `TLOAD`) and custom reentrancy locks where supported
- unchecked blocks
- unsafe casts
- shadowed variables
- storage references
- fallback/receive behavior
- gas-sensitive logic
- compiler-version-specific behavior

#### Gas and denial-of-service characteristics
- unbounded loops over attacker-influenced collections
- storage growth with no practical bound
- repeated cold storage/external access
- avoidable O(n) or O(n²) paths on state-changing functions
- gas-sensitive cleanup or withdrawal paths
- calldata and returndata amplification
- whether optimization suggestions preserve readability and security

Treat pure gas optimizations as Informational unless they create a realistic availability or economic-security problem.

#### Events and observability
- critical state changes emit events
- event values match stored values
- indexed fields are useful for verification
- off-chain consumers can reconstruct necessary facts

### 4. Test the assumptions

Write targeted tests for any plausible vulnerability or ambiguous behavior.

Prefer proof over speculation.

For Foundry, add focused tests and run:

```bash
forge test -vvv
```

Use fuzz tests for user-controlled values:

```solidity
function testFuzz_Example(uint256 x) public {
    // assert invariant
}
```

Use invariant tests when the contract has persistent accounting or state properties.

For Foundry invariants, prefer a handler-based setup with `targetContract(...)` or equivalent targeting when meaningful. Avoid shallow invariant tests that exercise only trivial direct calls and miss realistic action sequences.

Use coverage to identify untested paths when practical:

```bash
forge coverage
```

For upgradeable systems, inspect storage layout:

```bash
forge inspect <ContractName> storage-layout
```

For integrations, fork tests may be useful only when the user provides or authorizes a safe RPC endpoint. Never reuse production secrets found in the repository.

Typical invariants:

- funds cannot leave except through authorized paths
- one proof cannot be overwritten
- fees cannot be bypassed
- unauthorized accounts cannot change configuration
- total accounting remains consistent
- successful state changes emit the expected event
- a duplicate identifier cannot create inconsistent records

Where a finding is important, try to produce a minimal failing test demonstrating it.

### 5. Review dependencies and configuration

Check:

- imported library versions
- OpenZeppelin usage
- pinned dependency versions
- compiler version
- optimizer settings
- remappings
- deployment parameters
- constructor arguments
- proxy configuration
- environment-variable assumptions
- secrets accidentally committed to the repository

Prefer established libraries over custom security-sensitive primitives when practical.

### 6. Review deployed-contract consistency when applicable

If the contract is already deployed and network access is explicitly safe:

- fetch verified source from a reputable explorer where available
- record chain ID and contract address
- compare constructor/immutable configuration where possible
- compare deployed bytecode against the audited build using an appropriate verification method such as `forge verify-bytecode` or explorer tooling
- for proxies, identify proxy type, implementation address, admin, beacon if any, and current storage layout
- mark this entire step N/A if there is no safe network access or the deployment is unverified

Never use a private production RPC credential discovered in the repository for this check.

### 7. Review business-logic security

Do not stop at known vulnerability patterns.

Ask:

- Can a user achieve an outcome the product rules say should be impossible?
- Can the same action be performed twice?
- Can one user affect another user's state?
- Can a privileged actor rewrite supposedly permanent facts?
- Can fees be bypassed or manipulated?
- Can off-chain consumers misunderstand what the on-chain record actually proves?
- Does the contract prove existence only, or does the surrounding product incorrectly imply identity, ownership, authenticity, authorship, consent, or legal validity?
- Can front-running change who appears to have submitted something?
- Are timestamps being described more precisely than blockchain timestamps support?

This section is mandatory for simple contracts. Small contracts often fail through assumptions rather than complex code.

## Special checks for proof / timestamp contracts

When auditing contracts that record document or data hashes, specifically verify:

- whether the same hash can be registered more than once
- whether first-seen or latest-seen semantics are intended
- whether the submitter address is meaningful or merely the calling platform
- whether delegated/platform submissions distinguish platform from end user
- whether the contract claims more than it proves
- whether raw personal data is stored on-chain unnecessarily
- whether low-entropy personal data can be brute-forced from an unsalted hash
- whether a salted commitment or other construction is more appropriate for sensitive/guessable metadata
- whether immutable on-chain commitments create technical tension with later erasure requirements; flag this as a design/privacy issue, not a legal conclusion
- whether metadata should be hashed instead
- whether hash algorithm and input canonicalization are documented
- whether users can verify files independently
- whether chain reorganizations/finality assumptions are relevant
- whether the fee can be changed and by whom
- whether withdrawals can fail or be abused
- whether overpayments are accepted, refunded, or intentionally retained
- whether events alone are sufficient or direct state lookup is required
- whether batch submissions preserve individual proof semantics

A timestamped hash generally proves that a particular hash was included on-chain no later than the relevant block, subject to the chain's finality/reorg model and the timestamp semantics of that chain. `block.timestamp` is proposer-supplied within protocol rules and should not be described as a perfectly precise wall-clock timestamp. The proof does not establish how long before that block the underlying document existed. It also does not by itself prove authorship, ownership, identity, authenticity of the underlying content, or the legal truth of its contents.

## Severity model

Rate severity using both impact and likelihood.

| Likelihood \\ Impact | Low impact | Medium impact | High impact | Catastrophic impact |
|---|---|---|---|---|
| Unlikely | Informational / Low | Low | Medium | Medium |
| Plausible | Low | Medium | High | High |
| Likely | Medium | High | High | Critical |

Then apply judgment based on exploit prerequisites, attacker capability, affected assets/users, reversibility, and detectability.

Owner/admin centralization is not automatically a High finding. Rate it based on what the privileged actor can actually do, whether the power is disclosed and intended, whether a timelock/multisig is expected, and the impact of key compromise or abuse.

Use these levels:

### Critical
Direct loss of substantial funds, permanent protocol takeover, arbitrary asset theft, or catastrophic corruption reachable under realistic conditions.

### High
Serious exploitability or privilege bypass with major financial, integrity, or availability impact.

### Medium
Material security or correctness issue requiring plausible preconditions, limited impact, or meaningful business-logic failure.

### Low
Limited-impact weakness, defense-in-depth issue, edge case, or operational risk.

### Informational
Code quality, gas, observability, documentation, or hardening improvement without a concrete security impact.

Do not inflate severity to make the report look substantial.

## Finding format

Every confirmed finding should contain:

```text
ID:
Title:
Severity:
Location:
Status:
Classification:

Allowed initial Status values:
- Open
- Acknowledged
- Confirmed by test
- Needs confirmation

Allowed Classification values:
- Confirmed finding
- Likely issue requiring confirmation
- Design consideration
- Tool false positive

Description:
What the code does and why it matters.

Attack / failure scenario:
A concrete sequence showing how the issue can occur.

Impact:
What can actually go wrong.

Evidence:
Relevant code, test result, analyzer result, or execution trace.

Recommendation:
The smallest practical fix.

Suggested patch:
Code where useful.
```

Use exact `file:line` references whenever files are available.

Distinguish:

- Confirmed finding
- Likely issue requiring confirmation
- Design consideration
- False positive from tooling

Never present a theoretical pattern as an exploitable vulnerability without connecting it to the actual code.

## Final report

Keep the report proportional to the target. A tiny standalone contract should receive a concise report; mark irrelevant sections N/A rather than padding the report.

Return the audit in this order:

### 1. Executive summary

Include:

- contracts reviewed
- commit/hash or version if known
- toolchain used
- tests run
- overall scope
- count of findings by severity

Do not issue a meaningless score such as "95/100 secure."

Do not say "fully secure," "100% safe," or "audit passed."

A suitable conclusion is:

> No Critical or High severity issues were identified within the reviewed scope. This does not guarantee the absence of vulnerabilities.

### 2. System overview

Briefly explain:

- what the contract does
- privileged actors
- assets at risk
- important trust assumptions

### 3. Findings table

```text
| ID | Severity | Finding | Status |
|----|----------|---------|--------|
```

### 4. Detailed findings

Use the finding format above.

### 5. Tests, tools, installations, and audit artifacts

State the exact commands run and whether each succeeded.

Also list any audit tooling installed during the review, including whether the installation was project-local, isolated, or user-level. If nothing was installed, say so.

Example:

```text
Tool installation:
pipx install slither-analyzer  PASS
No global project dependencies changed.

Audit execution:
forge build                    PASS
forge test                     18/18 PASS
slither .                      2 results reviewed, 2 false positives
targeted exploit test          PASS / FAIL
fuzz tests                     10,000 runs PASS
```

Never claim a tool ran if it was unavailable.

State what happened to audit-only files: left in `test/audit/`, supplied as a patch, or removed.

### 6. Business-logic / trust observations

Explain important assumptions that are not necessarily vulnerabilities.

### 7. Deployment checklist

Give only project-specific steps. Typical items may include:

- deploy from intended admin/multisig
- verify source code on explorer
- confirm constructor parameters
- run tests against deployed bytecode where practical
- transfer ownership if intended
- confirm fee configuration
- publish contract address and chain ID
- preserve audit commit hash
- monitor privileged transactions

## Fix verification

If the developer supplies a patched version:

1. re-run compilation
2. re-run existing tests
3. re-run the exploit/failing test
4. re-run static analysis
5. check for regression
6. mark each finding `Resolved`, `Partially resolved`, or `Unresolved`

Do not mark an issue resolved from visual inspection alone when it can reasonably be tested.

## Guardrails

- Do not invent vulnerabilities.
- Do not treat linter warnings as security findings without analysis.
- Do not assume OpenZeppelin usage automatically makes a design safe.
- Do not ignore owner/admin risks.
- Do not recommend unnecessary complexity such as pausing, upgradeability, or multisigs for every contract; tie recommendations to actual risk.
- Do not encourage storing personal data, secrets, private keys, credentials, or confidential document contents on-chain.
- Do not expose private keys, seed phrases, API secrets, or environment secrets encountered during review. Redact them in output and flag the exposure.
- Do not make legal conclusions about whether an on-chain proof is admissible, legally binding, or sufficient evidence unless that question is separately researched for the relevant jurisdiction.
- Do not issue a security certification or guarantee.

## Fast mode for a single small contract

For a small standalone contract, still perform the following minimum:

1. Freeze scope (`git rev-parse HEAD`, `git status`) and inspect repo execution hooks/configuration.
2. Detect the available toolchain and, where already authorized, safely install missing core audit tools when worthwhile.
3. Compile it without modifying production configuration to force success.
4. Run existing tests only after reviewing executable config, lifecycle scripts, FFI, and secret/RPC exposure.
5. Run Slither when available or installable.
6. Map all external/public state-changing functions.
7. Review access control, value flows, signatures, token behavior, and EVM-version assumptions.
8. Review external calls, reentrancy, gas/DoS, duplicate/replay/front-running, MEV, and chain-specific behavior.
9. Review business-logic and trust assumptions.
10. Write at least one targeted test for every material concern.
11. Produce the standard findings report.

A short contract is not automatically a low-risk contract.

## Example trigger requests

Use this skill for requests such as:

- "Audit this Solidity contract."
- "Security review this smart contract before deployment."
- "Run Slither and fuzz this contract."
- "Find vulnerabilities in my Foundry project."
- "Check whether this payment contract is safe."
- "Audit this proof-of-existence contract."
- "Review this contract and give me an audit report."
