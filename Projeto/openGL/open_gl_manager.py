from openGL.draw_triangle import draw_triangle
from openGL.draw_square import draw_square
from openGL.draw_circle import draw_circle

class OpenGLManager:
    def __init__(self):
        self.shape = None  

    def set_shape(self, shape_name):
        self.shape = shape_name

    def draw(self):
        if self.shape == "triangle":
            draw_triangle()
        elif self.shape == "square":
            draw_square()
        elif self.shape == "circle":
            draw_circle()
        else:
            pass  
