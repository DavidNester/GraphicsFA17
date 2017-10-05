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
	gluOrtho2D(-2.0, 2.0, -2.0, 2.0)

def plotFunc():
        glClear(GL_COLOR_BUFFER_BIT)
        glColor3f(0.0, 0.0, 0.0)
        glPointSize(1.0)
        
        for a in arange(0.1, 2.0, 0.1):
            for t in arange(-4.4, 4.4, 0.01):
                x = 0.3*a*(t*t - 3)
                y = 0.1*a*t*(t*t - 3)
                glBegin(GL_POINTS)
                glVertex2f(x, y)
                glEnd()
        glFlush()
# End of plotfunc block

def main():
	glutInit(sys.argv)
	glutInitDisplayMode(GLUT_SINGLE|GLUT_RGB)
	glutInitWindowPosition(50,50)
	glutInitWindowSize(500,500)
	glutCreateWindow(b"#6")
	glutDisplayFunc(plotFunc)
	
	init()
	glutMainLoop()

main()
