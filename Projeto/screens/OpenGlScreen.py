# opengl_widget.py
from OpenGL import GL
from pyopengltk import OpenGLFrame

class OpenGLScreen(OpenGLFrame):    
    def initgl(self):
        """Inicializa os estados do OpenGL quando o frame é criado"""
        GL.glViewport(0, 0, self.width, self.height)
        GL.glClearColor(0.0, 0.0, 0.0, 1.0)  # Cor de fundo preta

    def redraw(self):
        """Renderiza um único quadro (desenha um quadrado simples)"""
        GL.glClear(GL.GL_COLOR_BUFFER_BIT)  # Limpa o buffer de cor
        # self.draw_square()

    def draw_square(self):
        """Desenha um quadrado simples"""
        GL.glBegin(GL.GL_QUADS)

        GL.glColor3f(1.0, 0.0, 0.0)  # Cor do quadrado (vermelho)

        GL.glVertex2f(-0.5, -0.5)  # Ponto inferior esquerdo
        GL.glVertex2f(0.5, -0.5)   # Ponto inferior direito
        GL.glVertex2f(0.5, 0.5)    # Ponto superior direito
        GL.glVertex2f(-0.5, 0.5)   # Ponto superior esquerdo

        GL.glEnd()
