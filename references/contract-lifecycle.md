# Conversation-to-contract lifecycle

Use this reference only when the user asks to create, redesign, or substantially extend a Solidity/EVM contract. The audit-only workflow does not require it.

## 1. Convert conversation into a contract brief

Extract requirements from the entire relevant conversation. Distinguish:

- facts and explicit user choices
- reasonable implementation assumptions
- unresolved choices that materially change assets, authority, compatibility, or user outcomes
- prohibited or out-of-scope behavior

Capture at least:

| Area | Required decision |
|---|---|
| Purpose | What on-chain outcome the contract must produce |
| Actors | Users, owner, admins, guardians, operators, relayers, external contracts |
| Assets | Native currency, tokens, NFTs, records, permissions, or no assets |
| State and lifecycle | Creation, transitions, terminal states, deletion/immutability, duplicates |
| Authorization | Who may perform each state-changing action and how roles change |
| Value rules | Fees, refunds, withdrawals, accounting, limits, rounding, recipient behavior |
| Invariants | Conditions that must always hold, including cross-user isolation and solvency |
| Ordering | Front-running, replay, deadlines, first/latest semantics, MEV assumptions |
| Failure behavior | Reverts, partial progress, recovery, paused or emergency behavior if justified |
| Integrations | Tokens, oracles, bridges, callbacks, signatures, wallets, off-chain services |
| Administration | Upgradeability, ownership transfer, timelocks, emergency powers, renunciation |
| Chain target | Chain IDs, native assets, supported EVM fork, finality and timestamp assumptions |
| Privacy and claims | Public data, commitments, identity assumptions, and what the contract does not prove |
| Deployment inputs | Constructor parameters and intended initial/operational owner |

Do not manufacture requirements merely to fill the table. Mark irrelevant areas `Not applicable` with a reason.

## 2. Resolve material ambiguity

Ask a consolidated question when the conversation does not determine a choice that could materially affect funds, permissions, permanence, interoperability, legal/product claims, or deployment compatibility. Typical blocking choices include:

- who can mint, withdraw, upgrade, pause, destroy, or alter records
- whether funds are custodial and who ultimately receives them
- whether duplicate, first-seen, latest-seen, or per-user behavior is intended
- whether upgradeability or emergency powers are actually required
- target chains and operational ownership
- token/oracle assumptions that define accounting

Do not block on cosmetic names or low-impact defaults. Record such defaults as assumptions.

## 3. Freeze the specification before release implementation

Write `SPEC.md` or an equivalent user-visible specification containing:

1. purpose and non-goals
2. actors and trust model
3. external/public functions and authorization
4. state transitions
5. value flows and accounting rules
6. explicit invariants
7. events and off-chain observability
8. failure and edge-case behavior
9. chain/EVM assumptions
10. constructor and deployment configuration
11. privacy, evidentiary, and operational limitations where applicable
12. acceptance tests stated as observable behavior

A contract is **high impact** when it can hold or move value, grant privileged powers, create irreversible records or permissions, govern another system, or become immutable after deployment. Obtain user confirmation of its material product choices before treating the specification as approved. If the user has already made those choices clearly and asked for immediate implementation, proceed and label remaining assumptions instead of repeating questions.

The specification is the source of product truth. Code comments and tests may elaborate but must not silently contradict it.

## 4. Design the smallest suitable system

- Prefer a non-upgradeable contract unless the specification requires upgradeability and its authority model is accepted.
- Prefer established, pinned libraries for security-sensitive primitives when their dependency cost is justified.
- Avoid adding pausing, arbitrary admin calls, token recovery, role hierarchies, or renunciation by habit.
- Minimize privileged powers and document every retained power.
- Separate facts recorded on-chain from claims the contract cannot establish.
- Select and pin the compiler, EVM version, optimizer settings, dependencies, and remappings.
- Verify that each target chain supports the selected EVM version before release.

For a new standalone project, prefer a minimal Foundry layout unless the user requests another framework or the surrounding project already establishes one:

```text
src/
test/
script/          optional; must never auto-broadcast
audit/
foundry.toml
SPEC.md
README.md
LICENSE          when requested or established by the project
```

## 5. Implement from acceptance properties

Before or alongside implementation, translate each material rule into one or more of:

- positive unit test
- negative authorization test
- boundary test
- fuzz property
- stateful invariant
- adversarial integration test
- deployment/configuration assertion

Every privileged external entry point needs a negative authorization test. Every value-moving path needs balance and failure-path assertions. Every persistent business invariant needs fuzz or stateful coverage when practical.

Maintain a traceability table:

```text
Requirement or invariant | Source location | Test evidence | Status
```

Compilation success is the start of verification, not completion.

## 6. Audit the implementation

Apply the complete audit workflow in `SKILL.md`, including hostile-repository checks, manual business-logic review, the evidence-led testing matrix, static-analysis triage, dependency/configuration review, and standards mapping where useful.

Audit against both:

- implementation security: whether the code contains an exploitable or correctness defect
- specification security: whether correctly implemented product rules still permit an unsafe or misleading outcome

Record the first specification-complete implementation as an auditable candidate before remediation. Preserve its source hash or commit, the failing test/trace, and a patch or diff to the corrected candidate. Do not erase the fact that a defect was found simply because the same workflow later fixed it.

## 7. Remediate and repeat

For each confirmed finding:

1. preserve the finding, severity, evidence, and affected requirement
2. add a regression test or other reproducible check where practical
3. make the smallest specification-preserving change
4. rerun the full build and test suite
5. rerun affected fuzz/invariant properties and static analysis
6. inspect the diff for new authority, external calls, storage changes, or assumptions
7. mark the finding `Resolved`, `Partially resolved`, `Unresolved`, or `Accepted risk` with evidence

If a correction changes an approved product rule, update the specification only after the user accepts that change. Continue until release blockers are resolved or the user elects to stop with documented residual risk.

## 8. Release gate

A candidate is eligible for a frozen release only when:

- the scope and specification are fixed
- it builds reproducibly
- required tests pass
- analyzer results are triaged rather than merely absent
- every Critical or High finding has resolution exactly `Resolved`; these severities cannot be released as accepted risk
- every Medium or Low finding has resolution `Resolved` or `Accepted risk`; acceptance must identify the finding, rationale, named human decision-maker, and decision time
- no Critical, High, Medium, or Low finding remains `Open`, `Partially resolved`, or `Unresolved`
- compiler, EVM, optimizer, dependencies, constructor schema, and target chains are recorded
- source and generated artifacts correspond exactly
- a clean-room rebuild using only the frozen sources, recorded compiler input, and pinned dependencies reproduces the ABI and creation/runtime bytecode, subject only to documented link and immutable references
- the final audit report identifies limitations and checks not performed

Do not use `audit passed`, `fully secure`, or similar language. State the evidence and residual risk.

## 9. Frozen release bundle

Follow [release-bundle.md](release-bundle.md). List every artifact that could not be produced and why. Never skip missing artifacts silently or set `deploymentReady: true` without satisfying that reference.

## 10. Final handoff

Explain:

- what was requested and what assumptions were made
- where the specification, source, tests, `audit/audit-report.md`, and release bundle are located
- findings discovered and their final status
- exact verification performed and omitted
- breaking ABI/storage changes
- residual owner, chain, integration, privacy, and operational risks
- the source/bytecode hashes the deployer must enforce

If the release bundle could not be generated, provide the reason and do not describe the project as deployment-ready.
