from PyQt5.QtWidgets import QDialog

from app_new_ui import LoginDialog, Role


class DummyAuth:
    def verify_user(self, username, password):
        if username == "admin" and password == "secret":
            return Role.ADMIN
        return None


def test_login_success(qtbot):
    dialog = LoginDialog(DummyAuth())
    qtbot.addWidget(dialog)
    dialog.username_input.setText("admin")
    dialog.password_input.setText("secret")
    dialog.handle_login()
    assert dialog.result() == QDialog.Accepted
    assert dialog.user_role == Role.ADMIN


def test_login_failure(qtbot):
    dialog = LoginDialog(DummyAuth())
    qtbot.addWidget(dialog)
    dialog.username_input.setText("admin")
    dialog.password_input.setText("bad")
    dialog.handle_login()
    assert dialog.user_role is None
    assert dialog.status_label.text() != ""
