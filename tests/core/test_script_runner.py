import platform
import subprocess

from command_templates import CommandTemplates
from sysadmin_actions import execute_intent


class DummyPopen:
    def __init__(self, *args, **kwargs):
        self.stdout_lines = ["done\n"]
        self.stderr_text = ""

    def poll(self):
        return 0

    @property
    def stdout(self):
        class S:
            def __init__(self, outer):
                self.outer = outer
            def readline(self):
                return outer.stdout_lines.pop(0) if outer.stdout_lines else ""
        outer = self
        return S(self)

    @property
    def stderr(self):
        class S:
            def __init__(self, outer):
                self.outer = outer
            def read(self):
                return outer.stderr_text
        outer = self
        return S(self)


def test_execute_intent(monkeypatch, sample_commands_json):
    ct = CommandTemplates()
    ct.load_from_json(sample_commands_json)
    outputs = []
    monkeypatch.setattr(subprocess, "Popen", lambda *a, **k: DummyPopen())
    monkeypatch.setattr(platform, "system", lambda: "Linux")
    execute_intent("test.echo", {"msg": "hi"}, ct, outputs.append)
    assert any("hi" in o for o in outputs)
