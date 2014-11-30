"""
media plugin
"""

import dashboard.plugins.abc

# Plugin Specific Imports
import media_chrome
import media_mpd

class Plugin(dashboard.plugins.abc.PluginABC):

    def __init__(self, core):
        self._core = core
        self._handlers = {}

        media_chrome.Thread(core, self).start()
        media_mpd.Thread(core, self, 'bumblebee.sparknet', local_path="/media/My_Book/Media/Music").start()

    def handle_message(self, message):
        print message


