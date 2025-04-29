from openGL.draw_square import draw_square
from openGL.functions.algorithms2d.reflexao2d import reflexao2d
from openGL.functions.algorithms2d.escala2d import escala2d
from openGL.functions.algorithms2d.rotacao2d import rotacao2d
from openGL.functions.algorithms2d.translacao2d import translacao2d
from openGL.functions.algorithms2d.cisalhamento2d import cisalhamento2d

import time

class OpenGLManager:
    def __init__(self):
        pass

    def draw(self):
        square_points = [
        [0, 0],
        [0, 150],
        [150, 150],
        [150, 0]
        ]

        # square_points = cisalhamento2d(square_points, shx=0.5, shy=0.0)
        # square_points = translacao2d(square_points, 50, 50)
        square_points = rotacao2d(square_points, 45)
        # square_points = escala2d(square_points, 2, 2)
        # square_points = reflexao2d(square_points, tipo='x')

        draw_square(square_points)

        time.sleep(30)