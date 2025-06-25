import numpy as np

def rotacao3d(matriz_vertices, angulo, eixo='z'):
    """
    Aplica rotação aos vértices em torno de um eixo.

    Parâmetros:
    - matriz_vertices: np.ndarray de forma (n, 3), onde cada linha é um vértice (x, y, z).
    - angulo: ângulo de rotação em graus.
    - eixo: eixo de rotação ('x', 'y' ou 'z').

    Retorna:
    - np.ndarray com os vértices rotacionados
    """
    # Converte o ângulo para radianos
    rad = np.radians(angulo)

    if eixo == 'x':
        matriz_rotacao = np.array([
            [1, 0, 0],
            [0, np.cos(rad), -np.sin(rad)],
            [0, np.sin(rad),  np.cos(rad)]
        ])
    elif eixo == 'y':
        matriz_rotacao = np.array([
            [ np.cos(rad), 0, np.sin(rad)],
            [ 0, 1, 0],
            [-np.sin(rad), 0, np.cos(rad)]
        ])
    elif eixo == 'z':
        matriz_rotacao = np.array([
            [np.cos(rad), -np.sin(rad), 0],
            [np.sin(rad),  np.cos(rad), 0],
            [0, 0, 1]
        ])
    else:
        raise ValueError("Eixo inválido. Escolha entre 'x', 'y' ou 'z'.")

    # Aplica a matriz de rotação
    return np.dot(matriz_vertices, matriz_rotacao)
