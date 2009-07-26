
def colorDiffGrade(c,d):
  r = c[0]-d[0]
  g = c[1]-d[1]
  b = c[2]-d[2]
  return abs(r) + abs(g) + abs(b)


def img_diff(w, h):
  global diffmap, pix, oldpix, diffpix, scantimes
  count = 0
  todopix = []
  for x in range(0, w):
    for y in range(0, h):
      if colorDiffGrade(pix[x,y], oldpix[x,y]) > 21:
        count += 1
        todopix.append((x,y))
  ratio = float(count)/float(w*h)
  print "R:",ratio
  if ratio < 0.5:
    scantimes += 1
    for lc in todopix:
      x = lc[0]
      y = lc[1]
      diffpix[x,y] = (diffpix[x,y][0]+1,diffpix[x,y][1]+1,diffpix[x,y][2]+1)
    return diffmap
  else:
    pix = oldpix
    return False


def average_img(w, h):
  global diffpix
  mt = 50
  for x in range(0, w):
    for y in range(0, h):
      diffpix[x,y] = (mt*diffpix[x,y][0]/scantimes,mt*diffpix[x,y][1]/scantimes,mt*diffpix[x,y][2]/scantimes)
      
def get_points(w, h):
  global diffpix, diffmap
  average_img(w,h)
  diffdraw = ImageDraw.Draw(diffmap)
  lvc = 0
  tfvw = 0
  fvw = 0
  lvw = 0
  yarr = []
  for x in range(0,w):
    vc = 0
    pvc = 0
    pve = 0
    for y in range(0, h):
      if diffpix[x,y][0] > 40:
        vc += 1
      else:
        if vc > pvc:
          pvc = vc
          pve = y
        vc = 0
    yarr.append((pve-pvc,pve))
    
    #diffdraw.line(((x,0),(x,pve)),fill=(0,255,255))
    #diffdraw.line(((x,0),(x,pvc)),fill=(255,255,255))
    diffpix[x,pvc] = (255,255,255)
    diffpix[x,pve] = (0,255,255)
    #diffpix[x,pve-pvc] = (0,255,0)
    if pvc > lvc:
      lvc = pvc
      if tfvw == 0 and pvc > 30:
        tfvw = x
    elif pvc > 30:
      lvw = x
      fvw = tfvw
    
  diffdraw.line(((lvw,0),(lvw,h)),fill=(0,0,255))
  diffdraw.line(((fvw,0),(fvw,h)),fill=(255,0,0))
  
  diffdraw.line(((0,30),(w,30)),fill=(255,0,0))
  #fvw is first (left)
  #lvw is last (right)
  #[0] is start x (top)
  #[1] is end x (bottom)
  diffdraw.line(((fvw,yarr[fvw][0]),(lvw,yarr[lvw][0])),fill=(0,255,255))
  diffdraw.line(((fvw,yarr[fvw][1]),(lvw,yarr[lvw][1])),fill=(0,255,255))
  
  global xs, xe, tl, bl, tr, br
  
  xs = fvw
  xe = lvw
  tl = yarr[fvw][0]
  bl = yarr[fvw][1]
  tr = yarr[lvw][0]
  br = yarr[lvw][1]
  
  #diffdraw.line(((0,pvc),(w,pvc)),fill=(0,0,255))
  #diffdraw.line(((0,pvc),(w,pvc)),fill=(0,0,255))
  #diffdraw.line(((0,pvc),(w,pvc)),fill=(0,0,255))
