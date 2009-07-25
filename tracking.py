#import mouse
#mousectl = mouse.MouseControl()

#mousedown = False
#lastcoord = (0,0)
#lasttime = 0

oldpix = 0
oldim = 0
autocal = 1
stateframecount = 0
switchcount = 0


diffmap = Image.new("RGB",(640,480))
diffpix = diffmap.load()

def colorDiffGrade(c,d):
  r = c[0]-d[0]
  g = c[1]-d[1]
  b = c[2]-d[2]
  return abs(r) + abs(g) + abs(b)


def img_diff(w, h):
  global diffmap, pix, oldpix
  for x in range(0, w):
    for y in range(0, h):
      if colorDiffGrade(pix[x,y], oldpix[x,y]) > 20:
        diffpix[x,y] = (diffpix[x,y][0]+20,diffpix[x,y][1]+20,diffpix[x,y][2]+20)
  return diffmap
     


def get_points(w, h):
  global diffpix, diffmap
  diffdraw = ImageDraw.Draw(diffmap)
  lvc = 0
  tfvw = 0
  fvw = 0
  lvw = 0
  yarr = []
  for x in range(0,w):
    vc = 0
    pvc = 0
    pve = 0
    for y in range(0, h):
      if diffpix[x,y][0] > 30:
        vc += 1
      else:
        if vc > pvc:
          pvc = vc
          pve = x
        vc = 0
    yarr.append((pve-pvc,pve))
    
    #diffdraw.line(((x,pve-pvc),(x,pve)),fill=(255,255,255))
    if pvc > lvc:
      lvc = pvc
      if tfvw == 0 and pvc > 30:
        tfvw = x
    elif pvc > 30:
      lvw = x
      fvw = tfvw
  diffdraw.line(((lvw,0),(lvw,h)),fill=(0,0,255))
  diffdraw.line(((fvw,0),(fvw,h)),fill=(255,0,0))
  #fvw is first (left)
  #lvw is last (right)
  #[0] is start x (top)
  #[1] is end x (bottom)
  diffdraw.line(((fvw,yarr[fvw][0]),(lvw,yarr[lvw][0])),fill=(0,255,255))
  diffdraw.line(((fvw,yarr[fvw][1]),(lvw,yarr[lvw][1])),fill=(0,255,255))
  
  #diffdraw.line(((0,pvc),(w,pvc)),fill=(0,0,255))
  #diffdraw.line(((0,pvc),(w,pvc)),fill=(0,0,255))
  #diffdraw.line(((0,pvc),(w,pvc)),fill=(0,0,255))
  
def get_pointsOld(w, h):
  global diffpix, diffmap
  diffdraw = ImageDraw.Draw(diffmap)
  lvc = 0
  lvw = 0
  fvw = 0
  tfvw = 0
  for x in range(0,w):
    vc = 0
    pvc = 0
    for y in range(0, h):
      if diffpix[x,y][0] > 30:
        vc += 1
      else:
        if vc + 5 > lvc and vc > 30:
          if vc > pvc:
            pvc = vc
          lvc = vc
          if lvc != 0:
            lvw = x
            fvw = tfvw
            print 'woot',fvw
            print lvc
            #diffdraw.line(((x,0),(x,h)),fill=(255,255,255))
        else:
          lvc = 0
          tfvw = x
        vc = 0
  diffdraw.line(((lvw,0),(lvw,h)),fill=(0,0,255))
  diffdraw.line(((fvw,0),(fvw,h)),fill=(255,0,0))     
def get_pointsx(w, h):
  global diffpix
  horconsec = 0
  yarr = []
  for x in range(0, w):
    vertconsec = 0
    hly = -1
    hlw = -1
    
    for y in range(0, h):
      if diffpix[x,y][0] > 20:
        vertconsec += 1
      else:
        if vertconsec > 40:
          hly = y
          hlw = vertconsec
        vertconsec = 0
    yarr.append((hly-hlw, hly))
    if hlw > 0 and hly > 0:
      horconsec += 1
    else:
      if horconsec > 10:
        print "STARTX",x-horconsec, "ENDX", x
        global xs, xe, br, tr, tl, bl
        xs = x-horconsec
        xe = x-1
        tr = yarr[xe][1]
        br = yarr[xe][0]
        tl = yarr[xs][1]
        bl = yarr[xs][0]
    
        diffpix[xs, tl] = (100,100,255,255)
        diffpix[xs, bl] = (100,100,255,255)
        diffpix[xe, tr] = (100,100,255,255)
        diffpix[xe, br] = (100,100,255,255)
      horconsec = 0
      
def get_image(dolog = False, getpix = False):
  global im, pix, draw, imsrc, autocal, stateframecount,switchcount, oldpix, oldim
  if imsrc == "cam":
    im = highgui.cvQueryFrame(camera)
    # Add the line below if you need it (Ubuntu 8.04+)
    im = opencv.cvGetMat(im)
    #convert Ipl image to PIL image
    im = opencv.adaptors.Ipl2PIL(im)
  else:
    im = Image.open(imsrc)
  pix = im.load()
  draw = ImageDraw.Draw(im)

  if switchcount == 5:
    get_points(640, 480)
    #autocal = 0
    #switchcount = 0
    #saveconfig()
    switchcount += 1
  if switchcount > 5:
    return diffmap
  if autocal == 1:
    stateframecount += 1
    if stateframecount > 3:
      if switchcount != 0:
        img_diff(640, 480)
        import datetime
        oldim.save("test/Aold"+str(datetime.datetime.now().isoformat())+".png","PNG")
        im.save("test/Anew"+str(datetime.datetime.now().isoformat())+".png","PNG")
      switchcount+=1
      oldpix = im.load()
      oldim = im
      stateframecount = 0
      autocal = 2
    return Image.new("RGB", (640,480), (255,255,255))
  if autocal == 2:
    stateframecount += 1
    if stateframecount > 3:
      img_diff(640, 480)
      import datetime
      oldim.save("test/Bold"+str(datetime.datetime.now().isoformat())+".png","PNG")
      im.save("test/Bnew"+str(datetime.datetime.now().isoformat())+".png","PNG")
      switchcount+=1
      oldpix = im.load()
      oldim = im
      stateframecount = 0
      autocal = 1
    return Image.new("RGB", (640,480), (0,0,0))

  if getpix != False:
    global rmin, rmax, gmin, gmax, bmin, bmax
    cr = pix[getpix[0],getpix[1]]
    if cr[0] < rmin:
      rmin = cr[0]
    if cr[0] > rmax:
      rmax = cr[0]
    if cr[1] < gmin:
      gmin = cr[1]
    if cr[1] > gmax:
      gmax = cr[1]
    if cr[2] < bmin:
      bmin = cr[2]
    if cr[2] > bmax:
      bmax = cr[2]
    print "Pixel Color:",cr
    saveconfig()

    
  pix[xs, tl] = (100,100,255,255)
  pix[xs, bl] = (100,100,255,255)
  pix[xe, tr] = (100,100,255,255)
  pix[xe, br] = (100,100,255,255)
  
  xp = 0
  yp = 0
  wp = 0
  oy = 0

  for x in range(0, w):
    count = 0
    #if x % 2 > 0:
    #  continue
    for y in range(tr + int(ytr*x), br + int(ybr * x)):
      #if y % 4 > 0:
      #  continue
      if colorTargetMatch(pix[xe-x,y]):
        pix[xe-x,y] = (0,255,0,255)
        count += 1
      else:
        #pix[xe-x,y] = (0,0,0,255)
        if count >= 1:
          #print "x:",(xe-x),"y:",(y-(count/2))
          xp = xe-x
          yp = y-(count/2)
          oy = y-count
          wp = count
          
          count = -1
          break
    if count == -1:
      break

  if xp > 0 and yp - 10> 0 and xp + 10 < im.size[0]:
    touchcolor = pix[xp-5,yp]
    pix[xp,yp] = (255,255,255,255)
    #if colorShadowTest(draw, pix[xp+5, yp-10], pix[xp+5,yp-10], xp, yp):
    if colorTest(xp, yp, dolog):
      #if colorTest(pix[xp+5,yp],pix[xp+5,yp-10], touchcolor, xp, yp, dolog):
      #print "reflectoin: x:",(xe-x),"y:",(y-(count/2))
      draw.rectangle(((xp-10, yp-10),(xp+10, oy+10)), outline=(100,255,100))
      xd = ((xp - xs)/float(w))*640
      disttop = (((tr-tl)/w) * (xp-xs)) + tl
      vwid = (bl-tl) + (((br-tr)-(bl-tl)) * ((xp - xs)/float(w)))
      yd = ((yp - disttop)/vwid) * 480
      draw2.rectangle(((xd-5, yd-5),(xd+5, yd+5)), outline=(100,255,100), fill=(100,255,100))
      
      #global mousectl, mousedown, lastcoord, lasttime
      #import datetime, math
      #if lasttime != 0:
      #  dist = math.sqrt((xd-lastcoord[0])*(xd-lastcoord[0]) + (yd-lastcoord[1])*(yd-lastcoord[1]))
      #  timediff = datetime.datetime.now() - lasttime
      #  if dist/(timediff.microseconds/1000) < 5:
      #    if mousedown == False:
      #      mousedown = True
      #      mousectl.mouse_down(1)
      #    scr = mousectl.get_screen_resolution()
      #    mousectl.mouse_warp(int(1600*(xd/640.0)),int(1200*(yd/480.0)))
      #lasttime = datetime.datetime.now()
    else:
      #global mousectl, mousedown
      #if mousedown == True:
      #  pass
      #  mousectl.mouse_up(1)
      #mousedown = False
      pass
  if mode == "draw":
    return canvas
  elif mode == "transform":
    return im.transform((640,480), Image.QUAD, (xs,tl,xs,bl,xe,br,xe,tr))
  else:
    return im


