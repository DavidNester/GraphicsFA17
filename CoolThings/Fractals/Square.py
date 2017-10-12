class Square(object):
    def __init__(self,b_left,b_right):
        self.b_left = b_left
        self.b_right = b_right
        self.step = 1.0
        self.width = distance(b_left,b_right)
    def points(self):
        return self.b_left,self.b_right,self.t_right(),self.t_left()
    def up(self):
        self.b_left = (self.b_left[0],self.b_right[1] + 1.0)
        self.b_right = (self.b_right[0],self.b_right[1] + 1.0)
    def down(self):
        self.b_left = (self.b_left[0],self.b_right[1] - 1.0)
        self.b_right = (self.b_right[0],self.b_right[1] - 1.0)
    def left(self):
        self.b_left = (self.b_left[0] - 1.0,self.b_right[1])
        self.b_right = (self.b_right[0] - 1.0,self.b_right[1])
    def right(self):
        self.b_left = (self.b_left[0] + 1.0,self.b_right[1])
        self.b_right = (self.b_right[0] + 1.0,self.b_right[1])
    def t_left(self):
        return (self.b_left[0],self.b_left[1]+self.width)
    def t_right(self):
        return (self.b_right[0],self.b_right[1]+self.width)

def distance(x,y):
    return ((x[0]-y[0])**2 + (x[1]-y[1])**2)**.5

def point(pt,d,m):
    x = pt[0] + (d)/((1+m**2)**.5)
    y = pt[1] + (d*m)/((1+m**2)**.5)
    return x,y

def slopeInt(x,y):
    m = (y[1]-x[1])/(y[0]-x[0])
    return m,(x[1] - m*x[0])

def others(x,y):
    cond1 = (x[0] >= y[0])
    cond2 = (x[1] >= y[1])
    mult = 1
    if not cond1 and not cond2:
        mult = -1
    elif cond1 and not cond2:
        mult = -1
    m,b = slopeInt(x,y)
    m2 = -1/m
    return point(x,mult*distance(x,y),m2),point(y,mult*distance(x,y),m2)
