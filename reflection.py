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

def colorTest2(x, y, dolog = False):
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
  if sumfs / abs(float(6-15)) > 10:
    return False
  return True

#divide as floats and return 0 if divide by zero
def fdivide(a,b):
  if b == 0:
    return 1.0
  return float(a)/float(b)

def colorTest(x, y, dolog = False):
  global imv, testmode, buildrange, draw, pix
  if buildrange == True:
    return False
  c = pix[x+15,y]
  d = pix[x+5,y-10]
  t = pix[x-5,y]
  
  irIM = fdivide(c[0]-d[0],t[0]-d[0])
  igIM = fdivide(c[1]-d[1],t[1]-d[1])
  ibIM = fdivide(c[2]-d[2],t[2]-d[2])
  idTL = (irIM+igIM+ibIM)/3.0
  
  print "Ideal rIM",irIM
  print "Ideal gIM",igIM
  print "Ideal bIM",ibIM
  print "Ideal total IM",idTL
  sm = 1.0-imv
  ra = t[0]*imv + d[0]*sm
  ga = t[1]*imv + d[1]*sm
  ba = t[2]*imv + d[2]*sm
  r = c[0] - ra
  g = c[1] - ga
  b = c[2] - ba
  #draw.line(((x,y),(x+40,y)), fill=(ra,ga,ba))
  draw.text((x,y), str(max(0,min(100,int(idTL*100)))), fill=(0,0,0))
  if dolog == True:
    print "Red",r
    print "Green",g
    print "Blue",b
  #if r > -55 and r < -20:
  #  if g > -20 and g < 10:
  #    if b > -25 and b < 5:
  #      return True
  
  pix[x+15,y] = (255,255,255,255)
  pix[x+5,y-10] = (255,0,255,255)
  pix[x-5,y] = (0,0,255,255)
  return False
    
#this project is a failure

def colorDiffGrade(c,d):
  r = c[0]-d[0]
  g = c[1]-d[1]
  b = c[2]-d[2]
  return abs(r) + abs(g) + abs(b)

def colorDiffAverage(c,d):
  r = c[0]-d[0]
  g = c[1]-d[1]
  b = c[2]-d[2]
  return (r + g + b)/3.0

