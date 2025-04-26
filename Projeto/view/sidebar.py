import tkinter as tk

class Sidebar:
    def __init__(self, parent, width, height, content_area, bg="#303030"):
        self.content_area = content_area

        self.frame = tk.Frame(parent, bg=bg, width=width, height=height)
        self.frame.pack(side=tk.LEFT, fill=tk.Y)

        self.create_buttons()

    def create_buttons(self):
        # Triângulo
        triangle_button = tk.Button(self.frame, text="Triângulo", command=lambda: self.change_shape("triangle"))
        triangle_button.pack(pady=10, padx=10, fill=tk.X)

        # Quadrado
        square_button = tk.Button(self.frame, text="Quadrado", command=lambda: self.change_shape("square"))
        square_button.pack(pady=10, padx=10, fill=tk.X)

        # Circunferência
        circle_button = tk.Button(self.frame, text="Circunferência", command=lambda: self.change_shape("circle"))
        circle_button.pack(pady=10, padx=10, fill=tk.X)

    def change_shape(self, shape):
        self.content_area.opengl.set_shape(shape)
        self.content_area.opengl.event_generate("<Configure>")

