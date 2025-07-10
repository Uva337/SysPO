from plugin_api import PluginBase


class ExamplePlugin(PluginBase):
    """Simple example plugin demonstrating plugin API usage."""

    def activate(self):
        print("ExamplePlugin activated")

    def deactivate(self):
        print("ExamplePlugin deactivated")

