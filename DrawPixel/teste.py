import glfw
from OpenGL.GL import *
import math

# Resolução do dispositivo
# width = 1920
# height = 1080

# Resolução do dispositivo com 125% de escala
width = 1536
height = 864

def initOpenGL():
    if not glfw.init():
        print("Erro ao inicializar GLFW")
        exit()

    window = glfw.create_window(width, height, "Sistemas de Coordenadas", None, None)
    if not window:
        print("Erro ao criar a janela GLFW")
        glfw.terminate()
        exit()

    glfw.make_context_current(window)

    return window

def drawPixel(x, y):
    glPointSize(10.0)
    glBegin(GL_POINTS)
    glVertex2f(x, y)
    glEnd()

# TRANSFORMAÇÕES PASSANDO PELO NDC

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

# TRANSFORMAÇÕES PASSANDO PELO OPENGL

# Transformação do mundo para OpenGL (WD -> OpenGL)
def worldToOpenGL(x, y, xmin, xmax, ymin, ymax):
    opx = (2 * (x - xmin) / (xmax - xmin)) - 1
    opy = (2 * (y - ymin) / (ymax - ymin)) - 1
    return opx, opy

# Transformação de OpenGL para coordenadas do dispositivo (OpenGL -> DC)
def OpenGLtoDevice(opx, opy, width, height):
    dcx = ((opx + 1) * (width - 1)) / 2
    dcy = ((opy + 1) * (height - 1)) / 2
    return dcx, dcy

def main():
    # Intervalo do mundo/usuário
    xmin = float(input("Digite a coordenada XMIN do mundo: "))
    xmax = float(input("Digite a coordenada XMAX do mundo: "))
    ymin = float(input("Digite a coordenada YMIN do mundo: "))
    ymax = float(input("Digite a coordenada YMAX do mundo: "))

    x = float(input("Digite a coordenada X do mundo: "))
    y = float(input("Digite a coordenada Y do mundo: "))

    # Perguntar ao usuário qual transformação ele deseja usar
    print("Escolha a sequência de transformações:")
    print("1. WD -> NDC -> DC")
    print("2. WD -> OpenGL -> DC")
    choice = input("Digite o número da opção desejada (1 ou 2): ")

    window = initOpenGL()

    if choice == '1':
        ndcx, ndcy = worldToNDC(x, y, xmin, xmax, ymin, ymax)
        dcx, dcy = NDCtoDevice(ndcx, ndcy, width, height)

    elif choice == '2':
        opx, opy = worldToOpenGL(x, y, xmin, xmax, ymin, ymax)
        dcx, dcy = OpenGLtoDevice(opx, opy, width, height)

    else:
        print("Opção inválida! Usando a transformação padrão (WD -> NDC -> DC).")
        ndcx, ndcy = worldToNDC(x, y, xmin, xmax, ymin, ymax)
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