def measureLength(x,y,xi=0,yi=1,r=25,smarty=30): #start x, start y, x incrementer, y incrementer
  xt = 0
  yt = 0
  #while colorDiffGrade(pix[x+xt,y+yt],pix[x+xt+xi,y+yt+yi]) < r: #use a more fine tuned function
  if smarty > 0:
    bgcolor = pix[x,y-15]
    pix[x,y-15] = (0,0,255)
  else:
    bgcolor = pix[x,y+15]
    pix[x,y+15] = (0,0,255)
  targetcolor = avg_color((pix[x,y],pix[x+1,y],pix[x,y+1]))
  while hueTriDiff(pix[x+xt+xi,y+yt+yi],targetcolor,bgcolor) < 0:
    pix[x+xt,y+yt] = (255,255,255,255)
    xt += xi
    yt += yi
    if xt + x < 5 or xt + x > 630 or yt+y < 5 or yt+y > 470:
      return 0
      #return yt+xt
  return yt+xt

def avg_color(colors):
  r = 0.0
  g = 0.0
  b = 0.0
  for color in colors:
    r += color[0]
    g += color[1]
    b += color[2]
  l = len(colors)
  return (r/l, g/l, b/l)

def in_range(x,y,space=20):
  global width, height
  return x < width - space and x > space and y > space and y < height - space

def colorTriDiff(c, f, s):
  return (valueTriDiff(c[0], f[0], s[0]) + valueTriDiff(c[1], f[1], s[1]) + valueTriDiff(c[2], f[2], s[2]))/3.0
  
def hueTriDiff(c, f, s):
  return valueTriDiff(hsv(c)[0], hsv(f)[0], hsv(s)[0])  
  
def valueTriDiff(compare, first, second):
  #if (first - compare) < 0 or (second - compare) < 0:
  #  print 'compare',compare
  #  print 'first', first
  #  print 'sec', second
  return abs(first - compare) - abs(second - compare)


def colorTestLength(x, y, dolog = False):
  global imv, testmode, buildrange, draw, pix
  if buildrange == True:
    return False
  
  c = pix[x+5,y]
  d = pix[x+5,y-10]
  t = pix[x-5,y]
  
  #draw.line(((x-4,y),(x+4,y)),fill=(255,255,0))
  #draw.line(((x,y-4),(x,y+4)),fill=(255,255,0))
  
  sumfs = 0
  sy = y
  fy = y
  
  for xpix in range(6,15):
    fpeak = measureLength(x-xpix,fy)
    speak = measureLength(x+xpix,sy)
    flen =  fpeak+abs(measureLength(x-xpix,fy-1,yi=-1,smarty=-30))
    slen =  speak+abs(measureLength(x+xpix,sy-1,yi=-1,smarty=-30))
    
    newfy = fy + fpeak - (flen/2)
    newsy = sy + speak - (slen/2)
    
    if in_range(x-xpix, newfy) and in_range(x + xpix, newsy):
      pix[x-xpix, newfy] = (255,0,0)
      pix[x+xpix, newsy] = (255,0,0)
      if abs(sy - newsy) < 5:
        sy = newsy
      if abs(fy - newfy) < 5:
        fy = newfy
      #sy = newsy
      #fy = newfy
      
    
    #print flen-slen
    sumfs += 42*(abs(flen/(slen+1))-1)
    #if abs(flen-slen) > 20:
    #  return False
  #print sumfs / abs(float(6-15))
  
  maxfs = 5
  
  avgfs = sumfs / abs(float(6-15))
  
  draw.line(((150, 20), (150+avgfs, 20)), fill=(255,0,0), width=10)
  draw.line(((150+maxfs, 0), (150+maxfs, 40)), fill=(0,0,255))
  
  if avgfs > maxfs:
    return False
  return True

#divide as floats and return 0 if divide by zero
def fdivide(a,b):
  if b == 0:
    return 1.0
  return float(a)/float(b)





