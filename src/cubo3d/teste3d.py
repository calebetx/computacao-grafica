import glfw
from OpenGL.GL import *
from OpenGL.GLU import *

from drawCube import desenhar_eixos, desenhar_cubo, gerar_cubo_na_origem
from algorithms3d.escala3d import escala3d

def inicializar_janela(largura, altura, titulo):
    if not glfw.init():
        raise Exception("Erro ao inicializar GLFW.")
    janela = glfw.create_window(largura, altura, titulo, None, None)
    if not janela:
        glfw.terminate()
        raise Exception("Erro ao criar janela.")
    glfw.make_context_current(janela)
    return janela

def definir_camera():
    glMatrixMode(GL_PROJECTION)
    glLoadIdentity()
    gluPerspective(45, 800 / 600, 0.1, 100.0)
    glMatrixMode(GL_MODELVIEW)
    glLoadIdentity()
    gluLookAt(5, 5, 5, 0, 0, 0, 0, 1, 0)

def main():
    janela = inicializar_janela(1600, 900, "Cubo na Origem")

    glEnable(GL_DEPTH_TEST)

    while not glfw.window_should_close(janela):
        glfw.poll_events()
        glClear(GL_COLOR_BUFFER_BIT | GL_DEPTH_BUFFER_BIT)
        definir_camera()

        desenhar_eixos()

        lado = 2
        vertices = gerar_cubo_na_origem(lado)
        fatores_escala = (1.0, 1.0, 0.5)

        vertices = escala3d(vertices, fatores_escala)

        desenhar_cubo(vertices)

        glfw.swap_buffers(janela)

    glfw.terminate()

if __name__ == "__main__":
    main()