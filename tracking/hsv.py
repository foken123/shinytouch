#pygame.display.set_mode(resolution=(0,0), flags=0, depth=0): return Surface

#convert to HSV, yay python standard library!
def hsv(c):
  return colorsys.rgb_to_hsv(c[0]/255.0, c[1]/255.0, c[2]/255.0)

def colorTargetMatch(c):
  c = hsv(c)
  if c[0] < rmax and c[0] > rmin: #red
    if c[1] < gmax and c[1] > gmin: #green
      if c[2] < bmax and c[2] > bmin: #blue
        return True
  return False
  
def expandTargetRange(cr):
  global rmin, rmax, gmin, gmax, bmin, bmax
  cr = hsv(cr)
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
