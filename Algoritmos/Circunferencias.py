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

def initOpenGL():
    if not glfw.init():
        print("GLFW não pôde ser inicializado")
        exit()

    window = glfw.create_window(width, height, "Circunferência", None, None)
    if not window:
        glfw.terminate()
        raise Exception("A janela não pôde ser criada")

    glfw.make_context_current(window)

    glClearColor(0.0, 0.0, 0.0, 1.0)
    gluOrtho2D(-width / 2, width / 2, -height / 2, height / 2)

    return window

def drawPixel(x, y):
    glPointSize(1.0)
    glBegin(GL_POINTS)
    glColor3f(1.0, 0.0, 0.0)
    glVertex2f(x, y)
    glEnd()

def ponto_circulo(x, y):
    drawPixel(x, y)
    drawPixel(x, -y)
    drawPixel(-x, y)
    drawPixel(-x, -y)
    drawPixel(y, x)
    drawPixel(y, -x)
    drawPixel(-y, x)
    drawPixel(-y, -x)

def cpontomedio(raio):
    x = 0
    y = raio
    d = 5/4 - raio

    ponto_circulo(x, y)

    while y > x:
        if d < 0: 
            d += 2 * x + 3
        else:
            d += 2 * (x - y) + 5
            y -= 1
        
        x += 1
        ponto_circulo(x, y)

def draw_circle_polynomial(raio):
    x = 0
    step_size = 1
    x_end = raio / math.sqrt(2)

    while x <= x_end:
        y = math.sqrt(raio ** 2 - x ** 2)
        
        x_round = round(x)
        y_round = round(y)
        
        ponto_circulo(x_round, y_round)
        
        x += step_size
        
        if x > x_end:
            break

def draw_circle_trigonometric(raio):
    theta = 0
    step_size = 0.01
    theta_end = math.pi / 4

    while theta <= theta_end:
        x = raio * math.cos(theta)
        y = raio * math.sin(theta)
        
        x_round = round(x)
        y_round = round(y)
        
        ponto_circulo(x_round, y_round)
        
        theta += step_size
        
        if theta > theta_end:
            break

def escolher_algoritmo():
    print("Escolha o algoritmo para desenhar a circunferência:")
    print("1. Algoritmo de Ponto Médio")
    print("2. Algoritmo Polinomial")
    print("3. Algoritmo Trigonométrico")
    escolha = int(input("Digite o número do algoritmo desejado (1, 2 ou 3): "))
    return escolha

def main():
    raio = float(input("Digite o raio da circunferência: "))
    raio = round(raio)

    window = initOpenGL()

    algoritmo = escolher_algoritmo()

    while not glfw.window_should_close(window):
        glClear(GL_COLOR_BUFFER_BIT)

        if algoritmo == 1:
            cpontomedio(raio)
        elif algoritmo == 2:
            draw_circle_polynomial(raio)
        elif algoritmo == 3:
            draw_circle_trigonometric(raio)
        else:
            print("Opção inválida")
            break

        glfw.swap_buffers(window)
        glfw.poll_events()

    glfw.terminate()

if __name__ == "__main__":
    main()
