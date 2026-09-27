# Reproducible release packaging

Use only after the lifecycle release gate is satisfied. The bundle is consumed by a separate deployer; it contains no keys and performs no broadcast.

## Build procedure

1. Create a clean-room copy containing only frozen sources, pinned dependencies/remappings and recorded configuration. For a committed Git scope, a reviewed pattern is `git archive --format=tar <audited-commit>` extracted into a new `mktemp -d` directory; then restore only the pinned dependencies recorded by the manifest. Do not copy the working tree, `.env`, wallets or build outputs.
2. Rebuild with the exact compiler, optimizer and EVM settings. For Foundry, use a reviewed equivalent of:

```text
forge clean
forge build --force --build-info
forge test -vvv
forge inspect <path:Contract> abi --json
forge inspect <path:Contract> bytecode
forge inspect <path:Contract> deployedBytecode
```

3. Preserve the compiler standard-JSON input from Foundry build-info and the contract artifact. `forge build --build-info` writes the compiler input under `out/build-info/`; select the entry corresponding to the audited artifact. `forge verify-contract --show-standard-json-input` may be used only as an offline extraction command when the installed version supports it and it does not contact a live service. Reject unlinked library placeholders; do not describe unlinked creation bytecode as deployable.
4. ABI-encode the exact approved constructor values using a reviewed command equivalent to `cast abi-encode "f(<constructor types>)" <values>`. Remove only the encoding's leading `0x`, append it to the canonical creation-bytecode hex, and prefix the combined init code with one `0x`. Compare the result to the compiler/toolchain output where available.
5. Compare clean-room ABI and bytecode to the audited candidate. Account only for compiler-recorded link and immutable references—never blanket-replace byte ranges.
6. Canonicalize JSON with a deterministic tool such as `jq -S`, normalize text as UTF-8/LF, normalize hex as lowercase `0x`-prefixed text with one trailing LF, then generate sorted checksums with `shasum -a 256`. Exclude `checksums.sha256` from itself.

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

Copy [deployment-manifest.schema.json](deployment-manifest.schema.json) into the bundle and validate `deployment-manifest.json` against it with JSON Schema draft 2020-12 format checking enabled. Use schema version `1.1.0`; [deployment-manifest.example.json](deployment-manifest.example.json) is deployment-ready, while [deployment-manifest.not-ready.example.json](deployment-manifest.not-ready.example.json) shows a valid parameterized build. The manifest is the normative machine interface; compiler input follows Solidity standard JSON, ABI follows the Solidity ABI JSON format, and framework build artifacts remain opaque evidence identified by path and hash. In addition to JSON Schema validation, enforce the cross-field hash relationships implemented by `scripts/test_manifest_schema.py`, including the dynamic requirement that every `sources[].path` appear in `files` with the same digest. Run that script after schema changes; each targeted invalid mutation must be rejected.

The manifest must define `deploymentReady` as a boolean. It may be `true` only when all required artifacts and exact human-approved constructor values exist, the clean-room comparison passed, every Critical/High is `Resolved`, and every Medium/Low is `Resolved` or has recorded human `Accepted risk` evidence. Otherwise it must be `false` with `missingArtifacts` and `limitations` arrays.

Each release bundle targets exactly one chain ID. A multi-chain project produces one independently approved bundle per chain.

Every SHA-256 field, including `files`, source, compiler input, artifact, bytecode, constructor encoding and init code, hashes the exact canonical file bytes present in the bundle. Use UTF-8/LF, lowercase `0x`-prefixed hex without internal whitespace and with one trailing LF, deterministic sorted-key JSON, normalized relative paths and sorted checksum entries. Exclude `checksums.sha256` from itself. Treat timestamps as provenance, not compiler inputs.

The separate deployer must validate the manifest schema and reject unknown schema versions, any checksum, chain ID, constructor value/encoding, init-code or bytecode mismatch, or any release-state rule inconsistent with `deploymentReady`.
