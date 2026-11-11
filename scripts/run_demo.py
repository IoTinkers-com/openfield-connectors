"""Demo end-to-end: genera la salida de los 4 simuladores y la ingiere en la plataforma.

Uso: python scripts/run_demo.py   (con openfield-platform corriendo en localhost:8000)
"""
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent.parent))

import httpx

from simulators import inventory, session_replay, telemetry, thermal

BASE = "http://localhost:8000"


def post(entity, doc):
    r = httpx.post(f"{BASE}/ingest/{entity}", json=doc, timeout=10)
    print(f"{entity:16s} {r.status_code} {r.json()}")


def main():
    for level, seq in (("T0", 1), ("T2", 2)):
        out = thermal.generate(level=level, seq=seq)
        post("thermal-capture", out["thermal-capture"])
        post("media-item", out["media-item"])

    inv = inventory.generate(asset_id="asset-001")
    post("asset", inv["asset"])
    for i in inv["identifiers"]:
        post("asset-identifier", i)
    post("observation", inv["observation"])

    replay = session_replay.generate()
    post("session", replay["session"])
    for m in replay["media-items"]:
        post("media-item", m)

    for o in telemetry.generate(n=3):
        post("observation", o)


if __name__ == "__main__":
    main()
