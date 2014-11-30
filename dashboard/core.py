#!/usr/bin/env python2

import os
import signal
import threading
import time

import dashboard.plugin_manager
import dashboard.view.gtk

from gi.repository import Gtk

class DashboardCore(object):

    cards = {}
    next_card_id = 0

    # List of objects that listen for changes in card state / new cards
    card_listeners = set()

    def __init__(self):

        # Used for thread-safe generation of IDS
        self._mutex = threading.BoundedSemaphore();

        self.plugin_manager = dashboard.plugin_manager.PluginManager(self)

    def recv_message(self, plugin, obj):
        """
        Used by an external entity to send a message to a plugin
        """
        self.plugin_manager.recv_message(plugin, obj)

    def recv_card_message(self, card_id, obj):
        """
        Used by a client to send a message to a specific card
        """
        if card_id in self.cards:
            self.cards[card_id].send(obj)

    def create_card(self, card_type, position, handler):
        """
        Used by a plugin to create a card
        """
        # Thread-safe generation of IDs
        with self._mutex:
            card = Card(self, self.next_card_id, card_type, position, handler)
            self.next_card_id += 1

            for l in self.card_listeners:
                l.new_card(card)
            self.cards[card.card_id] = card

            return card

    def delete_card(self, card):
        """
        Used by Card to delete itself
        """
        with self._mutex:
            for l in self.card_listeners:
                l.deleted_card(card)
            del self.cards[card.card_id]

    def update_card_state(self, card, key, value):
        """
        Used by Card to send a message to all listeners of new state
        """
        with self._mutex:
            for l in self.card_listeners:
                l.card_state_updated(card, key, value)

    def register_card_listener(self, listener):
        """
        Used by a client (view) to register itself with the core
        """
        with self._mutex:
            if listener not in self.card_listeners:
                self.card_listeners.add(listener)

                # Send all current cards + state to new handler
                for card in self.cards.values():
                    listener.new_card(card)

                    for key, value in card.state.items():
                        listener.card_state_updated(card.card_id, key, value)

    def unregister_card_listener(self, listener):
        """
        Used by a client (view) to unregister itself from the core
        """
        with self._mutex:
            print "UREG"
            self.card_listeners.remove(listener)


class Card(object):

    state = {}

    def __init__(self, core, card_id, card_type, position, handler):
        self._core = core
        self.card_id = card_id
        self.card_type = card_type
        self.position = position
        self._handler = handler

    def set_state(self, key, value):
        """
        Called by plugin managing the card to change a property of the card
        """
        self.state[key] = value
        self._core.update_card_state(self, key, value)

    def delete(self):
        """
        Called by plugin managing the card to delete the card
        """
        self._core.delete_card(self)

    def send(self, obj):
        """
        Called by a DashboardCore to send an object to the handler of the card
        """
        self._handler(obj)


if __name__ == "__main__":

    # Make close on Ctrl + C
    signal.signal(signal.SIGINT, signal.SIG_DFL)

    core = DashboardCore()

    dashboard.view.gtk.spawn_sidebar_window(core)

    # Start GTK in main Thread
    # (GTK needs to be in this thread)
    Gtk.main()
