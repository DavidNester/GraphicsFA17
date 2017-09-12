#  First Python OpenGL Program
#  ogl1.py
#**************FIRST ASSIGNMENT************************
#experiment with this
#change things
#remove things
#add things

from OpenGL.GLUT import *
from OpenGL.GLU import *
from OpenGL.GL import *
import sys

def draw():
	glClear(GL_COLOR_BUFFER_BIT)
	glutSolidTeapot(0.5)
	glFlush()
	
glutInit(sys.argv)
glutInitDisplayMode(GLUT_SINGLE|GLUT_RGB)
glutInitWindowPosition(100,100)
glutInitWindowSize(250, 250)
glutCreateWindow(b"My First OGL Program")
glutDisplayFunc(draw)
glutMainLoop()
