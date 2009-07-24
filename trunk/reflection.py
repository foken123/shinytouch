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
  
execfile("engines/hue.py")
execfile("engines/rgb.py")
execfile("engines/length.py")

def colorTest(x, y, dolog = False):
  #return colorTestLength(x, y, dolog)
  return colorTestHue(x, y, dolog)
  #return colorTestLength(x, y, dolog)
  #return colorTestLength(x, y, dolog)






