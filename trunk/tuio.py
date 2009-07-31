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


[{"elementId": "tuio", "action": "alive", "time": 1248986480687, "alive": [8]}, {"elementId": "tuio", "action": "move", "time": 1248986480687, "touches": [{"x": 218, "y": 87, "identifier": 8}]}]
[{"elementId": "tuio", "action": "alive", "time": 1248986481100, "alive": []}]

# remove the touches that are gone from the list
for id in touches.keys():
    if not id in evt['alive']:
        del touches[id]
# add new touches
for id in evt['alive']:
    if not touches.has_key(id):
        touches[id] = Touch(id)
osc.sendMsg("/tuio/2Dcur", ["fseq", fseq], osc_host, osc_port)
fseq += 1
args = ["alive"]
args.extend([t.id for t in touches.values()])
osc.sendMsg("/tuio/2Dcur", args, osc_host, osc_port)

#################MOVE


osc.sendMsg("/tuio/2Dcur", ["fseq", fseq], osc_host, osc_port)
fseq += 1
for t in evt['touches']:
    id = t['identifier']
    touches[id].update(float(t['x'])/surface_width, float(t['y'])/surface_height, evt['time'])
    osc.sendMsg("/tuio/2Dcur", ["set", id, touches[id].x, touches[id].y, touches[id].X, touches[id].Y, touches[id].m], osc_host, osc_port)

