# Evidence-led testing matrix

Use this matrix to plan an audit. Select tests based on the system's reachable behavior and threat model. Mark irrelevant rows `Not applicable` with a short reason; do not add empty test categories merely to make a report look complete.

| Area | Minimum question | Useful evidence when applicable |
|---|---|---|
| Build and compiler | Does the frozen source compile with the declared compiler, optimizer, EVM version, and remappings? | Reproducible build command, compiler output, metadata |
| Existing unit tests | Do reviewed project tests pass without unsafe hooks or live credentials? | Test output and inspected configuration |
| Boundary and input validation | Are zero, min/max, malformed, duplicate, expired, and unexpected values handled as intended? | Focused unit/fuzz tests |
| Access control | Can each privileged transition be executed only by intended roles, including initialization and ownership changes? | Negative tests for every privileged entry point |
| Reentrancy and callbacks | Can external calls or token hooks re-enter before invariants are restored? | Malicious receiver/token tests and traces |
| Value transfer and accounting | Can fees be bypassed, overpaid, trapped, double-counted, rounded, or withdrawn incorrectly? | Balance assertions, accounting invariants, adversarial tokens |
| Fuzzing | Do user-controlled values preserve stated invariants across a meaningful input range? | Run count, seed where useful, invariant results |
| Stateful invariants | Can realistic action sequences violate persistent accounting, authorization, uniqueness, or solvency? | Handler-based invariant tests |
| Static analysis | Do analyzer signals reproduce against the actual source? | Command, tool version, triage of each result |
| Signatures and replay | Are signer, nonce, deadline, domain, chain, fork, and ERC-1271 behavior correct? | Valid/invalid signature and replay tests |
| Token integrations | Are no-return, fee-on-transfer, rebasing, blacklist, callback, decimal, and allowance-reset behaviors handled? | Mock adversarial token tests |
| MEV and ordering | Can front-running, back-running, sandwiching, censorship, or sequencing change attribution or value? | Competing-transaction tests or explicit model |
| Gas and denial of service | Can attacker-controlled growth, loops, returndata, cleanup, or recipient behavior block progress? | Gas measurements and failure-path tests |
| Upgradeability | Are initializers, implementation state, authorization, proxy type, and storage layout safe? | Initialization tests and storage-layout diff |
| Chain and EVM assumptions | Are timestamp, block number, finality, precompiles, opcodes, and fork features valid on each target chain? | Explicit chain/EVM matrix |
| Business logic abuse | Can a user obtain an outcome the documented product rules prohibit? | Threat scenarios and targeted exploit tests |
| Configuration and deployment | Are constructor parameters, roles, optimizer/EVM settings, libraries, scripts, and secrets safe? | Reviewed configuration and deployment checklist |
| Deployed bytecode | Does deployed code and proxy state match the frozen audited build? | Chain ID, address, bytecode verification, implementation/admin state |

## Reporting

For each applicable area record:

```text
Status: Pass / Fail / Not applicable / Not tested
Evidence: exact command, test, trace, file:line, or artifact
Limitations: missing tooling, absent specification, chain not supplied, or other constraint
```

A passing test establishes only the property exercised under the tested assumptions. Coverage percentages and clean analyzer output do not establish security.
