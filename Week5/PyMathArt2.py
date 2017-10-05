# PyMathArt.py

from OpenGL.GL import *
from OpenGL.GLU import *
from OpenGL.GLUT import *
from numpy import *
import sys

#  Set the global width, height, and axis ranges of the window
global width
global height
global axrng

#  Initial values
width = 500
height = 500
axrng = 10.0
                
def init():
    glClearColor(1.0, 1.0, 1.0, 1.0)
    
def plotmathart():
    glClear(GL_COLOR_BUFFER_BIT)
##  glBegin(GL_POINTS)

    x_step_size = float(2*axrng/width)
    y_step_size = float(2*axrng/height)
    
    for x in arange(-axrng, axrng,x_step_size):
        for y in arange(-axrng, axrng,y_step_size): 
            r = cos(x) + sin(y)
            glBegin(GL_POINTS)
            glColor3f(cos(y*r), cos(x*y*r), sin(r*x))
            #glColor3f(cos(r), cos(r), cos(r))
            glVertex2f(x,y)
            glEnd()
            glFlush()
                        
    
def reshape(w, h):
    
    # To insure we don't have a zero height
    if h==0:
        h = 1
    
    #  Fill the entire graphics window!
    glViewport(0, 0, w, h)
    
    #  Set the projection matrix... our "view"
    glMatrixMode(GL_PROJECTION)
    glLoadIdentity()
    
    #  Set the aspect ratio of the plot so that it
    #  Always looks "OK" and never distorted.
    if w <= h:
        gluOrtho2D(-axrng, axrng, -axrng*h/w, axrng*h/w)
    else:
        gluOrtho2D(-axrng*w/h, axrng*w/h, -axrng, axrng)
    
    #  Set the matrix for the object we are drawing
    glMatrixMode(GL_MODELVIEW)
    glLoadIdentity()
    
def keyboard(key, x, y):
    #  Allows us to quit by pressing 'Esc' or 'q'
    print (key)
    if key == b"\x1b":
        sys.exit()
    if key == b"q":
        sys.exit()

def main():
    global width
    global height
    
    glutInit(sys.argv)
    glutInitDisplayMode(GLUT_RGB|GLUT_SINGLE)
    glutInitWindowPosition(100,100)
    glutInitWindowSize(width,height)
    glutCreateWindow(b"Math Art Patterns")
    glutReshapeFunc(reshape)
    glutDisplayFunc(plotmathart)
    glutKeyboardFunc(keyboard)
    
    init()  
    glutMainLoop()

main()    

#End of Program
