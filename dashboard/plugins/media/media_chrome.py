import json
import threading

import tornado.ioloop
import tornado.web
import tornado.websocket

class WebSocketHandler(tornado.websocket.WebSocketHandler):
    def initialize(self, core, plugin):
        self._core = core
        self._plugin = plugin
        # mapping from tab ID to card
        self.cards = {}

    def open(self, *args):
        self.stream.set_nodelay(True)

    def on_message(self, message):
        obj = json.loads(message)

        tab_id = obj['tab_id']
        if 'action' in obj:
            if obj['action'] == 'new_tab':

                def card_handler(message):
                    message['tab_id'] = tab_id
                    self.write_message(message)

                card = self._core.create_card('media', 'default', card_handler)
                self.cards[tab_id] = card
                card.set_state('type', obj['media_type'])

            elif obj['action'] == 'del_tab' and tab_id in self.cards:
                self.cards[tab_id].delete()
                del self.cards[tab_id]
        else:
            if tab_id in self.cards:
                print obj
                self.cards[tab_id].set_state(obj['key'], obj['value'])

    def on_close(self):
        for card in self.cards.values():
            card.delete()

    def check_origin(self, origin):
        return True

class Thread(threading.Thread):

    def __init__(self, core, plugin, port=8888):
        super(Thread, self).__init__()
        self._core = core
        self._plugin = plugin
        self._port = port

    def run(self):
        app = tornado.web.Application([
            (r'/', WebSocketHandler, {'core': self._core, 'plugin': self._plugin}),
        ])
        app.listen(self._port)
        tornado.ioloop.IOLoop.instance().start()
