import threading
import time

class Thread(threading.Thread):

    def __init__(self, manager):
        super(Thread, self).__init__()
        self._manager = manager

    def run(self):
        time.sleep(1)
        while(True):
            card = self._manager.create_card('media', 'top_first')

            card.send({
                'fn': 'set_info',
                'data': {
                    'title': 'foo',
                    'artist': 'bar',
                    'album': 'baz'
                }
            })
            time.sleep(2)
