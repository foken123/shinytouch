#this is the perspective distortion configuration section
xs = 138
xe = 245

tl = 163
bl = 401

tr = 37
br = 476

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