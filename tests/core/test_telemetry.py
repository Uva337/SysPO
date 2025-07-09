import pytest

telemetry = pytest.importorskip("telemetry")


def test_metrics_keys():
    data = telemetry.get_metrics()
    assert set(data.keys()) >= {"cpu_percent", "memory_percent"}
