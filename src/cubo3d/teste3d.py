import tkinter as tk
from tkinter import ttk, messagebox
import numpy as np
from OpenGL.GL import *
from OpenGL.GLU import *
from pyopengltk import OpenGLFrame

# --- Supondo que seus arquivos de algoritmos estão em subpastas ---
from algorithms3d.translacao3d import translacao3d
from algorithms3d.rotacao3d import rotacao3d
from algorithms3d.escala3d import escala3d
from algorithms3d.reflexao3d import reflexao3d
from algorithms3d.cisalhamento3d import cisalhamento3d
from drawCube import desenhar_eixos, desenhar_cubo, gerar_cubo_na_origem

from algorithms2d.reflexao2d import reflexao2d
from algorithms2d.escala2d import escala2d
from algorithms2d.rotacao2d import rotacao2d
from algorithms2d.translacao2d import translacao2d
from algorithms2d.cisalhamento2d import cisalhamento2d

# --- Funções de desenho 2D (simuladas ou suas reais) ---
def draw_line_2d(x0, y0, x1, y1):
    """Desenha uma linha usando a cor definida pelo glColor."""
    glBegin(GL_LINES)
    glVertex2f(x0, y0)
    glVertex2f(x1, y1)
    glEnd()

def draw_square_2d(points):
    """Desenha um polígono fechado a partir de 4 pontos."""
    if len(points) != 4: return
    glBegin(GL_LINE_LOOP)
    for point in points:
        glVertex2f(point[0], point[1])
    glEnd()

# --- Classe para o Canvas 3D ---
class Canvas3D(OpenGLFrame):
    def __init__(self, master=None, **kwargs):
        super().__init__(master, **kwargs)
        lado = 2.0
        # Gera o cubo centrado e depois o move para o primeiro octante
        vertices_centrados = gerar_cubo_na_origem(lado)
        self.vertices_base = translacao3d(vertices_centrados, (lado / 2, lado / 2, lado / 2))
        
        self.transformacoes = {
            'translacao': (0.0, 0.0, 0.0), 'escala': (1.0, 1.0, 1.0), 'rotacao': (0.0, 0.0, 0.0),
            'cisalhamento': (0.0, 0.0, 0.0), 'reflexao': 'nenhuma'
        }

    def initgl(self):
        glEnable(GL_DEPTH_TEST)
        glClearColor(0.1, 0.1, 0.2, 1.0)
        glMatrixMode(GL_PROJECTION)
        glLoadIdentity()
        if self.winfo_height() > 0:
            gluPerspective(45, self.winfo_width() / self.winfo_height(), 0.1, 100.0)
        glMatrixMode(GL_MODELVIEW)

    def redraw(self):
        glClear(GL_COLOR_BUFFER_BIT | GL_DEPTH_BUFFER_BIT)
        glLoadIdentity()
        gluLookAt(7, 6, 7, 0, 0, 0, 0, 1, 0)
        desenhar_eixos()

        v = np.copy(self.vertices_base)
        
        # Ordem de transformação: Reflexão > Escala > Cisalhamento > Rotação > Translação
        plano_reflexao = self.transformacoes['reflexao']
        if plano_reflexao != 'nenhuma': v = reflexao3d(v, plano_reflexao)
        
        v = escala3d(v, self.transformacoes['escala'])
        
        sh_xy, sh_xz, sh_yz = self.transformacoes['cisalhamento']
        if sh_xy != 0.0 or sh_xz != 0.0 or sh_yz != 0.0: v = cisalhamento3d(v, sh_xy, sh_xz, sh_yz)
        
        ax, ay, az = self.transformacoes['rotacao']
        if ax != 0: v = rotacao3d(v, ax, 'x')
        if ay != 0: v = rotacao3d(v, ay, 'y')
        if az != 0: v = rotacao3d(v, az, 'z')
        
        v = translacao3d(v, self.transformacoes['translacao'])
        
        desenhar_cubo(v)
        glFlush()

    def set_transformacoes(self, novas_transformacoes):
        self.transformacoes = novas_transformacoes
        self.tkExpose(None)

# --- Classe para o Canvas 2D ---
class Canvas2D(OpenGLFrame):
    def __init__(self, master=None, **kwargs):
        super().__init__(master, **kwargs)
        lado = 150.0
        self.pontos_originais = np.array([[0, 0], [0, lado], [lado, lado], [lado, 0]], dtype=float)
        self.pontos_atuais = np.copy(self.pontos_originais)

    def initgl(self):
        glClearColor(0.0, 0.0, 0.0, 1.0)

    def redraw(self):
        width, height = self.winfo_width(), self.winfo_height()
        glMatrixMode(GL_PROJECTION); glLoadIdentity()
        glOrtho(-width / 2, width / 2, -height / 2, height / 2, -1, 1)
        glMatrixMode(GL_MODELVIEW); glLoadIdentity()
        
        glClear(GL_COLOR_BUFFER_BIT | GL_DEPTH_BUFFER_BIT)
        
        glColor3f(0.5, 0.5, 0.5)
        if width > 0 and height > 0:
            draw_line_2d(-width / 2, 0, width / 2, 0) # Eixo X
            draw_line_2d(0, -height / 2, 0, height / 2) # Eixo Y
            
        glColor3f(0.0, 1.0, 1.0)
        draw_square_2d(self.pontos_atuais)
        glFlush()

    def aplicar_transformacao(self, func, *args):
        self.pontos_atuais = func(self.pontos_atuais, *args)
        self.tkExpose(None)

    def resetar(self):
        self.pontos_atuais = np.copy(self.pontos_originais)
        self.tkExpose(None)

# --- Classe Principal da Aplicação ---
class App(tk.Tk):
    def __init__(self):
        super().__init__()
        self.title("Projeto de Computação Gráfica - Transformações 2D e 3D")
        self.geometry("1400x800")

        self.painel_esquerdo = ttk.Frame(self, width=350, padding=10)
        self.painel_esquerdo.pack(side=tk.LEFT, fill=tk.Y, padx=5, pady=5)
        
        self.notebook = ttk.Notebook(self)
        self.notebook.pack(side=tk.RIGHT, fill=tk.BOTH, expand=True, padx=5, pady=5)
        
        frame_3d = ttk.Frame(self.notebook)
        frame_2d = ttk.Frame(self.notebook)
        self.notebook.add(frame_3d, text='Transformações 3D')
        self.notebook.add(frame_2d, text='Transformações 2D')
        
        self.canvas_3d = Canvas3D(frame_3d)
        self.canvas_3d.pack(fill=tk.BOTH, expand=True)
        self.canvas_2d = Canvas2D(frame_2d)
        self.canvas_2d.pack(fill=tk.BOTH, expand=True)
        
        self.controles_3d = ttk.Frame(self.painel_esquerdo)
        self.controles_2d = ttk.Frame(self.painel_esquerdo)
        
        self.criar_controles_3d()
        self.criar_controles_2d()
        
        self.notebook.bind("<<NotebookTabChanged>>", self.on_tab_changed)
        self.after(100, lambda: self.on_tab_changed(None))

    def on_tab_changed(self, event):
        tab_selecionada = self.notebook.tab(self.notebook.select(), "text")
        if tab_selecionada == 'Transformações 3D':
            self.controles_2d.pack_forget()
            self.controles_3d.pack(fill=tk.X)
            self.canvas_3d.tkExpose(None)
        else:
            self.controles_3d.pack_forget()
            self.controles_2d.pack(fill=tk.X)
            self.canvas_2d.tkExpose(None)

    def criar_controles_3d(self):
        self.entries_3d = {}
        frame = self.controles_3d

        def _criar_entry(parent, label, val):
            fr = ttk.Frame(parent)
            fr.pack(fill=tk.X, pady=2)
            ttk.Label(fr, text=label, width=8).pack(side=tk.LEFT)
            e = ttk.Entry(fr)
            e.pack(fill=tk.X, expand=True)
            e.insert(0, val)
            return e

        f_t = ttk.LabelFrame(frame, text="Translação", padding=10)
        f_t.pack(fill=tk.X, pady=5)
        self.entries_3d['tx'] = _criar_entry(f_t, "X:", "0.0")
        self.entries_3d['ty'] = _criar_entry(f_t, "Y:", "0.0")
        self.entries_3d['tz'] = _criar_entry(f_t, "Z:", "0.0")

        f_e = ttk.LabelFrame(frame, text="Escala", padding=10)
        f_e.pack(fill=tk.X, pady=5)
        self.entries_3d['sx'] = _criar_entry(f_e, "X:", "1.0")
        self.entries_3d['sy'] = _criar_entry(f_e, "Y:", "1.0")
        self.entries_3d['sz'] = _criar_entry(f_e, "Z:", "1.0")

        f_r = ttk.LabelFrame(frame, text="Rotação (Graus)", padding=10)
        f_r.pack(fill=tk.X, pady=5)
        self.entries_3d['rx'] = _criar_entry(f_r, "Eixo X:", "0.0")
        self.entries_3d['ry'] = _criar_entry(f_r, "Eixo Y:", "0.0")
        self.entries_3d['rz'] = _criar_entry(f_r, "Eixo Z:", "0.0")

        f_c = ttk.LabelFrame(frame, text="Cisalhamento", padding=10)
        f_c.pack(fill=tk.X, pady=5)
        self.entries_3d['sh_xy'] = _criar_entry(f_c, "XY:", "0.0")
        self.entries_3d['sh_xz'] = _criar_entry(f_c, "XZ:", "0.0")
        self.entries_3d['sh_yz'] = _criar_entry(f_c, "YZ:", "0.0")
        
        f_ref = ttk.LabelFrame(frame, text="Reflexão", padding=10)
        f_ref.pack(fill=tk.X, pady=5)
        self.entries_3d['reflexao_plano'] = ttk.Combobox(f_ref, values=['nenhuma', 'plano_xy', 'plano_yz', 'plano_xz'], state="readonly")
        self.entries_3d['reflexao_plano'].set('nenhuma')
        self.entries_3d['reflexao_plano'].pack(fill=tk.X)
        
        ttk.Button(frame, text="Aplicar Transformações 3D", command=self.aplicar_3d).pack(pady=20, fill=tk.X)

    def criar_controles_2d(self):
        self.entries_2d = {}
        frame = self.controles_2d
        
        ttk.Button(frame, text="Resetar Quadrado", command=self.canvas_2d.resetar).pack(pady=10, fill=tk.X)
        
        f_t = ttk.LabelFrame(frame, text="Translação", padding=10)
        f_t.pack(fill=tk.X, pady=5)
        self.entries_2d['tx'] = ttk.Entry(f_t, width=7); self.entries_2d['tx'].insert(0, "10.0")
        self.entries_2d['ty'] = ttk.Entry(f_t, width=7); self.entries_2d['ty'].insert(0, "10.0")
        ttk.Label(f_t, text="dx:").pack(side=tk.LEFT); self.entries_2d['tx'].pack(side=tk.LEFT, fill=tk.X, expand=True, padx=2)
        ttk.Label(f_t, text="dy:").pack(side=tk.LEFT); self.entries_2d['ty'].pack(side=tk.LEFT, fill=tk.X, expand=True, padx=2)
        ttk.Button(f_t, text="Aplicar", command=self.aplicar_translacao_2d).pack(side=tk.RIGHT, padx=5)
        
        f_e = ttk.LabelFrame(frame, text="Escala", padding=10)
        f_e.pack(fill=tk.X, pady=5)
        self.entries_2d['sx'] = ttk.Entry(f_e, width=7); self.entries_2d['sx'].insert(0, "1.2")
        self.entries_2d['sy'] = ttk.Entry(f_e, width=7); self.entries_2d['sy'].insert(0, "1.2")
        ttk.Label(f_e, text="sx:").pack(side=tk.LEFT); self.entries_2d['sx'].pack(side=tk.LEFT, fill=tk.X, expand=True, padx=2)
        ttk.Label(f_e, text="sy:").pack(side=tk.LEFT); self.entries_2d['sy'].pack(side=tk.LEFT, fill=tk.X, expand=True, padx=2)
        ttk.Button(f_e, text="Aplicar", command=self.aplicar_escala_2d).pack(side=tk.RIGHT, padx=5)
        
        f_r = ttk.LabelFrame(frame, text="Rotação", padding=10)
        f_r.pack(fill=tk.X, pady=5)
        self.entries_2d['angulo'] = ttk.Entry(f_r, width=7); self.entries_2d['angulo'].insert(0, "15.0")
        ttk.Label(f_r, text="Ângulo:").pack(side=tk.LEFT); self.entries_2d['angulo'].pack(side=tk.LEFT, fill=tk.X, expand=True, padx=2)
        ttk.Button(f_r, text="Aplicar", command=self.aplicar_rotacao_2d).pack(side=tk.RIGHT, padx=5)
        
        f_c = ttk.LabelFrame(frame, text="Cisalhamento", padding=10)
        f_c.pack(fill=tk.X, pady=5)
        self.entries_2d['shx'] = ttk.Entry(f_c, width=7); self.entries_2d['shx'].insert(0, "0.2")
        self.entries_2d['shy'] = ttk.Entry(f_c, width=7); self.entries_2d['shy'].insert(0, "0.0")
        ttk.Label(f_c, text="shx:").pack(side=tk.LEFT); self.entries_2d['shx'].pack(side=tk.LEFT, fill=tk.X, expand=True, padx=2)
        ttk.Label(f_c, text="shy:").pack(side=tk.LEFT); self.entries_2d['shy'].pack(side=tk.LEFT, fill=tk.X, expand=True, padx=2)
        ttk.Button(f_c, text="Aplicar", command=self.aplicar_cisalhamento_2d).pack(side=tk.RIGHT, padx=5)
        
        f_ref = ttk.LabelFrame(frame, text="Reflexão", padding=10)
        f_ref.pack(fill=tk.X, pady=5)
        self.entries_2d['reflexao_eixo'] = ttk.Combobox(f_ref, values=['x', 'y', 'origem', 'xy'], state="readonly")
        self.entries_2d['reflexao_eixo'].set('x')
        self.entries_2d['reflexao_eixo'].pack(side=tk.LEFT, fill=tk.X, expand=True)
        ttk.Button(f_ref, text="Aplicar", command=self.aplicar_reflexao_2d).pack(side=tk.RIGHT, padx=5)

    def _get_float(self, entry_name):
        try:
            return float(self.entries_2d[entry_name].get())
        except (ValueError, KeyError):
            messagebox.showerror("Erro de Entrada", f"Por favor, insira um número válido no campo '{entry_name}'.")
            return None

    def aplicar_translacao_2d(self):
        dx, dy = self._get_float('tx'), self._get_float('ty')
        if dx is not None and dy is not None:
            self.canvas_2d.aplicar_transformacao(translacao2d, dx, dy)
            
    def aplicar_escala_2d(self):
        sx, sy = self._get_float('sx'), self._get_float('sy')
        if sx is not None and sy is not None:
            self.canvas_2d.aplicar_transformacao(escala2d, sx, sy)

    def aplicar_rotacao_2d(self):
        angulo = self._get_float('angulo')
        if angulo is not None:
            self.canvas_2d.aplicar_transformacao(rotacao2d, angulo)

    def aplicar_cisalhamento_2d(self):
        shx, shy = self._get_float('shx'), self._get_float('shy')
        if shx is not None and shy is not None:
            self.canvas_2d.aplicar_transformacao(cisalhamento2d, shx, shy)

    def aplicar_reflexao_2d(self):
        eixo = self.entries_2d['reflexao_eixo'].get()
        self.canvas_2d.aplicar_transformacao(reflexao2d, eixo)
        
    def aplicar_3d(self):
        try:
            transformacoes = {
                'translacao': (float(self.entries_3d['tx'].get()), float(self.entries_3d['ty'].get()), float(self.entries_3d['tz'].get())),
                'escala': (float(self.entries_3d['sx'].get()), float(self.entries_3d['sy'].get()), float(self.entries_3d['sz'].get())),
                'rotacao': (float(self.entries_3d['rx'].get()), float(self.entries_3d['ry'].get()), float(self.entries_3d['rz'].get())),
                'cisalhamento': (float(self.entries_3d['sh_xy'].get()), float(self.entries_3d['sh_xz'].get()), float(self.entries_3d['sh_yz'].get())),
                'reflexao': self.entries_3d['reflexao_plano'].get()
            }
            self.canvas_3d.set_transformacoes(transformacoes)
        except ValueError:
            messagebox.showerror("Erro de Entrada", "Por favor, insira números válidos para todos os campos 3D.")
        except KeyError as e:
            messagebox.showerror("Erro de Programação", f"Chave de dicionário não encontrada: {e}. Verifique 'criar_controles_3d'.")

if __name__ == '__main__':
    app = App()
    app.mainloop()

