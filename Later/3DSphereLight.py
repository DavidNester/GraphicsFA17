"""
A bunch of Spheres

Think of it this way:
The camera in OpenGL cannot move and is defined to be located at (0,0,0)
facing the negative Z direction. That means that instead of moving and
rotating the camera, the world is moved and rotated around the camera
to construct the appropriate view.

Keys
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
P - rotates the light source in a giant circle

After running, type to back up from the image
XXXXXXXXXXXXXX

if you back up far enough, you can see the light source
"""

from OpenGL.GL import *
from OpenGL.GLUT import *
from OpenGL.GLU import *
import random
from math import cos
from math import sin

#translation variables
x_translation = 0.0
y_translation = 0.0
z_translation = -30.0
translation_amt = 1.0

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
zFar = 500

# LIGHTING Light values and coordinates
light_x = light_y = 0.0
light_z = 100.0
ambientLight =  (0.35, 0.35, 0.35, 1.0)
diffuseLight = ( 0.75, 0.75, 0.75, 0.7)
specular = (1.0, 1.0, 1.0, 1.0)
specref = (1.0, 1.0, 1.0, 1.0)
lightPos = [light_x, light_y, 100.0, 1.0]
auto_light = False
light_theta = 0.0
light_circle_radius = 150.0

def init(): 

        global fovy, aspect, zNear, zFar
        
        glClearColor(0.0, 0.0, 0.0, 0.0)
        
        glClearDepth(1.0)
        glDepthFunc(GL_LESS)
        glEnable(GL_DEPTH_TEST)

        # LIGHTING
        glEnable(GL_LIGHTING)
        glLightfv(GL_LIGHT1, GL_AMBIENT, ambientLight)
        glLightfv(GL_LIGHT1, GL_DIFFUSE, diffuseLight)
        glLightfv(GL_LIGHT1, GL_SPECULAR, specular)
        glEnable(GL_LIGHT1)
        glEnable(GL_COLOR_MATERIAL)
        glColorMaterial(GL_FRONT, GL_AMBIENT_AND_DIFFUSE)
        glMaterialfv(GL_FRONT, GL_SPECULAR, specref)
        glMateriali(GL_FRONT, GL_SHININESS, 128)

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
        global x_translation, y_translation, z_translation
        global light_x, light_y, light_theta
        global auto_light
        
        
        if key == b'\x1b':
                sys.exit()
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
        elif key == b"g":
                light_x -= 5.0
        elif key == b"h":
                light_x += 5.0
        elif key == b"b":
                light_y -= 5.0
        elif key == b"t":
                light_y += 5.0
        elif key == b"P":
                auto_light = not auto_light
        elif key == b"R":
                SCENE_X_AXIS = 0
                SCENE_Y_AXIS = 0
                SCENE_Z_AXIS = 0
                z_translation = 0
                x_translation = 0
                y_translation = 0
                x_rot = False
                y_rot = False
                z_rot = False
                fovy = 45.0
                light_x = 0.0
                light_y = 0.0
                auto_light = False
                light_theta = 0.0
        elif key == b"q":
                sys.exit()
        else:
                return

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
                

        
def draw_scene():
        global X_AXIS,Y_AXIS,Z_AXIS
        global x_translation, y_translation, z_translation
        global DIRECTION, ROTATION_ANGLE, DISTANCE_BETWEEN_CUBES
        global NUMBER_CUBE_ROWS
        global fovy, aspect, zNear, zFar
        global SCENE_X_AXIS, SCENE_Y_AXIS, SCENE_Z_AXIS
        # LIGHT
        global light_x, light_y, light_z, lightPos, auto_light, light_theta
 
        glClear(GL_COLOR_BUFFER_BIT | GL_DEPTH_BUFFER_BIT)

        glMatrixMode(GL_PROJECTION)
        glLoadIdentity()
        gluPerspective(fovy, aspect, zNear, zFar)
        
        #  Set the matrix for the object we are drawing
        glMatrixMode(GL_MODELVIEW)
        glLoadIdentity()

        # LIGHT
        if auto_light:
                automatic_light()
                
        lightPos = [light_x, light_y, light_z, 1.0]
        glLightfv(GL_LIGHT1, GL_POSITION, lightPos)
        
        # rotate the entire scene
        glRotatef(SCENE_X_AXIS, 1.0, 0.0, 0.0)
        glRotatef(SCENE_Y_AXIS, 0.0, 1.0, 0.0)
        glRotatef(SCENE_Z_AXIS, 0.0, 0.0, 1.0)

        # draw the light source
        # you really have to zoom out a long way to see it,
        # but it is cool when you do
        glPushMatrix()
        glTranslatef(light_x + x_translation, light_y + y_translation, light_z + z_translation)
        glColor3f(1.0,1.0,0.0)
        glutSolidSphere(1.0, 25, 25)
        glPopMatrix()
                                
        # draw the spheres in the scene
        for i in range (-1,2):
                for j in range (-1,2):
                        for k in range (-1,2): 
                                glPushMatrix()
                                glTranslatef(x_translation + (i*DISTANCE_BETWEEN_CUBES),y_translation + (j*DISTANCE_BETWEEN_CUBES),z_translation -(k*DISTANCE_BETWEEN_CUBES))
                                glColor3f(1.0,0.0,1.0)
                                glutSolidSphere(1.0, 25, 25)
                                glPopMatrix()
        
        glutSwapBuffers()

def automatic_light():
        global light_x, light_y, light_z, light_theta
        global light_circle_radius
        
        # 150 just works well here, probably should be a parameter
        r = light_circle_radius
        light_x = r*cos(light_theta)
        light_y = r*sin(light_theta)
        light_theta += 0.003
        
                

def print_parms():
        global x_translation, y_translation, z_translation
        global fovy, aspect, zNear, zFar
        
        translations = "SCENE TRANSLATION (x, y, z): " + str(x_translation) + ", " + str(y_translation) + ", " + str(z_translation)
        perspectives = "PERSPECTIVE fovy,aspect,zNear,zFar: " + str(fovy) + ", " + str(aspect) + ", " + str(zNear)+ ", " + str(zFar)
        entire_scene = "SCENE ROTATION (x, y, z): "+str(SCENE_X_AXIS)+", "+str(SCENE_Y_AXIS)+", "+str(SCENE_Z_AXIS)
        light_location = "LIGHT LOCATION (x, y, z):"+str(lightPos)
        print (perspectives)
        print (translations)
        print (entire_scene)
        print (light_location)
        print (" ")
 
def main():
        glutInit(sys.argv)
        glutInitDisplayMode(GLUT_RGBA | GLUT_DOUBLE | GLUT_DEPTH)
        glutInitWindowSize(WIDTH,HEIGHT)
        glutInitWindowPosition(50,50)
        
        glutCreateWindow(b'OpenGL Python Lighted Spheres')
        
        glutDisplayFunc(draw_scene)
        glutIdleFunc(draw_scene)
        glutKeyboardFunc(keyboard)
        glutSpecialFunc(special_input)
        
        init()
        glutMainLoop()
 
if __name__ == "__main__":
        main() 
