"""Helpers compartidos de los simuladores (deterministas)."""
TENANT_ID = "tenant-001"
DEVICE_ID = "dev-sim-001"
ASSET_ID = "asset-001"
SCHEMA_VERSION = "1.0"
FIXED_TIME = "2026-11-11T10:00:00Z"


def point(lon: float, lat: float) -> dict:
    return {"type": "Point", "coordinates": [lon, lat]}
