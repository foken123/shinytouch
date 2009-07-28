def saveconfig():
  conf = generate_autoconf()
  print conf
  f = open('autoconf.py', 'w')
  f.write(conf)
  f.close()
  print "Wrote configuration to file shinyautoconf.py"


def conf_calc():
  global xs, xe, tl, bl, tr, br
  w = xe-xs
  if w != 0:
    ytr = float(tl-tr)/float(w);
    ybr = float(bl-br)/float(w);
  else:
    set_defaults()

def set_defaults():
  global rmin, rmax, gmin, gmax, bmin, bmax
  global xs, xe, tl, bl, tr, br
  rmin = 255
  rmax = -255

  gmin = 255
  gmax = -255

  bmin = 255
  bmax = -255

  xs = 10
  xe = 20

  tl = 100
  bl = 110

  tr = 90
  br = 120

  conf_calc()

set_defaults()

def generate_autoconf():
  return """#this is the perspective distortion configuration section
xs = """+str(xs)+"""
xe = """+str(xe)+"""

tl = """+str(tl)+"""
bl = """+str(bl)+"""

tr = """+str(tr)+"""
br = """+str(br)+"""

#this is the color detection configuration section
rmin = """+str(rmin)+"""
rmax = """+str(rmax)+"""

gmin = """+str(gmin)+"""
gmax = """+str(gmax)+"""

bmin = """+str(bmin)+"""
bmax = """+str(bmax)+"""

#Run calculations based on configuration
conf_calc()
"""


if os.path.exists("autoconf.py"):
  execfile("autoconf.py")
else:
  saveconfig()
  w = xe-xs
  ytr = float(tl-tr)/float(w);
  ybr = float(bl-br)/float(w);
  
  

