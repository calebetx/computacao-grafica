import tkinter as tk
from tkinter import ttk, messagebox
import numpy as np
from OpenGL.GL import *
from OpenGL.GLU import *
from pyopengltk import OpenGLFrame
import math

from algorithms3d.translacao3d import translacao3d
from algorithms3d.rotacao3d import rotacao3d
from algorithms3d.escala3d import escala3d
from algorithms3d.cisalhamento3d import cisalhamento3d
from drawCube import desenhar_eixos, desenhar_cubo, gerar_cubo_na_origem

from algorithms2d.reflexao2d import reflexao2d
from algorithms2d.escala2d import escala2d
from algorithms2d.rotacao2d import rotacao2d
from algorithms2d.translacao2d import translacao2d
from algorithms2d.cisalhamento2d import cisalhamento2d


def bresenham_geral(x0, y0, x1, y1):
    """Implementação do algoritmo de Bresenham que funciona para todos os 8 octantes."""
    pontos = []
    dx = x1 - x0
    dy = y1 - y0
    
    # Determina a direção do incremento (1 ou -1)
    sx = 1 if dx > 0 else -1
    sy = 1 if dy > 0 else -1
    
    dx = abs(dx)
    dy = abs(dy)
    
    # Caso para retas com inclinação "suave" (mais largas que altas)
    if dx > dy:
        err = dx / 2.0
        while x0 != x1:
            pontos.append((x0, y0))
            err -= dy
            if err < 0:
                y0 += sy
                err += dx
            x0 += sx
    # Caso para retas com inclinação "íngreme" (mais altas que largas)
    else:
        err = dy / 2.0
        while y0 != y1:
            pontos.append((x0, y0))
            err -= dx
            if err < 0:
                x0 += sx
                err += dy
            y0 += sy
            
    pontos.append((x0, y0)) #  o último 
    return pontos

def line_dda(x0, y0, x1, y1):
    """Implementação do algoritmo DDA que retorna uma lista de pontos."""
    pontos = []
    dx = x1 - x0
    dy = y1 - y0
    
    steps = max(abs(dx), abs(dy))
    
    if steps == 0:
        pontos.append((x0, y0))
        return pontos

    x_increment = dx / steps
    y_increment = dy / steps
    
    x, y = float(x0), float(y0)
    
    for _ in range(int(steps) + 1):
        pontos.append((round(x), round(y)))
        x += x_increment
        y += y_increment
        
    return pontos

def reflexao3d(vertices, plano):
    matriz_reflexao = np.identity(4)
    if plano == 'plano_xy': matriz_reflexao[2, 2] = -1
    elif plano == 'plano_yz': matriz_reflexao[0, 0] = -1
    elif plano == 'plano_xz': matriz_reflexao[1, 1] = -1
    else: return vertices
    vertices_homogeneos = np.c_[vertices, np.ones(vertices.shape[0])]
    return (vertices_homogeneos @ matriz_reflexao.T)[:, :3]

# --- Funções de desenho ---
def draw_line_2d(points):
    glBegin(GL_POINTS)
    for p in points:
        glVertex2f(p[0], p[1])
    glEnd()

def draw_square_2d(points):
    if len(points) != 4: return
    glBegin(GL_LINE_LOOP)
    for point in points:
        glVertex2f(point[0], point[1])
    glEnd()

# --- Classes de Canvas ---
class Canvas3D(OpenGLFrame):
    def __init__(self, master=None, **kwargs):
        super().__init__(master, **kwargs)
        lado = 2.0
        vertices_centrados = gerar_cubo_na_origem(lado)
        self.vertices_base = translacao3d(vertices_centrados, (lado / 2, lado / 2, lado / 2))
        
        self.transformacoes = {
            'translacao': (0.0, 0.0, 0.0), 'escala': (1.0, 1.0, 1.0), 'rotacao': (0.0, 0.0, 0.0),
            'cisalhamento': (0.0, 0.0, 0.0), 'reflexao': 'nenhuma'
        }

    def initgl(self):
        glEnable(GL_DEPTH_TEST); glClearColor(0.1, 0.1, 0.2, 1.0)
        glMatrixMode(GL_PROJECTION); glLoadIdentity()
        if self.winfo_height() > 0: gluPerspective(45, self.winfo_width() / self.winfo_height(), 0.1, 100.0)
        glMatrixMode(GL_MODELVIEW)
    def redraw(self):
        glClear(GL_COLOR_BUFFER_BIT | GL_DEPTH_BUFFER_BIT); glLoadIdentity()
        gluLookAt(7, 6, 7, 0, 0, 0, 0, 1, 0)
        desenhar_eixos()
        v = np.copy(self.vertices_base)
        plano_reflexao = self.transformacoes['reflexao']
        if plano_reflexao != 'nenhuma': v = reflexao3d(v, plano_reflexao)
        v = escala3d(v, self.transformacoes['escala'])
        sh_xy, sh_xz, sh_yz = self.transformacoes['cisalhamento']
        if sh_xy != 0.0 or sh_xz != 0.0 or sh_yz != 0.0: v = cisalhamento3d(v, sh_xy, sh_xz, sh_yz)
        ax, ay, az = self.transformacoes['rotacao']
        if ax != 0: v = rotacao3d(v, ax, 'x');
        if ay != 0: v = rotacao3d(v, ay, 'y');
        if az != 0: v = rotacao3d(v, az, 'z')
        v = translacao3d(v, self.transformacoes['translacao'])
        desenhar_cubo(v)
        glFlush()
    def set_transformacoes(self, novas_transformacoes):
        self.transformacoes = novas_transformacoes; self.tkExpose(None)
    def reset_transformacoes(self):
        self.transformacoes = {
            'translacao': (0.0, 0.0, 0.0), 'escala': (1.0, 1.0, 1.0), 'rotacao': (0.0, 0.0, 0.0),
            'cisalhamento': (0.0, 0.0, 0.0), 'reflexao': 'nenhuma'
        }
        self.tkExpose(None)

class Canvas2D(OpenGLFrame):
    def __init__(self, master=None, **kwargs):
        super().__init__(master, **kwargs)
        lado = 150.0
        self.pontos_originais = np.array([[0, 0], [0, lado], [lado, lado], [lado, 0]], dtype=float)
        self.pontos_atuais = np.copy(self.pontos_originais)
    def initgl(self): glClearColor(0.0, 0.0, 0.0, 1.0)
    def redraw(self):
        width, height = self.winfo_width(), self.winfo_height()
        glMatrixMode(GL_PROJECTION); glLoadIdentity()
        glOrtho(-width / 2, width / 2, -height / 2, height / 2, -1, 1)
        glMatrixMode(GL_MODELVIEW); glLoadIdentity()
        glClear(GL_COLOR_BUFFER_BIT | GL_DEPTH_BUFFER_BIT)
        glColor3f(0.5, 0.5, 0.5)
        if width > 0 and height > 0:
            glBegin(GL_LINES); glVertex2f(-width/2, 0); glVertex2f(width/2, 0); glEnd()
            glBegin(GL_LINES); glVertex2f(0, -height/2); glVertex2f(0, height/2); glEnd()
        glColor3f(0.0, 1.0, 1.0)
        draw_square_2d(self.pontos_atuais)
        glFlush()
    def aplicar_transformacao(self, func, *args):
        self.pontos_atuais = func(self.pontos_atuais, *args); self.tkExpose(None)
    def resetar(self):
        self.pontos_atuais = np.copy(self.pontos_originais); self.tkExpose(None)

# CLASSE CanvasRetas CORRIGIDA
class CanvasRetas(OpenGLFrame):
    def __init__(self, master=None, **kwargs):
        super().__init__(master, **kwargs)
        self.linhas = []
        
    def initgl(self):
        glClearColor(0.1, 0.1, 0.1, 1.0)
        glPointSize(2.0) # MOVIMENTEI PARA CÁ

    def redraw(self):
        width, height = self.winfo_width(), self.winfo_height()
        glMatrixMode(GL_PROJECTION); glLoadIdentity()
        glOrtho(-width / 2, width / 2, -height / 2, height / 2, -1, 1)
        glMatrixMode(GL_MODELVIEW); glLoadIdentity()
        glClear(GL_COLOR_BUFFER_BIT | GL_DEPTH_BUFFER_BIT)
        glColor3f(0.4, 0.4, 0.4)
        if width > 0 and height > 0:
            glBegin(GL_LINES); glVertex2f(-width/2, 0); glVertex2f(width/2, 0); glEnd()
            glBegin(GL_LINES); glVertex2f(0, -height/2); glVertex2f(0, height/2); glEnd()
        for linha in self.linhas:
            glColor3fv(linha['cor'])
            draw_line_2d(linha['pontos'])
        glFlush()
    def adicionar_linha(self, p1, p2, algoritmo, cor):
        if algoritmo == 'DDA':
            pontos = line_dda(p1[0], p1[1], p2[0], p2[1])
        else: # Bresenham
            pontos = bresenham_geral(p1[0], p1[1], p2[0], p2[1])
        self.linhas.append({'pontos': pontos, 'cor': cor})
        self.tkExpose(None)
    def limpar_linhas(self):
        self.linhas = []; self.tkExpose(None)

# --- Classe Principal da Aplicação ---
class App(tk.Tk):
    def __init__(self):
        super().__init__()
        self.title("Computação Gráfica: Transformações e Retas")
        self.geometry("1400x800")

        self.painel_esquerdo = ttk.Frame(self, width=350, padding=10)
        self.painel_esquerdo.pack(side=tk.LEFT, fill=tk.Y, padx=5, pady=5)
        
        self.notebook = ttk.Notebook(self)
        self.notebook.pack(side=tk.RIGHT, fill=tk.BOTH, expand=True, padx=5, pady=5)
        
        frame_3d = ttk.Frame(self.notebook)
        frame_2d = ttk.Frame(self.notebook)
        frame_retas = ttk.Frame(self.notebook) # NOVO
        self.notebook.add(frame_3d, text='Transformações 3D')
        self.notebook.add(frame_2d, text='Transformações 2D')
        self.notebook.add(frame_retas, text='Desenho de Retas') # NOVO
        
        self.canvas_3d = Canvas3D(frame_3d); self.canvas_3d.pack(fill=tk.BOTH, expand=True)
        self.canvas_2d = Canvas2D(frame_2d); self.canvas_2d.pack(fill=tk.BOTH, expand=True)
        self.canvas_retas = CanvasRetas(frame_retas); self.canvas_retas.pack(fill=tk.BOTH, expand=True) # NOVO
        
        self.controles_3d = ttk.Frame(self.painel_esquerdo)
        self.controles_2d = ttk.Frame(self.painel_esquerdo)
        self.controles_retas = ttk.Frame(self.painel_esquerdo) # NOVO
        
        self.criar_controles_3d()
        self.criar_controles_2d()
        self.criar_controles_retas() # NOVO
        
        self.notebook.bind("<<NotebookTabChanged>>", self.on_tab_changed)
        self.after(100, lambda: self.on_tab_changed(None))

    def on_tab_changed(self, event):
        tab_selecionada = self.notebook.tab(self.notebook.select(), "text")
        self.controles_3d.pack_forget(); self.controles_2d.pack_forget(); self.controles_retas.pack_forget()
        if tab_selecionada == 'Transformações 3D':
            self.controles_3d.pack(fill=tk.X); self.canvas_3d.tkExpose(None)
        elif tab_selecionada == 'Transformações 2D':
            self.controles_2d.pack(fill=tk.X); self.canvas_2d.tkExpose(None)
        elif tab_selecionada == 'Desenho de Retas': # NOVO
            self.controles_retas.pack(fill=tk.X); self.canvas_retas.tkExpose(None)

    def criar_controles_retas(self):
        self.entries_retas = {}
        frame = self.controles_retas
        
        ttk.Button(frame, text="Limpar Tela", command=self.canvas_retas.limpar_linhas).pack(pady=10, fill=tk.X)
        
        def _criar_entry_reta(parent, label, key, val):
            ttk.Label(parent, text=label).pack(side=tk.LEFT, padx=(0,5))
            e = ttk.Entry(parent, width=7); e.insert(0, val); e.pack(side=tk.LEFT, padx=(0,10))
            self.entries_retas[key] = e

        f_p1 = ttk.LabelFrame(frame, text="Ponto Inicial (P1)", padding=10)
        f_p1.pack(fill=tk.X, pady=5)
        _criar_entry_reta(f_p1, "X0:", "x0", "-100")
        _criar_entry_reta(f_p1, "Y0:", "y0", "-50")
        
        f_p2 = ttk.LabelFrame(frame, text="Ponto Final (P2)", padding=10)
        f_p2.pack(fill=tk.X, pady=5)
        _criar_entry_reta(f_p2, "X1:", "x1", "150")
        _criar_entry_reta(f_p2, "Y1:", "y1", "80")

        f_algo = ttk.LabelFrame(frame, text="Algoritmo", padding=10)
        f_algo.pack(fill=tk.X, pady=5)
        self.entries_retas['algoritmo'] = ttk.Combobox(f_algo, values=['Bresenham', 'DDA'], state="readonly")
        self.entries_retas['algoritmo'].set('Bresenham')
        self.entries_retas['algoritmo'].pack(fill=tk.X)

        ttk.Button(frame, text="Desenhar Reta", command=self.aplicar_desenho_reta).pack(pady=20, fill=tk.X)

    def aplicar_desenho_reta(self):
        try:
            x0 = int(self.entries_retas['x0'].get())
            y0 = int(self.entries_retas['y0'].get())
            x1 = int(self.entries_retas['x1'].get())
            y1 = int(self.entries_retas['y1'].get())
            algo = self.entries_retas['algoritmo'].get()
            cor = tuple(np.random.rand(3)) # Gera uma cor aleatória
            self.canvas_retas.adicionar_linha((x0,y0), (x1,y1), algo, cor)
        except ValueError:
            messagebox.showerror("Erro de Entrada", "As coordenadas das retas devem ser números inteiros.")

    def criar_controles_3d(self):
        self.entries_3d = {}
        frame = self.controles_3d
        def _criar_entry(parent, label, val):
            fr = ttk.Frame(parent); fr.pack(fill=tk.X, pady=2)
            ttk.Label(fr, text=label, width=8).pack(side=tk.LEFT)
            e = ttk.Entry(fr); e.pack(fill=tk.X, expand=True); e.insert(0, val)
            return e
        ttk.Button(frame, text="Resetar Cubo", command=self.resetar_3d).pack(pady=10, fill=tk.X)
        f_t = ttk.LabelFrame(frame, text="Translação", padding=10); f_t.pack(fill=tk.X, pady=5)
        self.entries_3d['tx'] = _criar_entry(f_t, "X:", "0.0"); self.entries_3d['ty'] = _criar_entry(f_t, "Y:", "0.0"); self.entries_3d['tz'] = _criar_entry(f_t, "Z:", "0.0")
        f_e = ttk.LabelFrame(frame, text="Escala", padding=10); f_e.pack(fill=tk.X, pady=5)
        self.entries_3d['sx'] = _criar_entry(f_e, "X:", "1.0"); self.entries_3d['sy'] = _criar_entry(f_e, "Y:", "1.0"); self.entries_3d['sz'] = _criar_entry(f_e, "Z:", "1.0")
        f_r = ttk.LabelFrame(frame, text="Rotação (Graus)", padding=10); f_r.pack(fill=tk.X, pady=5)
        self.entries_3d['rx'] = _criar_entry(f_r, "Eixo X:", "0.0"); self.entries_3d['ry'] = _criar_entry(f_r, "Eixo Y:", "0.0"); self.entries_3d['rz'] = _criar_entry(f_r, "Eixo Z:", "0.0")
        f_c = ttk.LabelFrame(frame, text="Cisalhamento", padding=10); f_c.pack(fill=tk.X, pady=5)
        self.entries_3d['sh_xy'] = _criar_entry(f_c, "XY:", "0.0"); self.entries_3d['sh_xz'] = _criar_entry(f_c, "XZ:", "0.0"); self.entries_3d['sh_yz'] = _criar_entry(f_c, "YZ:", "0.0")
        f_ref = ttk.LabelFrame(frame, text="Reflexão", padding=10); f_ref.pack(fill=tk.X, pady=5)
        self.entries_3d['reflexao_plano'] = ttk.Combobox(f_ref, values=['nenhuma', 'plano_xy', 'plano_yz', 'plano_xz'], state="readonly")
        self.entries_3d['reflexao_plano'].set('nenhuma'); self.entries_3d['reflexao_plano'].pack(fill=tk.X)
        ttk.Button(frame, text="Aplicar Transformações 3D", command=self.aplicar_3d).pack(pady=20, fill=tk.X)

    def criar_controles_2d(self):
        self.entries_2d = {}
        frame = self.controles_2d
        ttk.Button(frame, text="Resetar Quadrado", command=self.canvas_2d.resetar).pack(pady=10, fill=tk.X)
        
        def _criar_controles_linha(parent, text, key1, val1, key2, val2, cmd):
            fr = ttk.LabelFrame(parent, text=text, padding=10)
            fr.pack(fill=tk.X, pady=5)
            
            ttk.Label(fr, text=f"{key1.replace('t','d').replace('s','s').replace('sh','sh')}:").pack(side=tk.LEFT)
            e1 = ttk.Entry(fr, width=7)
            e1.insert(0, val1)
            e1.pack(side=tk.LEFT, fill=tk.X, expand=True, padx=(0, 5))
            self.entries_2d[key1] = e1
            
            ttk.Label(fr, text=f"{key2.replace('t','d').replace('s','s').replace('sh','sh')}:").pack(side=tk.LEFT)
            e2 = ttk.Entry(fr, width=7)
            e2.insert(0, val2)
            e2.pack(side=tk.LEFT, fill=tk.X, expand=True, padx=(0, 5))
            self.entries_2d[key2] = e2
            
            ttk.Button(fr, text="Aplicar", command=cmd).pack(side=tk.LEFT)

        _criar_controles_linha(frame, "Translação", 'tx', "10.0", 'ty', "10.0", self.aplicar_translacao_2d)
        _criar_controles_linha(frame, "Escala", 'sx', "1.2", 'sy', "1.2", self.aplicar_escala_2d)
        _criar_controles_linha(frame, "Cisalhamento", 'shx', "0.2", 'shy', "0.0", self.aplicar_cisalhamento_2d)

        f_r = ttk.LabelFrame(frame, text="Rotação", padding=10)
        f_r.pack(fill=tk.X, pady=5)
        ttk.Label(f_r, text="Ângulo:").pack(side=tk.LEFT)
        self.entries_2d['angulo'] = ttk.Entry(f_r, width=7)
        self.entries_2d['angulo'].insert(0, "15.0")
        self.entries_2d['angulo'].pack(side=tk.LEFT, fill=tk.X, expand=True, padx=(0, 5))
        ttk.Button(f_r, text="Aplicar", command=self.aplicar_rotacao_2d).pack(side=tk.LEFT)
        
        f_ref = ttk.LabelFrame(frame, text="Reflexão", padding=10)
        f_ref.pack(fill=tk.X, pady=5)
        self.entries_2d['reflexao_eixo'] = ttk.Combobox(f_ref, values=['x', 'y', 'origem', 'xy'], state="readonly")
        self.entries_2d['reflexao_eixo'].set('x')
        self.entries_2d['reflexao_eixo'].pack(side=tk.LEFT, fill=tk.X, expand=True, padx=(0, 5))
        ttk.Button(f_ref, text="Aplicar", command=self.aplicar_reflexao_2d).pack(side=tk.LEFT)

    def _get_float(self, entry_name):
        try: return float(self.entries_2d[entry_name].get())
        except (ValueError, KeyError): messagebox.showerror("Erro de Entrada", f"Por favor, insira um número válido no campo '{entry_name}'."); return None
    def aplicar_translacao_2d(self):
        dx, dy = self._get_float('tx'), self._get_float('ty')
        if dx is not None and dy is not None: self.canvas_2d.aplicar_transformacao(translacao2d, dx, dy)
    def aplicar_escala_2d(self):
        sx, sy = self._get_float('sx'), self._get_float('sy')
        if sx is not None and sy is not None: self.canvas_2d.aplicar_transformacao(escala2d, sx, sy)
    def aplicar_rotacao_2d(self):
        angulo = self._get_float('angulo')
        if angulo is not None: self.canvas_2d.aplicar_transformacao(rotacao2d, angulo)
    def aplicar_cisalhamento_2d(self):
        shx, shy = self._get_float('shx'), self._get_float('shy')
        if shx is not None and shy is not None: self.canvas_2d.aplicar_transformacao(cisalhamento2d, shx, shy)
    def aplicar_reflexao_2d(self):
        eixo = self.entries_2d['reflexao_eixo'].get(); self.canvas_2d.aplicar_transformacao(reflexao2d, eixo)
    def resetar_3d(self):
        self.canvas_3d.reset_transformacoes()
        for key, entry in self.entries_3d.items():
            if key in ['tx', 'ty', 'tz', 'rx', 'ry', 'rz', 'sh_xy', 'sh_xz', 'sh_yz']: entry.delete(0, tk.END); entry.insert(0, "0.0")
            elif key in ['sx', 'sy', 'sz']: entry.delete(0, tk.END); entry.insert(0, "1.0")
            elif key == 'reflexao_plano': entry.set('nenhuma')
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
        except ValueError: messagebox.showerror("Erro de Entrada", "Por favor, insira números válidos para todos os campos 3D.")
        except KeyError as e: messagebox.showerror("Erro de Programação", f"Chave de dicionário não encontrada: {e}. Verifique 'criar_controles_3d'.")

if __name__ == '__main__':
    app = App()
    app.mainloop()
