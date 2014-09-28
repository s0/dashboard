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

        media_chrome.Thread(manager).start()
        #media_mpd.MPDThread(manager).start()


