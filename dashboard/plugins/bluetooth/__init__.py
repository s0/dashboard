"""
bluetooth plugin
"""

import subprocess
import threading
import time

import dashboard.plugins.abc

class Plugin(dashboard.plugins.abc.PluginABC):

    def __init__(self, manager):
        self._manager = manager
        self._handlers = {}

        Thread(manager, self, "00:00:00:00:00:00", "Nexus 5").start()

    def handle_message(self, message):
        if message['card_id'] in self._handlers:
            self._handlers[message['card_id']](message)


    def register_card_handler(self, card_id, handler):
        self._handlers[card_id] = handler


class Thread(threading.Thread):

    def __init__(self, manager, plugin, mac, name=None):
        super(Thread, self).__init__()
        self._manager = manager
        self._plugin = plugin
        self._mac = mac
        self._name = name
        self._card_when_disconnected = True
        self._card = None

    def run(self):

        # Wait for window to initialise
        # Can be removed after refactoring
        time.sleep(1)

        connected = False

        self.set_disconnected()

        while(True):

            # Check if Connected
            proc = subprocess.Popen(['hcitool','lq',self._mac], shell=False, stdout=subprocess.PIPE)
            status_str = proc.communicate()
            if status_str[0] == '':
                if connected:
                    self.set_disconnected()
                connected = False
            else:
                if not connected:
                    self.set_connected()
                connected = True

            time.sleep(3)

    def set_connected(self):

        self.create_card()
        self._card.send({
            'fn': 'set_info',
            'data': {
                'name': self._name,
                'status': 'connected'
            }
        })

    def set_disconnected(self):

        if(self._card_when_disconnected):
            self.create_card()
            self._card.send({
                'fn': 'set_info',
                'data': {
                    'name': self._name,
                    'status': 'disconnected'
                }
            })
        else:
            if self._card:
                self._card.delete()
                self._card = None

    def create_card(self):
        if not self._card:
            self._card = self._manager.create_card('bluetooth_device', 'bottom_first')
            self._plugin.register_card_handler(
                self._card.card_id, self.card_handler
            )

    def card_handler(self, message):
        print message
