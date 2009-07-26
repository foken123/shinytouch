#this is the perspective distortion configuration section
xs = 260
xe = 313

tl = 225
bl = 359

tr = 203
br = 377

#this is the color detection configuration section
rmin = 172
rmax = 243

gmin = 105
gmax = 185

bmin = 79
bmax = 180

#DO NOT EDIT BEYOND THIS POINT
w = xe-xs
ytr = float(tl-tr)/float(w);
ybr = float(bl-br)/float(w);