"""
A bunch of Rotating Cubes

Think of it this way:
The camera in OpenGL cannot move and is defined to be located at (0,0,0)
facing the negative Z direction. That means that instead of moving and
rotating the camera, the world is moved and rotated around the camera
to construct the appropriate view.

Keys
x - rotate each cube around their x-axis (toggle on/off)
y - rotate each cube around their y-axis (toggle on/off)
z - rotate each cube around their z-axis (toggle on/off)
Z - move along Z axis positive direction
X - move along Z axis negative direction
key left - x translation negative
key right - x translation positive
key up - y translation positive
key down - y translation negative
i - rotate entire world around y axis
k - rotate entire world around z axis
l - rotate entire world around x axis
q - increase field of view
a - decrease field of view
R - resets some of the variables

After running
XXXXXX

"""

from OpenGL.GL import *
from OpenGL.GLUT import *
from OpenGL.GLU import *
import random
 
x_rot = False
y_rot = False
z_rot = False

#translation variables
x_translation = 0.0
y_translation = 0.0
z_translation = -6.0
translation_amt = 0.25

#rotation
X_AXIS = 0.0
Y_AXIS = 0.0
Z_AXIS = 0.0
 
DIRECTION = 1
ROTATION_ANGLE = 1.0
WIDTH = 750
HEIGHT = 750
DISTANCE_BETWEEN_CUBES = 6.0

#scene rotation
SCENE_X_AXIS = 0.0
SCENE_Y_AXIS = 0.0
SCENE_Z_AXIS = 0.0

#perspective variables
fovy = 45.0
aspect = float(WIDTH)/float(HEIGHT)
zNear = 0.1
zFar = 100


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
        
        
def keyboard(key, x, y):
        #  Allows us to quit by pressing 'Esc' or 'q'
        global x_rot, y_rot, z_rot, z_translation
        global fovy, aspect, zNear, zFar
        global SCENE_X_AXIS, SCENE_Y_AXIS, SCENE_Z_AXIS
        global X_AXIS, Y_AXIS, Z_AXIS
        global x_translation, y_translation, z_translation
        
        
        if key == b'\x1b':
                sys.exit()
        elif key == b"x":
                # toggle x rotation
                x_rot = not x_rot
        elif key == b"y":
                # toggle y rotation
                y_rot = not y_rot
        elif key == b"z":
                # toggle z rotation
                z_rot = not z_rot
        elif key == b"Z":
                # z translation
                z_translation += translation_amt
        elif key == b"X":
                # z translation
                z_translation -= translation_amt
        elif key == b"q":
                # fovy
                fovy += 5.0
        elif key == b"a":
                # fovy
                fovy -= 5.0
        elif key == b"i":
                SCENE_Y_AXIS += 5.0
        elif key == b"k":
                SCENE_Z_AXIS += 5.0
        elif key == b"l":
                SCENE_X_AXIS += 5.0
        elif key == b"R":
                SCENE_X_AXIS = 0
                SCENE_Y_AXIS = 0
                SCENE_Z_AXIS = 0
                X_AXIS = 0
                Y_AXIS = 0
                Z_AXIS = 0
                z_translation = 0
                x_translation = 0
                y_translation = 0
                x_rot = False
                y_rot = False
                z_rot = False
                fovy = 45.0
        elif key == b"q":
                sys.exit()

        print_parms()
 
def special_input(key, x, y):
        global x_translation, y_translation, z_translation, translation_amt
        
        if key == GLUT_KEY_UP:
                y_translation += translation_amt
        elif key == GLUT_KEY_DOWN:
                y_translation -= translation_amt
        elif key == GLUT_KEY_LEFT:
                x_translation -= translation_amt
        elif key == GLUT_KEY_RIGHT:
                x_translation += translation_amt
                
        print_parms()
                
def draw_cube():
        # Draw Cube (multiple quads)
        glBegin(GL_QUADS)

        # note that one of the x, y, or z values will be the
        # same for all the points in that plane
        
        glColor3f(0.0,1.0,1.0)
        # top
        glVertex3f( 1.0, 1.0,-1.0)
        glVertex3f(-1.0, 1.0,-1.0)
        glVertex3f(-1.0, 1.0, 1.0)
        glVertex3f( 1.0, 1.0, 1.0) 
 
        glColor3f(1.0,0.0,0.0)
        # bottom
        glVertex3f( 1.0,-1.0, 1.0)
        glVertex3f(-1.0,-1.0, 1.0)
        glVertex3f(-1.0,-1.0,-1.0)
        glVertex3f( 1.0,-1.0,-1.0) 
 
        glColor3f(0.0,1.0,0.0)
        # front
        glVertex3f( 1.0, 1.0, 1.0)
        glVertex3f(-1.0, 1.0, 1.0)
        glVertex3f(-1.0,-1.0, 1.0)
        glVertex3f( 1.0,-1.0, 1.0)
 
        glColor3f(1.0,1.0,0.0)
        #back
        glVertex3f( 1.0,-1.0,-1.0)
        glVertex3f(-1.0,-1.0,-1.0)
        glVertex3f(-1.0, 1.0,-1.0)
        glVertex3f( 1.0, 1.0,-1.0)
 
        glColor3f(0.0,0.0,1.0)
        # left side
        glVertex3f(-1.0, 1.0, 1.0) 
        glVertex3f(-1.0, 1.0,-1.0)
        glVertex3f(-1.0,-1.0,-1.0) 
        glVertex3f(-1.0,-1.0, 1.0) 
 
        glColor3f(1.0,0.0,1.0)
        #right side
        glVertex3f( 1.0, 1.0,-1.0) 
        glVertex3f( 1.0, 1.0, 1.0)
        glVertex3f( 1.0,-1.0, 1.0)
        glVertex3f( 1.0,-1.0,-1.0)

        glEnd()

        
def draw_scene():
        global X_AXIS,Y_AXIS,Z_AXIS
        global x_translation, y_translation, z_translation
        global DIRECTION, ROTATION_ANGLE, DISTANCE_BETWEEN_CUBES
        global NUMBER_CUBE_ROWS
        global fovy, aspect, zNear, zFar
        global SCENE_X_AXIS, SCENE_Y_AXIS, SCENE_Z_AXIS
 
        glClear(GL_COLOR_BUFFER_BIT | GL_DEPTH_BUFFER_BIT)

        glMatrixMode(GL_PROJECTION)
        glLoadIdentity()
        gluPerspective(fovy, aspect, zNear, zFar)
        
        #  Set the matrix for the object we are drawing
        glMatrixMode(GL_MODELVIEW)
        glLoadIdentity()

        # rotate the entire scene
        glRotatef(SCENE_X_AXIS, 1.0, 0.0, 0.0)
        glRotatef(SCENE_Y_AXIS, 0.0, 1.0, 0.0)
        glRotatef(SCENE_Z_AXIS, 0.0, 0.0, 1.0)

        # draw the cubes in the scene
        for i in range (-1,2):
                for j in range (-1,2):
                        for k in range (-1,2): 
                                glPushMatrix()
                                glTranslatef(x_translation + (i*DISTANCE_BETWEEN_CUBES),y_translation + (j*DISTANCE_BETWEEN_CUBES),z_translation -(k*DISTANCE_BETWEEN_CUBES))
                                glRotatef(X_AXIS, 1.0, 0.0, 0.0)
                                glRotatef(Y_AXIS, 0.0, 1.0, 0.0)
                                glRotatef(Z_AXIS, 0.0, 0.0, 1.0)
                                draw_cube()
                                glPopMatrix()
        
        
        if x_rot:
            X_AXIS = X_AXIS + ROTATION_ANGLE
        if y_rot:
            Y_AXIS = Y_AXIS + ROTATION_ANGLE
        if z_rot:
            Z_AXIS = Z_AXIS + ROTATION_ANGLE

        
        glutSwapBuffers()

 

def print_parms():
        global x_translation, y_translation, z_translation
        global fovy, aspect, zNear, zFar
        
        translations = "SCENE TRANSLATION (x, y, z): " + str(x_translation) + ", " + str(y_translation) + ", " + str(z_translation)
        perspectives = "PERSPECTIVE fovy,aspect,zNear,zFar: " + str(fovy) + ", " + str(aspect) + ", " + str(zNear)+ ", " + str(zFar)
        entire_scene = "SCENE ROTATION (x, y, z): "+str(SCENE_X_AXIS)+", "+str(SCENE_Y_AXIS)+", "+str(SCENE_Z_AXIS)
        print (perspectives)
        print (translations)
        print (entire_scene)
        print (" ")
 
def main():
        glutInit(sys.argv)
        glutInitDisplayMode(GLUT_RGBA | GLUT_DOUBLE | GLUT_DEPTH)
        glutInitWindowSize(WIDTH,HEIGHT)
        glutInitWindowPosition(50,50)
        
        glutCreateWindow(b'OpenGL Python Cubes')
        
        glutDisplayFunc(draw_scene)
        glutIdleFunc(draw_scene)
        glutKeyboardFunc(keyboard)
        glutSpecialFunc(special_input)
        
        init()
        glutMainLoop()
 
if __name__ == "__main__":
        main() 
