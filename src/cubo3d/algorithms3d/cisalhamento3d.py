import numpy as np

def cisalhamento3d(matriz_vertices, sh_xy=0, sh_xz=0, sh_yz=0):
    """
    Aplica cisalhamento aos vértices de um cubo.

    Parâmetros:
    - matriz_vertices: np.ndarray de forma (n, 3), onde cada linha é um vértice (x, y, z).
    - sh_xy: cisalhamento de X em função de Y.
    - sh_xz: cisalhamento de X em função de Z.
    - sh_yz: cisalhamento de Y em função de Z.

    Retorna:
    - np.ndarray com os vértices cisalhados
    """
    # Cria a matriz de cisalhamento
    matriz_cisalhamento = np.array([
        [1, sh_xy, sh_xz],
        [0,    1, sh_yz],
        [0,    0,    1 ]
    ])

    # Aplica o cisalhamento nos vértices
    return np.dot(matriz_vertices, matriz_cisalhamento)
