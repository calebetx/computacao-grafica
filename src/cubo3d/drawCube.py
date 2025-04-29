from primitives import draw_pixel
from algorithms import draw_line_3d
import math

# Mantemos apenas os vertices

def gerar_cubo_na_origem(lado):
    vertices = [
        (0, 0, 0), (lado, 0, 0),
        (lado, lado, 0), (0, lado, 0),
        (0, 0, lado), (lado, 0, lado),
        (lado, lado, lado), (0, lado, lado),
    ]
    
    return vertices

def desenhar_eixos():
    from OpenGL.GL import glLineWidth, glBegin, glEnd, glColor3f, glVertex3f, GL_LINES

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

def desenhar_cubo(vertices, lado):
    # Desenhar vértices
    for x, y, z in vertices:
        draw_pixel(x, y, z, color=(1.0, 1.0, 1.0))

    # Conectar vértices que estão a uma distância igual ao lado do cubo
    for i in range(len(vertices)):
        for j in range(i + 1, len(vertices)):
            x0, y0, z0 = vertices[i]
            x1, y1, z1 = vertices[j]

            # Distância Euclidiana
            distancia = math.sqrt((x1 - x0)**2 + (y1 - y0)**2 + (z1 - z0)**2)

            # Se a distância for igual ao lado do cubo, conectar
            if math.isclose(distancia, lado, abs_tol=1e-6):
                draw_line_3d(x0, y0, z0, x1, y1, z1, color=(1.0, 1.0, 1.0))
