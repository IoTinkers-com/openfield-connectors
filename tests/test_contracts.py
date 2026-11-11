from contracts.validate import validate
from simulators import inventory, session_replay, telemetry, thermal


def test_thermal_t0():
    out = thermal.generate(level="T0")
    tc = out["thermal-capture"]
    assert tc["level"] == "T0"
    assert tc["temperature_matrix_c"] is None


def test_thermal_t1_t2_matrix():
    for level, w, h in (("T1", 32, 24), ("T2", 160, 120)):
        tc = thermal.generate(level=level)["thermal-capture"]
        assert tc["temperature_matrix_c"] is not None
        assert tc["resolution"] == {"width": w, "height": h}
        assert len(tc["temperature_matrix_c"]) == h


def test_inventory_equivalent_identifiers():
    out = inventory.generate(asset_id="asset-001")
    ids = out["identifiers"]
    assert len(ids) == 2
    assert all(i["asset_id"] == "asset-001" for i in ids)
    assert {i["type"] for i in ids} == {"qr", "tag"}


def test_session_replay_geometry():
    out = session_replay.generate()
    assert out["session"]["id"].startswith("sess-sim-")
    assert len(out["media-items"]) == 3
    for m in out["media-items"]:
        assert m["geometry"]["type"] == "Point"


def test_telemetry_observation():
    obs = telemetry.generate(n=3)
    assert len(obs) == 3
    assert all(o["type"] == "measurement" for o in obs)
    assert all(o["observed_at"] for o in obs)


def test_contract_envelope_present_everywhere():
    """Todo documento emitido lleva el envolvente común (tenant_id, schema_version)."""
    outputs = []
    outputs.append(thermal.generate("T2")["thermal-capture"])
    outputs.append(thermal.generate("T2")["media-item"])
    outputs.append(inventory.generate()["asset"])
    outputs.append(inventory.generate()["identifiers"][0])
    outputs.append(inventory.generate()["observation"])
    outputs.append(session_replay.generate()["session"])
    outputs.append(session_replay.generate()["media-items"][0])
    outputs.extend(telemetry.generate(n=2))
    for doc in outputs:
        assert doc.get("tenant_id") == "tenant-001"
        assert doc.get("schema_version") == "1.0"
