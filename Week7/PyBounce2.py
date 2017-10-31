# PyBounce.py

from OpenGL.GL import *
from OpenGL.GLU import *
from OpenGL.GLUT import *
import sys

#  globals for animation, ball position
#  and direction of motion
global anim, x_pos, y_pos ,hvel, vvel


# initial position of the ball
# see below for the gluOrtho2D coordinate system
# x_pos and y_pos are the center of the ball
x_pos = -0.67
y_pos = 0.34

dtime = 0.002
hvel = 0.75
vvel = 3.0
ang = 0.0
ang_step = -1

# Window dimensions
width = height = 600
axrng = 1.0

# No animation to start
anim = 0

def init():
        glClearColor(0.0, 0.0, 0.0, 1.0)
        glColor3ub(255, 0, 0)
        
        # Dimensions of the screen
        # Make axrng larger and see what happens!
        gluOrtho2D(-axrng, axrng, -axrng, axrng)


def idle():
        # what to do when not responding to mouse or keyboard
        # Note the glutIdleFunc() in main that calls this

        # We animate only if anim == 1, otherwise
        # the ball doesn't move
        if anim == 1:
                # really important
                # Mark the current window as needing to be redisplayed.
                # The next iteration through  glutMainLoop,
                # the window's display callback will be called to redisplay
                # the window
                glutPostRedisplay()
                

def plotfunc():
        global x_pos, y_pos, hvel, vvel,ang,ang_step

        # erase and get ready to redraw
        glClear(GL_COLOR_BUFFER_BIT)

        # changes x_pos and y_pos
        x_pos += hvel*dtime
        vvel = vvel - 9.8*dtime
        y_pos += vvel*dtime
        
        # Keep the motion mathematics safe from accidentally changing
        # the reference point
        # freeze the origin in the correct location
        # Move the ball location based on x_pos and y_pos
        # if this was not protected, it would change everyone's reference point
        # Text has a good example on page 252
        glPushMatrix()
        #glTranslatef(0, 0, 0);
        glTranslate(x_pos, y_pos, 0)
        glRotatef(ang, 0.0, 0.0, 0.01)
        glutWireSphere(0.1, 10, 10)
        glPopMatrix()
        
        # Collision detection!
        # What happens here and why does this work?
        if x_pos >= axrng - 0.1 or x_pos <= -axrng + 0.1:
                hvel = -1.0*hvel
                ang_step = ang_step*-1
        if y_pos >= axrng - 0.1 or y_pos <= -axrng + 0.1:
                vvel = -1.0*vvel
        ang += ang_step
        ang = ang%360.0

        # no more glFlush()!
        # makes for a nice smooth animation
        glutSwapBuffers()
        
def keyboard(key, x, y):
        #  Allows us to quit by pressing 'Esc' or 'q'
        #  We can animate by "a" and stop by "s"
        global anim
        
        if key == b'\x1b':
                sys.exit()
        if key == b"a":
                # Notice we are making anim = 1
                # What does this mean?  Look at the idle function
                anim = 1
        if key == b"s":
                # STOP the ball!
                anim = 0
        if key == b"q":
                sys.exit()

                
def mouse(button, state, x, y):
        global anim

        if (button == GLUT_LEFT_BUTTON):
                anim = 1
        if (button == GLUT_RIGHT_BUTTON):
                anim = 0
        
def special_input(key, x, y):
        global x_pos, y_pos

        if key == GLUT_KEY_UP:
                y_vel = y_pos + 0.05
        elif key == GLUT_KEY_DOWN:
                y_vel = y_pos - 0.05
        elif key == GLUT_KEY_LEFT:
                x_vel = x_pos - 0.05
        elif key == GLUT_KEY_RIGHT:
                x_vel = x_pos + 0.05
                
        glutPostRedisplay()
          
        
def main():
        glutInit(sys.argv)
        # We are in Double Buffer mode now
        glutInitDisplayMode(GLUT_RGB|GLUT_DOUBLE)
        glutInitWindowPosition(100,100)
        glutInitWindowSize(width,height)
        glutCreateWindow(b"PyBounce")

        # Event callback routines
        glutDisplayFunc(plotfunc)
        glutMouseFunc(mouse)
        glutKeyboardFunc(keyboard)
        glutIdleFunc(idle)
        glutSpecialFunc(special_input)
        
        init()
        # After a GLUT program has done initial setup such as creating windows
        # and menus, GLUT programs enter the GLUT event processing loop by
        # calling  glutMainLoop.
        # glutMainLoop enters the GLUT event processing loop. 
        glutMainLoop()

main()    
