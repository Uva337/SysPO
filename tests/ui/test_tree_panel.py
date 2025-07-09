from PyQt5.QtCore import Qt
from PyQt5.QtWidgets import QTreeWidget

from app_new_ui import MainWindow, Role


class DummyAuth:
    def get_all_users(self):
        return []


def test_tree_build(qtbot, sample_commands_json, monkeypatch):
    monkeypatch.setattr("app_new_ui.COMMANDS_FILE", sample_commands_json)
    monkeypatch.setattr("app_new_ui.FAVORITES_FILE", "missing.json")
    window = MainWindow("tester", Role.OPERATOR, DummyAuth())
    qtbot.addWidget(window)
    tree = window.function_tree
    # Expect one command loaded from sample json
    iterator = tree.findItems("", Qt.MatchContains | Qt.MatchRecursive)
    assert len(iterator) >= 1
