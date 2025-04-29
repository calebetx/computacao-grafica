import numpy as np

def translacao3d(matriz_vertices, deslocamento):
    """
    Translada (move) os vértices de um cubo.

    Parâmetros:
    - matriz_vertices: np.ndarray de forma (n, 3), onde cada linha é um vértice (x, y, z).
    - deslocamento: tupla ou lista com 3 valores (desloc_x, desloc_y, desloc_z)

    Retorna:
    - np.ndarray com os vértices transladados
    """
    # Cria um vetor de deslocamento
    vetor_deslocamento = np.array(deslocamento)

    # Soma o vetor de deslocamento a cada vértice
    return matriz_vertices + vetor_deslocamento
