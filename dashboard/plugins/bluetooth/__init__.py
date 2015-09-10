"""
bluetooth plugin
"""

import subprocess
import threading
import time

import dashboard.plugins.abc

class Plugin(dashboard.plugins.abc.PluginABC):

    def __init__(self, core):
        self._core = core
        self._handlers = {}

        Thread(core, self, "00:00:00:00:00:00", "Nexus 5").start()

    def handle_message(self, message):
        print message


class Thread(threading.Thread):

    def __init__(self, manager, plugin, mac, name=None):
        super(Thread, self).__init__()
        self._core = manager
        self._plugin = plugin
        self._mac = mac
        self._name = name
        self._card_when_disconnected = True
        self._card = None

    def run(self):

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
        self._card.set_state('info', {
            'name': self._name,
            'status': 'connected'
        })

    def set_disconnected(self):

        if(self._card_when_disconnected):
            self.create_card()
            self._card.set_state('info', {
                'name': self._name,
                'status': 'disconnected'
            })
        else:
            if self._card:
                self._card.delete()
                self._card = None

    def create_card(self):
        if not self._card:
            self._card = self._core.create_card('bluetooth_device', 'bottom_first', self.card_handler)

    def card_handler(self, message):
        print message
