import json
from gi.repository import GObject
import threading

import dashboard.plugins.media
import dashboard.plugins.bluetooth

GObject.threads_init()

class PluginManager(object):

    def __init__(self):

        self._mutex = threading.BoundedSemaphore();

        # Load Plugins
        self.plugins = {
            'media': dashboard.plugins.media.Plugin(self),
            'bluetooth': dashboard.plugins.bluetooth.Plugin(self),
        }

    def recv_message(self, plugin, obj):
        if plugin in self.plugins:
            self.plugins[plugin].handle_message(obj)

    def send_to_card(self, card_id, obj):
        js = "window.send_to_card(%s, %s)" % (card_id, json.dumps(obj))
        self.send_js(js)
