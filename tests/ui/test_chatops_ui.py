import pytest

chatops_ui = pytest.importorskip("chatops_ui")


def test_run_suggested_command(qtbot):
    ui = chatops_ui.ChatOpsUI()
    qtbot.addWidget(ui)
    ui.input.setText("test")
    ui.on_send()
    assert ui.chat_history.count() >= 1
