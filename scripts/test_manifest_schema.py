#!/usr/bin/env python3
"""Validate positive fixtures and prove the invalid release fixture is rejected."""

import json
from pathlib import Path

import jsonschema


ROOT = Path(__file__).resolve().parents[1]
REFERENCES = ROOT / "references"


def load(name: str) -> object:
    return json.loads((REFERENCES / name).read_text(encoding="utf-8"))


schema = load("deployment-manifest.schema.json")
jsonschema.validate(load("deployment-manifest.example.json"), schema)
jsonschema.validate(load("deployment-manifest.not-ready.example.json"), schema)

try:
    jsonschema.validate(load("deployment-manifest.invalid.example.json"), schema)
except jsonschema.ValidationError:
    print("manifest schema fixtures passed")
else:
    raise SystemExit("invalid deployment-ready manifest unexpectedly passed")
