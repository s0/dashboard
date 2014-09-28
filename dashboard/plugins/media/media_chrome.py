import json
import threading

import tornado.ioloop
import tornado.web
import tornado.websocket

class WebSocketHandler(tornado.websocket.WebSocketHandler):
    def initialize(self, manager, plugin):
        self._manager = manager
        self._plugin = plugin
        self.cards = {}

    def open(self, *args):
        self.stream.set_nodelay(True)

    def on_message(self, message):
        obj = json.loads(message)

        tab_id = obj['tab_id']
        if 'action' in obj:
            if obj['action'] == 'new_tab':
                card = self._manager.create_card('media')
                self.cards[tab_id] = card
                card.send({
                    'fn': 'set_type',
                    'data': obj['media_type']
                })

                def card_handler(message):
                    message['tab_id'] = tab_id
                    self.write_message(message)

                self._plugin.register_card_handler(card.card_id, card_handler)

            elif obj['action'] == 'del_tab' and tab_id in self.cards:
                self.cards[tab_id].delete()
                del self.cards[tab_id]
        else:
            if tab_id in self.cards:
                self.cards[tab_id].send(obj)

    def on_close(self):
        for card in self.cards.values():
            card.delete()

    def check_origin(self, origin):
        return True

class Thread(threading.Thread):

    def __init__(self, manager, plugin, port=8888):
        super(Thread, self).__init__()
        self._manager = manager
        self._plugin = plugin
        self._port = port

    def run(self):
        app = tornado.web.Application([
            (r'/', WebSocketHandler, {'manager': self._manager, 'plugin': self._plugin}),
        ])
        app.listen(self._port)
        tornado.ioloop.IOLoop.instance().start()
