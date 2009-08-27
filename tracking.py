from perspective import *

execfile("autocalibrate.py")
execfile("performance.py")
execfile("events.py")

speed = FpsMeter() #set up the new fps meter

##This function is what gets the image data from the input and then processes and gives an output
def get_image(dolog = False, getpix = False):
  global im, pix, draw, imsrc, autocal, input_type, speed, mode
  
  #it supports opencv and videocapture for input, or a image file
  if imsrc == "cam":
    if input_type == "opencv":
      #query camera
      im = highgui.cvQueryFrame(camera)
      # Add the line below if you need it (Ubuntu 8.04+)
      im = opencv.cvGetMat(im)
      #convert Ipl image to PIL image
      im = opencv.adaptors.Ipl2PIL(im)
    elif input_type == "videocapture":
      #videocaputre is so easy! i wish it was for linux too
      im = camera.getImage()
  else:
    #from files are easy too
    im = Image.open(imsrc)
  
  
 
  #generate a pixel grid to do pixel by pixel hacks
  pix = im.load()
  #the canvas to draw things on
  draw = ImageDraw.Draw(im)

 
  if autocal is not 0:
    return calibrate_phase() #do the real magic
  
  #this is for build range mode.
  if getpix != False:
    expandTargetRange(pix[getpix[0],getpix[1]])
    saveconfig() #hi!


  #where the values will be stored
  xp = 0 #the x point of contact
  yp = 0 #the y point of contact
  #wp = 0
  oy = 0
  matchcount = 0
  
  #loop x axis
  for x in range(0, w):
    count = 0 #consecutive finger pixels
    #if x % 2 > 0: #this is a speed hack to skip pixels
    #  continue
    for y in range(tr + int(ytr*x), br + int(ybr * x)): #loop y
      #if y % 4 > 0: #this is a speed hack to skip pixels
      #  continue
      if colorTargetMatch(pix[xe-x,y]) and count < 100: #detects the finger!
        pix[xe-x,y] = (0,255,0,255) #set a green dot on pixel
        count += 1 #increment consecutive
      else:
        #pix[xe-x,y] = (0,0,0,255)
        if count >= 2:
          #print "x:",(xe-x),"y:",(y-(count/2))
          xp = xe-x
          yp = y-(count/2)
          oy = y-count
          #wp = count
          count = -1 #signal for win
          break
    if count == -1: #WIN!
      matchcount += 1
      if matchcount > 2:
        break
      if xp > 0 and yp - 10> 0 and xp + 10 < im.size[0]:
        touchcolor = pix[xp-5,yp]
        pix[xp,yp] = (255,255,255,255)
        #if colorShadowTest(draw, pix[xp+5, yp-10], pix[xp+5,yp-10], xp, yp):
        if colorTest(xp, yp, dolog):
          #if colorTest(pix[xp+5,yp],pix[xp+5,yp-10], touchcolor, xp, yp, dolog):
          #print "reflectoin: x:",(xe-x),"y:",(y-(count/2))
          
          
          #draw the rectangle around the point of contact
          draw.rectangle(((xp-10, yp-10),(xp+10, oy+10)), outline=(100,255,100))
          
          #complexiful linear approximation algorithm that tries to fix distortion
          #only elitist people should venture to the following lines
          #pleez someone fix it!
          #erm okay, so i stole it from another elitist, so i guess that's okay.
          
          warper = Perspective()
          warper.setsrc((xs,tl),(xe,tr),(xs,bl),(xe,br))
          warper.setdst((0,0),(width,0),(0,height),(width,height))
          xd, yd = warper.warp(xp, yp)
          
          #draw the box for draw mode
          
          handle_touch(xd/float(width), yd/float(height))
          break
        else:
          handle_lift()
          pass
  else:
    draw.text((20, 20), "No Target Found", fill=(255,255,255))

      
      
  #draw the cute little trapezoid over the window
  
  draw.line(((xs, tl),(xe, tr)),fill=(0,255,255))
  draw.line(((xs, bl),(xe, br)),fill=(0,255,255))
  
  draw.line(((xs, tl),(xs, bl)),fill=(0,255,255))
  draw.line(((xe, tr),(xe, br)),fill=(0,255,255))
  
  
  #draw the fps meter
  draw.text((20, height - 40), "FPS: " + str(speed.go()), fill=(255,255,255))
  if mode == "draw":
    return canvas
  elif mode == "transform":
    return im.transform((width,height), Image.QUAD, (xs,tl,xs,bl,xe,br,xe,tr))
  else:
    return im


