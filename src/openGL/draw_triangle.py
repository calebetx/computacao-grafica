from openGL.functions.algorithms import draw_line

def draw_triangle():
    size = 150

    # Três vértices
    x0, y0 = 0, size
    x1, y1 = -size, -size
    x2, y2 = size, -size

    draw_line(x0, y0, x1, y1)  # Lado esquerdo
    draw_line(x1, y1, x2, y2)  # Base
    draw_line(x2, y2, x0, y0)  # Lado direito
