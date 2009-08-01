import tuio

def handle_touch(x, y):
  print "Touch",x,y
  tuio.alive([1]) #one alive
  tuio.fseq()
  tuio.move(1, x, y)
  
def handle_lift():
  print "Lift"
  tuio.alive([]) #none alive
  
