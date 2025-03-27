import tkinter as tk
from OpenGlScreen import OpenGLScreen  # Importando a classe OpenGLWidget

# Resolução de teste
width = 1000
height = 600
espaco_topo = 50
menuTopBarHeight = 30

backgroundColor = "#202020"
menuColor = "#303030"
menuTopBarColor = "#101010"

class TKinterMainScreen:    
    def __init__(self, root):
        self.root = root
        self.mainRoot()
        self.menuTopBar()
        self.menuBar()

        self.main_frame = tk.Frame(self.root, bg=backgroundColor)
        self.main_frame.pack(fill=tk.BOTH, expand=tk.YES)
        
        self.openGLRoot()

    def openGLRoot(self):
        self.opengl_frame = OpenGLScreen(self.main_frame, width=width * 0.75, height=height - espaco_topo * 2)
        self.opengl_frame.place(x=int(width * 0.25), y=espaco_topo)
        self.opengl_frame.pack(side=tk.RIGHT)

    def mainRoot(self):
        self.root.title("Computação Gráfica")
        self.root.geometry(f"{width}x{height}")

    def menuBar(self):
        self.menuBar = tk.Frame(self.root, bg=menuColor, width = width * 0.25, height = height)
        self.menuBar.pack(side=tk.LEFT)

    def menuTopBar(self):
        self.menuTopBar = tk.Frame(self.root, bg=menuTopBarColor, width = width, height = menuTopBarHeight)
        self.menuTopBar.pack(side=tk.TOP)

        options = ["Pixel", "Reta", "Circunferência"]
        self.selected_option = tk.StringVar()

        self.option_menu = tk.OptionMenu(self.menuTopBar, self.selected_option, *options)
        self.option_menu.place(x = width * 0.01)
        self.option_menu.config(bg=menuTopBarColor, fg = "lightgray")

    def run(self):
        """Inicia o loop principal do Tkinter"""
        self.root.mainloop()


# Execução principal
if __name__ == "__main__":
    root = tk.Tk()
    tkinterMain = TKinterMainScreen(root)
    tkinterMain.run()
