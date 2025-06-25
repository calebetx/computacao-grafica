import numpy as np

def reflexao3d(vertices, plano='XY'):
    """
    Reflete os vértices de um objeto 3D em relação a um plano.

    Parâmetros:
    - vertices: np.ndarray de forma (n, 3), onde cada linha é um vértice (x, y, z)
    - plano: str - 'XY', 'YZ', ou 'XZ'

    Retorna:
    - np.ndarray com os vértices refletidos
    """
    matriz_reflexao = np.identity(3)

    if plano.upper() == 'XY':
        matriz_reflexao[2][2] = -1  # Inverte Z
    elif plano.upper() == 'YZ':
        matriz_reflexao[0][0] = -1  # Inverte X
    elif plano.upper() == 'XZ':
        matriz_reflexao[1][1] = -1  # Inverte Y
    else:
        raise ValueError("Plano inválido. Use 'XY', 'YZ' ou 'XZ'.")

    return np.dot(vertices, matriz_reflexao)
