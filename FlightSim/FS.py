from OpenGL.GL import *
from OpenGL.GLU import *
from OpenGL.GLUT import *
import sys
from random import randint, gauss
import time
import math

# static global variables
WIDTH = 1400
HEIGHT = 800
DEPTH = -200
MAX_HEIGHT = 5
BETWEEN_BLOCKS = 4
SQUARE_LENGTH = 40
GROUND = -4
PLAYER_Z = -7
TIME = 0
DESTROY_BLOCKS = 40



class City(object):
    # class for floating blocks
    def __init__(self):
        # initialize with x value that is from normal distribution centered at 0 on x axis with SD of 55
        self.buildings = [[1,1,1,3,2,4,2,1],
                          [1,2,4,7,5,2,1,2],
                          [3,1,1,4,8,3,4,1],
                          [6,8,4,5,10,8,5,4],
                          [7,5,12,9,15,8,9,6,3],
                          [4,6,7,9,8,3,5,2],
                          [2,5,3,7,4,5,2,1],
                          [1,3,4,5,4,2,1,1]]
        self.x = -18
        self.z = -200

    def points(self):
        return self.x, GROUND + 1, self.z

    def inc(self, z_st, x_st):
        # move by a given step
        self.z += z_st
        self.x += x_st
        self.z = max(-200,self.z)
        self.z = min(200, self.z)
        self.x = max(-200, self.z)
        self.x = min(200, self.z)

    def render(self):
        a, b, c = self.points()
        i = 0
        for row in self.buildings:
            j = 0
            for building in row:
                j += 1
                glPushMatrix()
                glTranslatef(a+(10*j), b, c+(10*i))
                draw_building(building)
                glPopMatrix()
            i += 1

    def inside(self, pos):
        # checks if position is inside floating block
        # we only care about x and z for this game
        x, y, z = pos
        a = 1
        if self.x-a <= x <= self.x+a and self.z-a <= z <= self.z+a:
            return True
        return False

"""
Current idea: Make a 3D vector that is updated with mouse clicks. Move everything the opposite of it. 
"""

class Vector:
    def __init__(self):
        self.x = 0
        self.y = 0
        self.z = -1

    def down(self):
        pass

    def up(self):
        pass

    def left(self):
        pass

    def right(self):
        pass

# game variables
city = City()
floating_blocks_old = []
left_pressed = False
right_pressed = False
up_pressed = False
down_pressed = False
step = 1
score = -step
game_over = False
x_step = 0
y_step = 0
end_rot = 0
start = True
player_y = -3

# added for 3D
# perspective variables
fovy = 60.0
aspect = float(WIDTH)/float(HEIGHT)
zNear = .1
zFar = 200

# LIGHTING Light values and coordinates
light_x = 40.0
light_y = 0.0
light_z = 5.0
ambientLight = (0.5, 0.5, 0.5, 1.0)
diffuseLight = (0.75, 0.75, 0.75, 0.7)
specular = (1.0, 1.0, 1.0, 1.0)
specref = (1.0, 1.0, 1.0, 1.0)
lightPos = [light_x, light_y, 100.0, 1.0]
auto_light = False
light_theta = 0.0
light_circle_radius = 150.0


def draw_building(height):
    # Draw Cube (multiple quads)
    glBegin(GL_QUADS)

    # note that one of the x, y, or z values will be the
    # same for all the points in that plane
    # colors changed between vertices to give gradient effect

    # top
    glColor3f(0.05, 0.45, 0.70)
    glVertex3f(1.0, height, -1.0)
    glColor3f(0.1, 0.58, 0.68)
    glVertex3f(-1.0, height, -1.0)
    glColor3f(0.05, 0.45, 0.70)
    glVertex3f(-1.0, height, 1.0)
    glColor3f(0.1, 0.58, 0.68)
    glVertex3f(1.0, height, 1.0)

    glColor3f(1.0, 0.0, 0.0)
    # bottom
    glVertex3f(1.0, -1.0, 1.0)
    glVertex3f(-1.0, -1.0, 1.0)
    glVertex3f(-1.0, -1.0, -1.0)
    glVertex3f(1.0, -1.0, -1.0)

    # front
    glColor3f(0.63, 0.84, 0.89)
    glVertex3f(1.0, height, 1.0)
    glColor3f(0.5, 0.70, 0.89)
    glVertex3f(-1.0, height, 1.0)
    glColor3f(0.63, 0.84, 0.89)
    glVertex3f(-1.0, -1.0, 1.0)
    glColor3f(0.5, 0.70, 0.89)
    glVertex3f(1.0, -1.0, 1.0)

    # back
    glColor3f(0.63, 0.84, 0.89)
    glVertex3f(1.0, -1.0, -1.0)
    glColor3f(0.5, 0.70, 0.89)
    glVertex3f(-1.0, -1.0, -1.0)
    glColor3f(0.63, 0.84, 0.89)
    glVertex3f(-1.0, height, -1.0)
    glColor3f(0.5, 0.70, 0.89)
    glVertex3f(1.0, height, -1.0)

    # left side
    glColor3f(0.30, 0.60, 0.90)
    glVertex3f(-1.0, height, 1.0)
    glColor3f(0.15, 0.32, 0.45)
    glVertex3f(-1.0, height, -1.0)
    glColor3f(0.30, 0.60, 0.90)
    glVertex3f(-1.0, -1.0, -1.0)
    glColor3f(0.15, 0.32, 0.45)
    glVertex3f(-1.0, -1.0, 1.0)

    # right side
    glColor3f(.02, 0.22, 0.32)
    glVertex3f(1.0, height, -1.0)
    glColor3f(.04, 0.44, 0.64)
    glVertex3f(1.0, height, 1.0)
    glColor3f(.02, 0.22, 0.32)
    glVertex3f(1.0, -1.0, 1.0)
    glColor3f(.04, 0.44, 0.64)
    glVertex3f(1.0, -1.0, -1.0)

    glEnd()


def draw_cube():
    # Draw Cube (multiple quads)
    glBegin(GL_QUADS)

    # note that one of the x, y, or z values will be the
    # same for all the points in that plane
    # colors changed between vertices to give gradient effect

    # top
    glColor3f(0.05, 0.45, 0.70)
    glVertex3f(1.0, 1.0, -1.0)
    glColor3f(0.1, 0.58, 0.68)
    glVertex3f(-1.0, 1.0, -1.0)
    glColor3f(0.05, 0.45, 0.70)
    glVertex3f(-1.0, 1.0, 1.0)
    glColor3f(0.1, 0.58, 0.68)
    glVertex3f(1.0, 1.0, 1.0)

    glColor3f(1.0, 0.0, 0.0)
    # bottom
    glVertex3f(1.0, -1.0, 1.0)
    glVertex3f(-1.0, -1.0, 1.0)
    glVertex3f(-1.0, -1.0, -1.0)
    glVertex3f(1.0, -1.0, -1.0)

    # front
    glColor3f(0.63, 0.84, 0.89)
    glVertex3f(1.0, 1.0, 1.0)
    glColor3f(0.5, 0.70, 0.89)
    glVertex3f(-1.0, 1.0, 1.0)
    glColor3f(0.63, 0.84, 0.89)
    glVertex3f(-1.0, -1.0, 1.0)
    glColor3f(0.5, 0.70, 0.89)
    glVertex3f(1.0, -1.0, 1.0)

    # back
    glColor3f(0.63, 0.84, 0.89)
    glVertex3f(1.0, -1.0, -1.0)
    glColor3f(0.5, 0.70, 0.89)
    glVertex3f(-1.0, -1.0, -1.0)
    glColor3f(0.63, 0.84, 0.89)
    glVertex3f(-1.0, 1.0, -1.0)
    glColor3f(0.5, 0.70, 0.89)
    glVertex3f(1.0, 1.0, -1.0)

    # left side
    glColor3f(0.30, 0.60, 0.90)
    glVertex3f(-1.0, 1.0, 1.0)
    glColor3f(0.15, 0.32, 0.45)
    glVertex3f(-1.0, 1.0, -1.0)
    glColor3f(0.30, 0.60, 0.90)
    glVertex3f(-1.0, -1.0, -1.0)
    glColor3f(0.15, 0.32, 0.45)
    glVertex3f(-1.0, -1.0, 1.0)

    # right side
    glColor3f(.02, 0.22, 0.32)
    glVertex3f(1.0, 1.0, -1.0)
    glColor3f(.04, 0.44, 0.64)
    glVertex3f(1.0, 1.0, 1.0)
    glColor3f(.02, 0.22, 0.32)
    glVertex3f(1.0, -1.0, 1.0)
    glColor3f(.04, 0.44, 0.64)
    glVertex3f(1.0, -1.0, -1.0)

    glEnd()


def draw_ground_and_sky():

    glBegin(GL_QUADS)
    glColor3f(0, 191 / 255, 1.0)
    glVertex3f(-WIDTH, GROUND, -zFar)
    glVertex3f(WIDTH, GROUND, -zFar)
    glColor3f(0.4, 230 / 255, 1.0)
    glVertex3f(WIDTH, GROUND+40, -zFar/2)
    glVertex3f(-WIDTH, GROUND+40, -zFar/2)

    glColor3f(.55, .75, .30)
    glVertex3f(-WIDTH, GROUND, zFar)
    glVertex3f(WIDTH, GROUND, zFar)
    glColor3f(.20, .35, .15)
    glVertex3f(WIDTH, GROUND, -zFar)
    glVertex3f(-WIDTH, GROUND, -zFar)
    glEnd()


def draw_player():
    # draw player
    glPushMatrix()
    glTranslatef(0, -3, -7)
    glBegin(GL_TRIANGLES)

    # colors changed in between vertices to give gradient effect
    glColor3f(1, 1, 1)
    # left
    glColor3f(1, 0, 0)
    glVertex3f(-0.35, 0, 1)
    glColor3f(192/255, 192/255, 192/255)
    glVertex3f(0, .3, .5)
    glColor3f(1, 0, 0)
    glVertex3f(0, 0, -1)

    # right
    glColor3f(0, 1, 0)
    glVertex3f(0.35, 0, 1)
    glColor3f(192/255, 192/255, 192/255)
    glVertex3f(0, .3, .5)
    glColor3f(0, 1, 0)
    glVertex3f(0, 0, -1)

    # back
    glColor3f(0, 0, 1)
    glVertex3f(-0.35, 0, 1)
    glColor3f(192/255, 192/255, 192/255)
    glVertex3f(0, .3, .5)
    glColor3f(0, 0, 1)
    glVertex3f(0.35, 0, 1)
    glEnd()

    glPopMatrix()


def check_collision():
    if score < 95:
        return False
    # check if any of the corners are inside any of the blocks
    # points are the coordinates of the player plus the translation amounts
    points = [(0, GROUND+1, -8), (-.35, GROUND+1, -6), (.35, GROUND+1, -6)]
    for point in points:
        # could probably check fewer blocks but used a large selection to ensure collisions are always caught
        for block in floating_blocks[0:52]:
            if block.inside(point):
                return True
    return False


def disp_text(x, y, text, font=GLUT_STROKE_ROMAN, r=0, g=0, b=0):
    glPushMatrix()
    glTranslatef(x, y, -20)
    glScalef(1.0 / 152.38, 1.0 / 152.38, 1.0 / 152.38)
    # draw text
    glColor3f(r, g, b)
    for ch in text:
        glutStrokeCharacter(font, ctypes.c_int(ord(ch)))
    glPopMatrix()


def automatic_light():
    global light_x, light_y, light_z, light_theta
    global light_circle_radius

    # 150 just works well here, probably should be a parameter
    r = light_circle_radius
    light_x = r * cos(light_theta)
    light_y = r * sin(light_theta)
    light_theta += 0.003


def move_and_set_light():
    global lightPos, light_x, light_y
    # LIGHT
    if auto_light:
        automatic_light()
    # move light along elliptical path from right horizon to left horizon
    light_x -= .09
    if light_x < -40:
        light_x = 40
    light_y = 20 * ((1 - (light_x ** 2) / 1600) ** .5)
    lightPos = [light_x, light_y, light_z, 1.0]
    glLightfv(GL_LIGHT1, GL_POSITION, lightPos)


def end_game():
    global end_rot
    disp_text(-2.5, 6, 'Score: ' + str(score))
    disp_text(-2.8, 8, 'GAME OVER!')
    disp_text(-4, 4, 'ENTER to Restart')
    draw_ground_and_sky()
    # rotate around the center of the player
    glTranslatef(0, 0, PLAYER_Z)
    glRotatef(end_rot, 0.0, 1.0, 0.0)
    glTranslatef(0, 0, -PLAYER_Z)
    end_rot += .5


def plotfunc():
    global step, score, city, game_over, x_step, left_pressed, right_pressed, end_rot
    global light_x, light_y, light_z, lightPos, auto_light, light_theta, start, y_step, GROUND
    # erase and get ready to redraw
    glClear(GL_COLOR_BUFFER_BIT | GL_DEPTH_BUFFER_BIT)

    glMatrixMode(GL_PROJECTION)
    glLoadIdentity()
    gluPerspective(fovy, aspect, zNear, zFar)

    #  Set the matrix for the object we are drawing
    glMatrixMode(GL_MODELVIEW)
    glLoadIdentity()

    """
    if start:
        disp_text(-2.8, 8, 'CUBE RUNNER')
    if score > 150: # removes CUBE RUNNER banner from screen
        start = False
    if check_collision():
        left_pressed = right_pressed = False
        game_over = True  # tells idle to stop re-displaying image
    if game_over:
        end_game()
    else:
        # display score
        disp_text(-20, 10.6, "Score: " + str(score))
    """
    if abs(x_step) < .01: # fixes issue where blocks were fluttering
        x_step = 0
    if abs(y_step) < .01:  # fixes issue where blocks were fluttering
        y_step = 0
    draw_player()
    move_and_set_light()
    draw_ground_and_sky()
    glTranslatef(-2 if x_step > 0 else 2, 0, PLAYER_Z + 2)
    glRotatef(-5 * x_step, 0, 1, 0)  # rotate world if keys pressed
    glTranslatef(2 if x_step > 0 else -2, 0, -PLAYER_Z - 2)
    #glRotatef(-5 * y_step, 1, 0, 0)  # rotate world if keys pressed
    city.render()

    # move x step to 0 if keys not pressed
    #if not left_pressed and not right_pressed and x_step != 0:
    #    x_step += .1 if x_step < 0 else -.1
    if not down_pressed and not up_pressed and y_step != 0:
        y_step += .05 if y_step < 0 else -.05
    if not game_over:
        if left_pressed:
            x_step = x_step + .25
        if right_pressed:
            x_step = x_step - .05
        if up_pressed:
            y_step = y_step + .25
        if down_pressed:
            y_step = x_step - .05

        x_st = .3*math.sin(-math.radians(-5 * x_step))
        z_st = .3*math.cos(-math.radians(-5 * x_step))
        city.inc(z_st, x_st)
    print(x_step, y_step)
    GROUND += y_step
    GROUND = min(-3,GROUND)
    glutSwapBuffers()


def restart():
    global floating_blocks, right_pressed, left_pressed, x_step, score, step, start, game_over, end_rot
    # reset all game variables to initial state
    floating_blocks = [FloatingBlock()]

    left_pressed = False
    right_pressed = False
    step = 1
    score = -step
    game_over = False
    start = False
    x_step = 0
    end_rot = 0


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
    global left_pressed, right_pressed, up_pressed, down_pressed
    if key == GLUT_KEY_LEFT and not game_over:
        left_pressed = True
    if key == GLUT_KEY_RIGHT and not game_over:
        right_pressed = True
    if key == GLUT_KEY_DOWN and not game_over:
        down_pressed = True
    if key == GLUT_KEY_UP and not game_over:
        up_pressed = True


def idle():
    global TIME
    # checks time since last redraw and waits for the difference if greater than set amount
    # used to fix issue where it ran too fast on Windows
    diff = time.clock() - TIME
    TIME = time.clock()
    if diff < .005:
        time.sleep(.005-diff)
    glutPostRedisplay()


def up(key, x, y):
    global left_pressed, right_pressed, up_pressed, down_pressed
    if key == GLUT_KEY_LEFT:
        left_pressed = False
    if key == GLUT_KEY_RIGHT:
        right_pressed = False
    if key == GLUT_KEY_UP:
        up_pressed = False
    if key == GLUT_KEY_DOWN:
        down_pressed = False


def init():
    global fovy, aspect, zNear, zFar

    glClearColor(0.5, 0.5, 0.5, 0.0)

    glClearDepth(1.0)
    glDepthFunc(GL_LESS)
    glEnable(GL_DEPTH_TEST)

    # LIGHTING
    glEnable(GL_LIGHTING)
    glLightfv(GL_LIGHT1, GL_AMBIENT, ambientLight)
    glLightfv(GL_LIGHT1, GL_DIFFUSE, diffuseLight)
    # glLightfv(GL_LIGHT1, GL_SPECULAR, specular)
    glEnable(GL_LIGHT1)
    glEnable(GL_COLOR_MATERIAL)
    glColorMaterial(GL_FRONT, GL_AMBIENT_AND_DIFFUSE)
    glMaterialfv(GL_FRONT, GL_SPECULAR, specref)
    glMateriali(GL_FRONT, GL_SHININESS, 128)

    glMatrixMode(GL_PROJECTION)
    glLoadIdentity()

    gluPerspective(fovy, aspect, zNear, zFar)

    #  Set the matrix for the object we are drawing
    glMatrixMode(GL_MODELVIEW)
    glLoadIdentity()


def main():
    glutInit(sys.argv)
    glutInitDisplayMode(GLUT_RGBA | GLUT_DOUBLE | GLUT_DEPTH)
    glutInitWindowSize(WIDTH, HEIGHT)
    glutInitWindowPosition(50, 50)

    glutCreateWindow(b'Flight Sim')

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
