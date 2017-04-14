"""
Media control for MPD via MPC

"""

import json
import re
import subprocess
import threading
import time
import urllib
import urllib2

url_devices = "https://api.spotify.com/v1/me/player/devices"
url_player = "https://api.spotify.com/v1/me/player"
url_play = "https://api.spotify.com/v1/me/player/play"
url_pause = "https://api.spotify.com/v1/me/player/pause"
url_next = "https://api.spotify.com/v1/me/player/next"
url_previous = "https://api.spotify.com/v1/me/player/previous"
url_seek = "https://api.spotify.com/v1/me/player/seek"

class Thread(threading.Thread):

    def __init__(self, manager, plugin, token):
        super(Thread, self).__init__()
        self._manager = manager
        self._plugin = plugin
        self._token = token
        print "STARTING Spotify Connector"

    def run(self):

        self._card = None;

        while True:
            try:
                self.update()
                time.sleep(5)
            except urllib2.URLError as e:
                print e.reason
                print e.read()
            except Exception as e:
                print e
                time.sleep(5)

    def _request(self, url):
        headers = {
            'Authorization': "Bearer " + self._token,
            'Accept': 'application/json'
        }
        return urllib2.Request(url, None, headers)

    def get_url(self, url):
        req = self._request(url)
        response = urllib2.urlopen(req)
        return json.loads(response.read())

    def do_put(self, url):
        req = self._request(url)
        req.get_method = lambda: 'PUT'
        urllib2.urlopen(req)

    def do_post(self, url):
        req = self._request(url)
        req.get_method = lambda: 'POST'
        urllib2.urlopen(req)

    def update(self):
        state = None

        # Find an active device
        devices = self.get_url(url_devices)
        for device in devices['devices']:
            if device['is_active']:
                player = self.get_url(url_player)
                playing = player['is_playing'];
                title = ''
                artist = ''
                album = ''
                if player['item']:
                    title = player['item']['name']
                    if player['item']['album']:
                        album = player['item']['album']['name']
                    if player['item']['artists']:
                        artists = None
                        for a in player['item']['artists']:
                            if artists is None:
                                artists = a['name']
                            else:
                                artists += ', ' + a['name']
                        artist = artists

                # Set the state accordingly
                state = {
                    'device': device['name'],
                    'playing': playing,
                    'title': title,
                    'artist': artist,
                    'album': album,
                }
                break

        if state is None:
            if self._card:
                self._card.delete()
                self._card = None
        else:
            if not self._card:
                self._card = self._manager.create_card('media', 'default', self.card_handler)
            self._card.set_state('type', 'spotify: ' + state['device'])
            self._card.set_state('play_state', {
                    'state': 'playing' if state['playing'] else 'paused',
                    'toggle_enabled': True,
                    'stop_enabled': True,
                    'next_enabled': True,
                    'prev_enabled': True
                })
            self._card.set_state('info', {
                'title': state['title'],
                'artist': state['artist'],
                'album': state['album']
            })
        self._state = state

    def card_handler(self, message):
        action = message['action']
        try:
            if action == 'stop':
                pass

            elif action == 'prev':
                player = self.get_url(url_player)
                if player['progress_ms'] < 5000:
                    self.do_post(url_previous)
                else:
                    # Restart song
                    self.do_put(url_seek + '?position_ms=0')

            elif action == 'next':
                self.do_post(url_next)


            elif action == 'toggle':
                if self._state and self._state['playing']:
                    self.do_put(url_pause)
                else:
                    self.do_put(url_play)

            self.update()
        except urllib2.URLError as e:
            print e.reason
            print e.read()
        except Exception as e:
            print e
