import glfw
from OpenGL.GL import *
from OpenGL.GLU import *

# Resolução do dispositivo
# width = 1920
# height = 1080

# Resolução do dispositivo com 125% de escala
width = 1536
height = 864

# Função de inicialização do OpenGL
def initOpenGL():
    if not glfw.init():
        print("GLFW não pôde ser inicializado")
        exit()

    # Cria a janela
    window = glfw.create_window(width, height, "Circunferência - Ponto Médio", None, None)
    if not window:
        glfw.terminate()
        raise Exception("A janela não pôde ser criada")

    glfw.make_context_current(window)

    # Configurações iniciais do OpenGL
    glClearColor(0.0, 0.0, 0.0, 1.0)  # Cor de fundo (preto)
    gluOrtho2D(-width / 2, width / 2, -height / 2, height / 2)

    return window

# Função para desenhar os pontos da circunferência
def drawPixel(x, y):
    glPointSize(1.0)
    glBegin(GL_POINTS)
    glColor3f(1.0, 0.0, 0.0)
    glVertex2f(x, y)
    glEnd()

def ponto_circulo(x, y):
    drawPixel( x,  y)
    drawPixel( x, -y)
    drawPixel(-x,  y)
    drawPixel(-x, -y)
    drawPixel( y,  x)
    drawPixel( y, -x)
    drawPixel(-y,  x)
    drawPixel(-y, -x)


# Função para desenhar a circunferência pelo algoritmo de ponto médio
def cpontomedio(raio):
    x = 0
    y = raio
    d = 5/4 - raio  # Valor inicial do parâmetro de decisão

    # Desenha os primeiros pontos
    ponto_circulo(x, y)

    while y > x:
        if d < 0:  # Escolhe E
            d += 2 * x + 3
        else:  # Escolhe SE
            d += 2 * (x - y) + 5
            y -= 1
        
        x += 1
        ponto_circulo(x, y)  # Desenha o ponto


def main():
    # Entrada do raio da circunferência
    raio = int(input("Digite o raio da circunferência: "))

    # Inicializa o OpenGL e cria a janela
    window = initOpenGL()

    # Desenha a circunferência
    

    # Loop de renderização
    while not glfw.window_should_close(window):
        glClear(GL_COLOR_BUFFER_BIT)  # Limpa o buffer de cor

        cpontomedio(raio)
        # ponto_circulo(0, raio)
        # drawPixel(-50, -60)

        glfw.swap_buffers(window)  # Troca os buffers (mostra o que foi desenhado)
        glfw.poll_events()  # Processa os eventos

    glfw.terminate()

if __name__ == "__main__":
    main()
