# PyNewton.py
# Newton's Method in the complex plane

from OpenGL.GL import *
from OpenGL.GLU import *
from OpenGL.GLUT import *
from numpy import *
import sys


# Global variables for screen dimensions, axis range
# and loop step size
width = 400
height = 400
vcenter = 1.45
hcenter = 1.1
axrng = 3.0
hstep = 2*axrng/width
vstep = 2*axrng/height
step = .1

def init():
	# Black background
	glClearColor(0.0, 0.0, 0.0, 0.0)  
	gluOrtho2D(hcenter-axrng,hcenter+axrng,vcenter-axrng,vcenter+axrng)

def drawnewton():
    global axrng,step,hstep,vstep
    glClear(GL_COLOR_BUFFER_BIT)
    glBegin(GL_POINTS)
    axrng -= step
    hstep = 2 * axrng / width
    vstep = 2 * axrng / height
    gluOrtho2D(hcenter - axrng, hcenter + axrng, vcenter - axrng, vcenter + axrng)
    y = vcenter+axrng
    while y > vcenter-axrng:
        y -= vstep
        x = hcenter-axrng
        while x < hcenter+axrng:
            x += hstep

            n = 0

            # define the current complex number
            # using the x,y pixel values
            z = complex(x,y)

            endit = 0

            # 1000 iterations at maximum
            while n < 1000 and endit == 0:
                n+=1
                old = z
                z = z - (z**3 - 1)/(3*z**2)

                if abs(z - old) < 0.000001 or z.real == float("inf") or z.real == float("-inf") or z.real == float("nan"):
                    endit = 1
        
            # Pick color parameters based on quadrant
            if z.imag >= 0 and z.real < 1:
                c1 = 6
                c2 = 12
                c3 = 18

            elif z.imag < 0 and z.real < 1:
                c1 = 18
                c2 = 6
                c3 = 12

            if z.real > 0:
                c1 = 12
                c2 = 18
                c3 = 6
        
            glColor3ub(n*c1,n*c2,n*c3)	
            glVertex2f(x,y)
    glEnd()
    glFlush()
    glutPostRedisplay()

def keyboard(key, x, y):
    if key == chr(27) or key == "q":
        sys.exit()

def main():
	glutInitDisplayMode(GLUT_RGB | GLUT_SINGLE)
	glutInitWindowPosition(50, 50)
	glutInitWindowSize(width, height)
	glutInit(sys.argv)
	glutCreateWindow(b"Newton's Madness")
	glutDisplayFunc(drawnewton)
	glutKeyboardFunc(keyboard)
	init()
	glutMainLoop()
	
main()
