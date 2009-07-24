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
  
  
def colorTestRGB(x, y, dolog = False):
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


