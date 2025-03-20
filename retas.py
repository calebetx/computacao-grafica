import glfw
from OpenGL.GL import *
from OpenGL.GLU import *
from math import *

# Resolução da janela
default_width = 1536
default_height = 864

def initOpenGL():
    if not glfw.init():
        print("Erro ao inicializar GLFW")
        exit()

    window = glfw.create_window(default_width, default_height, "Algoritmos de Desenho de Linhas", None, None)
    if not window:
        print("Erro ao criar a janela GLFW")
        glfw.terminate()
        exit()

    glfw.make_context_current(window)
    
    # Configurando a projeção ortográfica
    gluOrtho2D(0, default_width, 0, default_height)

    return window

def drawPixel(x, y):
    glPointSize(2.0)
    glBegin(GL_POINTS)
    glVertex2f(x, y)
    glEnd()

def line_dda(x0, y0, x_end, y_end):
    dx = x_end - x0
    dy = y_end - y0
    steps = max(fabs(dx), fabs(dy))

    x_increment = dx / steps
    y_increment = dy / steps

    x, y = x0, y0

    # Desenhando o primeiro ponto
    drawPixel(round(x), round(y))

    for _ in range(int(steps)):
        x += x_increment
        y += y_increment
        drawPixel(round(x), round(y))

def inc_line(x1, y1, x2, y2):
    dx = x2 - x1
    dy = y2 - y1

    d = 2 * dy - dx  # Valor inicial de d
    incE = 2 * dy  # Incremento de E
    incNE = 2 * (dy - dx)  # Incremento de NE

    x = x1
    y = y1

    # Escreve o primeiro pixel
    drawPixel(x, y)

    while x < x2:
        if d <= 0:
            # Escolhe E
            d = d + incE
            x = x + 1
        else:
            # Escolhe NE
            d = d + incNE
            x = x + 1
            y = y + 1
        
        # Escreve o próximo pixel
        drawPixel(x, y)

def line_bresenham(x0, y0, x_end, y_end):
    dx = abs(x_end - x0)
    dy = abs(y_end - y0)

    p = 2 * dy - dx
    twoDy = 2 * dy
    twoDyMinusDx = 2 * (dy - dx)

    # Inicializando as coordenadas do ponto inicial
    if x0 > x_end:
        x = x_end
        y = y_end
        x_end = x0
    else:
        x = x0
        y = y0

    # Desenhando o primeiro ponto
    drawPixel(x, y)

    # Desenhando a linha
    while x < x_end:
        x += 1
        if p < 0:
            p += twoDy
        else:
            y += 1
            p += twoDyMinusDx
        drawPixel(x, y)

def main():
    # Entrada do usuário para coordenadas e escolha do algoritmo
    x0 = int(input("Digite a coordenada x0: "))
    y0 = int(input("Digite a coordenada y0: "))
    x_end = int(input("Digite a coordenada x_end: "))
    y_end = int(input("Digite a coordenada y_end: "))

    print("Escolha o algoritmo:")
    print("1: Algoritmo DDA")
    print("2: Algoritmo Incremental")
    print("3: Algoritmo de Bresenham")
    choice = int(input("Digite sua escolha (1/2/3): "))

    window = initOpenGL()

    while not glfw.window_should_close(window):
        glClear(GL_COLOR_BUFFER_BIT)
        
        if choice == 1:
            line_dda(x0, y0, x_end, y_end)
        elif choice == 2:
            inc_line(x0, y0, x_end, y_end)
        elif choice == 3:
            line_bresenham(x0, y0, x_end, y_end)
        else:
            print("Opção inválida! Nenhuma linha será desenhada.")
            break
        
        glfw.swap_buffers(window)
        glfw.poll_events()
    
    glfw.terminate()

if __name__ == "__main__":
    main()
