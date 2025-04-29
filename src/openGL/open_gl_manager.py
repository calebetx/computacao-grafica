from openGL.draw_square import draw_square

class OpenGLManager:
    def __init__(self):
        self.shape = "square"

    def set_shape(self, shape_name):
        self.shape = shape_name

    def draw(self):
        draw_square()