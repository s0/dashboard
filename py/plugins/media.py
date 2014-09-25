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
        time.sleep(1)
        while(True):
            card = self._manager.create_card('media', 'bottom_first')
            T(card).start()
            time.sleep(2)

class T(threading.Thread):

    def __init__(self, card):
        super(T, self).__init__()
        self.card = card

    def run(self):
        time.sleep(3)
        self.card.send({
            'fn': 'set_info',
            'data': {
                'title': 'foo',
                'artist': 'bar',
                'album': 'baz'
            }
        })
