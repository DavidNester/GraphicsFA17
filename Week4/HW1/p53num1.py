# PyFunc.py
# Plotting functions

from OpenGL.GL import *
from OpenGL.GLU import *
from OpenGL.GLUT import *
from numpy import *
import sys
import math
from random import random

def init():
	glClearColor(1.0, 1.0, 1.0, 1.0)
	gluOrtho2D(-5.0, 5.0, -5.0, 5.0)

def keyboard(key,x,y):
    if key == b'q':
        glColor3f(random(), random(), random())
        glutPostRedisplay()

def plotFunc():
        glClear(GL_COLOR_BUFFER_BIT)
        

        glPointSize(1.0)
        stepsize = 0.01
        #VARIABLES
        #************************
        a = .5
        b = .5
        c = .25
        d = 0
        #************************
        for t in arange(-4.0, 4.0+stepsize, stepsize):
                x = (c*t+d)*sin(t)
                y = sin(a*t+b)
                glBegin(GL_POINTS)
                glVertex2f(x,y)
                glEnd()
        glFlush()
# End of plotfunc block

def main():
    glutInit(sys.argv)
    glutInitDisplayMode(GLUT_SINGLE|GLUT_RGB)
    glutInitWindowPosition(50,50)
    glutInitWindowSize(500,500)
    glutCreateWindow(b"#1")
    glutDisplayFunc(plotFunc)
    glutKeyboardFunc(keyboard)
    glColor3f(1.0, 0.0, 0.0)

    init()
    glutMainLoop()

main()
