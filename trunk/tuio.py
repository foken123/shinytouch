from os import curdir, sep
import SocketServer
import osc
import json
import socket
import math
import sys

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
fseq_count = 0
touches = {}

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
  args = ["alive"]
  args.extend([t.id for t in touches.values()])
  osc.sendMsg("/tuio/2Dcur", args, osc_host, osc_port)
  
def fseq():
  global fseq_count
  osc.sendMsg("/tuio/2Dcur", ["fseq", fseq_count], osc_host, osc_port)
  fseq_count += 1

def move(id, x, y):
  global touches
  touches[id].update(x, y, now_time())
  #msg(["set", id, touches[id].x, touches[id].y, touches[id].X, touches[id].Y, touches[id].m])
  osc.sendMsg("/tuio/2Dcur", ["set", id, touches[id].x, touches[id].y, touches[id].X, touches[id].Y, touches[id].m], osc_host, osc_port)
  
def now_time():
  import time
  return int(time.time()*1000)

osc.init()
