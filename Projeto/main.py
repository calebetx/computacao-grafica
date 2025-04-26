from view.main_window import MainWindow
from view.header import Header
from view.sidebar import Sidebar
from view.content import Content
import tkinter as tk

if __name__ == "__main__":
    width = 1600
    height = 900

    app = MainWindow(width, height)

    # 1. Criar Header
    header = Header(app.root, width)

    # 2. Criar Main Frame (vai abrigar Sidebar + Content)
    main_frame = tk.Frame(app.root)
    main_frame.pack(fill=tk.BOTH, expand=True)

    # 3. Dentro do main_frame criar Sidebar e Content
    content = Content(main_frame, width * 0.75, height)
    sidebar = Sidebar(main_frame, width * 0.25, height, content)

    app.run()
