"""
Media control for MPD via MPC

"""

import re
import subprocess
import threading
import time

import mpd

import media_art

class Thread(threading.Thread):

    def __init__(self, manager, plugin, host='localhost', port=6600, local_path=None):
        super(Thread, self).__init__()
        self._manager = manager
        self._plugin = plugin
        self._host = host
        self._port = port
        self._local_path = local_path
        print "STARTING MPD"
        print host
        print port
        print local_path

    def run(self):

        # Wait for window to initialise
        # Can be removed after refactoring
        # time.sleep(1)

        self._client = mpd.MPDClient()
        self._client.timeout = 10
        self._client.idletimeout = None

        self._state = 'stop'
        self._card = None;
        self._info = None
        self._file = None

        while(True):
            try:
                self._client.connect(self._host, self._port)

                while(True):
                    self.update()
                    time.sleep(1)
            except Exception as e:
                print e
                time.sleep(5)

    def update(self):
        state = self._client.status()['state']

        if self._state != state:
            self._state = state
            if state == 'stop' and self._card:
                self._card.delete()
                self._card = None
            elif state == 'pause' or state == 'play':
                if not self._card:
                    self._card = self._manager.create_card('media', 'default', self.card_handler)
                self._card.set_state('type', 'mpd:' + self._host)
                self._card.set_state('play_state', {
                        'state': 'playing' if state == 'play' else 'paused',
                        'toggle_enabled': True,
                        'stop_enabled': True,
                        'next_enabled': True,
                        'prev_enabled': True
                    })

        if state == 'pause' or state == 'play':

            current_song = self._client.currentsong()

            info = {
                'title': current_song['title'],
                'artist': current_song['artist'],
                'album': current_song['album']
            }

            if self._info != info:
                self._info = info
                if self._card:
                    self._card.set_state('info', info)

            if self._file != current_song['file']:
                self._file = current_song['file']
                image = media_art.get_image(self._local_path, self._file)
                if image is not None:
                    self._card.set_state('album_art', image)

        else:
            self._info = None
            self._file = None

    def card_handler(self, message):
        action = message['action']
        if action == 'stop':
            self._client.stop()

        elif action == 'prev':
            status = self._client.status()
            if float(status['elapsed']) < 4:
                self._client.previous()
            else:
                self._client.seek(status['song'], 0)

        elif action == 'next':
            self._client.next()

        elif action == 'toggle':
            if self._client.status()['state'] == 'play':
                self._client.pause()
            else:
                self._client.play()

        self.update()
