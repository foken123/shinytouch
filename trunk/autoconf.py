#this is the perspective distortion configuration section
xs = 189
xe = 251

tl = 233
bl = 369

tr = 196
br = 389

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