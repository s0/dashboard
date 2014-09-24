import json
import gobject
import threading

import plugins.media

gobject.threads_init()

class PluginManager(object):

    def __init__(self, web_view):

        self.web_view = web_view
        self.plugins = {
            'media': plugins.media.MediaPlugin(self)
        }
        self._next_card_id = 0;
        self._mutex = threading.BoundedSemaphore();

        web_view.connect("notify::title", self.receive_title_change)

    def receive_title_change(self, *args):
        title = self.web_view.get_title()

        if title is None:
            return

        split = title.split(':::', 2)
        print split

        if len(split) == 3:
            plugin = split[1]
            obj = json.loads(split[2])

            if plugin in self.plugins:
                print "handling message in thread: " + str(threading.current_thread())
                self.plugins[plugin].handle_message(obj)

    def send_to_card(self, card_id, obj):
        js = "window.send_to_card(%s, %s)" % (card_id, json.dumps(obj))
        self.send_js(js)

    def create_card(self, card_type, position='default'):
        # Thread-Safe generation of IDs
        self._mutex.acquire()
        card_id = self._next_card_id
        self._next_card_id += 1
        self._mutex.release()

        js = 'window.new_card(%s, "%s", "%s")' % (card_id, card_type, position)
        self.send_js(js)

        return Card(self, card_id)

    def send_js(self, js):
        gobject.idle_add(self.__send_js, js)

    def __send_js(self, js):
        self.web_view.execute_script(js)


class Card(object):

    def __init__(self, manager, card_id):
        self._manager = manager
        self._card_id = card_id

    def send(self, obj):
        self._manager.send_to_card(self._card_id, obj)
