#convert to HSV, yay python standard library!
def hsv(c):
  return colorsys.rgb_to_hsv(c[0]/255.0, c[1]/255.0, c[2]/255.0)

#grade hue by diff
def hueDiffGrade(c, d):
  chsv = hsv(c)
  dhsv = hsv(d)
  return dhsv[0]-chsv[0]
  
  
#OMFG THIS ONE IS BRILLIANT
def colorTestHue(x, y, dolog = False):
  global imv, testmode, buildrange, draw, pix
  if buildrange == True:
    return False
    
  reflect = 5
  reflect_range = 25
  background_top = 10
  
  
  c = pix[x+reflect,y] #reflection
  d = pix[x+reflect,y-background_top] #background
  t = pix[x-5,y] #color of the finger
  
  cdg = 200 *(abs(hueDiffGrade(c,d)))
  
  if dolog == True:
    print "Finger ",t
    print "Reflection ",c
    print "Background ",d
    
  pix[x+reflect,y] = (255,255,255,255)
  pix[x+reflect,y-background_top] = (255,0,255,255)

  
  draw.rectangle(((40,0),(80,40)), fill=c)
  draw.rectangle(((80,0),(120,40)), fill=d)

  draw.line(((0, 20), (cdg, 20)), fill=(255,0,0), width=10)

  draw.line(((reflect_range, 0), (reflect_range, 40)), fill=(0,0,255))

  draw.text((0,20), str(cdg), fill=(0,0,0))

  if cdg > reflect_range:
    return True
  return False

#huesumstuff
def colorTestHueSum(x, y, dolog = False):
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
