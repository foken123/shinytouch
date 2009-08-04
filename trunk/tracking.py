


execfile("autocalibrate.py")
execfile("performance.py")
execfile("events.py")

speed = FpsMeter() #set up the new fps meter

def get_image(dolog = False, getpix = False):
  global im, pix, draw, imsrc, autocal, stateframecount,switchcount, oldpix, oldim, diffmap, scantimes, input_type, speed
  #yay for insanely large global statements
  
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

  ##########BEGIN AUTOCONFIG################
  if switchcount == 7: 
    #stop after seven and update config
    get_points(width, height)
    saveconfig()
    switchcount += 1
  if switchcount > 7:
    #over seven, display the b/w grayscale purtyfullness
    if switchcount < 100:
      switchcount += 1
      return diffmap
      #display
    else:
      reset_calibrate()
      #once it's over 100 frames past that, then return to normal state
  if autocal == 1: #state 1: the white
    stateframecount += 1
    if stateframecount > 3:
      if switchcount != 0:
        if img_diff(width, height) == False:
          switchcount -= 1
      switchcount+=1
      oldpix = im.load()
      oldim = im
      stateframecount = 0
      autocal = 2
    im = Image.new("RGB", (width,height), (255,255,255))
    draw = ImageDraw.Draw(im)
    import random
    draw.text((random.randint(0,width-100),random.randint(0,height-20)), "Auto Calibrating. Please Wait.", fill=(0,0,0))
    return im
  if autocal == 2: #state 1: the black
    stateframecount += 1
    if stateframecount > 3:
      if img_diff(width, height) == False:
          switchcount -= 1
      switchcount+=1
      oldpix = im.load()
      oldim = im
      stateframecount = 0
      autocal = 1
    im = Image.new("RGB", (width,height), (0,0,0))
    draw = ImageDraw.Draw(im)
    import random
    draw.text((random.randint(0,width-100),random.randint(0,height-20)), "Auto Calibrating. Please Wait.", fill=(255,255,255))
    return im
  ##########END AUTOCONFIG################
  
  #this is for build range mode.
  if getpix != False:
    expandTargetRange(pix[getpix[0],getpix[1]])
    saveconfig()

    
  #pix[xs, tl] = (100,100,255,255)
  #pix[xs, bl] = (100,100,255,255)
  #pix[xe, tr] = (100,100,255,255)
  #pix[xe, br] = (100,100,255,255)
  

  #where the values will be stored
  xp = 0 #the x point of contact
  yp = 0 #the y point of contact
  wp = 0
  oy = 0

  for x in range(0, w):
    count = 0 #consecutive finger pixels
    #if x % 2 > 0: #this is a speed hack to skip pixels
    #  continue
    for y in range(tr + int(ytr*x), br + int(ybr * x)):
      #if y % 4 > 0: #this is a speed hack to skip pixels
      #  continue
      if colorTargetMatch(pix[xe-x,y]): #detects the finger!
        pix[xe-x,y] = (0,255,0,255) #set a green dot on pixel
        count += 1 #increment consecutive
      else:
        #pix[xe-x,y] = (0,0,0,255)
        if count >= 1:
          #print "x:",(xe-x),"y:",(y-(count/2))
          xp = xe-x
          yp = y-(count/2)
          oy = y-count
          wp = count
          count = -1 #signal for win
          break
    if count == -1: #WIN!
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
      #"""
      xd = ((xp - xs)/float(w))*width
      disttop = (((tr-tl)/w) * (xp-xs)) + tl
      vwid = (bl-tl) + (((br-tr)-(bl-tl)) * ((xp - xs)/float(w)))
      yd = ((yp - disttop)/vwid) * height
      
      """
      xd = (xp-xs)*width/float(w) # x co-ordinate with distortion
      # smallest side + top bit*x-ratio + bottom bit*x-ratio
      top = tr + ((tl-tr)*(xd/float(width)))
      heightinsidequad = (bl-tl) + ((tl-tr)*(xd/float(width))) + ((br-bl)*(xd/float(width)))
      yd = (yp-top)*height/float(heightinsidequad)
      #"""
      #draw the box for draw mode
      
      handle_touch(xd/float(width), yd/float(height))
    else:
      handle_lift()
      pass
      
      
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


