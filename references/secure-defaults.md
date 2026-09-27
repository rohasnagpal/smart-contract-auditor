# Secure creation defaults

Apply these only when consistent with the approved specification and target chain:

- pin an exact released Solidity compiler and explicitly select the target EVM fork
- pin all dependencies and remappings; avoid floating Git branches or package ranges
- prefer audited library primitives over custom cryptography, token wrappers or role systems
- use OpenZeppelin 5.x only when compatible and pin the exact release; do not assume its use makes the design safe
- prefer `Ownable2Step` or an equivalent acceptance flow when transferable single-owner administration is required
- prefer custom errors for stable, gas-efficient reverts
- use `SafeERC20` for external ERC-20 interactions when token behavior is not strictly controlled
- prefer claimable/pull payments where a recipient revert must not block unrelated progress
- use checks-effects-interactions and add a reentrancy guard when invariants still permit harmful re-entry
- document external/public functions and material assumptions with NatSpec
- emit events for critical state and authority transitions
- reject invalid zero addresses and invalid value boundaries where the specification requires them
- avoid upgradeability, pausing, arbitrary calls and recovery powers unless justified and accepted

Defaults are not substitutes for threat modeling. Record deviations and their rationale.
