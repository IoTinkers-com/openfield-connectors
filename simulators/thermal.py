"""Simulador de cámara térmica T0–T2 (D1 · ADR-0010).

Genera un `ThermalCapture` + el `MediaItem` térmico asociado, conforme al contrato
canónico: T0 (solo imagen con paleta, matriz nula), T1 (MLX90640 32x24), T2 (Lepton 3.5).
"""
import argparse
import json

from contracts.validate import validate
from simulators import common

LEVELS = {
    "T0": {"sensor_model": None, "resolution": None},
    "T1": {"sensor_model": "MLX90640", "resolution": {"width": 32, "height": 24}},
    "T2": {"sensor_model": "Lepton 3.5", "resolution": {"width": 160, "height": 120}},
}


def _matrix(width, height, base=25.0):
    return [[round(base + x * 0.1 + y * 0.2, 2) for x in range(width)] for y in range(height)]


def generate(level="T0", seq=1, asset_id=common.ASSET_ID, session_id="sess-sim-001"):
    if level not in LEVELS:
        raise ValueError(f"nivel inválido: {level}")
    cfg = LEVELS[level]
    media_id = f"media-thermal-{seq:04d}"
    thermal_id = f"thermal-{seq:04d}"

    thermal = {
        "schema_version": common.SCHEMA_VERSION,
        "tenant_id": common.TENANT_ID,
        "id": thermal_id,
        "media_item_id": media_id,
        "level": level,
        "sensor_model": cfg["sensor_model"],
        "resolution": cfg["resolution"],
        "emissivity": 0.95 if level != "T0" else None,
        "reflected_temperature_c": 22.0 if level != "T0" else None,
        "distance_m": 1.5 if level != "T0" else None,
        "temperature_matrix_c": None if level == "T0" else _matrix(cfg["resolution"]["width"], cfg["resolution"]["height"]),
        "rendered_image": {"href": f"https://picsum.photos/seed/{thermal_id}/400/300", "media_type": "image/jpeg"},
        "original_asset": {"href": f"/media/{thermal_id}.raw", "media_type": "application/octet-stream", "format": "radiometric"},
        "captured_at": common.FIXED_TIME,
    }

    media = {
        "schema_version": common.SCHEMA_VERSION,
        "tenant_id": common.TENANT_ID,
        "id": media_id,
        "session_id": session_id,
        "asset_id": asset_id,
        "type": "thermal",
        "captured_at": common.FIXED_TIME,
        "geometry": common.point(-70.65, -33.45),
        "assets": {"primary": {"href": f"https://picsum.photos/seed/{thermal_id}/400/300", "media_type": "image/jpeg"}},
        "thermal_capture_id": thermal_id,
        "transcript_id": None,
        "created_at": common.FIXED_TIME,
    }

    # el contrato: ambos documentos validan
    validate("thermal-capture", thermal)
    validate("media-item", media)
    return {"thermal-capture": thermal, "media-item": media}


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--level", default="T0", choices=["T0", "T1", "T2"])
    ap.add_argument("--seq", type=int, default=1)
    args = ap.parse_args()
    print(json.dumps(generate(args.level, args.seq), indent=2))


if __name__ == "__main__":
    main()
