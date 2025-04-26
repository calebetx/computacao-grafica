import tkinter as tk

class Header:
    def __init__(self, parent, width, height=30, bg="#101010"):
        self.frame = tk.Frame(parent, bg=bg, width=width, height=height)
        self.frame.pack(side=tk.TOP, fill=tk.X)
        self.frame.pack_propagate(False)

        options = ["Pixel", "Reta", "Circunferência"]
        self.selected_option = tk.StringVar()
        self.option_menu = tk.OptionMenu(self.frame, self.selected_option, *options)
        self.option_menu.pack(side=tk.LEFT, padx=10)
