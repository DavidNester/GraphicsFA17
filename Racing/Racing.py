# PySkel.py
from OpenGL.GL import *
from OpenGL.GLU import *
from OpenGL.GLUT import *
from numpy import *
import sys
from PIL import Image
from random import randint,random
from math import pi
import time

# Initial values
WIDTH = 1024
HEIGHT = 768
GROUND = -4
SEGMENT = 6
TIME = 0

# added for 3D
# perspective variables
fovy = 60.0
aspect = float(WIDTH)/float(HEIGHT)
zNear = .1
zFar = 400

grass = [(16/255,200/255,16/255),(0,154/255,0)]
road = [(107/255,107/255,107/255),(105/255,105/255,105/255)]
rumble = [(1,1,1),(0,0,0)]

temp_ground = GROUND


"""
TODO: Use other functions that dont necessarily return to normal
"""

class Bump:
    def __init__(self):
        self.z = -250
        self.height = randint(1, 6) * [-1, 1][randint(0, 1)]
        self.width_coef = random() * .05

    def inc(self,st):
        self.z += st

    def difference(self,z):
        diff = abs(self.z-z)
        if diff > pi/(2*self.width_coef):
            return 0
        return self.height*cos(self.width_coef*diff)

    def camera(self):
        global temp_ground
        diff = abs(7 + self.z)
        if diff < pi/(2*self.width_coef):
            temp_ground = GROUND - self.height*cos(self.width_coef*diff)
        else:
            temp_ground = GROUND

"""
class Hill:
    def __init__(self):
        self.z = -300
        self.height = [-.5, .5][randint(0, 1)]

    def inc(self,st):
        self.z += st

    def difference(self, z):
        if z > self.z:
            return 0
        if abs(z - self.z) > 20:
            return 20 * self.height
        return abs(z - self.z) * self.height

    def camera(self):
        global temp_ground
        diff = 7 - self.z
        if self.z < -7:
            return
        elif self.z > 3:
            temp_ground -= self.height * 10
            return
        temp_ground -= self.height * diff
"""

class Curve:
    def __init__(self):
        self.z = -500
        self.height = randint(1, 5) * [-1, 1][randint(0, 1)]

    def inc(self,st):
        self.z += st

    def difference(self,z):
        diff = abs(self.z-z)
        if diff > pi/(2*.01):
            return 0
        return 6*cos(.01*diff)*self.height

offset = 1
road_width = 7
left_pressed = False
right_pressed = False
accelerator_pressed = False
forward = 0
bumps = [Bump()]
curves = [Curve()]
#hills = [Hill()]
x_step = 0
road_center = 0
curve_coefficient = .5
turn_step = 0

x_off = 0


def load_textures():
    im = Image.open("bg.jpg")

    ix, iy = im.size

    im = im.tobytes("raw", "RGBX", 0, -1)

    # Create Texture
    glBindTexture(GL_TEXTURE_2D, glGenTextures(1))  # 2d texture (x and y size)

    glPixelStorei(GL_UNPACK_ALIGNMENT, 1)
    glTexImage2D(GL_TEXTURE_2D, 0, 3, ix, iy, 0, GL_RGBA, GL_UNSIGNED_BYTE, im)
    glTexParameterf(GL_TEXTURE_2D, GL_TEXTURE_WRAP_S, GL_CLAMP)
    glTexParameterf(GL_TEXTURE_2D, GL_TEXTURE_WRAP_T, GL_CLAMP)
    glTexParameterf(GL_TEXTURE_2D, GL_TEXTURE_WRAP_S, GL_REPEAT)
    glTexParameterf(GL_TEXTURE_2D, GL_TEXTURE_WRAP_T, GL_REPEAT)
    glTexParameterf(GL_TEXTURE_2D, GL_TEXTURE_MAG_FILTER, GL_NEAREST)
    glTexParameterf(GL_TEXTURE_2D, GL_TEXTURE_MIN_FILTER, GL_NEAREST)
    glTexEnvf(GL_TEXTURE_ENV, GL_TEXTURE_ENV_MODE, GL_DECAL)


def difference(z):
    return (z) * curve_coefficient


def draw_quad(color, x1, z1, x2, z2, up1=0, up2=0, side1=0, side2=0):
    glBegin(GL_QUADS)
    glColor3f(color[0], color[1], color[2])
    glVertex3f(x1+side1, temp_ground + up1, z1)
    glVertex3f(x1+side2, temp_ground + up2, z2)
    glVertex3f(x2+side2, temp_ground + up2, z2)
    glVertex3f(x2+side1, temp_ground + up1, z1)
    glEnd()


def draw_player():
    # draw player
    glPushMatrix()
    glTranslatef(0, GROUND+1, -7)
    glBegin(GL_TRIANGLES)

    # colors changed in between vertices to give gradient effect
    glColor3f(1, 1, 1)
    # left
    glColor3f(1, 0, 0)
    glVertex3f(-0.35, 0, 1)
    glColor3f(forward**2,forward**2,forward**2)
    glVertex3f(0, .3, .5)
    glColor3f(1, 0, 0)
    glVertex3f(0, 0, -1 - forward)

    # right
    glColor3f(0, 1, 0)
    glVertex3f(0.35, 0, 1)
    glColor3f(forward**2, forward**2, forward**2)
    glVertex3f(0, .3, .5)
    glColor3f(0, 1, 0)
    glVertex3f(0, 0, -1 - forward)

    # back
    glColor3f(0, 0, 1)
    glVertex3f(-0.35, 0, 1)
    glColor3f(forward**2, forward**2, forward**2)
    glVertex3f(0, .3, .5)
    glColor3f(0, 0, 1)
    glVertex3f(0.35, 0, 1)
    glEnd()

    glPopMatrix()


def draw_ground():
    # background
    glEnable(GL_TEXTURE_2D)
    glPushMatrix()
    glBegin(GL_QUADS)
    glTexCoord2f(0.0, 0.0); glVertex3f(-200, GROUND - 8, -zFar/2)  # Bottom Left Of The Texture and Quad
    glTexCoord2f(1.0, 0.0); glVertex3f(200, GROUND - 8, -zFar/2)  # Bottom Right Of The Texture and Quad
    glTexCoord2f(1.0, 1.0); glVertex3f(200, GROUND + 124, -zFar/2)  # Top Right Of The Texture and Quad
    glTexCoord2f(0.0, 1.0); glVertex3f(-200, GROUND + 124, -zFar/2)  # Top Left Of The Texture and Quad
    glEnd()
    glPopMatrix()
    glDisable(GL_TEXTURE_2D)

    # road
    for i in range(50):
        color_index = i%2
        up1 = 0
        up2 = 0
        for bump in bumps:
            up1 += bump.difference(-(SEGMENT * i - offset))
            up2 += bump.difference(-(SEGMENT * (i + 1) - offset))
        """
        for hill in hills:
            up1 += hill.difference(-(SEGMENT * i - offset))
            up2 += hill.difference(-(SEGMENT * (i + 1) - offset))
        """
        side1 = 0
        side2 = 0
        for curve in curves:
            side1 += curve.difference(-(SEGMENT * i - offset))
            side2 += curve.difference(-(SEGMENT * (i + 1) - offset))
        side1 += difference(-(SEGMENT * i - offset)) + x_off
        side2 += difference(-(SEGMENT * (i + 1) - offset)) + x_off

        # right grass
        draw_quad(grass[color_index], WIDTH, -(SEGMENT * i - offset), road_center+road_width+1, -(SEGMENT * (i + 1) - offset), up1, up2, side1, side2)
        # left grass
        draw_quad(grass[color_index], road_center-road_width-1, -(SEGMENT * i - offset), -WIDTH, -(SEGMENT * (i + 1) - offset), up1, up2, side1, side2)
        # left rumble
        draw_quad(rumble[color_index], road_center-road_width, -(SEGMENT * i - offset), road_center-road_width-1, -(SEGMENT * (i + 1) - offset), up1, up2, side1, side2)
        # right rumble
        draw_quad(rumble[color_index], road_center+road_width + 1, -(SEGMENT * i - offset), road_center + road_width, -(SEGMENT * (i + 1) - offset), up1, up2, side1, side2)
        # road
        draw_quad(road[color_index], road_center+road_width, -(SEGMENT * i - offset), road_center - road_width, -(SEGMENT * (i + 1) - offset), up1, up2, side1, side2)


def off_road():
    if randint(0,1):
        return True
    return False


def update():
    global bumps, curves, hills, curve_coefficient, x_off, turn_step
    x_off -= forward * curve_coefficient
    for bump in bumps:
        bump.inc(forward)
    for curve in curves:
        curve.inc(forward)
    if bumps[0].z > 140:
        bumps.pop(0)
        bumps += [Bump()]
    if curves[0].z > 150:
        curves.pop(0)
    if not randint(0,30):
        curves += [Curve()]
    """
    for hill in hills:
        hill.inc(forward)
    if not randint(0,100):
        hills += [Hill()]
    """
    # idea to think about for turning: have this adjustment depending on left pressed and right pressed
    # may need to have a variable to offset the the starting point
    if left_pressed:
        turn_step = max(turn_step-.001,-.01)
    elif right_pressed:
        turn_step = min(turn_step+.001,.01)
    else:
        turn_step += -.001 if turn_step > 0 else .001
    curve_coefficient += turn_step * forward


def plotfunc():
    global offset, forward, bumps, player_x_offset, x_step, road_center, curves, temp_ground
    glClear(GL_COLOR_BUFFER_BIT)
    glClear(GL_COLOR_BUFFER_BIT | GL_DEPTH_BUFFER_BIT)

    glMatrixMode(GL_PROJECTION)
    glLoadIdentity()
    gluPerspective(fovy, aspect, zNear, zFar)

    #  Set the matrix for the object we are drawing
    glMatrixMode(GL_MODELVIEW)
    glLoadIdentity()

    for bump in bumps:
        bump.camera()
    """
    for hill in hills:
        hill.camera()
    """
    draw_ground()

    offset = (offset + forward)%(SEGMENT*2)
    if accelerator_pressed:
        forward = min(forward + .1, 1.5)
    else:
        forward = max(forward - .01, 0)
    update()
    road_center += x_step
    draw_player()
    temp_ground = GROUND
    glutSwapBuffers()


def keyboard(key, x, y):
    global game_over, accelerator_pressed
    # Allows us to quit by pressing 'Esc' or 'q'
    if key == b'\x1b' or key == b"q":
        sys.exit()
    if key == b' ':
        accelerator_pressed = True
    # hit enter to restart if game is over
    #if key == b"\r" and game_over:
    #    game_over = False
    #    restart()
    #    glutPostRedisplay()


def special_input(key, x, y):
    global left_pressed, right_pressed
    if key == GLUT_KEY_LEFT:
        left_pressed = True
    if key == GLUT_KEY_RIGHT:
        right_pressed = True


def idle():
    global TIME
    # checks time since last redraw and waits for the difference if greater than set amount
    # used to fix issue where it ran too fast on Windows
    diff = time.clock() - TIME
    TIME = time.clock()
    print(diff)
    if diff < .009:
        time.sleep(.005-diff)
    glutPostRedisplay()


def up(key, x, y):
    global left_pressed, right_pressed, accelerator_pressed
    if key == GLUT_KEY_LEFT:
        left_pressed = False
    if key == GLUT_KEY_RIGHT:
        right_pressed = False
    if key == b' ':
        accelerator_pressed = False

def init():
    global fovy, aspect, zNear, zFar
    load_textures()
    glClearColor(0.0, 0.0, 0.0, 0.0)

    glClearDepth(1.0)
    glDepthFunc(GL_LESS)
    glEnable(GL_DEPTH_TEST)

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

    glutCreateWindow(b'Racing')

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
