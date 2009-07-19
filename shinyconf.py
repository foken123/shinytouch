rmax = -255
rmin = 255
gmax = -255
gmin = 255
bmax = -255
bmin = 255


lastx = 0
lasty = 0
lastt = 0


imv = .3

testmode = "reflection"

  
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
  while colorTriDiff(pix[x+xt+xi,y+yt+yi],pix[x+xt,y+yt],pix[x,y-smarty]) < 0:
    pix[x+xt,y+yt] = (255,255,255,255)
    xt += xi
    yt += yi
    if xt + x < 5 or xt + x > 630 or yt+y < 5 or yt+y > 470:
      return yt+xt
  return yt+xt

def colorTriDiff(c, f, s):
  return (valueTriDiff(c[0], f[0], s[0]) + valueTriDiff(c[1], f[1], s[1]) + valueTriDiff(c[2], f[2], s[2]))/3.0
  
def valueTriDiff(compare, first, second):
  return abs(abs(first - compare) - abs(second - compare))

def colorTargetMatch(c):
  if c[0] < rmax and c[0] > rmin: #red
    if c[1] < gmax and c[1] > gmin: #green
      if c[2] < bmax and c[2] > bmin: #blue
        return True
  return False

def colorTest(x, y, dolog = False):
  global imv, testmode, buildrange, draw, pix
  c = pix[x+5,y]
  d = pix[x+5,y-10]
  t = pix[x-5,y]
  
  
  sumfs = 0
  for xpix in range(8,15):
    flen =  measureLength(x-xpix,y)+abs(measureLength(x-xpix,y-1,yi=-1,smarty=-30))
    slen =  measureLength(x+xpix,y,r=10)+abs(measureLength(x+xpix,y-1,yi=-1,r=10,smarty=-30))
    
    #print flen-slen
    sumfs += abs(flen-slen)
    #if abs(flen-slen) > 20:
    #  return False
  print sumfs / (8-16)
  if sumfs / (8-16) > 5:
    return False
  return True
  
  if buildrange == True:
    return False
  if testmode == "shadow":
    dAV = colorDiffAverage(c,d)
    draw.text((x,y), str(dAV), fill=(0,0,0))
    if dAV < -20:
      return True
    return False
  else:
    if dolog == True:
      irIM = float(c[0]-d[0])/float(t[0]-d[0])
      igIM = float(c[1]-d[1])/float(t[1]-d[1])
      ibIM = float(c[2]-d[2])/float(t[2]-d[2])
      print "Ideal rIM",irIM
      print "Ideal gIM",igIM
      print "Ideal bIM",ibIM
      print "Ideal total IM",(irIM+igIM+ibIM)/4.0
    sm = 1.0-imv
    ra = t[0]*imv + d[0]*sm
    ga = t[1]*imv + d[1]*sm
    ba = t[2]*imv + d[2]*sm
    r = c[0] - ra
    g = c[1] - ga
    b = c[2] - ba
    draw.line(((x,y),(x+40,y)), fill=(ra,ga,ba))
    #draw.text((x,y), str(int(r))+","+str(int(g))+","+str(int(b)), fill=(0,0,0))
    if dolog == True:
      print "Red",r
      print "Green",g
      print "Blue",b
    if r > -55 and r < -20:
      if g > -20 and g < 10:
        if b > -25 and b < 5:
          return True
    return False

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

