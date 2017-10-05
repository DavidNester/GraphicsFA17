# PyFunc.py
# Plotting functions

from OpenGL.GL import *
from OpenGL.GLU import *
from OpenGL.GLUT import *
from numpy import *
import sys
import math

a = 4
b = 2
c = 3
d = 3

def init():
	glClearColor(1.0, 1.0, 1.0, 1.0)
	gluOrtho2D(-10.0, 10.0, -10.0, 10.0)

#added keyboard control which changes the parameters on the ellipse
#pressing wsad changes the ellipse
def keyboard(key,x,y):
    global a,b,c,d
    if key == b'w':
        c += 1
        d += 1
        glutPostRedisplay()
    elif key == b's':
        c -= 1
        d -= 1
        glutPostRedisplay()
    elif key == b'd':
        a += 1
        b += 1
        glutPostRedisplay()
    elif key == b'a':
        a -= 1
        b -= 1
        glutPostRedisplay()
def plotFunc():
        glClear(GL_COLOR_BUFFER_BIT)
        stepsize = 0.01
        for t in arange(-4.0, 4.0+stepsize, stepsize):
                x = a*cos(t)+c*sin(t)
                y = b*sin(t)+d*cos(t)
                glColor3f(1.0, 0.0, 0.0)
                glBegin(GL_POINTS)
                glVertex2f(x,y)
                glEnd()
                
        glFlush()
# End of plotfunc block

def main():
    glutInit(sys.argv)
    glutInitDisplayMode(GLUT_SINGLE|GLUT_RGB)
    glutInitWindowPosition(50,50)
    glutInitWindowSize(900,900)
    glutCreateWindow(b"hit 'w' 's' 'a' 'd' to alter ellipse")
    glutDisplayFunc(plotFunc)
    glutKeyboardFunc(keyboard)

    init()
    glutMainLoop()

main()
