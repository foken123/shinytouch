#!/usr/bin/python

from PIL import Image, ImageColor, ImageDraw
import itertools

im = Image.open("2009-07-01-144040.jpg")
#im = im.transform(im.size, Image.QUAD, (32-15,23-10,44-15,192-10,208-15,186-10,208-15,20-10))
pix = im.load()
draw = ImageDraw.Draw(im)

box = 10

xs = 275
xe = 414

tr = 61
br = 436

tl = 167
bl = 378


w = xe-xs
ytr = float(tl-tr)/float(w);
ybr = float(bl-br)/float(w);

def colorTargetMatch(c):
  if c[0] < 245 and c[0] > 160: #red
    if c[1] < 220 and c[1] > 120: #green
      if c[2] < 205 and c[2] > 110: #blue
        return True
  return False

def colorReflectionMatch(c):
  if c[0] < 245 and c[0] > 160: #red
    if c[1] < 220 and c[1] > 120: #green
      if c[2] < 205 and c[2] > 110: #blue
        return True
  return False

def colorReflectionDiff(c,d):
  #print "Red",c[0]-d[0]
  if c[0]-d[0] < 30 and c[0]-d[0] > 10: #red
    #print "Green",c[1]-d[1]
    if c[1]-d[1] < -20 and c[1]-d[1] > -40: #green
      #print "Blue",c[2]-d[2]
      if c[2]-d[2] < -20 and c[2]-d[2] > -40: #blue
        return True
  return False

xp = 0
yp = 0
wp = 0

for x in range(0, w):
  count = 0
  for y in range(tr + int(ytr*x), br + int(ybr * x)):
    if colorTargetMatch(pix[xe-x,y]):
      pix[xe-x,y] = (0,255,0,255)
      count += 1
    else:
      #pix[xe-x,y] = (0,0,0,255)
      if count > 5:
        #print "x:",(xe-x),"y:",(y-(count/2))
        xp = xe-x
        yp = y-(count/2)
        wp = count
        count = -1
  if count == -1:
    break

if xp > 0 and yp > 0:
  pix[xp,yp] = (255,255,255,255)
  if colorReflectionDiff(pix[xp+5,yp],pix[xp+5,yp-20]):
    print "reflectoin: x:",(xe-x),"y:",(y-(count/2))
    draw.rectangle(((xp-10, yp-10),(xp+10, yp+10)), outline=(100,255,100))
  else:
    print "fayle"
    
im.show()
im.save("ShinyOut.png", "PNG")
