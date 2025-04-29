from OpenGL.GL import *
from transform import aplicar_translacao, aplicar_rotacao, aplicar_escala

def desenhar_eixos():
    glLineWidth(2.0)
    glBegin(GL_LINES)

    glColor3f(1, 0, 0)  # Eixo X
    glVertex3f(-5, 0, 0)
    glVertex3f(5, 0, 0)

    glColor3f(0, 1, 0)  # Eixo Y
    glVertex3f(0, -5, 0)
    glVertex3f(0, 5, 0)

    glColor3f(0, 0, 1)  # Eixo Z
    glVertex3f(0, 0, -5)
    glVertex3f(0, 0, 5)

    glEnd()
    glLineWidth(1.0)

def gerar_cubo_na_origem(lado=2):
    half = lado / 2
    vertices = [
        (-half, -half, -half), (half, -half, -half),
        (half, half, -half), (-half, half, -half),
        (-half, -half, half), (half, -half, half),
        (half, half, half), (-half, half, half),
    ]
    arestas = [
        (0, 1), (1, 2), (2, 3), (3, 0),
        (4, 5), (5, 6), (6, 7), (7, 4),
        (0, 4), (1, 5), (2, 6), (3, 7)
    ]
    return vertices, arestas

def desenhar_cubo():
    glPushMatrix()

    aplicar_translacao(0, 0, 0)
    aplicar_rotacao(0, 0, 1, 0)
    aplicar_escala(1, 1, 1)

    vertices, arestas = gerar_cubo_na_origem()

    glColor3f(1.0, 1.0, 1.0)  # Cor do cubo
    glLineWidth(2.0)          # Espessura da linha
    glBegin(GL_LINES)

    for i, j in arestas:
        glVertex3fv(vertices[i])
        glVertex3fv(vertices[j])

    glEnd()
    glPopMatrix()
