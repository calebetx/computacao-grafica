from OpenGL.GL import *

def draw_pixel(x, y, color=(1.0, 1.0, 1.0)):
    glColor3f(*color)
    glPointSize(1.0)
    glBegin(GL_POINTS)
    glVertex2f(x, y)
    glEnd()
