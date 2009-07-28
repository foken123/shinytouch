#!/usr/bin/env python
# clock_ex4.py

# a pygtk widget that implements a clock face
# porting of Davyd Madeley's
# http://www.gnome.org/~davyd/gnome-journal-cairo-article/clock-ex4.c

# author: Lawrence Oluyede <l.oluyede@gmail.com>
# date: 16 February 2005

import gtk
from gtk import gdk
import gobject

import math
from datetime import datetime

class EggClockFace(gtk.DrawingArea):
    # EggClockFace signals

    def __init__(self):
        super(EggClockFace, self).__init__()

        # gtk.Widget signals
        self.connect("expose_event", self.expose)
        self.connect("button_press_event", self.button_press)

        # unmask events
        self.add_events(gdk.BUTTON_PRESS_MASK |
                        gdk.BUTTON_RELEASE_MASK |
                        gdk.POINTER_MOTION_MASK)

        self.update()
        # update the clock once a second
        gobject.timeout_add(1000, self.update)

    def expose(self, widget, event):
        context = widget.window.cairo_create()

        # set a clip region for the expose event
        context.rectangle(event.area.x, event.area.y,
                          event.area.width, event.area.height)
        context.clip()

        self.draw(context)

        return False

    def button_press(self, widget, event):
        widget.window.fullscreen()

    def draw(self, context):
        rect = self.get_allocation()

        x = rect.x + rect.width / 2.0
        y = rect.y + rect.height / 2.0

        # clock back
        context.set_source_rgb(1.0, 1.0, 1.0)
        context.rectangle(0, 0, rect.width, rect.height)
        context.fill()
        
        context.set_source_rgb(0.1, 0.1, 0.1)
        context.select_font_face("Helvetica", cairo.FONT_SLANT_NORMAL, cairo.FONT_WEIGHT_NORMAL)
        context.set_font_size(13)
        context.move_to(rect.width/2)-90, 20)
        context.show_text("ShinyTouch AutoConfiguration Tool")


    def redraw_canvas(self):
        if self.window:
            alloc = self.get_allocation()
            #rect = gdk.Rectangle(alloc.x, alloc.y, alloc.width, alloc.height)
            #self.window.invalidate_rect(rect, True)
            self.queue_draw_area(alloc.x, alloc.y, alloc.width, alloc.height)
            
            
            self.window.process_updates(True)

    def update(self):
        # update the time
        self.time = datetime.now()

        return True # keep running this event

def main():
    window = gtk.Window()
    clock = EggClockFace()

    window.add(clock)
    window.connect("destroy", gtk.main_quit)
    window.show_all()

    gtk.main()

if __name__ == "__main__":
    main()

