#from http://ubuntuforums.org/showthread.php?t=715256


import Xlib.display
import Xlib.ext.xtest

class MouseControl:
  def __init__(self):
    self.display = Xlib.display.Display()
    self.screen = self.display.screen()
    self.root = self.screen.root

  def mouse_click(self, button):
    self.mouse_down(button)
    self.mouse_up(button)

  def mouse_down(self, button): #button= 1 left, 2 middle, 3 right
    Xlib.ext.xtest.fake_input(self.display,Xlib.X.ButtonPress, button)
    self.display.sync()

  def mouse_up(self, button):
    Xlib.ext.xtest.fake_input(self.display,Xlib.X.ButtonRelease, button)
    self.display.sync()

  def mouse_warp(self, x,y):
    self.root.warp_pointer(x,y)
    self.display.sync()

  def get_screen_resolution(self):
    return self.screen['width_in_pixels'], self.screen['height_in_pixels']
