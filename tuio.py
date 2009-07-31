import osc

#based on http://www.pillowsopher.com/blog/?p=79

class Touch(object):
    def __init__(self, id):
        self.id = id
        self.x = None
        self.y = None
        self.X = None
        self.Y = None
        self.m = None
        self.time = None
    def update(self, x, y, time):
        if (self.time):
            dt = float(time - self.time) / 1000
            if not ((time - self.time) == 0):
                new_X = (x - self.x) / dt
                new_Y = (y - self.y) / dt
                dX = new_X - self.X
                dY = new_Y - self.Y
                self.m = math.sqrt((dX ** 2) + (dY ** 2))
                self.X = new_X
                self.Y = new_Y
                self.x = x
                self.y = y
                self.time = time
        else:
            self.x = float(x)
            self.y = float(y)
            self.X = 0.0
            self.Y = 0.0
            self.m = 0.0
            self.time = time

osc_host = "127.0.0.1"
osc_port = 3333
fseq = 0

def msg(args):
  global osc_host, osc_port
  osc.sendMsg("/tuio/2dcur", args, osc_host, osc_port)
  
def alive(ids = []):
  global touches
  fseq()
  # remove the touches that are gone from the list
  for id in touches.keys():
      if not id in ids:
          del touches[id]
  # add new touches
  for id in ids:
      if not touches.has_key(id):
          touches[id] = Touch(id)
  tuio_msg(["alive"].extend(ids))
  
def fseq():
  global fseq
  tuio_msg(["fseq", fseq])
  fseq += 1

def move(id, x, y):
  global touches
  touches[id].update(x, y, now_time())
  tuio_msg(["set", id, touches[id].x, touches[id].y, touches[id].X, touches[id].Y, touches[id].m])
  
def now_time():
  import time, datetime
  return time.mktime(datetime.datetime.now().timetuple()



  
  
  
  
  
  
  
  
  
  
