from OpenGL.GL import *
from OpenGL.GLU import *
from OpenGL.GLUT import *
import sys
from random import randint

# static global variables
WIDTH = 1400
HEIGHT = 800
DEPTH = -200
MAX_HEIGHT = 5
BETWEEN_BLOCKS = 4
SQUARE_LENGTH = 40
GROUND = -4

#TODO: Ground
#TODO: Scoreboard
#TODO: Collisions
#TODO: Lighting
#TODO: Shading
#TODO: Block Creation function


class FloatingBlock(object):
    # class for floating blocks
    def __init__(self):
        # initialize with random height
        self.y = GROUND + 1
        self.x = randint(-100, 100)
        self.z = -100

    def points(self):
        return self.x, self.y, self.z

    def inc(self, z_st, x_st=0):
        # move to by a given step
        self.z += z_st
        self.x += x_st

    def inside(self, pos):
        # checks if position is inside floating block
        x, y = pos
        a = SQUARE_LENGTH/2
        if self.x-a <= x <= self.x+a and self.y-a <= y <= self.y+a:
            return True
        return False


# game variables
floating_blocks = [FloatingBlock()]

left_pressed = False
right_pressed = False
step = 1
score = -step
game_over = False
start = False
x_step = 0

# added for 3D
# perspective variables
fovy = 60.0
aspect = float(WIDTH)/float(HEIGHT)
zNear = 0.1
zFar = 100


def draw_cube():
    # Draw Cube (multiple quads)
    glBegin(GL_QUADS)

    # note that one of the x, y, or z values will be the
    # same for all the points in that plane

    glColor3f(1.0, 0.0, 0.0)
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


def draw_ground():
    glPushMatrix()
    glBegin(GL_QUADS)

    glColor3f(1.0, 0.0, 0.0)
    glVertex3f(-WIDTH, GROUND, 0)
    glVertex3f(WIDTH, GROUND, zFar)
    glVertex3f(WIDTH, GROUND, zFar)
    glVertex3f(-WIDTH, GROUND, 0)

    glEnd()
    glPopMatrix()


def draw_floating():
    # draw floating blocks
    for block in floating_blocks:
        a, b, c = block.points()
        glPushMatrix()
        glTranslatef(a, b, c)
        draw_cube()
        glPopMatrix()


def draw_player(a=SQUARE_LENGTH/2):
    # draw player square
    glPushMatrix()
    glTranslatef(0, GROUND+1, -7)
    glBegin(GL_TRIANGLES)

    #left
    glColor3f(0,1,0)
    glVertex3f(-0.35,0,1)
    glVertex3f(0, .003, 0)
    glVertex3f(0, 0, -1)

    #right
    glColor3f(1, 0, 0)
    glVertex3f(0.35, 0, 1)
    glVertex3f(0, .003, 0)
    glVertex3f(0, 0, -1)

    #back
    glColor3f(0, 0, 1)
    glVertex3f(-0.35, 0, 1)
    glVertex3f(0, .003, 0)
    glVertex3f(0.35, 0, 1)
    glEnd()
    glPopMatrix()

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
    global step, score, floating_blocks, game_over, x_step
    # erase and get ready to redraw
    glClear(GL_COLOR_BUFFER_BIT | GL_DEPTH_BUFFER_BIT)

    glMatrixMode(GL_PROJECTION)
    glLoadIdentity()
    gluPerspective(fovy, aspect, zNear, zFar)

    #  Set the matrix for the object we are drawing
    glMatrixMode(GL_MODELVIEW)
    glLoadIdentity()

    # initial instructions
    #if not start:
    #    disp_text(WIDTH / 2, HEIGHT / 2, 'Click To Start', r=1, g=1, b=1)
    #    disp_text(WIDTH / 2, HEIGHT / 2-SQUARE_LENGTH, 'Press Space To Fly', r=1, g=1, b=1)


    # draw blocks
    draw_player()
    glRotatef(-5 * x_step, 0, 0, 1)
    draw_floating()
    draw_ground()

    if not randint(0,1):
        floating_blocks += [FloatingBlock()]
    if floating_blocks[0].z > 0:
        floating_blocks.pop(0)

    score += step
    # determine direction that blocks need to move
    if left_pressed:
        x_step = min(1,x_step+.1)
    if right_pressed:
        x_step = max(-1,x_step-.1)
    if not left_pressed and not right_pressed and x_step != 0:
        x_step += .1 if x_step < 0 else -.1
    for block in floating_blocks:
        # move blocks towards camera and left or right
        block.inc(step, x_st=x_step)
    # display score
    #disp_text(.5*SQUARE_LENGTH, HEIGHT - .75 * SQUARE_LENGTH, "Score: " + str(score))
    glutSwapBuffers()
    #if check_collision():
    #   game_over = True  # tells idle to stop redisplaying image
    #   end_of_game()  # does end of game animation and displays score


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
    global left_pressed, right_pressed, game_over
    # Allows us to quit by pressing 'Esc' or 'q'
    if key == b'\x1b' or key == b"q":
        sys.exit()
    # hit enter to restart if game is over
    if key == b"\r" and game_over:
        game_over = False
        restart()
        glutPostRedisplay()


def special_input(key, x, y):
    global left_pressed, right_pressed
    if key == GLUT_KEY_LEFT:
        left_pressed = True
    elif key == GLUT_KEY_RIGHT:
        right_pressed = True


def idle():
    # redraw the window if the game has started and is not over
    #if start and not game_over:
    glutPostRedisplay()


def up(key, x, y):
    global left_pressed, right_pressed
    # stop rising player when space bar is released
    if key == GLUT_KEY_LEFT:
        left_pressed = False
    elif key == GLUT_KEY_RIGHT:
        right_pressed = False


def init():
    global fovy, aspect, zNear, zFar

    glClearColor(0.5, 0.5, 0.5, 0.0)

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
    glutKeyboardUpFunc(up)
    glutSpecialFunc(special_input)
    glutSpecialUpFunc(up)

    init()
    glutMainLoop()


if __name__ == "__main__":
    main()
