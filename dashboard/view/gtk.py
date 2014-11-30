import threading
import os

from gi.repository import Gtk, Gdk, WebKit, GObject

thread = None

class SidebarWindow(Gtk.Window):

    def __init__(self, core):
        super(SidebarWindow, self).__init__()

        self._core = core

        self.set_title("dashboard")

        # Start Compositing
        screen = self.get_screen()
        rgba_visual = screen.get_rgba_visual()
        if rgba_visual != None and screen.is_composited():
            print "compositing supported"
            self.set_visual(rgba_visual)

        # Set Background Color
        self.override_background_color(Gtk.StateFlags.NORMAL, Gdk.RGBA(0, 0, 0, 0))

        # Setup Webview
        self.webview = SidebarWebView()
        self.add(self.webview)

        # Listen for webview changes
        self.connect("destroy", lambda *a: core.unregister_card_listener(self))
        self.webview.connect("notify::title", self.receive_title_change)

        # Listen for card changes
        core.register_card_listener(self)

        # Show
        self.show_all()

    def close(self, *args):
        print "closed window"
        core.unregister_card_listener(self)

    def receive_title_change(self, *args):
        title = self.webview.get_title()

        if title is None:
            return

        split = title.split(':::', 2)

        if len(split) == 3:
            card_id = int(split[1])
            obj = json.loads(split[2])
            self._core.recv_card_message(card_id, obj)

    def new_card(self, card):
        print "CC"
        js = 'window.new_card(%s, "%s", "%s")' % (card.card_id, card.card_type, card.position)
        self.send_js(js)

    def deleted_card(self, card):
        js = "window.del_card(%s)" % (card.card_id)
        self.send_js(js)

    def card_state_updated(self, card, key, value):
        pass

    def send_js(self, js):
        GObject.idle_add(self.__send_js, js)

    def __send_js(self, js):
        print "SENDING JS: " + js
        self.webview.execute_script(js)

class SidebarWebView(WebKit.WebView):

    def __init__(self):
        super(SidebarWebView, self).__init__()

        # Enable Transparency
        self.set_transparent(True)

        # Load HTML
        project = os.path.dirname(os.path.dirname(os.path.dirname(os.path.realpath(__file__))))
        html = os.path.join(project, "static/dashboard.html")

        self.load_string(file(html).read(), 'text/html', 'UTF-8', "file://" + html)

class ViewThread(threading.Thread):

    def run(self):
        pass #Gtk.main()

    def new_window(self, core):
        SidebarWindow(core)

def spawn_sidebar_window(core):
    global thread
    if thread is None:
        thread = ViewThread()
        thread.start()

    def new_window():
        SidebarWindow(core)

    GObject.idle_add(new_window)

