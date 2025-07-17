from __future__ import annotations

"""Simple ChatOps UI using LocalGPTAssistant."""

from PyQt5.QtWidgets import (
    QWidget, QVBoxLayout, QTextEdit, QLineEdit, QPushButton, QHBoxLayout,
    QMessageBox
)
from PyQt5.QtCore import Qt

from offline_gpt import LocalGPTAssistant


class ChatOpsUI(QWidget):
    def __init__(self, parent=None):
        super().__init__(parent)
        self.assistant = LocalGPTAssistant()
        self._setup_ui()

    def _setup_ui(self) -> None:
        layout = QVBoxLayout(self)
        self.chat_history = QTextEdit()
        self.chat_history.setReadOnly(True)
        layout.addWidget(self.chat_history)

        input_layout = QHBoxLayout()
        self.input = QLineEdit()
        self.input.returnPressed.connect(self.on_send)
        send_btn = QPushButton("Send")
        send_btn.clicked.connect(self.on_send)
        input_layout.addWidget(self.input)
        input_layout.addWidget(send_btn)
        layout.addLayout(input_layout)

    def on_send(self) -> None:
        text = self.input.text().strip()
        if not text:
            return
        self.chat_history.append(f"<b>You:</b> {text}")
        self.input.clear()
        try:
            reply = self.assistant.generate(text)
        except Exception as e:
            QMessageBox.critical(self, "GPT Error", str(e))
            return
        self.chat_history.append(f"<b>Assistant:</b> {reply}")

