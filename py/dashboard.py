#! /bin/python2

#!/usr/bin/env python

import cairo
import os
import signal

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

        # Set Background Color
        self.override_background_color(Gtk.StateFlags.NORMAL, Gdk.RGBA(0, 0, 0, 0))

        # Setup Webview
        webview = SidebarWebView()
        self.add(webview)

        # Window Listeners
        self.connect("destroy", lambda g: Gtk.main_quit())

        # Show
        self.show_all()

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
    # Make close on Ctrl + C
    signal.signal(signal.SIGINT, signal.SIG_DFL)
    Gtk.main()
