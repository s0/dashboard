"""
media plugin
"""

import threading
import time

import abc

class MediaPlugin(abc.PluginABC):

    def __init__(self, manager):
        self._manager = manager

        MPDThread(manager).start()

class MPDThread(threading.Thread):

    def __init__(self, manager):
        super(MPDThread, self).__init__()
        self._manager = manager

    def run(self):
        time.sleep(2)
        print "RUN"
        self._manager.create_card("media")
