import numpy as np

def cisalhamento2d(pontos, shx=0.0, shy=0.0):
    """
    Aplica cisalhamento 2D a um array de pontos.

    Parâmetros:
    - pontos: lista ou np.array de forma (N, 2), com pontos [x, y]
    - shx: fator de cisalhamento no eixo X
    - shy: fator de cisalhamento no eixo Y

    Retorna:
    - np.array com os pontos após cisalhamento
    """
    pontos = np.array(pontos)

    # Matriz de cisalhamento
    matriz_cisalhamento = np.array([
        [1, shx],
        [shy, 1]
    ])

    # Aplica cisalhamento
    pontos_cisalhados = pontos @ matriz_cisalhamento.T

    return pontos_cisalhados
