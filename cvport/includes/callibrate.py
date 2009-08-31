class Callibrate:
    def __init__(self):
        self.clicks = 0
        
    def click(self, x, y):
        global warp_points, perspective
        warp_points[self.clicks] = [x, y]

        print "Click"

        if self.clicks==3: # last click
            self.clicks=0
            perspective.update_matrix()
        else:
            self.clicks=self.clicks+1
            
            
