rmin = 255
rmax = -255

gmin = 255
gmax = -255

bmin = 255
bmax = -255

xs = 203
xe = 285

tl = 164
bl = 391

tr = 65
br = 450


imv = .3

testmode = "reflection"
imsrc = "2009-07-20-102011.jpg"
imsrc = "2009-07-20-103327.jpg"
imsrc = "cam"
  
#def colorTargetMatch(c):
#  if c[0] < 245 and c[0] > 170: #red
#    if c[1] < 220 and c[1] > 85: #green
#      if c[2] < 205 and c[2] > 70: #blue
#        return True
#  return False


import colorsys
  

def measureLength(x,y,xi=0,yi=1,r=25,smarty=30): #start x, start y, x incrementer, y incrementer
  xt = 0
  yt = 0
  #while colorDiffGrade(pix[x+xt,y+yt],pix[x+xt+xi,y+yt+yi]) < r: #use a more fine tuned function
  bgcolor = pix[x,y-30]
  targetcolor = pix[x,y]
  while colorTriDiff(pix[x+xt+xi,y+yt+yi],targetcolor,bgcolor) < 0:
    pix[x+xt,y+yt] = (255,255,255,255)
    xt += xi
    yt += yi
    if xt + x < 5 or xt + x > 630 or yt+y < 5 or yt+y > 470:
      return yt+xt
  return yt+xt

def colorTriDiff(c, f, s):
  return (valueTriDiff(c[0], f[0], s[0]) + valueTriDiff(c[1], f[1], s[1]) + valueTriDiff(c[2], f[2], s[2]))/3.0
  
def valueTriDiff(compare, first, second):
  return abs(first - compare) - abs(second - compare)

def colorTargetMatch(c):
  if c[0] < rmax and c[0] > rmin: #red
    if c[1] < gmax and c[1] > gmin: #green
      if c[2] < bmax and c[2] > bmin: #blue
        return True
  return False

def colorTestLineWidth(x, y, dolog = False):
  global imv, testmode, buildrange, draw, pix
  if buildrange == True:
    return False
  
  c = pix[x+5,y]
  d = pix[x+5,y-10]
  t = pix[x-5,y]
  
  draw.line(((x-4,y),(x+4,y)),fill=(255,255,0))
  draw.line(((x,y-4),(x,y+4)),fill=(255,255,0))
  
  sumfs = 0
  for xpix in range(6,15):
    flen =  measureLength(x-xpix,y)+abs(measureLength(x-xpix,y-1,yi=-1,smarty=-30))
    slen =  measureLength(x+xpix,y)+abs(measureLength(x+xpix,y-1,yi=-1,smarty=-30))
    if y < 445 and y > 35:
      pix[x-xpix,y+30] = (255,0,255)
      pix[x-xpix,y-30] = (255,0,255)
      pix[x+xpix,y+30] = (255,0,255)
      pix[x+xpix,y-30] = (255,0,255)
      
    #print flen-slen
    sumfs += abs(flen-slen)
    #if abs(flen-slen) > 20:
    #  return False
  print sumfs / abs(float(6-15))
  
  
  draw.line(((100, 20), (100+sumfs, 20)), fill=(255,0,0), width=10)
  
  if sumfs / abs(float(6-15)) > 10:
    return False
  return True

#divide as floats and return 0 if divide by zero
def fdivide(a,b):
  if b == 0:
    return 1.0
  return float(a)/float(b)

#OMFG THIS ONE IS BRILLIANT
def colorTest(x, y, dolog = False):
  global imv, testmode, buildrange, draw, pix
  if buildrange == True:
    return False
  c = pix[x+10,y] #reflection
  d = pix[x+10,y-15] #background
  
  cdg = 200 *(abs(hueDiffGrade(c,d)))
  
  if dolog == True:
    print "Finger ",t
    print "Reflection ",c
    print "Background ",d
    
  pix[x+10,y] = (255,255,255,255)
  pix[x+10,y-15] = (255,0,255,255)

  draw.line(((0, 20), (cdg, 20)), fill=(255,0,0), width=10)
  draw.rectangle(((40,0),(80,40)), fill=c)
  draw.rectangle(((80,0),(120,40)), fill=d)

  draw.text((0,20), str(cdg), fill=(0,0,0))

  if cdg > 25:
    return True
  
  return False
  

def colorTest3(x, y, dolog = False):
  global imv, testmode, buildrange, draw, pix
  if buildrange == True:
    return False
  c = pix[x+10,y] #reflection
  d = pix[x+10,y-15] #background
  t = pix[x-5,y] #color of the finger
  
  irIM = fdivide(c[0]-d[0],t[0]-d[0])
  igIM = fdivide(c[1]-d[1],t[1]-d[1])
  ibIM = fdivide(c[2]-d[2],t[2]-d[2])
  
  pix[x+10,y] = (255,255,255,255)
  pix[x+10,y-15] = (255,0,255,255)
  pix[x-5,y] = (0,0,255,255)
  
  
  
  #draw.line(((x,y),(x+40,y)), fill=(ra,ga,ba))
  
  if dolog == True:
    print "Finger ",t
    print "Reflection ",c
    print "Background ",d
    print "Ideal rIM",irIM
    print "Ideal gIM",igIM
    print "Ideal bIM",ibIM
  #if r > -55 and r < -20:
  #  if g > -20 and g < 10:
  #    if b > -25 and b < 5:
  #      return True
  
  
  draw.rectangle(((0,0),(40,40)), fill=t)
  draw.rectangle(((40,0),(80,40)), fill=c)
  draw.rectangle(((80,0),(120,40)), fill=d)
  
  
  draw.text((0,20), str(int(irIM*10000)/100), fill=(0,0,0))
  draw.text((40,20), str(int(igIM*10000)/100), fill=(0,0,0))
  draw.text((80,20), str(int(ibIM*10000)/100), fill=(0,0,0))
  
  draw.line(((100, 10), (100+int(irIM*10000)/100, 10)), fill=(255,0,0), width=10)
  draw.line(((100, 30), (100+int(igIM*10000)/100, 30)), fill=(0,255,0), width=10)
  draw.line(((100, 50), (100+int(ibIM*10000)/100, 50)), fill=(0,0,255), width=10)
  
  pix[x+10,y] = (255,255,255,255)
  pix[x+10,y-15] = (255,0,255,255)
  pix[x-5,y] = (0,0,255,255)
  
  if irIM > 0.1:
    return True
  
  return False



def colorTestWHATEVER(x, y, dolog = False):
  global imv, testmode, buildrange, draw, pix
  if buildrange == True:
    return False
  c = pix[x+10,y] #reflection
  d = pix[x+10,y-15] #background
  t = pix[x-5,y] #color of the finger
  
  ihIM = fdivide(hsv(c)[0]-hsv(d)[0],hsv(t)[0]-hsv(d)[0])
  
  pix[x+10,y] = (255,255,255,255)
  pix[x+10,y-15] = (255,0,255,255)
  pix[x-5,y] = (0,0,255,255)
  
  
  #draw.line(((x,y),(x+40,y)), fill=(ra,ga,ba))
  
  if dolog == True:
    print "Finger ",t
    print "Reflection ",c
    print "Background ",d
    print "Ideal Hue IM",ihIM
  #if r > -55 and r < -20:
  #  if g > -20 and g < 10:
  #    if b > -25 and b < 5:
  #      return True
  
  
  draw.rectangle(((0,0),(40,40)), fill=t)
  draw.rectangle(((40,0),(80,40)), fill=c)
  draw.rectangle(((80,0),(120,40)), fill=d)
  
  
  draw.text((0,20), str(int(ihIM*10000)/100), fill=(0,0,0))
  
  draw.line(((100, 30), (100+int(ihIM*10000)/100, 30)), fill=(0,255,0), width=10)
  
  pix[x+10,y] = (255,255,255,255)
  pix[x+10,y-15] = (255,0,255,255)
  pix[x-5,y] = (0,0,255,255)
  
  if ihIM > 0.1:
    return True
  
  return False

#this project is a failure

def colorDiffGrade(c,d):
  r = c[0]-d[0]
  g = c[1]-d[1]
  b = c[2]-d[2]
  return abs(r) + abs(g) + abs(b)

def hsv(c):
  return colorsys.rgb_to_hsv(c[0]/255.0, c[1]/255.0, c[2]/255.0)

def hueDiffGrade(c, d):
  chsv = hsv(c)
  dhsv = hsv(d)
  return dhsv[0]-chsv[0]
  
def colorDiffAverage(c,d):
  r = c[0]-d[0]
  g = c[1]-d[1]
  b = c[2]-d[2]
  return (r + g + b)/3.0

