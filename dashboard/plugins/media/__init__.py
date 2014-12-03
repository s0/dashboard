"""
media plugin
"""

import dashboard.plugins.abc

# Plugin Specific Imports
import media_chrome
import media_mpd

class Plugin(dashboard.plugins.abc.PluginABC):

    # TODO: add mutexes

    def __init__(self, core):
        self._core = core
        self._handlers = {}
        self._last_active_card = None

        media_chrome.Thread(core, self).start()
        media_mpd.Thread(core, self, 'bumblebee.sparknet', local_path="/media/My_Book/Media/Music").start()

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

    def get_active_media_card(self):
        media_cards = {
        }
        for card in self._core.cards.values():
            if card.card_type == "media":
                if ('play_state' in card.state and
                    'state' in card.state['play_state'] and
                    'toggle_enabled' in card.state['play_state'] and
                    card.state['play_state']['toggle_enabled']):
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
