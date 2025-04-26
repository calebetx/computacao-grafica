from OpenGL import GL

def draw_square():
    GL.glBegin(GL.GL_QUADS)
    GL.glColor3f(0.0, 1.0, 0.0) 
    GL.glVertex2f(-0.5, -0.5)
    GL.glVertex2f(0.5, -0.5)
    GL.glVertex2f(0.5, 0.5)
    GL.glVertex2f(-0.5, 0.5)
    GL.glEnd()
