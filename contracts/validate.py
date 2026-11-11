"""Pruebas de contrato: carga de los schemas canónicos y validación.

Es el MISMO arnés que usarán los adaptadores reales (D10 · ADR-0010): un conector
es aceptable solo si emite documentos que validan contra estos schemas.
"""
import json
from pathlib import Path

from jsonschema import Draft202012Validator

SCHEMAS_DIR = Path(__file__).resolve().parent.parent / "schemas"

ENTITY_TYPES = [
    "session",
    "device",
    "asset",
    "asset-identifier",
    "media-item",
    "thermal-capture",
    "observation",
    "transcript",
    "form-template",
    "form-response",
    "sync-event",
]


def load_schemas():
    schemas = {}
    for path in sorted(SCHEMAS_DIR.glob("*.schema.json")):
        stem = path.name.split(".")[0]
        schemas[stem] = json.loads(path.read_text(encoding="utf-8"))
    return schemas


SCHEMAS = load_schemas()


def validate(entity_type: str, doc: dict) -> dict:
    schema = SCHEMAS.get(entity_type)
    if schema is None:
        raise KeyError(f"entity_type desconocido: {entity_type}")
    Draft202012Validator(schema).validate(doc)
    return doc
