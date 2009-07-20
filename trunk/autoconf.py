#this is the perspective distortion configuration section
xs = 197
xe = 292

tl = 166
bl = 403

tr = 49
br = 473

#this is the color detection configuration section
rmin = 172
rmax = 220

gmin = 105
gmax = 153

bmin = 79
bmax = 142

#DO NOT EDIT BEYOND THIS POINT
w = xe-xs
ytr = float(tl-tr)/float(w);
ybr = float(bl-br)/float(w);