# Tool bootstrap and execution safety

Inspect the project before running it. Check tool versions and relevant files such as `foundry.toml`, `hardhat.config.*`, package manifests/lockfiles, Python dependency files, `.env*`, `Makefile`, scripts and submodules.

Prefer the existing project toolchain. If a core tool is missing:

1. use a project-local or isolated installation
2. use an established official installation method
3. obtain host-required approval for network or external writes
4. never use `sudo` or alter global tooling without explicit need and authorization
5. never change production dependencies, compiler or configuration merely to make analysis pass
6. verify the installed version and record the command

For Python analyzers prefer `pipx` or a virtual environment under the host-designated temporary directory, not a hard-coded path. For Node projects inspect lifecycle scripts before `npm ci --ignore-scripts`; run scripts only after review.

Before Foundry tests, inspect FFI and every invoked command. Before Hardhat commands, inspect configuration because it executes code. Do not load repository secrets or use repository RPC URLs.

If installation is blocked, try one documented fallback, continue manually and mark the check `Not tested`. Never imply an unavailable tool ran.

Keep audit-only files in a documented scratch or `test/audit/` location and report whether they remain, were delivered, or were removed.
