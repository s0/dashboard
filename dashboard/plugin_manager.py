import json
from gi.repository import GObject
import threading

import dashboard.plugins.media
import dashboard.plugins.bluetooth

GObject.threads_init()

class PluginManager(object):

    def __init__(self, core):

        self._mutex = threading.BoundedSemaphore();

        # Load Plugins
        self.plugins = {
            'media': dashboard.plugins.media.Plugin(core),
            'bluetooth': dashboard.plugins.bluetooth.Plugin(core),
        }

    def recv_message(self, plugin, obj):
        if plugin in self.plugins:
            self.plugins[plugin].handle_message(obj)

    def get_plugin(self, plugin):
        if plugin in self.plugins:
            return self.plugins[plugin]