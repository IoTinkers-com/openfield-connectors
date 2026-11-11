"""Simulador de telemetría MQTT -> Observation (OGC SensorThings, D9).

Un tópico MQTT produce `Observation` con `observed_at` (= phenomenonTime). En Fase 0 se
generan documentos deterministas; el adaptador MQTT real (paho-mqtt) llega en Fase 2.
"""
import argparse
import json

from contracts.validate import validate
from simulators import common


def generate(n=3, asset_id=common.ASSET_ID):
    observations = []
    for i in range(n):
        obs = {
            "schema_version": common.SCHEMA_VERSION,
            "tenant_id": common.TENANT_ID,
            "id": f"obs-mqtt-{i + 1:04d}",
            "asset_id": asset_id,
            "session_id": None,
            "media_item_id": None,
            "type": "measurement",
            "value": round(40.0 + i * 0.5, 2),
            "unit": "degC",
            "observed_at": common.FIXED_TIME,
            "form_response_id": None,
            "created_at": common.FIXED_TIME,
        }
        validate("observation", obs)
        observations.append(obs)
    return observations


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--n", type=int, default=3)
    args = ap.parse_args()
    print(json.dumps(generate(args.n), indent=2))


if __name__ == "__main__":
    main()
