# AGENTS.md — openfield-connectors

Adaptadores a dispositivos/sistemas externos + `simulators/` de OpenField (IoTinkers).

## Reglas
- Los **simuladores son las pruebas de contrato** de los adaptadores reales (D10 · ADR-0010):
  un conector real es aceptable solo si pasa las mismas pruebas que su simulador.
- Todo documento emitido valida contra los schemas canónicos de `schemas/` (via `contracts/validate.py`).
- Tecnologías propietarias (FLIR/Seek) se integran vía SDK/wrappers y se normalizan al contrato (ADR-0001).
- Nunca presentar el sistema como apto para atmósferas explosivas ni equipo de seguridad (ADR-0016).

## Terminado
- `python scripts/validate_schemas.py` pasa.
- `pytest` pasa.

## Referencias del plan
Paquete de planificación en `../openfield-planning/`: `DECISIONS.md`, `03-adr/`,
`04-esquemas/`, `05-estructura-repos.md`, `07-simulacion-y-pruebas.md`.
