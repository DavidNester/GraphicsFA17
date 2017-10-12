#  PyPoints.py
#  Setting a coordinate system with central origin

from OpenGL.GL import *
from OpenGL.GLU import *
from OpenGL.GLUT import *
import sys
import time
import random

first = [148,75,0,0,255,255,255]
second = [0,0,0,255,255,127,0]
third = [211,130,255,0,0,0,0]
first = [x/255.0 for x in first]
second = [x/255.0 for x in second]
third = [x/255.0 for x in third]
first = first[::-1]
second = second[::-1]
third = third[::-1]

def init():
	glClearColor(1.0, 1.0, 1.0, 0.0)
	gluOrtho2D(0.0, 81.0, 0.0, 81.0)

def frac(origin,width,step):
    glColor3f(first[int(step+2)%7],second[int(step+2)%7],third[int(step+2)%7])
    if step > 6.0:
        return
    x = width/3.0
    a = origin[0]
    b = origin[1]
    glBegin(GL_QUADS)
    glVertex2f(a+2*x,b+x)
    glVertex2f(a+2*x,b+2*x)
    glVertex2f(a+x,b+2*x)
    glVertex2f(a+x,b+x)
    glEnd()
    width = width/3.0

    frac(origin,width,step+1.0)
    frac((a,b+x),width,step+1.0)
    frac((a,b+2*x),width,step+1.0)
    frac((a+x,b),width,step+1.0)
    frac((a+x,b+2*x),width,step+1.0)
    frac((a+2*x,b),width,step+1.0)
    frac((a+2*x,b+x),width,step+1.0)
    frac((a+2*x,b+2*x),width,step+1.0)


def plotPoints():
    glClear(GL_COLOR_BUFFER_BIT)
    glClearColor(1.0, 1.0, 1.0, 0.0)
    glColor3f(0.5,0.5,0.5)
    
    
    frac((0.0,0.0),81.0,1.0)
        
    glFlush()
    #glutPostRedisplay()

def main():
    glutInit(sys.argv)
    glutInitDisplayMode(GLUT_SINGLE|GLUT_RGB)
    glutInitWindowPosition(0,0)
    glutInitWindowSize(1000,1000)
    glutCreateWindow(b"Plot Points")
    glutDisplayFunc(plotPoints)

    init()
    glutMainLoop()

main()
