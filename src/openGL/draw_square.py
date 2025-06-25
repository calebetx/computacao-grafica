from openGL.functions.algorithms import draw_line

def draw_square(points):
    """
    Desenha um quadrado a partir de uma matriz de pontos.

    Parâmetros:
    - points: lista ou array de 4 pontos no formato [[x0, y0], [x1, y0], [x1, y1], [x0, y1]]
    """

    if len(points) != 4:
        raise ValueError("A matriz deve conter exatamente 4 pontos para formar um quadrado.")

    # Desenha as 4 linhas conectando os pontos
    for i in range(4):
        x0, y0 = points[i]
        x1, y1 = points[(i + 1) % 4]  # conecta o último com o primeiro
        draw_line(x0, y0, x1, y1)