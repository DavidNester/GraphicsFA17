# PyFunc.py
# Plotting functions

from OpenGL.GL import *
from OpenGL.GLU import *
from OpenGL.GLUT import *
from numpy import *
import sys
import math
from Square import Square

Squares = []
sq = Square((-1.0,0.0),(1.0,0.0))
Squares += [sq]
def init():
	glClearColor(1.0, 1.0, 1.0, 1.0)
	gluOrtho2D(-10.0, 10.0, -10.0, 10.0)

def keyboard(key,x,y):
    global sq
    if key == b'w':
        sq.up()
        glutPostRedisplay()
    elif key == b's':
        sq.down()
        glutPostRedisplay()
    elif key == b'd':
        sq.right()
        glutPostRedisplay()
    elif key == b'a':
        sq.left()
        glutPostRedisplay()

def draw(square):
    glBegin(GL_QUADS)
    for point in square.points():
        glVertex2f(point[0],point[1])
    glEnd()


def plotFunc():
        glColor3f(0.0,0.0,0.0)
        glClear(GL_COLOR_BUFFER_BIT)
        for square in Squares:
            draw(square)
        glFlush()
# End of plotfunc block

def main():
    glutInit(sys.argv)
    glutInitDisplayMode(GLUT_SINGLE|GLUT_RGB)
    glutInitWindowPosition(50,50)
    glutInitWindowSize(900,900)
    glutCreateWindow(b"hit 'w' 's' 'a' 'd' to alter ellipse")
    glutDisplayFunc(plotFunc)
    glutKeyboardFunc(keyboard)

    init()
    glutMainLoop()

main()
