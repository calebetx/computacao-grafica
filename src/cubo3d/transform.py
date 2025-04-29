from OpenGL.GL import *

# Variáveis globais para transformações (se quiser usar depois)
posicao = [0, 0, 0]
rotacao = [0, 0, 0, 0]
escala = [1, 1, 1]

def aplicar_translacao(x, y, z):
    glTranslatef(x, y, z)

def aplicar_rotacao(angulo, x, y, z):
    glRotatef(angulo, x, y, z)

def aplicar_escala(x, y, z):
    glScalef(x, y, z)
