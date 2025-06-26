# dentro de algorithms3d/escala3d.py
import numpy as np

def escala3d(vertices, fatores):
    sx, sy, sz = fatores
    matriz_escala = np.array([
        [sx, 0,  0,  0],
        [0,  sy, 0,  0],
        [0,  0,  sz, 0],
        [0,  0,  0,  1]
    ])
    # Adiciona a coordenada homogênea (w=1)
    vertices_homogeneos = np.c_[vertices, np.ones(vertices.shape[0])]
    # Aplica a transformação
    vertices_transformados = vertices_homogeneos @ matriz_escala.T
    # Remove a coordenada homogênea
    return vertices_transformados[:, :3]