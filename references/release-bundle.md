# Reproducible release packaging

Use only after the lifecycle release gate is satisfied. The bundle is consumed by a separate deployer; it contains no keys and performs no broadcast.

## Build procedure

1. Create a clean-room copy containing only frozen sources, pinned dependencies/remappings and recorded configuration.
2. Rebuild with the exact compiler, optimizer and EVM settings. For Foundry, use a reviewed equivalent of:

```text
forge clean
forge build --force --build-info
forge test -vvv
forge inspect <path:Contract> abi --json
forge inspect <path:Contract> bytecode
forge inspect <path:Contract> deployedBytecode
```

3. Preserve the compiler standard-JSON input/build-info and the contract artifact. Reject unlinked library placeholders; do not describe unlinked creation bytecode as deployable.
4. ABI-encode the exact approved constructor values with the reviewed toolchain. Concatenate creation bytecode and constructor encoding to obtain init code; hash both.
5. Compare clean-room ABI and bytecode to the audited candidate. Account only for compiler-recorded link and immutable references—never blanket-replace byte ranges.
6. Canonicalize and checksum the bundle as specified by the lifecycle reference.

If a command or artifact format is unavailable in the installed tool version, record the exact missing artifact and reason. Do not silently omit it or claim `deploymentReady: true`.

## Required bundle

```text
release/
├── sources/
├── deployment-manifest.schema.json
├── abi.json
├── creation-bytecode.hex
├── deployed-bytecode.hex
├── compiler-input.json
├── compiler-settings.json
├── build-artifact.json
├── constructor-schema.json
├── deployment-values.json
├── constructor-args.hex
├── init-code.hex
├── deployment-manifest.json
├── checksums.sha256
├── SPEC.md
├── traceability.json
├── remediation-history.md
└── audit-report.md
```

Copy [deployment-manifest.schema.json](deployment-manifest.schema.json) into the bundle and validate `deployment-manifest.json` against it. Use schema version `1.0.0`; [deployment-manifest.example.json](deployment-manifest.example.json) is deployment-ready, while [deployment-manifest.not-ready.example.json](deployment-manifest.not-ready.example.json) shows a valid parameterized build. The manifest is the normative machine interface; compiler input follows Solidity standard JSON, ABI follows the Solidity ABI JSON format, and framework build artifacts remain opaque evidence identified by path and hash. Run `scripts/test_manifest_schema.py` after schema changes; its intentionally invalid fixture must be rejected.

The manifest must define `deploymentReady` as a boolean. It may be `true` only when all required artifacts and exact human-approved constructor values exist, the clean-room comparison passed, every Critical/High is `Resolved`, and every Medium/Low is `Resolved` or has recorded human `Accepted risk` evidence. Otherwise it must be `false` with `missingArtifacts` and `limitations` arrays.

Use UTF-8/LF, lowercase `0x`-prefixed hex without internal whitespace, deterministic sorted-key JSON, normalized relative paths and sorted checksum entries. Exclude `checksums.sha256` from itself. Treat timestamps as provenance, not compiler inputs.

The separate deployer must validate the manifest schema and reject unknown schema versions, any checksum, chain ID, constructor value/encoding, init-code or bytecode mismatch, or any release-state rule inconsistent with `deploymentReady`.
