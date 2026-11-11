# openfield-connectors

Adaptadores a dispositivos/sistemas externos + `simulators/` de OpenField (IoTinkers).
**Fase 0:** los 4 simuladores que emiten el contrato canónico y son las pruebas de contrato
de los adaptadores reales.

## Simuladores (Fase 0)
| Módulo | Qué emite | Contrato |
| --- | --- | --- |
| `simulators/thermal.py` | `ThermalCapture` T0/T1/T2 + `MediaItem` | D1 |
| `simulators/inventory.py` | `Asset` + `AssetIdentifier` (QR/TAG) + `Observation` | D3, ADR-0017 |
| `simulators/session_replay.py` | `Session` + `MediaItem` (ruta GPX/sintética) | D2, D4 |
| `simulators/telemetry.py` | `Observation` (estilo MQTT/SensorThings) | D9 |

Cada uno expone `generate(...)` (determinista) y un CLI que imprime JSON.

## Uso
```sh
python -m simulators.thermal --level T2        # imprime el documento
python scripts/run_demo.py                      # ingiere todo en la plataforma (localhost:8000)
```

## Tests y contrato
```sh
python scripts/validate_schemas.py   # valida los ejemplos de schemas/
pytest                               # pruebas de contrato (simuladores)
```

## Principio
Un conector real (Fase 2) es aceptable solo si pasa las mismas pruebas que su simulador.
