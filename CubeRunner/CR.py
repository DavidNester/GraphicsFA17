from OpenGL.GL import *
from OpenGL.GLU import *
from OpenGL.GLUT import *
import sys
from random import randint, gauss
import time
from PIL import Image

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

# TODO: Shadows
# TODO: Clouds of some kind
# TODO: Adjust lighting
def load_textures():
    im = Image.open("bg2.jpg")

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

class FloatingBlock(object):
    # class for floating blocks
    def __init__(self):
        # initialize with x value that is from normal distribution centered at 0 on x axis with SD of 55
        self.y = GROUND + 1
        self.x = gauss(0, 55)
        self.z = -100

    def points(self):
        return self.x, self.y, self.z

    def inc(self, z_st, x_st=0):
        # move by a given step
        self.z += z_st
        self.x += x_st

    def render(self):
        a, b, c = self.points()
        glPushMatrix()
        glTranslatef(a, b, c)
        draw_cube()
        glPopMatrix()

    def inside(self, pos):
        # checks if position is inside floating block
        # we only care about x and z for this game
        x, y, z = pos
        a = 1
        if self.x-a <= x <= self.x+a and self.z-a <= z <= self.z+a:
            return True
        return False


# game variables
floating_blocks = [FloatingBlock()]
floating_blocks_old = []
left_pressed = False
right_pressed = False
step = 1
score = -step
game_over = False
x_step = 0
end_rot = 0
start = True

# added for 3D
# perspective variables
fovy = 60.0
aspect = float(WIDTH)/float(HEIGHT)
zNear = .1
zFar = 100

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
    glEnable(GL_TEXTURE_2D)
    #glPushMatrix()
    glBegin(GL_QUADS)
    glTexCoord2f(0.0, 0.0);
    glVertex3f(-125, GROUND, -zFar+1)  # Bottom Left Of The Texture and Quad
    glTexCoord2f(1.0, 0.0);
    glVertex3f(125, GROUND, -zFar+1)  # Bottom Right Of The Texture and Quad
    glTexCoord2f(1.0, 1.0);
    glVertex3f(125, GROUND + 65, -zFar+1)  # Top Right Of The Texture and Quad
    glTexCoord2f(0.0, 1.0);
    glVertex3f(-125, GROUND + 65, -zFar+1)  # Top Left Of The Texture and Quad
    glEnd()
    #glPopMatrix()

    """
    glBegin(GL_QUADS)
    glVertex3f(-WIDTH, GROUND, -zFar)
    glVertex3f(WIDTH, GROUND, -zFar)
    glColor3f(0.4, 230 / 255, 1.0)
    glVertex3f(WIDTH, GROUND+40, -zFar/2)
    glVertex3f(-WIDTH, GROUND+40, -zFar/2)
    """
    glBegin(GL_QUADS)
    #glColor3f(.55, .75, .30)
    glTexCoord2f(0.0, 0.0);
    glVertex3f(-125, GROUND, zFar)
    glTexCoord2f(1.0, 0.0);
    glVertex3f(125, GROUND, zFar)
    #glColor3f(.20, .35, .15)
    glTexCoord2f(1.0, 1.0);
    glVertex3f(125, GROUND, -zFar)
    glTexCoord2f(0.0, 1.0);
    glVertex3f(-125, GROUND, -zFar)
    glEnd()
    glDisable(GL_TEXTURE_2D)

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
    global step, score, floating_blocks, game_over, x_step, left_pressed, right_pressed, end_rot, floating_blocks_old
    global light_x, light_y, light_z, lightPos, auto_light, light_theta, start
    # erase and get ready to redraw
    glClear(GL_COLOR_BUFFER_BIT | GL_DEPTH_BUFFER_BIT)

    glMatrixMode(GL_PROJECTION)
    glLoadIdentity()
    gluPerspective(fovy, aspect, zNear, zFar)

    #  Set the matrix for the object we are drawing
    glMatrixMode(GL_MODELVIEW)
    glLoadIdentity()


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

    if abs(x_step) < .1: # fixes issue where blocks were fluttering
        x_step = 0
    draw_player()
    move_and_set_light()
    glRotatef(-5 * x_step, 0, 0, 1) # rotate world if keys pressed
    for block in floating_blocks:
        block.render()
    draw_ground_and_sky()

    # move x step to 0 if keys not pressed
    if not left_pressed and not right_pressed and x_step != 0:
        x_step += .1 if x_step < 0 else -.1
    if not game_over:
        # add a block for every other redraw
        if not randint(0, 1):
            floating_blocks += [FloatingBlock()]
        # keep blocks until they are 40 units behind camera
        if floating_blocks[0].z > DESTROY_BLOCKS:
            floating_blocks.pop(0)
        score += step
        # determine direction that blocks need to move
        if left_pressed:
            x_step = min(.8, x_step+.1)
        if right_pressed:
            x_step = max(-.8, x_step-.1)
        for block in floating_blocks:
            # move blocks towards camera and left or right
            block.inc(step, x_st=x_step)
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
    global left_pressed, right_pressed
    if key == GLUT_KEY_LEFT and not game_over:
        left_pressed = True
    elif key == GLUT_KEY_RIGHT and not game_over:
        right_pressed = True


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
    global left_pressed, right_pressed
    if key == GLUT_KEY_LEFT:
        left_pressed = False
    elif key == GLUT_KEY_RIGHT:
        right_pressed = False


def init():
    global fovy, aspect, zNear, zFar

    glClearColor(0.5, 0.5, 0.5, 0.0)

    load_textures()

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
