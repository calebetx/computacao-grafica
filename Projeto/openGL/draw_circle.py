from OpenGL import GL
import math

def draw_circle(segments=50):
    GL.glBegin(GL.GL_POLYGON)
    GL.glColor3f(0.0, 0.0, 1.0) 

    for i in range(segments):
        theta = 2.0 * math.pi * i / segments
        x = 0.5 * math.cos(theta)
        y = 0.5 * math.sin(theta)
        GL.glVertex2f(x, y)

    GL.glEnd()
