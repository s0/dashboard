"""
media plugin
"""

import dashboard.plugins.abc

# Plugin Specific Imports
import media_chrome
import media_mpd
import media_spotify

class Plugin(dashboard.plugins.abc.PluginABC):

    # TODO: add mutexes

    def __init__(self, core):
        self._core = core
        self._handlers = {}
        self._last_active_card = None

        print self._core.config.get('plugins', 'media')

        media_config = self._core.config.get('plugins', 'media');

        if media_config is not None:
            for item in media_config:
                if item['type'] == 'chrome':
                    kwargs = {}
                    self._core.config.transfer(item, kwargs, 'port')
                    media_chrome.Thread(core, self, **kwargs).start()
                elif item['type'] == 'mpd':
                    kwargs = {}
                    self._core.config.transfer(item, kwargs, 'host', 'port', 'local_path')
                    media_mpd.Thread(core, self, **kwargs).start()
                elif item['type'] == 'spotify':
                    kwargs = {}
                    self._core.config.transfer(item, kwargs, 'token')
                    media_spotify.Thread(core, self, **kwargs).start()
                elif item['type'] == 'dummy':

                    state = {
                        'playing': False
                    }

                    def card_handler(message):
                        print "Message to Dummy: " + repr(message)
                        if message['action'] == 'toggle':
                            state['playing'] ^= True
                            update_state()


                    card = self._core.create_card('media', 'default', card_handler)
                    card.set_state('info', {
                        'title': 'Title',
                        'artist': 'Artist',
                        'album': 'Album'
                    })

                    def update_state():
                        card.set_state('play_state', {
                            'state': 'playing' if state['playing'] else 'paused',
                            'toggle_enabled': True,
                            'stop_enabled': False,
                            'next_enabled': False,
                            'prev_enabled': False
                        })
                    update_state()

                else:
                    print "Unrecognized Media Type in config: " + item['type']
                    exit(1)

    def handle_message(self, message):
        card = self.get_active_media_card()
        if message == "toggle":
            if card is not None:
                card.send({"action": "toggle"})
        elif message == "next":
            if card is not None:
                card.send({"action": "next"})
        elif message == "prev":
            if card is not None:
                card.send({"action": "prev"})
        else:
            print message

    def toggle(self):
        print "Toggling Music"

        card = self.get_active_media_card()
        if card is not None:
            card.send({"action": "toggle"})

    def get_active_media_card(self, require_toggleable=True):
        media_cards = {
        }
        for card in self._core.cards.values():
            if card.card_type == "media":
                if ('play_state' in card.state and
                    'state' in card.state['play_state']):
                    toggleable = (
                        'toggle_enabled' in card.state['play_state'] and
                        card.state['play_state']['toggle_enabled'])
                    if toggleable or not require_toggleable:
                        state = card.state['play_state']['state']
                        if state not in media_cards:
                            media_cards[state] = []
                        media_cards[state].append(card)

        state_order = ['playing', 'paused']

        for state in state_order:
            if state in media_cards:
                if (self._last_active_card is not None and
                    self._last_active_card in media_cards[state]):
                    return self._last_active_card
                self._last_active_card = media_cards[state][0]
                return self._last_active_card

    def get_active_media_info(self):
        card = self.get_active_media_card(False)
        if card is not None:
            state = None
            return {
                'state': card.state['play_state']['state'],
                'info': card.state['info'] if 'info' in card.state else None
            }
