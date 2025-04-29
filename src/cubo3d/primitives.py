from OpenGL.GL import *

def draw_pixel(x, y, z=0, color=(1.0, 1.0, 1.0)):
    glColor3f(*color)
    glPointSize(1.0)
    glBegin(GL_POINTS)
    glVertex3f(x, y, z)
    glEnd()
