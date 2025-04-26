from openGL.functions.algorithms import draw_line

def draw_square():
    size = 150

    x0, y0 = -size, -size
    x1, y1 = size, -size
    x2, y2 = size, size
    x3, y3 = -size, size

    draw_line(x0, y0, x1, y1)  # Base inferior
    draw_line(x1, y1, x2, y2)  # Lado direito
    draw_line(x2, y2, x3, y3)  # Base superior
    draw_line(x3, y3, x0, y0)  # Lado esquerdo
