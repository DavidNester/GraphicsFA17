from OpenGL.GL import *
from OpenGL.GLU import *
from OpenGL.GLUT import *
import sys
from random import randint
import time

# static global variables
WIDTH = 1400
HEIGHT = 800
MAX_HEIGHT = 5
BETWEEN_BLOCKS = 4
SQUARE_LENGTH = 40
TIME = 0

class FloatingBlock(object):
    # class for floating blocks
    def __init__(self):
        # initialize with random height
        self.y = randint((MAX_HEIGHT+1)*SQUARE_LENGTH, HEIGHT-(MAX_HEIGHT+1)*SQUARE_LENGTH)
        self.x = WIDTH + SQUARE_LENGTH

    def points(self):
        y = self.y
        x = self.x
        a = SQUARE_LENGTH/2
        return [(x-a, y-a), (x+a, y-a), (x+a, y+a),
                (x-a, y+a)]

    def inc(self, st):
        # move to by a given step
        self.x -= st

    def inside(self, pos):
        # checks if position is inside floating block
        x, y = pos
        a = SQUARE_LENGTH/2
        if self.x-a <= x <= self.x+a and self.y-a <= y <= self.y+a:
            return True
        return False


# game variables
top_squares = []
bottom_squares = []
floating_blocks = [FloatingBlock()]
offset = 0

x_pos = 300
y_pos = 500
key_pressed = False
vel = -2
step = 2
score = -step
shield = False
next_block = BETWEEN_BLOCKS
game_over = False
start = False


def plus_or_minus():
    # returns 1 or -1
    return [-1, 1][randint(0, 1)]


def next_top_or_bottom(previous):
    # return the next value to be added to the top or bottom within 1 of previous from 1 to MAX_HEIGHT inclusive
    if previous == MAX_HEIGHT:
        return [MAX_HEIGHT - 1]
    elif previous == 1:
        return [2]
    else:
        return [previous + plus_or_minus()]


def populate_top_and_bottom():
    global top_squares, bottom_squares
    # random numbers to top and bottom
    top_squares = [1, 1, 1, 1, 2]
    bottom_squares = [1, 1, 1, 1, 2]
    for i in range(int(WIDTH / SQUARE_LENGTH) + 1):
        top_squares += next_top_or_bottom(top_squares[-1])
        bottom_squares += next_top_or_bottom(bottom_squares[-1])


def draw_top_and_bottom():
    for num in range(len(bottom_squares)):
        glColor3f(255, 0, 0)
        base_x = SQUARE_LENGTH * num - offset

        # top
        glBegin(GL_QUADS)
        top_y = SQUARE_LENGTH * top_squares[num]
        glVertex2f(base_x, HEIGHT - top_y)
        glVertex2f(base_x + SQUARE_LENGTH, HEIGHT - top_y)
        glVertex2f(base_x + SQUARE_LENGTH, HEIGHT)
        glVertex2f(base_x, HEIGHT)
        glEnd()

        # bottom
        bottom_y = SQUARE_LENGTH * bottom_squares[num]
        glBegin(GL_QUADS)
        glVertex2f(base_x, 0)
        glVertex2f(base_x + SQUARE_LENGTH, 0)
        glVertex2f(base_x + SQUARE_LENGTH, bottom_y)
        glVertex2f(base_x, bottom_y)
        glEnd()


def draw_floating():
    # draw floating blocks
    for block in floating_blocks:
        glBegin(GL_POLYGON)
        for point in block.points():
            glVertex2f(point[0], point[1])
        glEnd()


def draw_player(a=SQUARE_LENGTH/2):
    # draw player square
    glColor3f(0, 255, 0)
    glBegin(GL_QUADS)
    glVertex2f(x_pos-a, y_pos-a)
    glVertex2f(x_pos+a, y_pos-a)
    glVertex2f(x_pos+a, y_pos+a)
    glVertex2f(x_pos-a, y_pos+a)
    glEnd()


def clean_up():
    global top_squares, bottom_squares, floating_blocks, next_block, offset
    # get rid of blocks that are off screen and generate next ones
    # deal with floating  blocks
    next_block -= 1
    if next_block < 0:
        next_block = BETWEEN_BLOCKS
        floating_blocks += [FloatingBlock()]
        if floating_blocks[0].x < 0:
            floating_blocks.pop(0)

    # deal with bottom and top
    offset = offset % SQUARE_LENGTH
    top_squares.pop(0)
    bottom_squares.pop(0)
    top_squares += next_top_or_bottom(top_squares[-1])
    bottom_squares += next_top_or_bottom(bottom_squares[-1])


def check_collision():
    # check if any of the corners are inside any of the blocks
    a = SQUARE_LENGTH/2
    corners = [(x_pos-a, y_pos-a), (x_pos+a, y_pos-a), (x_pos+a, y_pos+a), (x_pos-a, y_pos+a)]
    for corner in corners:
        for i in range(min(3, len(floating_blocks))):
            if floating_blocks[i].inside(corner):
                return True
        for j in range(7, 10):
            if (SQUARE_LENGTH*j - offset) <= int(corner[0]) <= (SQUARE_LENGTH*(j+1) - offset):
                if corner[1] > HEIGHT - SQUARE_LENGTH*top_squares[j] or corner[1] < SQUARE_LENGTH*bottom_squares[j]:
                    return True
    return False


def end_of_game():
    # expanding player to fill screen animation
    for i in range(0, WIDTH, 10):
        draw_player(i)
        glutSwapBuffers()
    disp_text(WIDTH / 2 - 1.5 * SQUARE_LENGTH - 5, HEIGHT / 2, 'Score: ' + str(score), white=False)
    disp_text(WIDTH / 2 - 1.5 * SQUARE_LENGTH, HEIGHT / 2 + 3 * SQUARE_LENGTH, 'GAME OVER!', white=False)
    disp_text(WIDTH / 2 - 2.25 * SQUARE_LENGTH, HEIGHT / 2 - 3 * SQUARE_LENGTH, 'ENTER to Restart', white=False)
    glutSwapBuffers()


def disp_text(x, y, text, font=GLUT_BITMAP_9_BY_15, r=0, g=0, b=0, white=True):
    # draw white square behind score
    if white:
        glColor3f(1, 1, 1)
        glBegin(GL_QUADS)
        glVertex2f(0, HEIGHT - 1.5 * SQUARE_LENGTH)
        glVertex2f(4 * SQUARE_LENGTH, HEIGHT - 1.5 * SQUARE_LENGTH)
        glVertex2f(4 * SQUARE_LENGTH, HEIGHT)
        glVertex2f(0, HEIGHT)
        glEnd()
    # draw text
    glColor3f(r, g, b)
    glRasterPos2f(x, y)
    for ch in text:
        glutBitmapCharacter(font, ctypes.c_int(ord(ch)))


def plotfunc():
    global x_pos, y_pos, vel, offset, top_squares, bottom_squares, shield, step, score, floating_blocks, next_block,\
        game_over
    # erase and get ready to redraw
    glClear(GL_COLOR_BUFFER_BIT)

    # initial instructions
    if not start:
        disp_text(WIDTH / 2, HEIGHT / 2, 'Click To Start', r=1, g=1, b=1)
        disp_text(WIDTH / 2, HEIGHT / 2-SQUARE_LENGTH, 'Press Space To Fly', r=1, g=1, b=1)

    # Give cube "momentum"
    if key_pressed and vel < 6:
        vel += 1
    elif vel > -5:
        vel -= 1

    # update y_pos
    y_pos += vel

    # draw blocks
    draw_top_and_bottom()
    draw_floating()
    draw_player()

    offset += step
    score += step
    if offset >= SQUARE_LENGTH:
        # add blocks and get rid of those off the screen
        clean_up()
    for block in floating_blocks:
        # move floating blocks to the left
        block.inc(step)
    if score % WIDTH == 0:
        # increase speed every time you travel the width of the window
        step += 1
    # display score
    disp_text(.5*SQUARE_LENGTH, HEIGHT - .75 * SQUARE_LENGTH, "Score: " + str(score))
    glutSwapBuffers()
    if check_collision():
        game_over = True  # tells idle to stop redisplaying image
        end_of_game()  # does end of game animation and displays score


def restart():
    global top_squares, bottom_squares, floating_blocks, offset, x_pos, y_pos, key_pressed, vel, score, step, shield, \
        next_block, game_over, start
    # reset all game variables to initial state
    top_squares = []
    bottom_squares = []
    floating_blocks = [FloatingBlock()]
    offset = 0
    x_pos = 300
    y_pos = 500
    key_pressed = False
    vel = -2
    step = 2
    score = -step
    shield = False
    next_block = BETWEEN_BLOCKS
    game_over = False
    start = False
    populate_top_and_bottom()


def keyboard(key, x, y):
    global key_pressed, game_over
    #  Allows us to quit by pressing 'Esc' or 'q'
    if key == b'\x1b' or key == b"q":
        sys.exit()
    if key == b" ":
        key_pressed = True
    # hit enter to restart if game is over
    if key == b"\r" and game_over:
        game_over = False
        restart()
        glutPostRedisplay()


def idle():
    global TIME
    # redraw the window if the game has started and is not over
    diff = time.clock() - TIME
    TIME = time.clock()
    if diff < .0025:
        time.sleep(.0025 - diff)
    if start and not game_over:
        glutPostRedisplay()


def mouse(button, state, x, y):
    global start
    # start on click
    if button == GLUT_LEFT_BUTTON:
        start = 1


def up(key, x, y):
    global key_pressed
    # stop rising player when space bar is released
    if key == b" ":
        key_pressed = False


def init():
    glClearColor(0.0, 0.0, 0.0, 1.0)

    # Dimensions of the screen
    gluOrtho2D(0, WIDTH, 0, HEIGHT)
    populate_top_and_bottom()


def main():
        glutInit(sys.argv)
        # We are in Double Buffer mode now
        glutInitDisplayMode(GLUT_RGB | GLUT_DOUBLE)
        glutInitWindowPosition(100, 100)
        glutInitWindowSize(WIDTH, HEIGHT)
        glutCreateWindow(b"Don't Touch Anything")

        # Event callback routines
        glutDisplayFunc(plotfunc)
        glutMouseFunc(mouse)
        glutKeyboardFunc(keyboard)
        glutIdleFunc(idle)
        glutKeyboardUpFunc(up)

        init()
        glutMainLoop()

main()    
