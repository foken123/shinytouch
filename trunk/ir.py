#######
#FILE 2: BASIC IR-DEMO (hack an IR-webcam and IR emitter for optimal experience)
#######
##################################
#BASIC DEMO:
#Demonstrates basic ability of IRM: get motion data and translate it into motion point coordinates
##################################
# Copyright (C) 2007 Erol Baykal
# License: GPL
#ONLY WORKS ON WINDOWS, this is due to videocapture being windows 32 only
#NEEDS:
#   PIL (python image library http://www.pythonware.com/products/pil/)
#   Pygame (http://www.pygame.org/)
#   Videocapture (http://videocapture.sourceforge.net/)
#   Psyco (http://psyco.sourceforge.net/)
#AUTHOR:
#   Baykal Erol (erol@baykal.be)
#LAST UPDATE: 6 SEP 07
##################################
#
#MODULES
########
import Image, ImageDraw, motion, time, pygame, sys, random, performance
from VideoCapture import Device

#GLOBAL VARIABLES
#################
#options
########
FULLSCREEN = 0
COLORTHRESHOLD = 60 #color threshold for motion detection, the higher the more strict (avg. 50 is ok)
SIZE = 320,240 # resolution of the screen (and camera, but can be seperated), needs to be 4/3 (I think)
CSIZE = 160,120 #compressed size, needs to be 4/3 (widescreen hack?)

#init vars
##########
#psyco.full() #PSYCO speeds up python
pygame.init() #We need to initialize pygame early on, so that certain stuff works (loading sound..)
ratio = SIZE[0]/CSIZE[0] #ratio of compression
fps = performance.FpsMeter() #an FPS meter
font = pygame.font.Font(None, 36) #a font for writing :)

#select cam and set resolution
cam = Device(devnum=0)
cam.setResolution(SIZE[0],SIZE[1])

#the pygame screen
if FULLSCREEN:
    screen = pygame.display.set_mode(SIZE, pygame.FULLSCREEN)
else:
    screen = pygame.display.set_mode(SIZE)
    
#new empty images, we will be using them in the main loop
#ni = newest image
#nci = newest compressed image
#oci = older compressed image
cci = Image.new("RGB",CSIZE,(255,255,255))
ni = Image.new("RGB",SIZE,(255,255,255))
oci = cci

tracklist = [(10,10)]

#a new surface the size of our window, will serve as a bg
background = pygame.Surface(screen.get_size())
background = background.convert()
background.fill((250, 250, 250))


#################################################
#MAIN LOOP
##########
do = 1
while do:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
           do = 0
           del cam
           sys.exit()
        elif event.type == pygame.KEYDOWN and event.key == pygame.K_ESCAPE:
           do = 0
           del cam
           sys.exit()
    #Get the images
    ###############
    #oci and nci are used for motion detection, they don't show up on screen
    #if you want to show something use ni
    oci = cci #make the current compressed image the old one
    ni = cam.getImage() #get new image for compression
    ni = ni.transpose(Image.FLIP_LEFT_RIGHT) #Flip image for mirror movement, this way topleft == (0,0)
    cci = ni.resize(CSIZE,Image.BILINEAR) #compress the new image and make it the current one

    #Get motion from images
    #######################
    motionArray = motion.getMotionArray(oci,cci,COLORTHRESHOLD) #compare the images and get the array of pixels with difference
    motionPoint = motion.getMotionPoint(motionArray) #calculate the avarage point
    if motionPoint[0] > 0 and motionPoint[1] > 0: #chek X and Y values
        #if a real avarage point of motion has been returned
        wp = motionPoint
        px = wp[0]*ratio #multiply by compression ratio to get the position
        py = wp[1]*ratio #of the coordinate on the uncompressed image
        wp = (px,py)

        if len(tracklist) < 240: #we keep track of some frames' avarage points
           tracklist.append(wp)
        else:
           tracklist.pop(0)
           tracklist.append(wp)

    #Draw everything
    #################
    background.fill((255,255,255)) #clear the background
    pygame.draw.lines(background, (0,255,0), 0, tracklist)
    screen.blit(background,(0,0))
    txtFPS = font.render(str(fps.go()), 1, (100, 100, 100))
    screen.blit(txtFPS, (10,10))
    pygame.display.flip()

del screen # delete the screen
pygame.quit()
del cam #delete the cam on exit of loop
