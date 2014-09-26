import tornado.ioloop
import tornado.web
import tornado.websocket

from tornado.options import define, options, parse_command_line

define("port", default=8888, help="run on the given port", type=int)

# we gonna store clients in dictionary..
clients = dict()

class WebSocketHandler(tornado.websocket.WebSocketHandler):
    def open(self, *args):
        #self.id = self.get_argument("Id")
        self.stream.set_nodelay(True)
        print("open")

    def on_message(self, message):        
        """
        when we receive some message we want some message handler..
        for this example i will just print message to console
        """
        print("Client {} received a message : {}".format(self, message))
        self.write_message(u"You said: " + message)

    def on_close(self):
       pass

    def check_origin(self, origin):
        print "origin: " + str(origin)
        return True

app = tornado.web.Application([
    (r'/', WebSocketHandler),
])

if __name__ == '__main__':
    parse_command_line()
    app.listen(options.port)
    tornado.ioloop.IOLoop.instance().start()
