from primitives import draw_pixel
from algorithms import draw_line_3d

# Mantemos apenas os vertices

def gerar_cubo_na_origem(lado=2):
    vertices = [
        (0, 0, 0), (lado, 0, 0),
        (lado, lado, 0), (0, lado, 0),
        (0, 0, lado), (lado, 0, lado),
        (lado, lado, lado), (0, lado, lado),
    ]
    arestas = [
        (0, 1), (1, 2), (2, 3), (3, 0),
        (4, 5), (5, 6), (6, 7), (7, 4),
        (0, 4), (1, 5), (2, 6), (3, 7)
    ]
    return vertices, arestas


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

def desenhar_cubo():
    vertices, arestas = gerar_cubo_na_origem()

    # desenha os vertices
    for v in vertices:
        draw_pixel(v[0], v[1], v[2], color=(1.0, 1.0, 1.0))

    # desenha as arestas usando draw_line_3d
    for i, j in arestas:
        x0, y0, z0 = vertices[i]
        x1, y1, z1 = vertices[j]
        draw_line_3d(x0, y0, z0, x1, y1, z1, color=(1.0, 1.0, 1.0))
