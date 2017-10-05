# PyFunc.py
# Plotting functions

from OpenGL.GL import *
from OpenGL.GLU import *
from OpenGL.GLUT import *
from numpy import *
import sys

def init():
	glClearColor(1.0, 1.0, 1.0, 1.0)
	gluOrtho2D(-5.0, 5.0, -5.0, 5.0)

def plotFunc():
        glClear(GL_COLOR_BUFFER_BIT)
        glColor3f(0.0, 0.0, 0.0)

        glColor3f(0.0, 0.0, 0.0)
        glBegin(GL_LINES)
        glVertex2f(-5.0, 0.0)
        glVertex2f(5.0, 0.0)
        glVertex2f(0.0, 5.0)
        glVertex2f(0.0, -5.0)
        glEnd()

        glPointSize(2.0)
        stepsize = 0.01
        for t in arange(-4.0, 4.0+stepsize, stepsize):
                x = (3.3 - 0.4*t**2)*sin(t)
                y = (2.5 - 0.3*t**2)*cos(t)
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
	glutCreateWindow(b"Cameron MATLAB Homework Pretzel Plotter")
	glutDisplayFunc(plotFunc)
	
	init()
	glutMainLoop()

main()
