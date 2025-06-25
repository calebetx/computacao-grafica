import numpy as np

def translacao2d(pontos, tx, ty):
    """
    Aplica translação 2D a um array de pontos.

    Parâmetros:
    - pontos: lista ou np.array de forma (N, 2), com pontos [x, y]
    - tx: deslocamento no eixo X
    - ty: deslocamento no eixo Y

    Retorna:
    - np.array com os pontos translacionados
    """
    pontos = np.array(pontos)

    # Aplica a translação a cada ponto
    pontos_translacionados = pontos + np.array([tx, ty])

    return pontos_translacionados
