def get_image(dolog = False, getpix = False):
  global im, pix, draw, imsrc
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
    if x % 3 > 0:
      continue
    for y in range(tr + int(ytr*x), br + int(ybr * x)):
      if y % 4 > 0:
        continue
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
    else:
      #print "fayle"
      pix[xp+5,oy-10] = (255,255,255,255)
      pix[xp+5,yp] = (255,0,255,255)
      pix[xp-5,yp] = (0,0,255,255)
  if mode == "draw":
    return canvas
  elif mode == "transform":
    return im.transform((640,480), Image.QUAD, (xs,tl,xs,bl,xe,br,xe,tr))
  else:
    return im


