#! /bin/python2

#!/usr/bin/env python

import cairo
import os
from gi.repository import Gtk, Gdk, WebKit

class SidebarWindow (Gtk.Window):
    def __init__(self):
        super(SidebarWindow, self).__init__()

        # Start Compositing
        screen = self.get_screen()
        rgba_visual = screen.get_rgba_visual()
        if rgba_visual != None and screen.is_composited():
            print "compositing supported"
            self.set_visual(rgba_visual)
        self.set_app_paintable(True)

        # Setup Webview
        webview = SidebarWebView()
        self.add(webview)

        # Window Listeners
        self.connect("draw", self.draw_bg)
        self.connect("destroy", lambda g: Gtk.main_quit())

        # Show
        self.show_all()

    def draw_bg(self, widget, cr):
        """
        Draw the transparent backround
        """
        cr.set_source_rgba(.0, .0, .0, 0.0)
        cr.set_operator(cairo.OPERATOR_SOURCE)
        cr.paint()
        cr.set_operator(cairo.OPERATOR_OVER)

class SidebarWebView (WebKit.WebView):

    def __init__(self):
        super(SidebarWebView, self).__init__()

        # Enable Transparency
        self.set_transparent(True)

        # Load HTML
        project = os.path.dirname(os.path.dirname(os.path.realpath(__file__)))
        html = os.path.join(project, "static/dashboard.html")

        self.load_string(file(html).read(), 'text/html', 'UTF-8', "file://" + html)

if __name__ == "__main__":
    SidebarWindow()
    Gtk.main()
