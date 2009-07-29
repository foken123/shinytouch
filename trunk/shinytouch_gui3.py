import pygame
import Image
from pygame.locals import *
import sys
from PIL import Image, ImageColor, ImageDraw
import itertools
import os
import Tkinter
import threading

fps = 60.0
width = 640
height = 480
input_type = "opencv"

########END USEFUL CONFIGURATIOn########

mode = "image"
calibrate = False
box = 10
buildrange = False
imsrc = "cam"


canvas = Image.new("RGB", (width, height))
canvaspix = canvas.load()
draw2 = ImageDraw.Draw(canvas)
touchconf = False

if input_type == "opencv":
  import opencv #this is important for capturing/displaying images
  from opencv import highgui 
  camera = highgui.cvCreateCameraCapture(0)
elif input_type == "videocapture":
  import VideoCapture
  camera = VideoCapture.Device()
  camera.setResolution(width,height)
else:
  print "No Camera Input type selected!"
  
w = 0
ytr = 0
ybr = 0


execfile("reflection.py")
execfile("tracking.py")
execfile("misc.py")



pygame.init()
window = pygame.display.set_mode((width,height))
pygame.display.set_caption("ShinyTouch")
screen = pygame.display.get_surface()
clicks = 0
subavg = 0

# init GUI


class GUI(threading.Thread):
    def __init__(self):
        self.root=Tkinter.Tk()
        
        self.button_exit = Tkinter.Button(self.root, text="QUIT", fg="red", command=self.quitapp)
        self.button_exit.pack()

        self.button_autocal = Tkinter.Button(self.root, text="Auto Calibrate", command=self.autocal)
        self.button_autocal.pack()

        self.button_mancal = Tkinter.Button(self.root, text="Manual Calibration", command=self.mancal)
        self.button_mancal.pack()

        self.button_draw = Tkinter.Button(self.root, text="Draw Mode", command=self.draw)
        self.button_draw.pack()

        self.button_transform = Tkinter.Button(self.root, text="Transform Mode", command=self.transform)
        self.button_transform.pack()

        self.button_normal = Tkinter.Button(self.root, text="Normal Mode", command=self.normalmode)
        self.button_normal.pack()

        self.button_clear = Tkinter.Button(self.root, text="Clear Settings", command=self.clearsettings)
        self.button_clear.pack()
        
        threading.Thread.__init__(self)

    def run(self):
        self.root.mainloop()

    def quitapp(self):
      global exitapp
      exitapp=True
      sys.exit(0)

    def draw(self):
      global mode
      mode = "draw"

    def normalmode(self):
      global mode
      mode = "image"

    def autocal(self):
      global autocal
      autocal=1

    def transform(self):
      global mode
      mode = "transform"

    def mancal(self):
      global calibrate
      calibrate = True
      print "Click Top Left Corner"

    def clearsettings(self):
      os.remove("autoconf.py")
      self.quitapp()

app = GUI()
app.start()

exitapp=False


while not exitapp:
    dolog = False
    getpix = False
    events = pygame.event.get()
    for event in events:

      if event.type == QUIT:
          sys.exit(0)
      if event.type == KEYDOWN:
        if event.unicode == "g":
          touchconf = True
          print "Move your finger around the visible area, click to stop"
        else:
          touchconf = False  
        if event.unicode == "d":
          mode = "draw"
        elif event.unicode == "i":
          mode = "image"
        elif event.unicode == "a":
          global autocal
          autocal = 1
        elif event.unicode == "b":
          if buildrange == True:
            buildrange = False
            print "Disabled Color Range Building"
          else:
            buildrange = True
            print "Enabled Color Range Building"
        elif event.unicode == "f":
          pygame.display.set_mode((width,height),pygame.FULLSCREEN)
        elif event.unicode == "t":
          if mode == "transform":
            mode = ""
            print "Disabled Auto Transform"
          else:
            mode = "transform"
            print "Enabled Auto Transform"
        elif event.unicode == "s":
          import datetime
          canvas.save("imgs/purty"+str(datetime.datetime.now().isoformat())+".png","PNG")
          print "Saved Image"
        elif event.unicode == "c":
          calibrate = True
          print "Click Top Left Corner"
      if event.type == MOUSEBUTTONDOWN:
          touchconf = False
          if event.button == 3:
            dolog = True
          elif event.button == 2:
            canvas = Image.new("RGB", (width,height))
            canvaspix = canvas.load()
            draw2 = ImageDraw.Draw(canvas)
            print "Reset Canvas"
            execfile("tracking.py")
            print "Loaded finger tracker core"
            execfile("reflection.py")
            print "Loaded Reflection Detection Algorithm"
            execfile("autoconf.py")
            print "Loaded Automatic Generated Configuration"
          elif event.button == 1 and calibrate == False and buildrange == True:
            #yes, i did something very stupid and ugly just to not edit the calibration code
            getpix = event.pos
            #buildrange = False
          elif event.button == 1 and calibrate == True:
            clicks += 1
            if clicks == 1:
              tl = event.pos[1]
              subavg = event.pos[0]
              xs = subavg
              print "Click Bottom Left Corner"
            elif clicks == 2:
              bl = event.pos[1]
              xs = (subavg + event.pos[0])/2
              print "Click Bottom Right Corner"
            elif clicks == 3:
              br = event.pos[1]
              subavg = event.pos[0]
              xe = subavg
              print "Click Top Right Corner"
            elif clicks == 4:
              tr = event.pos[1]
              xe = (subavg + event.pos[0])/2
              print "Done. To recalibrate, press c and then click Top Left corner again."
              calibrate = False
              saveconfig()
              clicks = 0
    im = get_image(dolog, getpix)
    pg_img = pygame.image.frombuffer(im.tostring(), im.size, im.mode)
    screen.blit(pg_img, (0,0))
    pygame.display.flip()
    pygame.time.delay(int(1000 * 1.0/fps))

