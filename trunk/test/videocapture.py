#http://techlists.org/archives/programming/pythonlist/2007-03/msg02546.shtml

import VideoCapture
import pygame
from pygame.locals import *
import sys

fps = 20.0
webcam = VideoCapture.Device()
webcam.setResolution(640,480)
pygame.init()
window = pygame.display.set_mode((640,480))
pygame.display.set_caption("WebCam Demo")
screen = pygame.display.get_surface()
while True:
    events = pygame.event.get()
    for event in events:
        if event.type == QUIT or event.type == KEYDOWN:
            sys.exit(0)
    im = webcam.getImage()
    pg_img = pygame.image.frombuffer(im.tostring(), im.size, im.mode)
    screen.blit(pg_img, (0,0))
    pygame.display.flip()
    pygame.time.delay(int(1000 * 1.0/fps))


