import sys

from plugin_api import PluginManager, PluginBase



class DummyContext:
    pass


def test_plugin_activation(tmp_path, monkeypatch):
    plugins_dir = tmp_path / "plug"
    plugins_dir.mkdir()
    (plugins_dir / "__init__.py").write_text("")
    plugin_code = (
        "from plugin_api import PluginBase\n"
        "class MyPlugin(PluginBase):\n"
        "    def __init__(self, app_context=None):\n"
        "        super().__init__(app_context)\n"
        "        self.active = False\n"
        "    def activate(self):\n        self.active=True\n"
        "    def deactivate(self):\n        self.active=False\n"
    )
    (plugins_dir / "plg.py").write_text(plugin_code)
    sys.path.insert(0, str(tmp_path))
    pm = PluginManager(plugin_dir=plugins_dir.name, app_context=DummyContext())
    pm.load_plugins()
    assert len(pm.plugins) == 1
    plugin = pm.plugins[0]
    assert isinstance(plugin, PluginBase)
    assert getattr(plugin, "active", False) is True
    sys.path.pop(0)


def test_plugin_load_error(tmp_path, capsys):
    plugins_dir = tmp_path / "plug2"
    plugins_dir.mkdir()
    (plugins_dir / "__init__.py").write_text("")
    (plugins_dir / "bad.py").write_text("def broken(")
    pm = PluginManager(plugin_dir=plugins_dir.name)
    pm.load_plugins()
    captured = capsys.readouterr()
    assert "Failed" in captured.out
    assert len(pm.plugins) == 0
