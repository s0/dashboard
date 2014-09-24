#! /bin/python2

#!/usr/bin/env python

import cairo
from gi.repository import Gtk, Gdk

class SidebarWindow (Gtk.Window):
    def __init__(self):
        super(SidebarWindow, self).__init__()

        # Start Compositing
        screen = self.get_screen()
        rgba_visual = screen.get_rgba_visual()
        if rgba_visual != None and screen.is_composited():
            print "compositing supported"
            self.set_visual(rgba_visual)

        # Setup Components
        box = Gtk.Box()
        self.add(box)

        self.set_app_paintable(True)
        self.connect("draw", self.area_draw)


        # Window Listeners
        self.connect("destroy", lambda g: Gtk.main_quit())

        self.show_all()

    def area_draw(self, widget, cr):
        cr.set_source_rgba(.2, .2, .2, 0.0)
        cr.set_operator(cairo.OPERATOR_SOURCE)
        cr.paint()
        cr.set_operator(cairo.OPERATOR_OVER)


if __name__ == "__main__":
    SidebarWindow()
    Gtk.main()
