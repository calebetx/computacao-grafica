import numpy as np

def escala3d(matriz_vertices, escala):
    """
    Escala os vértices de um cubo.

    Parâmetros:
    - matriz_vertices: np.ndarray de forma (n, 3), onde cada linha é um vértice (x, y, z).
    - escala: tupla ou lista com 3 valores (escala_x, escala_y, escala_z)

    Retorna:
    - np.ndarray com os vértices escalados
    """
    # Cria uma matriz de escala 3x3
    matriz_escala = np.diag(escala)

    # Multiplica os vértices pela matriz de escala
    return np.dot(matriz_vertices, matriz_escala)