#pygame.display.set_mode(resolution=(0,0), flags=0, depth=0): return Surface

def colorTargetMatch(c):
  if c[0] < rmax and c[0] > rmin: #red
    if c[1] < gmax and c[1] > gmin: #green
      if c[2] < bmax and c[2] > bmin: #blue
        return True
  return False
  
def expandTargetRange(cr):
  global rmin, rmax, gmin, gmax, bmin, bmax
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
