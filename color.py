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
  
execfile("reflection/hue.py")
execfile("reflection/rgb.py")
execfile("reflection/length.py")

execfile("tracking/rgb.py")

def colorTest(x, y, dolog = False):
  #return colorTestLength(x, y, dolog)
  return colorTestHue(x, y, dolog)
  #return colorTestLength(x, y, dolog)
  #return colorTestLength(x, y, dolog)






