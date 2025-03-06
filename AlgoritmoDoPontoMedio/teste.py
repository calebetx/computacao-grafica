import glfw
from OpenGL.GL import *
from OpenGL.GLU import *
import math

# Resolução do dispositivo
# width = 1920
# height = 1080

# Resolução do dispositivo com 125% de escala
width = 1536
height = 864

# Função para desenhar a linha utilizando o algoritmo de Bresenham
def line_bresenham(x0, y0, xEnd, yEnd):
    dx = abs(xEnd - x0)
    dy = abs(yEnd - y0)
    
    p = 2 * dy - dx
    twoDy = 2 * dy
    twoDyMinusDx = 2 * (dy - dx)
    
    if x0 > xEnd:
        x = xEnd
        y = yEnd
        xEnd = x0
    else:
        x = x0
        y = y0
    
    # Desenhando o ponto inicial
    set_pixel(x, y)
    
    while x < xEnd:
        x += 1
        if p < 0:
            p += twoDy
        else:
            y += 1
            p += twoDyMinusDx
        
        # Desenhando o ponto
        set_pixel(x, y)

# Função para desenhar um pixel no OpenGL
def set_pixel(x, y):
    glVertex2i(x, y)  # Função OpenGL para desenhar um ponto no espaço 2D

# Função para configurar a visualização do OpenGL
def setup():
    glClearColor(0.0, 0.0, 0.0, 1.0)  # Cor de fundo preta
    glMatrixMode(GL_PROJECTION)
    glLoadIdentity()
    gluOrtho2D(0, 500, 0, 500)  # Definindo o sistema de coordenadas 2D

# Função para desenhar
def draw():
    glClear(GL_COLOR_BUFFER_BIT)  # Limpa a tela
    glBegin(GL_POINTS)  # Começa o desenho de pontos
    line_bresenham(x0, y0, xEnd, yEnd)  # Chama o algoritmo de Bresenham com as coordenadas fornecidas
    glEnd()  # Finaliza o desenho de pontos
    glfw.swap_buffers(window)  # Troca o buffer para renderizar

# Função de loop principal
def main():
    # Inicializa o GLFW
    if not glfw.init():
        return

    # Criação da janela GLFW
    global window
    window = glfw.create_window(width, height, "Algoritmo de Bresenham com OpenGL", None, None)
    
    if not window:
        glfw.terminate()
        return

    glfw.make_context_current(window)  # Estabelece o contexto de renderização
    
    setup()  # Configura a visualização do OpenGL

    # Pergunta ao usuário as coordenadas da reta
    global x0, y0, xEnd, yEnd
    try:
        x0 = int(input("Insira a coordenada x0 (ponto inicial, eixo X): "))
        y0 = int(input("Insira a coordenada y0 (ponto inicial, eixo Y): "))
        xEnd = int(input("Insira a coordenada xEnd (ponto final, eixo X): "))
        yEnd = int(input("Insira a coordenada yEnd (ponto final, eixo Y): "))
    except ValueError:
        print("Por favor, insira valores inteiros válidos.")
        glfw.terminate()
        return

    # Loop de renderização
    while not glfw.window_should_close(window):
        draw()  # Chama a função de desenho
        glfw.poll_events()  # Processa eventos da janela

    glfw.terminate()  # Finaliza o GLFW

# Inicia a aplicação
if __name__ == "__main__":
    main()
