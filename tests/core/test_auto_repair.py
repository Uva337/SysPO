import pytest

auto_repair = pytest.importorskip("auto_repair")


def test_rule_matching(tmp_path):
    sample = "rules:\n  - match: error\n    action: fix.sh"
    cfg = tmp_path / "auto_repair.yaml"
    cfg.write_text(sample)
    rules = auto_repair.load_rules(str(cfg))
    assert rules[0]["match"] == "error"
