from PyQt5.QtCore import Qt

from app_new_ui import MainWindow, Role


class DummyAuth:
    def get_all_users(self):
        return []


def test_run_command_button(qtbot, sample_commands_json, monkeypatch):
    monkeypatch.setattr("app_new_ui.COMMANDS_FILE", sample_commands_json)
    monkeypatch.setattr("app_new_ui.FAVORITES_FILE", "missing.json")
    window = MainWindow("tester", Role.OPERATOR, DummyAuth())
    qtbot.addWidget(window)
    window.nlu_input.setText("echo message")
    window.on_nlu_enter()
    assert window.current_intent == "test.echo"
