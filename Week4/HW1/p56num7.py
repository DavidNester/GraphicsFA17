# PyFunc.py
# Plotting functions

from OpenGL.GL import *
from OpenGL.GLU import *
from OpenGL.GLUT import *
from numpy import *
import sys
import math

def init():
	glClearColor(1.0, 1.0, 1.0, 1.0)
	gluOrtho2D(-5.0, 5.0, -5.0, 5.0)

def plotFunc():
        glClear(GL_COLOR_BUFFER_BIT)
        glColor3f(0.0, 0.0, 0.0)

        glPointSize(1.0)
        stepsize = 0.01
        for t in arange(-200.0, 200.0+stepsize, .005):
                x = sin(0.99*t) - 0.7*cos(3.01*t)
                y = cos(1.01*t) + 0.1*sin(15.03*t)
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
	glutInitWindowSize(500,500)
	glutCreateWindow(b"#7")
	glutDisplayFunc(plotFunc)
	
	init()
	glutMainLoop()

main()
