from openGL.draw_square import draw_square
from openGL.functions.algorithms2d.reflexao2d import reflexao2d

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

        square_points = reflexao2d(square_points, tipo='x')

        draw_square(square_points)