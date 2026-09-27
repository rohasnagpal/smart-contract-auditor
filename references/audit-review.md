# Manual and business-logic review

Use this reference for every substantive audit. Select checks by reachable behavior and record irrelevant areas as `Not applicable` rather than inventing findings.

## System map

Map external/public entry points, state transitions, roles, storage, value flows, external calls, callbacks, signatures, integrations, initialization, upgrade paths, and deployment configuration. State what the system is intended to do before judging it.

## Review areas

### Authorization and administration

- missing or inconsistent authorization, unprotected initialization, privilege escalation
- unsafe ownership/role transfer, renunciation consequences, compromised-admin blast radius
- undisclosed or excessive admin powers, timelock/multisig assumptions
- negative authorization behavior for every privileged entry point

### External interaction and reentrancy

- ETH transfers, token hooks, callbacks, arbitrary calls, return values and returndata
- checks-effects-interactions, cross-function and read-only reentrancy
- gas griefing, malicious recipients, callback-driven state changes
- failure atomicity and availability when an integration reverts

### Value and accounting

- exact `msg.value`, overpayment/refund behavior, trapped value, withdrawals
- rounding, precision, fees, solvency, double claims, donation/accounting manipulation
- push versus pull payment design and recipient failure
- ERC-20 no-return behavior, fee-on-transfer, rebasing, blacklist/freeze, decimals and allowance resets
- ERC-4626 inflation, flash-loan manipulation, slippage and deadlines where relevant

### State, ordering and availability

- duplicate/overwrite/stale state, invalid transitions, cross-user interference
- front-running, replay, sequencing, censorship, MEV and transaction-order dependence
- unbounded loops, attacker-controlled growth, cleanup paths, O(n²) behavior
- gas-sensitive progress and calldata/returndata amplification

### Inputs, signatures and cryptography

- zero/min/max/malformed values and unsafe casts
- EIP-712 signer, nonce, deadline, domain, `chainId`, fork/cross-chain replay
- ERC-1271, `ecrecover(address(0))`, malleability and permit griefing
- `abi.encodePacked` collisions, predictable randomness, `tx.origin`, `blockhash`
- timestamp precision and finality assumptions

### Integrations and chain assumptions

- oracle manipulation/staleness, sequencer uptime, bridges and trust boundaries
- L2-specific block/timestamp semantics, precompiles and opcode/fork support
- compiler output versus explicitly selected EVM version on every target chain
- governance, timelocks, emergency roles and dependency behavior

### Upgradeability and EVM hazards

- initializer and implementation initialization, storage layout and upgrade authorization
- proxy/admin/beacon/UUPS assumptions and delegatecall hazards
- inline assembly, transient storage, unchecked blocks, storage references
- `selfdestruct` under target-fork semantics
- EOA-only assumptions such as `tx.origin == msg.sender` or `extcodesize == 0`

### Events and off-chain interpretation

- critical transitions emit accurate events with useful indexed fields
- indexers can reconstruct required facts and handle reorganizations
- interfaces and product language do not claim more than the on-chain state proves

## Business-logic questions

- Can a user obtain an outcome forbidden by the specification?
- Can an action occur twice, out of order, or on another user's state?
- Can a privileged actor rewrite supposedly permanent facts?
- Can fees, deadlines, accounting, attribution or eligibility be manipulated?
- Do correctly implemented rules remain unsafe under adversarial incentives?

Small contracts still require this analysis; their main risks are often semantic rather than syntactic.

## Proof and timestamp contracts

Additionally verify duplicate and first/latest/per-submitter semantics, platform-versus-user attribution, canonical hashing, independent verification, low-entropy commitments, personal-data exposure, finality/reorg handling, fee changes, overpayments, withdrawal failure, and event/state lookup.

A timestamped digest establishes only that the digest was included no later than the relevant finalized block under that chain's timestamp rules. It does not by itself prove authorship, ownership, identity, authenticity, consent, legal validity, or how long the underlying content existed beforehand.
