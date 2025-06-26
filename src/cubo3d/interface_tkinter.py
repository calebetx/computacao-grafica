import tkinter as tk
from tkinter import ttk

class ControleUI:
    def __init__(self, master):
        """Inicializa a interface de controle em uma janela Tkinter."""
        self.root = master
        self.root.title("Controles")
        # Posiciona a janela de controles à esquerda da tela
        self.root.geometry("300x600+50+50") 

        # Variáveis do Tkinter para armazenar os valores dos controles
        # Usar DoubleVar permite que os sliders atualizem os valores automaticamente
        self.translacao_x = tk.DoubleVar(value=0)
        self.translacao_y = tk.DoubleVar(value=0)
        self.translacao_z = tk.DoubleVar(value=0)

        self.escala_x = tk.DoubleVar(value=1)
        self.escala_y = tk.DoubleVar(value=1)
        self.escala_z = tk.DoubleVar(value=1)

        self.rotacao_x = tk.DoubleVar(value=0)
        self.rotacao_y = tk.DoubleVar(value=0)
        self.rotacao_z = tk.DoubleVar(value=0)

        # Frame principal
        frame = ttk.Frame(self.root, padding="10")
        frame.pack(fill=tk.BOTH, expand=True)

        # --- Controles de Translação ---
        transl_frame = ttk.LabelFrame(frame, text="Translação", padding="10")
        transl_frame.pack(fill=tk.X, pady=5)
        self._criar_slider(transl_frame, "X:", self.translacao_x, -5, 5)
        self._criar_slider(transl_frame, "Y:", self.translacao_y, -5, 5)
        self._criar_slider(transl_frame, "Z:", self.translacao_z, -5, 5)

        # --- Controles de Escala ---
        escala_frame = ttk.LabelFrame(frame, text="Escala", padding="10")
        escala_frame.pack(fill=tk.X, pady=5)
        self._criar_slider(escala_frame, "X:", self.escala_x, 0.1, 3)
        self._criar_slider(escala_frame, "Y:", self.escala_y, 0.1, 3)
        self._criar_slider(escala_frame, "Z:", self.escala_z, 0.1, 3)

        # --- Controles de Rotação ---
        rot_frame = ttk.LabelFrame(frame, text="Rotação (Graus)", padding="10")
        rot_frame.pack(fill=tk.X, pady=5)
        self._criar_slider(rot_frame, "Eixo X:", self.rotacao_x, -180, 180)
        self._criar_slider(rot_frame, "Eixo Y:", self.rotacao_y, -180, 180)
        self._criar_slider(rot_frame, "Eixo Z:", self.rotacao_z, -180, 180)
        
        # --- Botão de Reset ---
        reset_button = ttk.Button(frame, text="Resetar Transformações", command=self.resetar_valores)
        reset_button.pack(pady=20)


    def _criar_slider(self, parent, label, variable, from_, to):
        """Função auxiliar para criar um Label e um Slider."""
        row = ttk.Frame(parent)
        row.pack(fill=tk.X, pady=2)
        ttk.Label(row, text=label, width=6).pack(side=tk.LEFT)
        slider = ttk.Scale(row, from_=from_, to=to, orient=tk.HORIZONTAL, variable=variable)
        slider.pack(fill=tk.X, expand=True, padx=5)

    def resetar_valores(self):
        """Reseta todos os controles para seus valores iniciais."""
        self.translacao_x.set(0)
        self.translacao_y.set(0)
        self.translacao_z.set(0)
        self.escala_x.set(1)
        self.escala_y.set(1)
        self.escala_z.set(1)
        self.rotacao_x.set(0)
        self.rotacao_y.set(0)
        self.rotacao_z.set(0)

    def get_valores(self):
        """Retorna um dicionário com os valores atuais dos controles."""
        return {
            'translacao': (self.translacao_x.get(), self.translacao_y.get(), self.translacao_z.get()),
            'escala': (self.escala_x.get(), self.escala_y.get(), self.escala_z.get()),
            'rotacao': {
                'x': self.rotacao_x.get(),
                'y': self.rotacao_y.get(),
                'z': self.rotacao_z.get()
            }
        }