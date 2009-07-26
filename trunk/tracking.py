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
scantimes = 0

diffmap = Image.new("RGB",(640,480))
diffpix = diffmap.load()

def colorDiffGrade(c,d):
  r = c[0]-d[0]
  g = c[1]-d[1]
  b = c[2]-d[2]
  return abs(r) + abs(g) + abs(b)


def img_diff(w, h):
  global diffmap, pix, oldpix, diffpix, scantimes
  backup = diffmap
  backuppix = diffpix
  count = 0
  for x in range(0, w):
    for y in range(0, h):
      if colorDiffGrade(pix[x,y], oldpix[x,y]) > 20:
        count += 1
        diffpix[x,y] = (diffpix[x,y][0]+1,diffpix[x,y][1]+1,diffpix[x,y][2]+1)
  ratio = float(count)/float(w*h)
  print "R:",ratio
  if ratio < 0.5:
    scantimes += 1
    return diffmap
  else:
    diffmap = backup
    diffpix = backuppix
    return False


def average_img(w, h):
  global diffpix
  mt = 50
  for x in range(0, w):
    for y in range(0, h):
      diffpix[x,y] = (mt*diffpix[x,y][0]/scantimes,mt*diffpix[x,y][1]/scantimes,mt*diffpix[x,y][2]/scantimes)
      
def get_points(w, h):
  global diffpix, diffmap
  average_img(w,h)
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
      if diffpix[x,y][0] > 60:
        vc += 1
      else:
        if vc > pvc:
          pvc = vc
          pve = y
        vc = 0
    yarr.append((pve-pvc,pve))
    
    #diffdraw.line(((x,0),(x,pve)),fill=(0,255,255))
    #diffdraw.line(((x,0),(x,pvc)),fill=(255,255,255))
    diffpix[x,pvc] = (255,255,255)
    diffpix[x,pve] = (0,255,255)
    diffpix[x,pve-pvc] = (0,255,0)
    if pvc > lvc:
      lvc = pvc
      if tfvw == 0 and pvc > 30:
        tfvw = x
    elif pvc > 30:
      lvw = x
      fvw = tfvw
    
  diffdraw.line(((lvw,0),(lvw,h)),fill=(0,0,255))
  diffdraw.line(((fvw,0),(fvw,h)),fill=(255,0,0))
  
  diffdraw.line(((0,30),(w,30)),fill=(255,0,0))
  #fvw is first (left)
  #lvw is last (right)
  #[0] is start x (top)
  #[1] is end x (bottom)
  diffdraw.line(((fvw,yarr[fvw][0]),(fvw,yarr[fvw][0])),fill=(0,255,255))
  diffdraw.line(((lvw,yarr[lvw][1]),(lvw,yarr[lvw][1])),fill=(0,255,255))
  
  #diffdraw.line(((0,pvc),(w,pvc)),fill=(0,0,255))
  #diffdraw.line(((0,pvc),(w,pvc)),fill=(0,0,255))
  #diffdraw.line(((0,pvc),(w,pvc)),fill=(0,0,255))
  
  
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

  if switchcount == 7:
    get_points(640, 480)
    #autocal = 0
    #switchcount = 0
    #saveconfig()
    switchcount += 1
  if switchcount > 7:
    return diffmap
  if autocal == 1:
    stateframecount += 1
    if stateframecount > 3:
      if switchcount != 0:
        if img_diff(640, 480) == False:
          switchcount -= 1
        import datetime
        #oldim.save("test/Aold"+str(datetime.datetime.now().isoformat())+".png","PNG")
        #im.save("test/Anew"+str(datetime.datetime.now().isoformat())+".png","PNG")
      switchcount+=1
      oldpix = im.load()
      oldim = im
      stateframecount = 0
      autocal = 2
    return Image.new("RGB", (640,480), (255,255,255))
  if autocal == 2:
    stateframecount += 1
    if stateframecount > 3:
      if img_diff(640, 480) == False:
          switchcount -= 1
      import datetime
      #oldim.save("test/Bold"+str(datetime.datetime.now().isoformat())+".png","PNG")
      #im.save("test/Bnew"+str(datetime.datetime.now().isoformat())+".png","PNG")
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


