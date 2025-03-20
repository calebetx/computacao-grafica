import pygame
import glfw
from OpenGL.GL import *
from OpenGL.GLU import *
import tkinter as tk
from tkinter import simpledialog

width = 1536
height = 864

# Função de inicialização do OpenGL
def initOpenGL():
    if not glfw.init():
        print("GLFW não pôde ser inicializado")
        exit()

    # Cria a janela OpenGL
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
    drawPixel(x, y)
    drawPixel(x, -y)
    drawPixel(-x, y)
    drawPixel(-x, -y)
    drawPixel(y, x)
    drawPixel(y, -x)
    drawPixel(-y, x)
    drawPixel(-y, -x)

# Função para desenhar a circunferência pelo algoritmo de ponto médio
def cpontomedio(raio):
    x = 0
    y = raio
    d = 5/4 - raio  # Valor inicial do parâmetro de decisão

    ponto_circulo(x, y)

    while y > x:
        if d < 0:  # Escolhe E
            d += 2 * x + 3
        else:  # Escolhe SE
            d += 2 * (x - y) + 5
            y -= 1
        
        x += 1
        ponto_circulo(x, y)  # Desenha o ponto

# Função que usa o Tkinter para obter o raio do círculo
def obter_raio():
    root = tk.Tk()
    root.withdraw()  # Oculta a janela principal do Tkinter
    raio = simpledialog.askinteger("Raio", "Digite o raio da circunferência:", minvalue=1, maxvalue=500)
    root.destroy()  # Fecha a janela após a entrada
    return raio

def main():
    # Obter o raio usando o Tkinter
    raio = obter_raio()
    if raio is None:
        print("Raio não foi fornecido. Encerrando o programa.")
        return

    # Inicializa o OpenGL e cria a janela
    window = initOpenGL()

    # Loop de renderização
    while not glfw.window_should_close(window):
        glClear(GL_COLOR_BUFFER_BIT)  # Limpa o buffer de cor

        # Desenha a circunferência com o algoritmo de ponto médio
        cpontomedio(raio)

        glfw.swap_buffers(window)  # Troca os buffers (mostra o que foi desenhado)
        glfw.poll_events()  # Processa os eventos

    glfw.terminate()

if __name__ == "__main__":
    main()
