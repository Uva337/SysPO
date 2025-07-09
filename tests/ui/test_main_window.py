from PyQt5.QtWidgets import QApplication

from app_new_ui import MainWindow, Role


class DummyAuth:
    def get_all_users(self):
        return []


def test_main_window_layout(qtbot, sample_commands_json, monkeypatch):
    monkeypatch.setattr("app_new_ui.COMMANDS_FILE", sample_commands_json)
    monkeypatch.setattr("app_new_ui.FAVORITES_FILE", "missing.json")
    window = MainWindow(username="tester", user_role=Role.OPERATOR, auth_manager=DummyAuth())
    qtbot.addWidget(window)
    assert window.main_stack.count() >= 3
    assert window.findChild(type(window.main_stack))
