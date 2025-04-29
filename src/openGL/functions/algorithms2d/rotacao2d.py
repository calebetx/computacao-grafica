import numpy as np

def rotacao2d(pontos, angulo_graus):
    """
    Aplica rotação 2D a um array de pontos.

    Parâmetros:
    - pontos: lista ou np.array de forma (N, 2), com pontos [x, y]
    - angulo_graus: ângulo de rotação no sentido anti-horário (em graus)

    Retorna:
    - np.array com os pontos rotacionados
    """
    pontos = np.array(pontos)

    # Converte para radianos
    theta = np.radians(angulo_graus)

    # Coordenadas homogêneas
    pontos_h = np.hstack([pontos, np.ones((pontos.shape[0], 1))])

    # Matriz de rotação em torno da origem
    matriz_rotacao = np.array([
        [np.cos(theta), -np.sin(theta), 0],
        [np.sin(theta),  np.cos(theta), 0],
        [0, 0, 1]
    ])

    # Aplica rotação
    pontos_rotacionados = pontos_h @ matriz_rotacao.T

    return pontos_rotacionados[:, :2]