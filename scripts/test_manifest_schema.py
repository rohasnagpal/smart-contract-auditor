#!/usr/bin/env python3
"""Exercise the manifest schema and its cross-field release invariants."""

from copy import deepcopy
import json
from pathlib import Path

from jsonschema import Draft202012Validator


ROOT = Path(__file__).resolve().parents[1]
REFERENCES = ROOT / "references"


def load(name: str) -> dict:
    return json.loads((REFERENCES / name).read_text(encoding="utf-8"))


def semantic_errors(document: dict) -> list[str]:
    """Check relationships JSON Schema cannot express with dynamic file keys."""
    errors: list[str] = []
    files = document.get("files", {})

    for source in document.get("sources", []):
        if files.get(source["path"]) != source["sha256"]:
            errors.append(f"source hash is absent or inconsistent: {source['path']}")

    contract = document.get("contract", {})
    build = document.get("build", {})
    constructor = document.get("constructor", {})
    relationships = [
        (contract.get("sourcePath"), contract.get("sourceSha256")),
        ("compiler-input.json", build.get("compilerInputSha256")),
        ("build-artifact.json", build.get("artifactSha256")),
        ("creation-bytecode.hex", build.get("creationBytecodeSha256")),
        ("deployed-bytecode.hex", build.get("deployedBytecodeSha256")),
        ("constructor-args.hex", constructor.get("encodedArgsSha256")),
        ("init-code.hex", constructor.get("initCodeSha256")),
    ]
    for path, expected_hash in relationships:
        if expected_hash is not None and path in files and files[path] != expected_hash:
            errors.append(f"hash is inconsistent: {path}")

    if document.get("deploymentReady"):
        for path, expected_hash in relationships:
            if expected_hash is not None and files.get(path) != expected_hash:
                errors.append(f"ready release lacks matching hash: {path}")

    if document.get("target", {}).get("evmVersion") != build.get("evmVersion"):
        errors.append("target and compiler EVM versions differ")

    return errors


schema = load("deployment-manifest.schema.json")
Draft202012Validator.check_schema(schema)
validator = Draft202012Validator(schema, format_checker=Draft202012Validator.FORMAT_CHECKER)
ready = load("deployment-manifest.example.json")
not_ready = load("deployment-manifest.not-ready.example.json")


def validation_errors(document: dict) -> list[str]:
    errors = [error.message for error in validator.iter_errors(document)]
    errors.extend(semantic_errors(document))
    return errors


def assert_valid(name: str, document: dict) -> None:
    errors = validation_errors(document)
    if errors:
        raise SystemExit(f"{name} unexpectedly failed: {errors}")


def assert_invalid(name: str, document: dict) -> None:
    if not validation_errors(document):
        raise SystemExit(f"{name} unexpectedly passed")


assert_valid("deployment-ready fixture", ready)
assert_valid("not-ready fixture", not_ready)

mutations: list[tuple[str, dict]] = []

critical_accepted = deepcopy(ready)
critical_accepted["findings"] = [{
    "id": "TEST-01",
    "severity": "Critical",
    "classification": "Confirmed finding",
    "verification": "Confirmed by test/trace",
    "resolution": "Accepted risk",
    "acceptance": {
        "decisionMaker": "release owner",
        "decidedAt": "2026-09-27T00:00:00Z",
        "rationale": "targeted negative fixture"
    }
}]
mutations.append(("ready Critical accepted risk", critical_accepted))

missing_required_file = deepcopy(ready)
del missing_required_file["files"]["abi.json"]
mutations.append(("ready missing required file", missing_required_file))

failed_rebuild = deepcopy(ready)
failed_rebuild["cleanRoomRebuild"]["result"] = "Fail"
mutations.append(("ready failed clean-room rebuild", failed_rebuild))

missing_constructor_value = deepcopy(ready)
del missing_constructor_value["constructor"]["parameters"][0]["value"]
mutations.append(("ready missing constructor value", missing_constructor_value))

reported_missing_artifact = deepcopy(ready)
reported_missing_artifact["missingArtifacts"] = ["abi.json"]
mutations.append(("ready non-empty missingArtifacts", reported_missing_artifact))

bad_date = deepcopy(ready)
bad_date["createdAt"] = "yesterday"
mutations.append(("invalid date-time", bad_date))

accepted_without_evidence = deepcopy(not_ready)
accepted_without_evidence["findings"][0].update({
    "severity": "Low",
    "classification": "Confirmed finding",
    "verification": "Code review",
    "resolution": "Accepted risk"
})
mutations.append(("accepted risk without evidence", accepted_without_evidence))

accepted_with_bad_date = deepcopy(not_ready)
accepted_with_bad_date["findings"][0].update({
    "severity": "Low",
    "classification": "Confirmed finding",
    "verification": "Code review",
    "resolution": "Accepted risk",
    "acceptance": {
        "decisionMaker": "release owner",
        "decidedAt": "yesterday",
        "rationale": "targeted negative fixture"
    }
})
mutations.append(("accepted risk with invalid decision date", accepted_with_bad_date))

unconfirmed_high = deepcopy(ready)
unconfirmed_high["findings"] = [{
    "id": "TEST-02",
    "severity": "High",
    "classification": "Potential issue",
    "verification": "Needs confirmation",
    "resolution": "Resolved"
}]
mutations.append(("ready unconfirmed High", unconfirmed_high))

missing_source = deepcopy(ready)
del missing_source["files"]["sources/Example.sol"]
mutations.append(("ready source absent from files", missing_source))

inconsistent_hash = deepcopy(ready)
inconsistent_hash["files"]["creation-bytecode.hex"] = "0" * 64
mutations.append(("inconsistent creation-bytecode hash", inconsistent_hash))

for mutation_name, mutation in mutations:
    assert_invalid(mutation_name, mutation)

print(f"manifest schema fixtures passed ({len(mutations)} targeted invalid mutations)")
