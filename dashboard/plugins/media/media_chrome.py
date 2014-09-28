import json
import threading

import tornado.ioloop
import tornado.web
import tornado.websocket

class WebSocketHandler(tornado.websocket.WebSocketHandler):
    def initialize(self, manager):
        self._manager = manager
        self.cards = {}

    def open(self, *args):
        self.stream.set_nodelay(True)

    def on_message(self, message):
        obj = json.loads(message)

        print obj

        tab_id = obj['tab_id']
        if 'action' in obj:
            if obj['action'] == 'new_tab':
                card = self._manager.create_card('media')
                self.cards[tab_id] = card
                card.send({
                    'fn': 'set_type',
                    'data': obj['media_type']
                })

                # Sent test message
                self.write_message(json.dumps({'tab_id': obj['tab_id']}))

            elif obj['action'] == 'del_tab':
                self.cards[tab_id].delete()
        else:
            self.cards[tab_id].send(obj)

    def on_close(self):
       pass

    def check_origin(self, origin):
        print "origin: " + str(origin)
        return True

class Thread(threading.Thread):

    def __init__(self, manager, port=8888):
        super(Thread, self).__init__()
        self._manager = manager
        self._port = port

    def run(self):
        app = tornado.web.Application([
            (r'/', WebSocketHandler, {'manager': self._manager}),
        ])
        app.listen(self._port)
        tornado.ioloop.IOLoop.instance().start()
