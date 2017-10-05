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

        a = 4
        b = 2
        c = 1
        d = 1
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
	glutInitWindowSize(500,500)
	glutCreateWindow(b"#9")
	glutDisplayFunc(plotFunc)
	
	init()
	glutMainLoop()

main()
