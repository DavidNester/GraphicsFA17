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
        #VARIABLES
        #************************
        #doesnt make the exact one from the book but it is still a lissajous
        A = 1
        B = 1
        omega_x = 4
        omega_y = 5
        delta_x = math.pi/2
        delta_y = math.pi/2
        #************************
        for t in arange(-4.0, 4.0+stepsize, stepsize):
                x = A*cos(omega_x*t + delta_x)
                y = B*cos(omega_y*t + delta_y)
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
	glutCreateWindow(b"Lissajous")
	glutDisplayFunc(plotFunc)
	
	init()
	glutMainLoop()

main()
