# PyBounce.py

from OpenGL.GL import *
from OpenGL.GLU import *
from OpenGL.GLUT import *
import sys
import random
import time
from copy import copy,deepcopy

#  globals for animation, ball position
#  and direction of motion
global anim, width, height, grid_rows, delay, square_size, grayscale, COLOR

# initialize global constants
HEIGHT = 500
WIDTH = 500
ROWS = 5
DELAY =.5
SQUARE_SIZE = int(HEIGHT/ROWS)
COLUMNS = int(WIDTH/SQUARE_SIZE)
#maze
"""
trans = [[(0,1),    (0,2),  (1,2),  (0,4),  (1,4)],
         [(0,0),    (1,0),  (1,3),  (0,3),  (2,4)],
         [(2,1),    (1,1),(-1,-1),  (2,2),  (2,3)],
        [(2,0),    (4,1),  (3,1),  (4,3),  (3,3)],
         [(3,0),    (4,0),  (3,2),  (4,2),  (3,4)]]
"""
#spiral
trans = [[(0,1),    (0,2),  (0,3),  (1,3),  (1,4)],
         [(0,0),    (1,2),  (2,2),  (2,3),  (2,4)],
         [(1,0),    (1,1),(-1,-1),  (3,3),  (3,4)],
         [(2,0),    (2,1),  (3,1),  (3,2),  (4,4)],
         [(3,0),    (4,0),  (4,1),  (4,2),  (4,3)]]

COLOR = [list(range(5)),list(range(5)),list(range(5)),list(range(5)),list(range(5))]
grayscale = False
anim = True
COUNTER = 0
C = (random.random(),random.random(),random.random())

def random_color():
    global COUNTER,C
    if COUNTER > 2:  # increase value to increase length of snakes
        C = (random.random(),random.random(),random.random())
        COUNTER = 0
    COUNTER += 1
    return C

def white():
    return (1,1,1)


for i in range(ROWS):
    for j in range(COLUMNS):
        COLOR[i][j] = white()

def init():
    glClearColor(0.0, 0.0, 0.0, 1.0)
    glColor3ub(255, 0, 0)

    gluOrtho2D(0, WIDTH, 0, HEIGHT)


def idle():
    if anim:
        glutPostRedisplay()


def update():
    global COLOR
    temp = deepcopy(COLOR)
    for i in range(ROWS):
        for j in range(COLUMNS):
            COLOR[i][j] = temp[trans[i][j][0]][trans[i][j][1]]
            if -1 in trans[i][j]:
                COLOR[i][j] = random_color()
                
def draw_square(x1, x2, y1, y2,i,j):
    glColor3f(COLOR[i][j][0], COLOR[i][j][1], COLOR[i][j][2])
    glBegin(GL_POLYGON);
    glVertex3f(x1, y1,0.0);
    glVertex3f(x2, y1,0.0);
    glVertex3f(x2, y2,0.0);
    glVertex3f(x1, y2,0.0);
    glEnd();
        
def plotfunc():
    global WIDTH, ROWS, COLUMNS, DELAY, SQUARE_SIZE, COLOR
        
    glClear(GL_COLOR_BUFFER_BIT)
        
    for i in range(0,COLUMNS):
        for j in range(0,ROWS):
            x1_vertex = i * SQUARE_SIZE
            x2_vertex = (i+1) * SQUARE_SIZE
            y1_vertex = j * SQUARE_SIZE
            y2_vertex = (j+1) * SQUARE_SIZE
            if grayscale:
                draw_square(x1_vertex, x2_vertex, y1_vertex, y2_vertex, i,j)
            else:
                draw_square(x1_vertex, x2_vertex, y1_vertex, y2_vertex, i,j)
    time.sleep(DELAY)
    # makes for a nice smooth animation
    glutSwapBuffers()
    update()
        
def keyboard(key, x, y):
        #  Allows us to quit by pressing 'Esc' or 'q'
        #  We can animate by "a" and stop by "s"
        global anim, grayscale
        
        if key == b'\x1b':
                sys.exit()
        if key == b"a":
                anim = True
        if key == b"s":
                anim = False
        if key == b"g":
                grayscale = True
                glutPostRedisplay()
        if key == b"h":
                grayscale = False
                glutPostRedisplay()
        if key == b"q":
                sys.exit()

        
def main():
        glutInit(sys.argv)
        # We are in Double Buffer mode now
        glutInitDisplayMode(GLUT_RGB|GLUT_DOUBLE)
        glutInitWindowPosition(50,50)
        glutInitWindowSize(WIDTH,HEIGHT)
        glutCreateWindow(b"For Alex")

        # Event callback routines
        glutDisplayFunc(plotfunc)
        glutKeyboardFunc(keyboard)
        glutIdleFunc(idle)
        
        init()
        glutMainLoop()

main()    
