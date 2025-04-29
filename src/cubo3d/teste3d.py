import glfw
from OpenGL.GL import *
from OpenGL.GLU import *
import numpy as np
import threading
import time

from algorithms3d.translacao3d import translacao3d
from algorithms3d.cisalhamento3d import cisalhamento3d
from algorithms3d.rotacao3d import rotacao3d
from drawCube import desenhar_eixos, desenhar_cubo, gerar_cubo_na_origem
from algorithms3d.escala3d import escala3d
from algorithms3d.reflexao3d import reflexao3d

from menu import menu_transformacoes

# Lista de transformações acumuladas
transformacoes = []

def executar_menu_em_loop():
    while True:
        tipo, parametros = menu_transformacoes()
        if tipo == 'sair':
            print("Encerrando entrada de transformações.")
            break
        transformacoes.append((tipo, parametros))
        print(f"[INFO] Transformação '{tipo}' adicionada.\n")

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

def aplicar_transformacoes(vertices):
    for tipo, parametros in transformacoes:
        if tipo == 'escala':
            vertices = escala3d(vertices, parametros)
        elif tipo == 'translacao':
            vertices = translacao3d(vertices, parametros)
        elif tipo == 'reflexao':
            vertices = reflexao3d(vertices, parametros)
        elif tipo == 'cisalhamento':
            sh_xy, sh_xz, sh_yz = parametros
            vertices = cisalhamento3d(vertices, sh_xy, sh_xz, sh_yz)
        elif tipo == 'rotacao':
            angulo, eixo = parametros
            vertices = rotacao3d(vertices, angulo, eixo)
    return vertices

def main():
    # Inicia o menu em thread paralela
    menu_thread = threading.Thread(target=executar_menu_em_loop, daemon=True)
    menu_thread.start()

    # Inicia janela e cubo
    janela = inicializar_janela(1600, 900, "Cubo Interativo")
    glEnable(GL_DEPTH_TEST)

    lado = 2
    vertices_base = gerar_cubo_na_origem(lado)

    while not glfw.window_should_close(janela):
        glfw.poll_events()
        glClear(GL_COLOR_BUFFER_BIT | GL_DEPTH_BUFFER_BIT)
        definir_camera()
        desenhar_eixos()

        vertices = np.copy(vertices_base)
        vertices = aplicar_transformacoes(vertices)

        desenhar_cubo(vertices)
        glfw.swap_buffers(janela)

        # Pequeno delay para reduzir uso de CPU
        time.sleep(0.01)

    glfw.terminate()

if __name__ == "__main__":
    main()
