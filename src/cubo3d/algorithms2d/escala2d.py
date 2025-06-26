import numpy as np

def escala2d(pontos, sx=1.0, sy=1.0):
    """
    Aplica escala 2D a um array de pontos.

    Parâmetros:
    - pontos: lista ou np.array de forma (N, 2), com pontos [x, y]
    - sx: fator de escala no eixo X
    - sy: fator de escala no eixo Y

    Retorna:
    - np.array com os pontos escalados
    """
    pontos = np.array(pontos)

    # Adiciona coordenadas homogêneas
    pontos_h = np.hstack([pontos, np.ones((pontos.shape[0], 1))])

    # Matriz de escala homogênea 3x3
    matriz_escala = np.array([
        [sx,  0, 0],
        [ 0, sy, 0],
        [ 0,  0, 1]
    ])

    # Aplica transformação
    pontos_escalados = pontos_h @ matriz_escala.T

    return pontos_escalados[:, :2]  # retorna apenas x, y
