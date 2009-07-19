#this is the perspective distortion configuration section
xs = 203
xe = 285

tl = 164
bl = 391

tr = 65
br = 450

#this is the color detection configuration section
rmin = 255
rmax = -255

gmin = 255
gmax = -255

bmin = 255
bmax = -255

#DO NOT EDIT BEYOND THIS POINT
w = xe-xs
ytr = float(tl-tr)/float(w);
ybr = float(bl-br)/float(w);