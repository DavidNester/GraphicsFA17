#  PyPoints.py
#  Setting a coordinate system with central origin

from OpenGL.GL import *
from OpenGL.GLU import *
from OpenGL.GLUT import *
import sys
import time
import random
x = -4.0
one = True
counter = 0

first = [148,75,0,0,255,255,255]
second = [0,0,0,255,255,127,0]
third = [211,130,255,0,0,0,0]
first = [x/255.0 for x in first]
second = [x/255.0 for x in second]
third = [x/255.0 for x in third]

def color(x):
    return int((x + 3))%7



def init():
	glClearColor(1.0, 1.0, 1.0, 0.0)
	gluOrtho2D(-4.0, 4.0, 0.0, 16.0)


def plotPoints():
    global x,one,counter
    glClear(GL_COLOR_BUFFER_BIT)
    glColor3f(random.random(),random.random(),random.random())
    glClearColor(1.0, 1.0, 1.0, 0.0)
    counter += 1
    step = .1
    glBegin(GL_TRIANGLES)
    while x<=4.0:
        glColor3f(first[color(10*x+counter)],second[color(10*x+counter)],third[color(10*x+counter)])
        glVertex2f(0.0,16.0)
        glVertex2f(x,x**2)
        x += 0.1
        glVertex2f(x,x**2)
        x += 0.1
        x -= 0.1
        glColor3f(first[color(10*x+3*counter)],second[color(10*x+3*counter)],third[color(10*x+3*counter)])
        if x<0:
            glVertex2f(-4.0,0.0)
        else:
            glVertex2f(4.0,0.0)
        glVertex2f(x,x**2)
        x = x+0.1
        glVertex2f(x,x**2)
        x = x+0.1
        x -= 0.1
    if one:
        x= -3.9
        one = False
    else:
        x = -4.0
        one = True
    glEnd()
        
    glFlush()
    time.sleep(.1)
    glutPostRedisplay()

def main():
    glutInit(sys.argv)
    glutInitDisplayMode(GLUT_SINGLE|GLUT_RGB)
    glutInitWindowPosition(0,0)
    glutInitWindowSize(1800,1800)
    glutCreateWindow(b"Plot Points")
    glutDisplayFunc(plotPoints)

    init()
    glutMainLoop()

main()
