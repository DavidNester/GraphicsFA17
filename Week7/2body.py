# 2Body.py
# a 2 star system based on Piet Hut
# and Jun Makino's MSA text with
# Modifications by Stan Blank for
# use in Python OpenGL/GLUT

from OpenGL.GL import *
from OpenGL.GLU import *
from OpenGL.GLUT import *
from numpy import *
import sys


#  Set the width and height of the window
global width, height, fov, asp_ratio, near_clipping_plane, far_clipping_plane
global lookat_x, lookat_y, lookat_z

#field of view angle
fov = 45.0
#aspect ratio
asp_ratio = 1.0

near_clipping_plane = 5.0
far_clipping_plane = 1000.0

lookat_x = 0.0
lookat_y = 0.0
lookat_z = 5.0

#  Initial values
width = 500
height = 500
                
# initial values for position, velocity components, and time increment
global vx1, vy1, vz1, x1, y1, z1, r2, r3, ax1, ay1, az1, dt
global vx2, vy2, vz2, x2, y2, z2, ax2, ay2, az2, G

# initial x,y,z positions for both stars
x1 = 1.0
y1 = 0.0
z1 = 0.0
x2 = -1.0
y2 = 0.0
z2 = 0.0

# initial vx,vy,vz velocities for both stars
vx1 = 0.0
vy1 = -0.128571428
vz1 = 0.0
vx2 = 0.0
vy2 = 0.3
vz2 = 0.0

# initial masses for both stars
m1 = 0.7
m2 = 0.3
rad1 = 0.1*m1
rad2 = 0.1*m2

# arbitrary "Big G" gravitational constant
G = 1.0

# calculate distance and r**3 denominator for universal gravitation
r2 = (x1-x2)*(x1-x2) + (y1-y2)*(y1-y2) + (z1-z2)*(z1-z2)
r3 = r2*sqrt(r2)

# calculate acceleration components along x,y,z axes
ax1 = -G*(x1-x2)*m2/r3
ay1 = -G*(y1-y2)*m2/r3
az1 = -G*(z1-z2)*m2/r3
ax2 = -G*(x2-x1)*m1/r3
ay2 = -G*(y2-y1)*m1/r3
az2 = -G*(z2-z1)*m1/r3

#This value keeps a smooth orbit on my workstation
#Smaller values slow down the orbit, higher values speed things up
dt = 0.001

def init():
        glClearColor(0.0, 0.0, 0.0, 1.0)
        # NEW If enabled, do depth comparisons 
        glEnable(GL_DEPTH_TEST)
        
def plotFunc():
        # NEW
        # Indicates the buffers currently enabled for color writing
        # Indicates the depth buffer
        glClear(GL_COLOR_BUFFER_BIT|GL_DEPTH_BUFFER_BIT)
        
        # plot the first star (m1) position
        glPushMatrix()
        glTranslatef(x1,y1,z1)
        glColor3ub(245, 230, 100)
        #glColor3ub(245, 150, 30)
        glutSolidSphere(rad1, 10, 10)
        glPopMatrix()
        
        # plot the second star (m2) position
        glPushMatrix()
        glTranslatef(x2,y2,z2)
        glColor3ub(245, 150, 30)
        #glColor3ub(245, 230, 100)
        glutSolidSphere(rad2, 10, 10)
        glPopMatrix()
        
        # swap the drawing buffers
        glutSwapBuffers()
        
def Reshape(  w,  h):
        global fov, asp_ratio, near_clipping_plane, far_clipping_plane
        global lookat_x, lookat_y, lookat_z
        
        # To insure we don't have a zero height
        if h==0:
                h = 1
        
        #  Fill the entire graphics window!
        glViewport(0, 0, w, h)
        
        #  Set the projection matrix... our "view"
        glMatrixMode(GL_PROJECTION)
        glLoadIdentity()

        # NEW set up a perspective projection matrix
        # Specifies the field of view angle, in degrees, in the y direction.
        # Specifies the aspect ratio that determines the field of view in the x direction. The aspect ratio is the ratio of x (width) to y (height). 
        # Specifies the distance from the viewer to the near clipping plane (always positive). 
        # Specifies the distance from the viewer to the far clipping plane (always positive).
        gluPerspective(fov, asp_ratio, near_clipping_plane, far_clipping_plane)

        # NEW gluLookAt creates a viewing matrix derived
        # from an eye point,
        # from a reference point indicating the center of the scene
        # and from an UP vector
        gluLookAt(lookat_x, lookat_y, lookat_z, 0.0, 0.0, 0.0, 0.0, 1.0, 0.0)

        #  Set the matrix for the object we are drawing
        glMatrixMode(GL_MODELVIEW)
        glLoadIdentity()
        
def keyboard(key, x, y):
        global fov, width, height, asp_ratio, near_clipping_plane, far_clipping_plane
        global lookat_x, lookat_y, lookat_z
        
        if key == b'\x1b':
                sys.exit()
        if key == b"q":
                sys.exit()
        if key == b"f":
                fov += 5.0
                print ("field of view = ",fov)
        if key == b"g":
                fov -= 5.0
                print ("field of view = ",fov)
        if key == b"a":
                asp_ratio += 0.1
                print ("aspect ratio = ",asp_ratio)
        if key == b"s":
                asp_ratio -= 0.1
                print ("aspect ratio = ",asp_ratio)
        if key == b"n":
                near_clipping_plane += 1.0
                print ("near_clipping_plane = ",near_clipping_plane)
        if key == b"m":
                near_clipping_plane -= 1.0
                print ("near_clipping_plane = ",near_clipping_plane)
        if key == b"k":
                far_clipping_plane += 100.0
                print ("far_clipping_plane = ",far_clipping_plane)
        if key == b"l":
                far_clipping_plane -= 100.0
                print ("far_clipping_plane = ",far_clipping_plane)
        if key == b"x":
                lookat_x += 1
                print ("eye point x = ",lookat_x)
        if key == b"c":
                lookat_x -= 1
                print ("eye point x = ",lookat_x)
        if key == b"y":
                lookat_y += 1
                print ("eye point y = ",lookat_y)
        if key == b"u":
                lookat_y -= 1
                print ("eye point y = ",lookat_y)
        if key == b"z":
                lookat_z += 1
                print ("eye point z = ",lookat_z)
        if key == b"v":
                lookat_z -= 1
                print ("eye point z = ",lookat_z)
        if key == b"V":
                print ("CURRENT PARAMETERS VALUES")
                print ("fov = ",fov)
                print ("asp_ratio = ",asp_ratio)
                print ("near_clipping_plane = ",near_clipping_plane)
                print ("far_clipping_plane + ",far_clipping_plane)
                print ("lookat_x = ",lookat_x)
                print ("lookat_y = ",lookat_y)
                print ("lookat_z = ",lookat_z)
        if key == b"R":
                print ("RESETTING ALL PERSPECTIVE and LOOKAT PARAMETERS TO DEFAULT VALUES")
                fov = 45.0
                asp_ratio = 1.0
                near_clipping_plane = 1.0
                far_clipping_plane = 1000.0
                lookat_x = 0.0
                lookat_y = 0.0
                lookat_z = 5.0
                
        Reshape(width, height)
                

def orbits():
        global vx1, vy1, vz1, x1, y1, z1, r2, r3, ax1, ay1, az1
        global vx2, vy2, vz2, x2, y2, z2, ax2, ay2, az2
        
        # calculate front half of velocity vector components
        vx1 += 0.5*ax1*dt
        vy1 += 0.5*ay1*dt
        vz1 += 0.5*az1*dt
        vx2 += 0.5*ax2*dt
        vy2 += 0.5*ay2*dt
        vz2 += 0.5*az2*dt
        
        # calculate x,y,z positions for both stars
        x1 += vx1*dt
        y1 += vy1*dt
        z1 += vz1*dt
        x2 += vx2*dt
        y2 += vy2*dt
        z2 += vz2*dt
        
        # calculate the new r**3 denominator for each star position
        r2 = (x1-x2)*(x1-x2) + (y1-y2)*(y1-y2) + (z1-z2)*(z1-z2)
        r3 = r2*sqrt(r2)
        
        # calculate the new acceleration components
        ax1 = -G*(x1-x2)*m2/r3
        ay1 = -G*(y1-y2)*m2/r3
        az1 = -G*(z1-z2)*m2/r3
        ax2 = -G*(x2-x1)*m1/r3
        ay2 = -G*(y2-y1)*m1/r3
        az2 = -G*(z2-z1)*m1/r3
        
        # calculate the back half velocity components
        vx1 += 0.5*ax1*dt
        vy1 += 0.5*ay1*dt
        vz1 += 0.5*az1*dt
        vx2 += 0.5*ax2*dt
        vy2 += 0.5*ay2*dt
        vz2 += 0.5*az2*dt
        
        #send calculated x,y,z star positions to the display
        glutPostRedisplay()
        
def main():
        global width
        global height
        
        glutInit(sys.argv)
        glutInitDisplayMode(GLUT_RGB|GLUT_DOUBLE)
        glutInitWindowPosition(100,100)
        glutInitWindowSize(width,height)
        glutCreateWindow(b"2 Body Problem")
        glutReshapeFunc(Reshape)
        glutDisplayFunc(plotFunc)
        glutKeyboardFunc(keyboard)
        glutIdleFunc(orbits)
        
        init()  
        glutMainLoop()

main()    
