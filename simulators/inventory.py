"""Simulador de inventario: Asset + AssetIdentifier (QR/TAG equivalentes) + Observation.

Demuestra D3 (identificadores equivalentes) y ADR-0017 (asset_id explícito).
"""
import argparse
import json

from contracts.validate import validate
from simulators import common


def generate(asset_id=common.ASSET_ID, seq=1):
    asset = {
        "schema_version": common.SCHEMA_VERSION,
        "tenant_id": common.TENANT_ID,
        "id": asset_id,
        "name": f"Tablero eléctrico {asset_id}",
        "category": "electrical",
        "location": common.point(-70.65, -33.45),
        "created_at": common.FIXED_TIME,
        "updated_at": None,
    }

    # dos identificadores equivalentes del MISMO activo (D3)
    identifiers = [
        {
            "schema_version": common.SCHEMA_VERSION,
            "tenant_id": common.TENANT_ID,
            "id": f"id-qr-{seq:04d}",
            "asset_id": asset_id,
            "type": "qr",
            "value": f"https://iotinkers.com/a/{asset_id}",
            "source": "platform-qr",
            "confidence": None,
            "created_at": common.FIXED_TIME,
        },
        {
            "schema_version": common.SCHEMA_VERSION,
            "tenant_id": common.TENANT_ID,
            "id": f"id-tag-{seq:04d}",
            "asset_id": asset_id,
            "type": "tag",
            "value": f"PLACA-{asset_id}",
            "source": "client-plate",
            "confidence": None,
            "created_at": common.FIXED_TIME,
        },
    ]

    observation = {
        "schema_version": common.SCHEMA_VERSION,
        "tenant_id": common.TENANT_ID,
        "id": f"obs-inv-{seq:04d}",
        "asset_id": asset_id,
        "session_id": None,
        "media_item_id": None,
        "type": "note",
        "value": "Equipo registrado por simulador",
        "unit": None,
        "observed_at": common.FIXED_TIME,
        "form_response_id": None,
        "created_at": common.FIXED_TIME,
    }

    validate("asset", asset)
    for i in identifiers:
        validate("asset-identifier", i)
    validate("observation", observation)
    return {"asset": asset, "identifiers": identifiers, "observation": observation}


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--asset-id", default=common.ASSET_ID)
    args = ap.parse_args()
    print(json.dumps(generate(args.asset_id), indent=2))


if __name__ == "__main__":
    main()
