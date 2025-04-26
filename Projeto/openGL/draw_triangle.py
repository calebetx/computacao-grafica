from OpenGL import GL

def draw_triangle():
    GL.glBegin(GL.GL_TRIANGLES)
    GL.glColor3f(1.0, 0.0, 0.0)  
    GL.glVertex2f(-0.5, -0.5)
    GL.glVertex2f(0.5, -0.5)
    GL.glVertex2f(0.0, 0.5)
    GL.glEnd()
