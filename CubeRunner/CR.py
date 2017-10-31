from OpenGL.GL import *
from OpenGL.GLU import *
from OpenGL.GLUT import *
import sys
from random import randint

# static global variables
WIDTH = 1400
HEIGHT = 800
DEPTH = 1400
MAX_HEIGHT = 5
BETWEEN_BLOCKS = 4
SQUARE_LENGTH = 40


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
floating_blocks = [FloatingBlock()]
offset = 0

x_pos = 300
y_pos = 00
z_pos = -200
left_pressed = False
right_pressed = False
step = 2
score = -step
game_over = False
start = False

# added for 3D
#perspective variables
fovy = 45.0
aspect = float(WIDTH)/float(HEIGHT)
zNear = 0.1
zFar = 100

x_translation = 0.0
y_translation = 0.0
z_translation = -6.0
translation_amt = 0.25


def draw_cube():
    # Draw Cube (multiple quads)
    glBegin(GL_QUADS)

    # note that one of the x, y, or z values will be the
    # same for all the points in that plane

    glColor3f(0.0, 1.0, 1.0)
    # top
    glVertex3f(1.0, 1.0, -1.0)
    glVertex3f(-1.0, 1.0, -1.0)
    glVertex3f(-1.0, 1.0, 1.0)
    glVertex3f(1.0, 1.0, 1.0)

    glColor3f(1.0, 0.0, 0.0)
    # bottom
    glVertex3f(1.0, -1.0, 1.0)
    glVertex3f(-1.0, -1.0, 1.0)
    glVertex3f(-1.0, -1.0, -1.0)
    glVertex3f(1.0, -1.0, -1.0)

    glColor3f(0.0, 1.0, 0.0)
    # front
    glVertex3f(1.0, 1.0, 1.0)
    glVertex3f(-1.0, 1.0, 1.0)
    glVertex3f(-1.0, -1.0, 1.0)
    glVertex3f(1.0, -1.0, 1.0)

    glColor3f(1.0, 1.0, 0.0)
    # back
    glVertex3f(1.0, -1.0, -1.0)
    glVertex3f(-1.0, -1.0, -1.0)
    glVertex3f(-1.0, 1.0, -1.0)
    glVertex3f(1.0, 1.0, -1.0)

    glColor3f(0.0, 0.0, 1.0)
    # left side
    glVertex3f(-1.0, 1.0, 1.0)
    glVertex3f(-1.0, 1.0, -1.0)
    glVertex3f(-1.0, -1.0, -1.0)
    glVertex3f(-1.0, -1.0, 1.0)

    glColor3f(1.0, 0.0, 1.0)
    # right side
    glVertex3f(1.0, 1.0, -1.0)
    glVertex3f(1.0, 1.0, 1.0)
    glVertex3f(1.0, -1.0, 1.0)
    glVertex3f(1.0, -1.0, -1.0)

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
    glClear(GL_COLOR_BUFFER_BIT | GL_DEPTH_BUFFER_BIT)

    glMatrixMode(GL_PROJECTION)
    glLoadIdentity()
    gluPerspective(fovy, aspect, zNear, zFar)

    #  Set the matrix for the object we are drawing
    glMatrixMode(GL_MODELVIEW)
    glLoadIdentity()

    # draw the cubes in the scene
    for i in range(-1, 2):
        for j in range(-1, 2):
            for k in range(-1, 2):
                glPushMatrix()
                glTranslatef(x_translation + (i * DISTANCE_BETWEEN_CUBES), y_translation + (j * DISTANCE_BETWEEN_CUBES),
                             z_translation - (k * DISTANCE_BETWEEN_CUBES))
                glRotatef(X_AXIS, 1.0, 0.0, 0.0)
                glRotatef(Y_AXIS, 0.0, 1.0, 0.0)
                glRotatef(Z_AXIS, 0.0, 0.0, 1.0)
                draw_cube()
                glPopMatrix()

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

def special_input(key, x, y):
    global x_translation, y_translation, z_translation, translation_amt

    if key == GLUT_KEY_LEFT:
        x_translation -= translation_amt
    elif key == GLUT_KEY_RIGHT:
        x_translation += translation_amt

    print_parms()


def idle():
    # redraw the window if the game has started and is not over
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
    global fovy, aspect, zNear, zFar

    glClearColor(0.0, 0.0, 0.0, 0.0)

    glClearDepth(1.0)
    glDepthFunc(GL_LESS)
    glEnable(GL_DEPTH_TEST)

    glMatrixMode(GL_PROJECTION)
    glLoadIdentity()

    """
    fovy - Specifies the field of view angle, in degrees, in the y direction. 
    aspect - Specifies the aspect ratio that determines the field of view in the x direction. The aspect ratio is the ratio of x (width) to y (height). 
    zNear - Specifies the distance from the viewer to the near clipping plane (always positive). 
    zFar - Specifies the distance from the viewer to the far clipping plane (always positive). 
    """
    gluPerspective(fovy, aspect, zNear, zFar)

    #  Set the matrix for the object we are drawing
    glMatrixMode(GL_MODELVIEW)
    glLoadIdentity()

    def main():
        glutInit(sys.argv)
        glutInitDisplayMode(GLUT_RGBA | GLUT_DOUBLE | GLUT_DEPTH)
        glutInitWindowSize(WIDTH, HEIGHT)
        glutInitWindowPosition(50, 50)

        glutCreateWindow(b'CubeRunner')

        glutDisplayFunc(plotfunc)
        glutIdleFunc(idle)
        glutKeyboardFunc(keyboard)
        glutSpecialFunc(special_input)

        init()
        glutMainLoop()


if __name__ == "__main__":
    main()
