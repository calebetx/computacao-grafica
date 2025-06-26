import numpy as np

def rotacao2d(pontos, angulo_graus):
    pontos = np.array(pontos)

    # Calcula o centro
    centro = pontos.mean(axis=0)

    # Converte ângulo para radianos
    theta = np.radians(angulo_graus)

    # Matriz de rotação 2x2
    matriz_rotacao = np.array([
        [np.cos(theta), -np.sin(theta)],
        [np.sin(theta),  np.cos(theta)]
    ])

    # Translada para a origem
    pontos_transladados = pontos - centro

    # Aplica a rotação
    pontos_rotacionados = pontos_transladados @ matriz_rotacao.T

    # Volta para a posição original
    pontos_final = pontos_rotacionados + centro

    # print(pontos_final)
    return pontos_final
