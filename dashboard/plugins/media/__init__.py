"""
media plugin
"""

import dashboard.plugins.abc

# Plugin Specific Imports
import media_chrome
import media_mpd

class Plugin(dashboard.plugins.abc.PluginABC):

    def __init__(self, manager):
        self._manager = manager
        self._handlers = {}

        media_chrome.Thread(manager, self).start()
        media_mpd.Thread(manager, self, 'bumblebee.sparknet', local_path="/media/My_Book/Media/Music").start()

    def handle_message(self, message):
        if message['card_id'] in self._handlers:
            self._handlers[message['card_id']](message)


    def register_card_handler(self, card_id, handler):
        self._handlers[card_id] = handler


