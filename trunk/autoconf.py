#this is the perspective distortion configuration section
xs = 168
xe = 271

tl = 168
bl = 402

tr = 38
br = 474

#this is the color detection configuration section
rmin = 172
rmax = 220

gmin = 105
gmax = 154

bmin = 79
bmax = 145

#DO NOT EDIT BEYOND THIS POINT
w = xe-xs
ytr = float(tl-tr)/float(w);
ybr = float(bl-br)/float(w);