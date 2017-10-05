# PyFunc.py
# Plotting functions

from OpenGL.GL import *
from OpenGL.GLU import *
from OpenGL.GLUT import *
from numpy import *
import sys
##import time

def init():
    glClearColor(1.0, 1.0, 1.0, 1.0)
    gluOrtho2D(-5.0, 5.0, -5.0, 5.0)

def plotFunc():
    glClear(GL_COLOR_BUFFER_BIT)
    glColor3f(0.0, 0.0, 0.0)
    glPointSize(3.0)
	
    for x in arange(-5.0,5.0,0.1):
        y = x*x
        glBegin(GL_POINTS)
        glVertex2f(x,y)
        glEnd()
        glFlush()
##        time.sleep(0.25)
        


def main():
    glutInit(sys.argv)
    glutInitDisplayMode(GLUT_SINGLE|GLUT_RGB)
    glutInitWindowPosition(50,50)
    glutInitWindowSize(400,400)
    glutCreateWindow(b"Function Plotter")
    glutDisplayFunc(plotFunc)
	
    init()
    glutMainLoop()

main()
