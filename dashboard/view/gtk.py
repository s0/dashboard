import json
import threading
import os
import cairo


from gi.repository import Gtk, Gdk, WebKit, GObject

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
        #self.override_background_color(Gtk.StateFlags.NORMAL, Gdk.RGBA(0, 0, 0, 0))

        # Setup Webview
        self.webview = SidebarWebView()
        self.add(self.webview)

        # Listen for webview changes
        self.connect("destroy", lambda *a: core.unregister_card_listener(self))
        self.webview.connect("notify::title", self.receive_title_change)

        # Listen for card changes
        core.register_card_listener(self)

        self.set_app_paintable(True)
        self.connect("draw", self.area_draw)

        # Show
        self.show_all()

    def area_draw(self, widget, cr):
        # Clear Window
        cr.set_source_rgba(0, 0, 0, 0)
        cr.set_operator(0) # OPERATOR_CLEAR
        cr.paint()
        # Paint internal Elements
        cr.set_operator(cairo.OPERATOR_SOURCE)
        cr.paint()

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
        js = 'window.new_card(%s, "%s", "%s")' % (card.card_id, card.card_type, card.position)
        self.send_js(js)

    def deleted_card(self, card):
        js = 'window.del_card(%s)' % (card.card_id)
        self.send_js(js)

    def card_state_updated(self, card, key, value):
        js = 'window.set_card_state(%s, "%s", %s)' % (card.card_id, key, json.dumps(value))
        self.send_js(js)

    def send_js(self, js):
        GObject.idle_add(self.__send_js, js)

    def __send_js(self, js):
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

def spawn_sidebar_window(core):

    def new_window():
        SidebarWindow(core)

    GObject.idle_add(new_window)

