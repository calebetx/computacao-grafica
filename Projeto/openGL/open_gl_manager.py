from openGL.draw_triangle import draw_triangle
from openGL.draw_square import draw_square
from openGL.draw_circle import draw_circle

class OpenGLManager:
    def __init__(self):
        self.shape = "circle"

    def set_shape(self, shape_name):
        self.shape = shape_name

    def draw(self):
        if self.shape == "circle":
            from openGL.draw_circle import draw_circle
            draw_circle()
        elif self.shape == "square":
            from openGL.draw_square import draw_square
            draw_square()
        elif self.shape == "triangle":
            from openGL.draw_triangle import draw_triangle
            draw_triangle()
