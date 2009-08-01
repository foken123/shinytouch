import tuio

def handle_touch(x, y):
  tuio.alive([1]) #one alive
  tuio.fseq()
  tuio.move(1, x, y)
  
def handle_lift():
  tuio.alive([]) #none alive
  
