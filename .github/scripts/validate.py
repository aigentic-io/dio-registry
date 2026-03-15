"""Validate model_registry.json against the model entry schema.

spec_model is skipped — it serves as a human-readable template, not a real entry.
"""
import json
import sys
from pathlib import Path

import jsonschema

SKIP_MODELS = {"spec_model"}
ROOT = Path(__file__).parent.parent.parent
SCHEMA_PATH = ROOT / ".github" / "schemas" / "model_registry.schema.json"
REGISTRY_PATH = ROOT / "model_registry.json"

schema = json.loads(SCHEMA_PATH.read_text())
registry = json.loads(REGISTRY_PATH.read_text())

errors = []
validated = 0

for key, model in registry.get("models", {}).items():
    if key in SKIP_MODELS:
        continue
    try:
        jsonschema.validate(instance=model, schema=schema)
        validated += 1
    except jsonschema.ValidationError as e:
        errors.append(f"  [{key}] {e.path}: {e.message}")

if errors:
    print(f"Schema validation failed ({len(errors)} error(s)):", file=sys.stderr)
    for err in errors:
        print(err, file=sys.stderr)
    sys.exit(1)

print(f"OK — {validated} model(s) validated successfully.")
