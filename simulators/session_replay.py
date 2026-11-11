"""Simulador de repetición de sesiones grabadas + rutas GPX (D2 · D4)."""
import argparse
import json
import xml.etree.ElementTree as ET

from contracts.validate import validate
from simulators import common

# Ruta sintética por defecto (Santiago): (lon, lat)
SYNTHETIC_ROUTE = [(-70.6500, -33.4500), (-70.6520, -33.4510), (-70.6540, -33.4520)]


def parse_gpx(path):
    """Extrae waypoints <trkpt lat lon> de un GPX (stdlib)."""
    ns = {"g": "http://www.topografix.com/GPX/1/1"}
    root = ET.parse(path).getroot()
    pts = []
    for trkpt in root.findall(".//g:trkpt", ns):
        pts.append((float(trkpt.attrib["lon"]), float(trkpt.attrib["lat"])))
    return pts


def generate(route=None, seq=1, asset_id=common.ASSET_ID):
    route = route or SYNTHETIC_ROUTE
    session_id = f"sess-sim-{seq:04d}"

    session = {
        "schema_version": common.SCHEMA_VERSION,
        "tenant_id": common.TENANT_ID,
        "id": session_id,
        "device_id": common.DEVICE_ID,
        "operator": "simulador",
        "asset_id": asset_id,
        "started_at": common.FIXED_TIME,
        "ended_at": None,
        "location": common.point(*route[0]),
        "device_capabilities": {"thermal_level": "T0", "gps": True, "audio": True},
        "consent": {"recorded": True, "method": "simulado"},
        "created_at": common.FIXED_TIME,
    }

    media_items = []
    for i, (lon, lat) in enumerate(route, start=1):
        media = {
            "schema_version": common.SCHEMA_VERSION,
            "tenant_id": common.TENANT_ID,
            "id": f"{session_id}-m{i:02d}",
            "session_id": session_id,
            "asset_id": asset_id,
            "type": "image",
            "captured_at": common.FIXED_TIME,
            "geometry": common.point(lon, lat),
            "assets": {"primary": {"href": f"/media/{session_id}-m{i:02d}.jpg", "media_type": "image/jpeg"}},
            "thermal_capture_id": None,
            "transcript_id": None,
            "created_at": common.FIXED_TIME,
        }
        media_items.append(media)

    validate("session", session)
    for m in media_items:
        validate("media-item", m)
    return {"session": session, "media-items": media_items}


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--gpx", default=None, help="archivo GPX (opcional)")
    args = ap.parse_args()
    route = parse_gpx(args.gpx) if args.gpx else SYNTHETIC_ROUTE
    print(json.dumps(generate(route=route), indent=2))


if __name__ == "__main__":
    main()
