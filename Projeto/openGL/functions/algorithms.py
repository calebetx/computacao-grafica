from .primitives import draw_pixel

def draw_line(x0, y0, x1, y1, color=(1.0, 1.0, 1.0)):
    """Algoritmo de Bresenham para desenhar linha."""
    dx = abs(x1 - x0)
    dy = abs(y1 - y0)
    sx = 1 if x0 < x1 else -1
    sy = 1 if y0 < y1 else -1
    err = dx - dy

    while True:
        draw_pixel(x0, y0, color)

        if x0 == x1 and y0 == y1:
            break

        e2 = 2 * err
        if e2 > -dy:
            err -= dy
            x0 += sx
        if e2 < dx:
            err += dx
            y0 += sy

def draw_circle_midpoint(center_x, center_y, radius, color=(1.0, 1.0, 1.0)):
    """Algoritmo de ponto médio para desenhar circunferência."""
    x = 0
    y = radius
    d = 1 - radius

    plot_circle_points(center_x, center_y, x, y, color)

    while y > x:
        if d < 0:
            d += 2 * x + 3
        else:
            d += 2 * (x - y) + 5
            y -= 1
        x += 1
        plot_circle_points(center_x, center_y, x, y, color)

def plot_circle_points(cx, cy, x, y, color):
    """Plota os 8 pontos de simetria."""
    draw_pixel(cx + x, cy + y, color)
    draw_pixel(cx - x, cy + y, color)
    draw_pixel(cx + x, cy - y, color)
    draw_pixel(cx - x, cy - y, color)
    draw_pixel(cx + y, cy + x, color)
    draw_pixel(cx - y, cy + x, color)
    draw_pixel(cx + y, cy - x, color)
    draw_pixel(cx - y, cy - x, color)
