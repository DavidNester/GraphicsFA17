# Below is my modification to PyFunc2 that draws grid lines on the axes.

# PyFunc.py
# Plotting functions

from OpenGL.GL import *
from OpenGL.GLU import *
from OpenGL.GLUT import *
from numpy import *
import sys

windowSize = 400

def init():
    glClearColor(1.0, 1.0, 1.0, 1.0)
    gluOrtho2D(-10.0, 10.0, -10.0, 10.0)

def plotFunc():
    delta = 1
    
    glClear(GL_COLOR_BUFFER_BIT)
    glColor3f(0.0, 0.0, 0.0)

    #glPointSize(3.0)
    #glLineWidth(2.0)
    glBegin(GL_LINES)
    glVertex2f(-10,0)
    glVertex2f(10,0)
    glVertex2f(0,10)
    glVertex2f(0,-10)
    glEnd()
    partitionAxis('x', 1)
    partitionAxis('y', 1)
    
    glPointSize(3.0)
        
    glColor3f(1.0,0.0,0.0)
    glBegin(GL_POINTS)

    for x in arange(-10.0,10.0,0.5):
        # y = x**2 - 2
        # y = 2*x**3 - 9*x**2 - 24*x -12
        y = sin(x)
        # y = sin(x/3)
        glVertex2f(x, y)
    glEnd()
    glFlush()

def partitionAxes():
    pass
    
def partitionAxis(axis, delta, labelEvery=2, width=.25):
    textXStart = windowSize-windowSize/2-5
    textX = textXStart
    textY = windowSize-windowSize/2-20
    glBegin(GL_LINES)
    if axis == 'x':
        x = 0
        while x <= windowSize:
            x += delta
            glVertex2f(x, width)
            glVertex2f(x, -width)
        x = 0
        while x >= -windowSize:
            x -= delta
            glVertex2f(x, width)
            glVertex2f(x, -width)
    else:
        y = 0
        while y <= windowSize:
            y += delta
            glVertex2f(width, y)
            glVertex2f(-width, y)
        y = 0
        while y >= -windowSize:
            y -= delta
            glVertex2f(width, y)
            glVertex2f(-width, y)
    glEnd()

def main():
    glutInit(sys.argv)
    glutInitDisplayMode(GLUT_SINGLE|GLUT_RGB)
    glutInitWindowPosition(50,50)
    glutInitWindowSize(windowSize,windowSize)
    glutCreateWindow(b"Function Plotter")
    glutDisplayFunc(plotFunc)
    
    init()
    glutMainLoop()

main()
