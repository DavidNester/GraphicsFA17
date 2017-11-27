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
import time
from math import cos
from math import sin
from math import sqrt

#translation variables
x_translation = 0.0
y_translation = 0.0
z_translation = 0.0
translation_amt = 0.1
z_translation_amt = 0.005

SPHERE_RADIUS = 1.0

#rotation
X_AXIS = 0.0
Y_AXIS = 0.0
Z_AXIS = 0.0
 
DIRECTION = 1
ROTATION_ANGLE = 1.0
WIDTH = 750
HEIGHT = 750
#DISTANCE_BETWEEN_CUBES = 6.0

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

all_spheres = []
add_spheres_time = 0.0
STARTING_NUMBER_SPHERES = 10
GAME_WIDTH = 25
GAME_HEIGHT = 25
STARTING_Z_POS = -75
Z_SPEED = 0.01
ADD_SPHERES_EVERY_N_SECONDS = 0.8
REMOVE_DISTANCE = 10

ADD_MOTHERSHIP_TIME = 10
add_mothership = False
mothership_already_added = False
STARTING_MS_POS = -100
mothership = [0.0, 0.0, 0.0]
mothership_spin_angle = 0.0
mothership_spin_delta = 1.0

collision = False
successful_dock = False
game_over = False
write_once = False

final_x = 0.0
final_y = 0.0
final_z = 0.0

def init(): 

        global fovy, aspect, zNear, zFar
        global add_spheres_time, start_time
        
        glClearColor(0.0, 0.0, 0.0, 0.0)
        
        glClearDepth(1.0)
        glDepthFunc(GL_LESS)
        glEnable(GL_DEPTH_TEST)

        # LIGHTING
        glEnable(GL_LIGHTING)
        #glLightfv(GL_LIGHT1, GL_AMBIENT, ambientLight)
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

        # load some initial spheres
        # time will be used to trigger new objects after start
        add_spheres_time = time.time()
        start_time = time.time()
        
        for i in range(0,STARTING_NUMBER_SPHERES):
                # random position along z-axis
                random_width_pos = (-GAME_WIDTH/2)+int(random.random()*GAME_WIDTH)
                random_height_pos = (-GAME_HEIGHT/2)+int(random.random()*GAME_HEIGHT)
                list_of_starting_positions = [random_width_pos,random_height_pos,STARTING_Z_POS]
                all_spheres.append(list_of_starting_positions)

                
def keyboard(key, x, y):
        #  Allows us to quit by pressing 'Esc' or 'q'
        global x_rot, y_rot, z_rot, z_translation
        global fovy, aspect, zNear, zFar
        global SCENE_X_AXIS, SCENE_Y_AXIS, SCENE_Z_AXIS
        global x_translation, y_translation, z_translation
        global light_x, light_y, light_theta
        global auto_light, game_over
        
        if game_over:
                return
        
        if key == b'\x1b':
                sys.exit()
        elif key == b"Z" or key == b"z":
                # z translation
                z_translation += translation_amt
        elif key == b"X" or key == b"x":
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
                z_translation = -25
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
        global x_translation, y_translation, z_translation, translation_amt, game_over

        if game_over:
                return
        if key == GLUT_KEY_UP:
                y_translation -= translation_amt
        elif key == GLUT_KEY_DOWN:
                y_translation += translation_amt
        elif key == GLUT_KEY_LEFT:
                x_translation += translation_amt
        elif key == GLUT_KEY_RIGHT:
                x_translation -= translation_amt
                
        print_parms()
                
def move_objs():
        global all_spheres, mothership
        global Z_SPEED

        for obj in all_spheres:
                # just move closer in Z
                obj[2] += Z_SPEED

        mothership[2] += Z_SPEED

def generate_more_objs():
        global add_spheres_time, start_time, all_spheres
        global ADD_SPHERES_EVERY_N_SECONDS
        global ADD_MOTHERSHIP_TIME, add_mothership, mothership, STARTING_MS_POS, mothership_already_added

        if (time.time()- add_spheres_time > ADD_SPHERES_EVERY_N_SECONDS):
                # random position along z-axis
                random_width_pos = (-GAME_WIDTH/2)+int(random.random()*GAME_WIDTH)
                random_height_pos = (-GAME_HEIGHT/2)+int(random.random()*GAME_HEIGHT)
                list_of_starting_positions = [random_width_pos,random_height_pos,STARTING_Z_POS]
                all_spheres.append(list_of_starting_positions)
                add_spheres_time = time.time()

        if ((time.time() - start_time) > ADD_MOTHERSHIP_TIME) and not mothership_already_added:
                add_mothership = True
                mothership_already_added = True
                mothership = [0.0, 0.0, STARTING_MS_POS]
                        
        
def remove_off_screen_objs():
        global all_spheres

        for obj in all_spheres:
                if obj[2] > REMOVE_DISTANCE:
                        all_spheres.remove(obj)
                        
# compute the distance between two points in space
def distance_between_points_in_space(x1, y1, z1, x2, y2, z2):
        discriminant = ((x1 - x2)**2) + ((y1 - y2)**2) + ((z1 - z2)**2)
        distance = sqrt(discriminant)
        return distance


def detect_collision():
        global all_spheres, SPHERE_RADIUS
        global x_translation, y_translation, z_translation
        global mothership
        global game_over, successful_dock, collision
        global final_x, final_y, final_z

        # I am at (0,0,0) plus any translations
        my_x_pos = 0.0-x_translation
        my_y_pos = 0.0-y_translation
        my_z_pos = 0.0+z_translation

        for obj in all_spheres:
                if (distance_between_points_in_space(my_x_pos, my_y_pos, my_z_pos, obj[0], obj[1], obj[2]) < SPHERE_RADIUS):
                        #print ("collision with ",obj," with my position = ",my_x_pos, my_y_pos, my_z_pos)
                        collision = True
                        game_over = True

        if mothership_already_added:
                if (distance_between_points_in_space(my_x_pos, my_y_pos, my_z_pos, mothership[0], mothership[1], mothership[2]) < SPHERE_RADIUS):
                        #print ("successful dock with mothership ",mothership," with my position = ",my_x_pos, my_y_pos, my_z_pos)
                        successful_dock = True
                        game_over = True
        if game_over:
                final_x = my_x_pos
                final_y = my_y_pos
                final_z = my_z_pos
                
                        
def draw_objs():
        global x_translation, y_translation, z_translation
        global all_spheres, SPHERE_RADIUS
        
        # draw the light source
        # you really have to zoom out a long way to see it,
        # but it is cool when you do
        glPushMatrix()
        glTranslatef(light_x + x_translation, light_y + y_translation, light_z + z_translation)
        glColor3f(1.0,1.0,0.0)
        glutSolidSphere(SPHERE_RADIUS, 25, 25)
        glPopMatrix()

        for obj in all_spheres:
                # draw the spheres in the scene
                glPushMatrix()
                glTranslatef(x_translation+obj[0], y_translation+obj[1], obj[2])
                glColor3f(1.0,0.0,1.0)
                glutSolidSphere(SPHERE_RADIUS, 25, 25)
                glPopMatrix()

                
def draw_mothership():
        global add_mothership, mothership
        global x_translation, y_translation, z_translation
        global SPHERE_RADIUS
        global successful_dock
        global mothership_spin_angle, mothership_spin_delta

        if add_mothership:
                glPushMatrix()
                glTranslatef(x_translation+mothership[0], y_translation+mothership[1], mothership[2])
                glRotatef(mothership_spin_angle, 0.0, 1.0, 0.0)
                mothership_spin_angle += mothership_spin_delta
                glColor3f(0.0,0.0,1.0)
##                glutSolidSphere(SPHERE_RADIUS/2, 25, 25)
                glutSolidTorus(SPHERE_RADIUS/2, SPHERE_RADIUS, 10, 25)
##                glutSolidDodecahedron()
##                glutSolidOctahedron()
##                glutSolidTetrahedron()
##                glutSolidIcosahedron()
                glPopMatrix()


def glut_print_3D(font, text):
        for ch in text :
                glutStrokeCharacter(font, ctypes.c_int(ord(ch)))

                
def draw_game_over():
        global successful_dock, collision
        global final_x, final_y, final_z

        glPushMatrix()
        glTranslatef(final_x - 7.5, final_y, final_z - 20)
        # The fonts are 152 units.  I am working in much smaller units,
        # so I only want to take a fraction of their size
        # this one stumped me for a while!
        glScalef(1.0/152.38, 1.0/152.38, 1.0/152.38)
        glColor3f(0.0,1.0,0.0)

        if successful_dock:
                glut_print_3D(GLUT_STROKE_ROMAN , "SUCCESSFUL DOCK : GAME OVER")
        else:
                glut_print_3D(GLUT_STROKE_ROMAN , "    COLLISION : GAME OVER")

        glPopMatrix()
        

def draw_scene():
        global SPHERE_RADIUS, X_AXIS,Y_AXIS,Z_AXIS
        global x_translation, y_translation, z_translation
        global DIRECTION, ROTATION_ANGLE, DISTANCE_BETWEEN_CUBES
        global NUMBER_CUBE_ROWS
        global fovy, aspect, zNear, zFar
        global SCENE_X_AXIS, SCENE_Y_AXIS, SCENE_Z_AXIS
        global light_x, light_y, light_z, lightPos, auto_light, light_theta
        global all_spheres
        global game_over, stop_the_game

        
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

        if game_over:
                draw_game_over()
        draw_objs()
        draw_mothership()
        detect_collision()
        move_objs()
        generate_more_objs()
        remove_off_screen_objs()
        
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
        """
        translations = "SCENE TRANSLATION (x, y, z): " + str(x_translation) + ", " + str(y_translation) + ", " + str(z_translation)
        perspectives = "PERSPECTIVE fovy,aspect,zNear,zFar: " + str(fovy) + ", " + str(aspect) + ", " + str(zNear)+ ", " + str(zFar)
        entire_scene = "SCENE ROTATION (x, y, z): "+str(SCENE_X_AXIS)+", "+str(SCENE_Y_AXIS)+", "+str(SCENE_Z_AXIS)
        light_location = "LIGHT LOCATION (x, y, z):"+str(lightPos)
        print (perspectives)
        print (translations)
        print (entire_scene)
        print (light_location)
        print (" ")
        """
        return
 
def main():
        glutInit(sys.argv)
        glutInitDisplayMode(GLUT_RGBA | GLUT_DOUBLE | GLUT_DEPTH)
        glutInitWindowSize(WIDTH,HEIGHT)
        glutInitWindowPosition(50,50)
        
        glutCreateWindow(b'OpenGL Python 3D Game')
        
        glutDisplayFunc(draw_scene)
        glutIdleFunc(draw_scene)
        glutKeyboardFunc(keyboard)
        glutSpecialFunc(special_input)
        
        init()
        glutMainLoop()
 
if __name__ == "__main__":
        main() 
