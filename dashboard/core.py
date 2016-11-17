#!/usr/bin/env python2

import os
import signal
import sys
import threading
import time

import dashboard.command_listener
import dashboard.config
import dashboard.plugin_manager
import dashboard.title_output
import dashboard.view.gtk

from gi.repository import Gtk

class DashboardCore(object):

    cards = {}
    next_card_id = 0

    # List of objects that listen for changes in card state / new cards
    card_listeners = set()

    def __init__(self, config_file):

        self.config = dashboard.config.Config(config_file)

        # Used for thread-safe generation of IDS
        self._mutex = threading.BoundedSemaphore();

        self.plugin_manager = dashboard.plugin_manager.PluginManager(self)

        if (self.config.get('core', 'spawn_window') is True):
            self.spawn_window()

        commands_fifo = self.config.get('core', 'commands_fifo')
        if commands_fifo is not None:
            dashboard.command_listener.CommandListener(self, commands_fifo).start()

        title_command = self.config.get('core', 'title_command')
        if title_command is not None:
            dashboard.title_output.TitleOutput(self, title_command).start()

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

    def get_plugin(self, plugin):
        return self.plugin_manager.get_plugin(plugin)

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
                        listener.card_state_updated(card, key, value)

    def unregister_card_listener(self, listener):
        """
        Used by a client (view) to unregister itself from the core
        """
        with self._mutex:
            print "UREG"
            self.card_listeners.remove(listener)

    def spawn_window(self):
        dashboard.view.gtk.spawn_sidebar_window(self)

class Card(object):

    def __init__(self, core, card_id, card_type, position, handler):
        self._core = core
        self.card_id = card_id
        self.card_type = card_type
        self.position = position
        self._handler = handler
        self.state = {}

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

    if len(sys.argv) < 2:
        print "config file path not included in command"
        sys.exit(1)

    config_file = sys.argv[1]
    core = DashboardCore(config_file)

    # Start GTK in main Thread
    # (GTK needs to be in this thread)
    Gtk.main()
