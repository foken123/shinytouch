def saveconfig():
  conf = generate_autoconf()
  print conf
  f = open('autoconf.py', 'w')
  f.write(conf)
  f.close()
  print "Wrote configuration to file shinyautoconf.py"

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

#DO NOT EDIT BEYOND THIS POINT
w = xe-xs
ytr = float(tl-tr)/float(w);
ybr = float(bl-br)/float(w);"""
  
if os.path.exists("autoconf.py"):
  execfile("autoconf.py")
else:
  saveconfig()
  w = xe-xs
  ytr = float(tl-tr)/float(w);
  ybr = float(bl-br)/float(w);

