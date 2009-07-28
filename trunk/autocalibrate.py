oldpix = 0
oldim = 0
autocal = 0
stateframecount = 0
switchcount = 0
scantimes = 0

diffmap = Image.new("RGB",(width,height))
diffpix = diffmap.load()


def reset_calibrate():
  global oldpix, oldim, autocal, stateframecount, switchcount, scantimes, diffmap, diffpix, width, height
  oldpix = 0
  oldim = 0
  autocal = 0
  stateframecount = 0
  switchcount = 0
  scantimes = 0

  diffmap = Image.new("RGB",(width,height))
  diffpix = diffmap.load()

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
  average_img(w, h) #average out values
  diffdraw = ImageDraw.Draw(diffmap) #create canvas
  bar_heights = []
  global_peak_height = 0
  last_peak_height = 0
  last_last_peak_height = 0
  temp_end_width = 0
  end_width = 0
  start_width = 0
  temp_start_width = 0
  jump_peak = -10
  for x in range(0,w): #loop horizontally
    consec_height = 0 #current vertical bar containing screen
    peak_consec_height = 0 #peak
    peak_consec_end = 0 #end of peak
    for y in range(0, h): #loop vertically
      if diffpix[x,y][0] > 40: #if gray-ish and not blackish
        consec_height += 1
      else:
        if consec_height >  peak_consec_height:
          peak_consec_height = consec_height
          peak_consec_end = y
        consec_height = 0
    bar_heights.append((peak_consec_end - peak_consec_height, peak_consec_end))
    #diffdraw.line(((x,0),(x,peak_consec_height)),fill=(0,255,0))
    if peak_consec_height + 5 > global_peak_height:
      if peak_consec_height > global_peak_height:
        global_peak_height = peak_consec_height
      #do stuff like stuff
      temp_end_width = x
      if last_last_peak_height - peak_consec_height > jump_peak and peak_consec_height > 30 and temp_start_width == 0:
        jump_peak = last_peak_height - peak_consec_height
        #diffdraw.line(((x,100),(x,100+10*(last_last_peak_height - peak_consec_height))),fill=(255,0,0))
        temp_start_width = x
    elif peak_consec_height > 30:
      #end
      end_width = temp_end_width
      start_width = temp_start_width
      #temp_end_width = 0
      #temp_start_width = 0
    last_last_peak_height = last_peak_height
    last_peak_height = peak_consec_height
  diffdraw.line(((end_width,0),(end_width,h)),fill=(0,0,255))
  diffdraw.line(((start_width,0),(start_width,h)),fill=(255,0,0))

  global xs, xe, tl, bl, tr, br
  
  
  xs = start_width - 1
  xe = end_width + 1
  tl = bar_heights[start_width][0]
  bl = bar_heights[start_width][1]
  tr = bar_heights[end_width][0]
  br = bar_heights[end_width][1]

  diffdraw.line(((xs, tl),(xe, tr)),fill=(0,255,255))
  diffdraw.line(((xs, bl),(xe, br)),fill=(0,255,255))

  conf_calc()

def get_pointssomething(w, h):
  global diffpix, diffmap
  average_img(w,h)
  diffdraw = ImageDraw.Draw(diffmap)
  lvc = 0
  tfvw = 0
  fvw = 0
  lvw = 0
  lastvc = 0
  peakdiff = 0
  yarr = []
  for x in range(0,w): #loop horizontally
    vc = 0 #vertical length
    pvc = 0 #peak vertical
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
    
    
    diffdraw.line(((x,0),(x,max(0,pvc - lastvc))),fill=(0,255,0))
    #diffdraw.line(((x,0),(x,pvc)),fill=(255,255,255))
    diffpix[x,pvc] = (255,255,255)
    diffpix[x,pve] = (255,255,0)
    #diffpix[x,vc - lastvc] = (0,255,0)
    
    #diffpix[x,pve-pvc] = (0,255,0)
    if pvc > lvc:
      lvc = pvc
      if lastvc - pvc > peakdiff:
        print peakdiff, x
        diffdraw.line(((x,0),(x,h)),fill=(0,255,0))
        tfvw = x
        peakdiff = lastvc - pvc
    elif pvc > 30:
      lvw = x-1
      fvw = tfvw+1
    lastvc = vc
  diffdraw.line(((lvw,0),(lvw,h)),fill=(0,0,255))
  diffdraw.line(((fvw,0),(fvw,h)),fill=(255,0,0))
  
  diffdraw.line(((0,30),(w,30)),fill=(255,0,0))
  #fvw is first (left)
  #lvw is last (right)
  #[0] is start x (top)
  #[1] is end x (bottom)
  #diffdraw.line(((fvw,yarr[fvw][0]),(lvw,yarr[lvw][0])),fill=(0,255,255))
  #diffdraw.line(((fvw,yarr[fvw][1]),(lvw,yarr[lvw][1])),fill=(0,255,255))
  
  global xs, xe, tl, bl, tr, br
  
  xs = fvw
  xe = lvw
  tl = yarr[fvw+1][0]
  bl = yarr[fvw+1][1]
  tr = yarr[lvw-1][0]
  br = yarr[lvw-1][1]
  
  diffdraw.line(((xs, tl),(xe, tr)),fill=(0,255,255))
  diffdraw.line(((xs, bl),(xe, br)),fill=(0,255,255))
  
  
  #diffdraw.line(((0,pvc),(w,pvc)),fill=(0,0,255))
  #diffdraw.line(((0,pvc),(w,pvc)),fill=(0,0,255))
  #diffdraw.line(((0,pvc),(w,pvc)),fill=(0,0,255))
