# First Python OpenGL program
# ogl1.py
from OpenGL.GLUT import *
from OpenGL.GL import *
from OpenGL.GLU import *

def draw():
    glClear(GL_COLOR_BUFFER_BIT)
    tess = gluNewTess(glutWireSphere(0.5,10,10))
    #glutSolidTeapot(0.5)
    #glutSolidSphere(0.5, 10, 10)
    #glutSolidCube(1.0)
    #glutWireCone(0.25, 1.0, 10, 10)
    #glutWireTorus(0.25, 0.75, 10, 10)
    #glutWireDodecahedron()  ???
    #glutWireOctahedron()
    #glutWireTetrahedron()
    #glutWireIcosahedron()
    glFlush()

glutInit(sys.argv)
glutInitDisplayMode(GLUT_SINGLE | GLUT_RGB)
glutInitWindowSize(500, 500)
glutInitWindowPosition(100, 100)
glutCreateWindow("Drawing a Wire Teapot")
glutDisplayFunc(draw)
glutMainLoop()

# End of program
