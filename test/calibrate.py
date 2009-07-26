import gtk
import cairo
import math
import pygtk
from gtk import gdk
import pygame
import random

import Image
import sys
import time

import opencv
import threading

#this is important for capturing/displaying images
from opencv import highgui 


class calibrateWindow(gtk.Window):
    def __init__(self):
        super(calibrateWindow, self).__init__()
        h = 640
        w = 480
        
        self.set_title("ShinyTouch Auto Configuration Tool")
        self.set_size_request(h, w)
        self.set_position(gtk.WIN_POS_CENTER)

        self.connect("destroy", gtk.main_quit)
        #self.set_decorated(gtk.FALSE)
        #self.fullscreen()
        darea = gtk.DrawingArea()
        darea.connect("expose-event", self.expose)
        darea.connect("button_press_event", self.button_press)
        self.add(darea)
        
        self.mode = 0
        
        # unmask events
        darea.add_events(gdk.BUTTON_PRESS_MASK |
                        gdk.BUTTON_RELEASE_MASK |
                        gdk.POINTER_MOTION_MASK)

        self.show_all()
    
    def expose(self, widget, event):
        context = widget.window.cairo_create()

        # set a clip region for the expose event
        context.rectangle(event.area.x, event.area.y,
                          event.area.width, event.area.height)
        context.clip()

        self.draw(context)

        return False

    def button_press(self, widget, event):
        if self.mode == 0:
          self.fullscreen()
        elif self.mode == 4:
          self.unfullscreen()
        self.mode += 1
          
    def draw(self, context):
    
        rect = self.get_allocation()

        x = rect.x + rect.width / 2.0
        y = rect.y + rect.height / 2.0

        # clock back
        context.set_source_rgb(1.0,1.0,1.0)
        context.rectangle(0, 0, rect.width, rect.height)
        context.fill()        
        context.set_source_rgb(0.1, 0.1, 0.1)
        context.select_font_face("Helvetica", cairo.FONT_SLANT_NORMAL, cairo.FONT_WEIGHT_NORMAL)
        context.set_font_size(30)
        context.move_to(20, 50)
        if self.mode == 0:
          context.show_text("ShinyTouch AutoConfiguration Tool")
          context.move_to(20, 100)
          context.set_font_size(13)
          context.show_text("Please check that there are no obstacles to the camera's view. Click to start")
        elif self.mode == 1:
          context.show_text("")
          threading.Thread(target=self.snapshot).start()
          
    def snapshot(arg):
      time.sleep(1.0)
      camera = highgui.cvCreateCameraCapture(0)
      im = highgui.cvQueryFrame(camera)
      # Add the line below if you need it (Ubuntu 8.04+)
      im = opencv.cvGetMat(im)
      #convert Ipl image to PIL image
      im = opencv.adaptors.Ipl2PIL(im)
      im.save('test.png',"PNG")
      
      
    def redraw_canvas(self):
        if self.window:
            alloc = self.get_allocation()
            #rect = gdk.Rectangle(alloc.x, alloc.y, alloc.width, alloc.height)
            #self.window.invalidate_rect(rect, True)
            self.queue_draw_area(alloc.x, alloc.y, alloc.width, alloc.height)
            self.window.process_updates(True)

    def kill(self):
			gtk.main_quit()

calibrateWindow()
gtk.main()

