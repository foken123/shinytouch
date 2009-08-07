#from http://www.jperla.com/blog/2007/09/26/capturing-frames-from-a-webcam-on-linux/
import pygame
import Image, ImageDraw
from pygame.locals import *
import sys

import opencv
#this is important for capturing/displaying images
from opencv import highgui 
import performance

speed = performance.FpsMeter()

camera = highgui.cvCreateCameraCapture(0)
def get_image():
    im = highgui.cvQueryFrame(camera)
    # Add the line below if you need it (Ubuntu 8.04+)
    im = opencv.cvGetMat(im)
    #convert Ipl image to PIL image
    im = opencv.adaptors.Ipl2PIL(im) 
    
    draw = ImageDraw.Draw(im)
    global speed
    draw.text((20,20), "FPS: " + str(speed.go()), fill=(255,255,255))
    return im

fps = 240.0
pygame.init()
window = pygame.display.set_mode((640,480))
pygame.display.set_caption("WebCam Demo")
screen = pygame.display.get_surface()

while True:
    events = pygame.event.get()
    for event in events:
        if event.type == QUIT or event.type == KEYDOWN:
            sys.exit(0)
    im = get_image()
    pg_img = pygame.image.frombuffer(im.tostring(), im.size, im.mode)
    screen.blit(pg_img, (0,0))
    pygame.display.flip()
    pygame.time.delay(int(1000 * 1.0/fps))

