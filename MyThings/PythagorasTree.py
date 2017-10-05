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


def init():
	glClearColor(1.0, 1.0, 1.0, 0.0)
	gluOrtho2D(0.0, 120.0, 0.0, 75.0)

def distance(x,y):
    return ((x[0]-y[0])**2 + (x[1]-y[1])**2)**.5

def intersect(m1,b1,m2,b2):
    x = -(b1-b2)/(m1-m2)
    return x, m1*x + b1

def slopeInt(x,y):
    m = (y[1]-x[1])/(y[0]-x[0])
    return m,(x[1] - m*x[0])
def point(pt,d,m):
    x = pt[0] + (d)/((1+m**2)**.5)
    y = pt[1] + (d*m)/((1+m**2)**.5)
    return (x,y)
def others(x,y):
    #need to multiply distance by something that is positive or negative
    cond1 = (x[0] >= y[0])
    cond2 = (x[1] >= y[1])
    mult = 1
    if not cond1 and not cond2:
        mult = -1
    elif cond1 and not cond2:
        mult = -1
    m,b = slopeInt(x,y)
    m2 = -1/m
    return point(x,mult*distance(x,y),m2),point(y,mult*distance(x,y),m2)

def frac(left,right,step):
    glColor3f(first[int(step)%7],second[int(step)%7],third[int(step)%7])
    if step > 15.0:
        return
    if left[1] == right[1]:
        mult = 1
        if left[0] > right[0]:
            mult = -1
        topL = (left[0],left[1]+(distance(left,right)*mult))
        topR = (right[0],right[1]+(distance(left,right)*mult))
    elif left[0] == right[0]:
        mult = 1
        if left[1] < right[1]:
            mult = -1
        topL = (left[0]+(distance(left,right)*mult),left[1])
        topR = (right[0]+(distance(left,right)*mult),right[1])
    else:
        topL,topR = others(left,right)
    #print left,right,topR,topL
    glBegin(GL_QUADS)
    glVertex2f(left[0],left[1])
    glVertex2f(right[0],right[1])
    glVertex2f(topR[0],topR[1])
    glVertex2f(topL[0],topL[1])
    glEnd()
    if topR[0] == left[0]:
        other = (topL[0],topR[1])
    elif topR[1] == left[1]:
        other = (topR[0],topL[1])
    else:
        m2,b1 = slopeInt(left,topR)
        m1 = -1/m2
        other = intersect(m1,(topR[1]-m1*topR[0]),m2,(topL[1]-m2*topL[0]))
    frac(topL,other,step+1.0)
    frac(other,topR,step+1.0)


def plotPoints():
    glClear(GL_COLOR_BUFFER_BIT)
    glClearColor(1.0, 1.0, 1.0, 0.0)
    glColor3f(0.5,0.5,0.5)
    
    
    frac((55.0,32.5),(65.0,32.5),1.0)
    frac((65.0,42.5),(55.0,42.5),1.0)
        
    glFlush()
    #glutPostRedisplay()

def main():
    glutInit(sys.argv)
    glutInitDisplayMode(GLUT_SINGLE|GLUT_RGB)
    glutInitWindowPosition(0,0)
    glutInitWindowSize(1600,1000)
    glutCreateWindow(b"Plot Points")
    glutDisplayFunc(plotPoints)

    init()
    glutMainLoop()

main()
