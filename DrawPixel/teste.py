import glfw
from OpenGL.GL import *
import math

# Resolução do dispositivo
width = 1920
height = 1080

def initOpenGL():
    if not glfw.init():
        print("Erro ao inicializar GLFW")
        exit()

    glfw.window_hint(glfw.CONTEXT_VERSION_MAJOR, 3)
    glfw.window_hint(glfw.CONTEXT_VERSION_MINOR, 3)

    window = glfw.create_window(width, height, "Coordenadas do Mundo", None, None)
    if not window:
        print("Erro ao criar a janela GLFW")
        glfw.terminate()
        exit()

    glfw.make_context_current(window)

    return window

def drawPixel(x, y):
    glPointSize(1.0)
    glBegin(GL_POINTS)
    glColor3f(1.0, 0.0, 0.0)
    glVertex2f(x, y)
    glEnd()

# Mapear as coordenadas do mundo para as coordenadas normalizadas do dispositivo (WD -> NDC)
def worldToNDC(x, y, xmin, xmax, ymin, ymax):
    ndcx = (x - xmin) / (xmax - xmin)
    ndcy = (y - ymin) / (ymax - ymin)
    return ndcx, ndcy

# Mapear as coordenadas normalizadas do dispositivo para as coordenadas do dispositivo (NDC -> DC)
def NDCtoDevice(ndcx, ndcy, width, height):
    dcx = round(ndcx * (width - 1))
    dcy = round(ndcy * (height - 1))
    return dcx, dcy

def main():
    window = initOpenGL()

    # Intervalo do mundo/usuário
    xmin = 10.5
    xmax = 100.3
    ymin = 15.2
    ymax = 100.4

    x = float(input("Digite a coordenada X do mundo: "))
    y = float(input("Digite a coordenada Y do mundo: "))

    # Transformação do mundo para NDC
    ndcx, ndcy = worldToNDC(x, y, xmin, xmax, ymin, ymax)

    # Transformação de NDC para coordenadas do dispositivo
    dcx, dcy = NDCtoDevice(ndcx, ndcy, width, height)

    while not glfw.window_should_close(window):
        glClear(GL_COLOR_BUFFER_BIT)

        # Desenhando o ponto nas coordenadas do dispositivo
        drawPixel(int(dcx) / width * 2 - 1, int(dcy) / height * 2 - 1)

        glfw.swap_buffers(window)
        glfw.poll_events()

    glfw.terminate()

if __name__ == "__main__":
    main()
