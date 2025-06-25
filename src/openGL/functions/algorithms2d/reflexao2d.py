import numpy as np

def reflexao2d(pontos, tipo):
    """
    Reflete um array de pontos 2D em relação a um eixo ou linha.

    Parâmetros:
    - pontos: lista ou np.array de forma (N, 2), com pontos [x, y]
    - tipo: tipo de reflexão ('x', 'y', 'origem', 'xy')

    Retorna:
    - np.array de pontos refletidos
    """
    pontos = np.array(pontos)

    # Converte para coordenadas homogêneas (x, y, 1)
    pontos_h = np.hstack([pontos, np.ones((pontos.shape[0], 1))])

    # Define matriz de reflexão
    if tipo == 'x':
        matriz = np.array([
            [1,  0, 0],
            [0, -1, 0],
            [0,  0, 1]
        ])
    elif tipo == 'y':
        matriz = np.array([
            [-1, 0, 0],
            [ 0, 1, 0],
            [ 0, 0, 1]
        ])
    elif tipo == 'origem':
        matriz = np.array([
            [-1, 0, 0],
            [ 0, -1, 0],
            [ 0, 0, 1]
        ])
    elif tipo == 'xy':  # reflexão na reta y = x
        matriz = np.array([
            [0, 1, 0],
            [1, 0, 0],
            [0, 0, 1]
        ])
    else:
        raise ValueError("Tipo de reflexão inválido. Use 'x', 'y', 'origem' ou 'xy'.")

    # Aplica a reflexão
    pontos_refletidos = pontos_h @ matriz.T

    # Retorna apenas x e y
    return pontos_refletidos[:, :2]
