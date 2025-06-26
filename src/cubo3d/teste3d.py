import tkinter as tk
from tkinter import ttk, messagebox, filedialog
import numpy as np
from OpenGL.GL import *
from OpenGL.GLU import *
from pyopengltk import OpenGLFrame
import math
from PIL import Image

# --- Módulos de algoritmos (simulados para o exemplo ser autônomo) ---
# Em seu projeto real, você deve importar seus próprios arquivos.
def translacao3d(vertices, t): return vertices + np.array(t)
def escala3d(vertices, s): 
    centro = vertices.mean(axis=0)
    return (vertices - centro) * np.array(s) + centro
def rotacao3d(vertices, angulo, eixo): 
    # Implementação simplificada para o exemplo funcionar
    rad = np.radians(angulo)
    c, s = np.cos(rad), np.sin(rad)
    if eixo == 'x':
        matriz_rotacao = np.array([[1, 0, 0], [0, c, -s], [0, s, c]])
    elif eixo == 'y':
        matriz_rotacao = np.array([[c, 0, s], [0, 1, 0], [-s, 0, c]])
    elif eixo == 'z':
        matriz_rotacao = np.array([[c, -s, 0], [s, c, 0], [0, 0, 1]])
    else:
        return vertices
    centro = vertices.mean(axis=0)
    return (vertices - centro) @ matriz_rotacao.T + centro
def cisalhamento3d(vertices, xy, xz, yz): return vertices
def desenhar_eixos():
    glBegin(GL_LINES)
    glColor3f(1.0, 0.0, 0.0); glVertex3f(-10, 0, 0); glVertex3f(10, 0, 0)
    glColor3f(0.0, 1.0, 0.0); glVertex3f(0, -10, 0); glVertex3f(0, 10, 0)
    glColor3f(0.0, 0.0, 1.0); glVertex3f(0, 0, -10); glVertex3f(0, 0, 10)
    glEnd()
def gerar_cubo_na_origem(lado):
    m = lado / 2
    return np.array([[-m,-m,-m], [m,-m,-m], [m,m,-m], [-m,m,-m], [-m,-m,m], [m,-m,m], [m,m,m], [-m,m,m]])
def desenhar_cubo(vertices):
    arestas = [(0,1), (1,2), (2,3), (3,0), (4,5), (5,6), (6,7), (7,4), (0,4), (1,5), (2,6), (3,7)]
    glColor3f(1.0, 1.0, 0.0); glBegin(GL_LINES)
    for aresta in arestas:
        for vertice in aresta: glVertex3fv(vertices[vertice])
    glEnd()
def reflexao2d(pontos, eixo):
    if eixo == 'x': matriz = np.array([[1, 0], [0, -1]])
    elif eixo == 'y': matriz = np.array([[-1, 0], [0, 1]])
    elif eixo == 'origem': matriz = np.array([[-1, 0], [0, -1]])
    else: matriz = np.array([[0, 1], [1, 0]]) # reta y=x
    centro = pontos.mean(axis=0)
    return (pontos - centro) @ matriz + centro
def escala2d(pontos, sx, sy):
    centro = pontos.mean(axis=0)
    return (pontos - centro) * np.array([sx, sy]) + centro
def rotacao2d(pontos, angulo):
    rad = np.radians(angulo); c, s = np.cos(rad), np.sin(rad)
    matriz = np.array([[c, -s], [s, c]])
    centro = pontos.mean(axis=0)
    return (pontos - centro) @ matriz.T + centro
def translacao2d(pontos, dx, dy): return pontos + np.array([dx, dy])
def cisalhamento2d(pontos, shx, shy):
    matriz = np.array([[1, shy], [shx, 1]])
    return pontos @ matriz
# --- Fim dos Módulos Simulados ---

def bresenham_geral(x0, y0, x1, y1):
    pontos = []; dx = x1 - x0; dy = y1 - y0; sx = 1 if dx > 0 else -1; sy = 1 if dy > 0 else -1
    dx = abs(dx); dy = abs(dy)
    if dx > dy:
        err = dx / 2.0
        while x0 != x1:
            pontos.append((x0, y0)); err -= dy
            if err < 0: y0 += sy; err += dx
            x0 += sx
    else:
        err = dy / 2.0
        while y0 != y1:
            pontos.append((x0, y0)); err -= dx
            if err < 0: x0 += sx; err += dy
            y0 += sy
    pontos.append((x0, y0)); return pontos

def line_dda(x0, y0, x1, y1):
    pontos = []; dx = x1 - x0; dy = y1 - y0; steps = max(abs(dx), abs(dy))
    if steps == 0: pontos.append((x0, y0)); return pontos
    x_inc = dx / steps; y_inc = dy / steps; x, y = float(x0), float(y0)
    for _ in range(int(steps) + 1):
        pontos.append((round(x), round(y))); x += x_inc; y += y_inc
    return pontos

def reflexao3d(vertices, plano):
    matriz_reflexao = np.identity(4)
    if plano == 'plano_xy': matriz_reflexao[2, 2] = -1
    elif plano == 'plano_yz': matriz_reflexao[0, 0] = -1
    elif plano == 'plano_xz': matriz_reflexao[1, 1] = -1
    else: return vertices
    v_homogeneos = np.c_[vertices, np.ones(vertices.shape[0])]
    return (v_homogeneos @ matriz_reflexao.T)[:, :3]

def draw_line_2d(points):
    glBegin(GL_POINTS);
    for p in points: glVertex2f(p[0], p[1])
    glEnd()

def draw_square_2d(points):
    if len(points) != 4: return
    glBegin(GL_LINE_LOOP)
    for point in points: glVertex2f(point[0], point[1])
    glEnd()

class Canvas3D(OpenGLFrame):
    def __init__(self, master=None, **kwargs):
        super().__init__(master, **kwargs)
        lado = 2.0
        v_centrados = gerar_cubo_na_origem(lado)
        self.vertices_base = translacao3d(v_centrados, (lado / 2, lado / 2, lado / 2))
        self.transformacoes = { 'translacao': (0,0,0), 'escala': (1,1,1), 'rotacao': (0,0,0), 'cisalhamento': (0,0,0), 'reflexao': 'nenhuma' }
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
        if sh_xy != 0 or sh_xz != 0 or sh_yz != 0: v = cisalhamento3d(v, sh_xy, sh_xz, sh_yz)
        ax, ay, az = self.transformacoes['rotacao']
        if ax != 0: v = rotacao3d(v, ax, 'x');
        if ay != 0: v = rotacao3d(v, ay, 'y');
        if az != 0: v = rotacao3d(v, az, 'z')
        v = translacao3d(v, self.transformacoes['translacao'])
        desenhar_cubo(v)
        glFlush()
    def set_transformacoes(self, t): self.transformacoes = t; self.tkExpose(None)
    def reset_transformacoes(self):
        self.transformacoes = { 'translacao': (0,0,0), 'escala': (1,1,1), 'rotacao': (0,0,0), 'cisalhamento': (0,0,0), 'reflexao': 'nenhuma' }
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
        glMatrixMode(GL_PROJECTION); glLoadIdentity(); glOrtho(-width/2, width/2, -height/2, height/2, -1, 1)
        glMatrixMode(GL_MODELVIEW); glLoadIdentity()
        glClear(GL_COLOR_BUFFER_BIT | GL_DEPTH_BUFFER_BIT); glColor3f(0.5, 0.5, 0.5)
        if width > 0 and height > 0:
            glBegin(GL_LINES); glVertex2f(-width/2, 0); glVertex2f(width/2, 0); glEnd()
            glBegin(GL_LINES); glVertex2f(0, -height/2); glVertex2f(0, height/2); glEnd()
        glColor3f(0.0, 1.0, 1.0); draw_square_2d(self.pontos_atuais)
        glFlush()
    def aplicar_transformacao(self, func, *args): self.pontos_atuais = func(self.pontos_atuais, *args); self.tkExpose(None)
    def resetar(self): self.pontos_atuais = np.copy(self.pontos_originais); self.tkExpose(None)

class CanvasRetas(OpenGLFrame):
    def __init__(self, master=None, **kwargs):
        super().__init__(master, **kwargs)
        self.linhas = []; self.clipping_enabled = tk.BooleanVar(value=False)
        self.clipping_rect = {'xmin':-200, 'ymin':-150, 'xmax':200, 'ymax':150}
        self.INSIDE, self.LEFT, self.RIGHT, self.BOTTOM, self.TOP = 0, 1, 2, 4, 8
    def initgl(self): glClearColor(0.1, 0.1, 0.1, 1.0); glPointSize(2.0)
    def redraw(self):
        width, height = self.winfo_width(), self.winfo_height()
        glMatrixMode(GL_PROJECTION); glLoadIdentity(); glOrtho(-width/2, width/2, -height/2, height/2, -1, 1)
        glMatrixMode(GL_MODELVIEW); glLoadIdentity()
        glClear(GL_COLOR_BUFFER_BIT | GL_DEPTH_BUFFER_BIT); glColor3f(0.4, 0.4, 0.4)
        if width > 0 and height > 0:
            glBegin(GL_LINES); glVertex2f(-width/2, 0); glVertex2f(width/2, 0); glEnd()
            glBegin(GL_LINES); glVertex2f(0, -height/2); glVertex2f(0, height/2); glEnd()
        if self.clipping_enabled.get():
            glColor3f(0.3, 0.3, 0.3); glBegin(GL_LINE_LOOP)
            glVertex2f(self.clipping_rect['xmin'], self.clipping_rect['ymin']); glVertex2f(self.clipping_rect['xmax'], self.clipping_rect['ymin'])
            glVertex2f(self.clipping_rect['xmax'], self.clipping_rect['ymax']); glVertex2f(self.clipping_rect['xmin'], self.clipping_rect['ymax'])
            glEnd()
        for linha in self.linhas:
            if 'pontos_originais' in linha: glColor3f(0.2, 0.2, 0.2); draw_line_2d(linha['pontos_originais'])
            glColor3fv(linha['cor']); draw_line_2d(linha['pontos'])
        glFlush()
    def adicionar_linha(self, p1_orig, p2_orig, algoritmo, cor):
        p1 = list(p1_orig); p2 = list(p2_orig); linha_info = {}
        if self.clipping_enabled.get():
            linha_info['pontos_originais'] = bresenham_geral(p1[0], p1[1], p2[0], p2[1])
            clipped_line = self.cohen_sutherland_clip(p1[0], p1[1], p2[0], p2[1])
            if clipped_line: p1, p2 = [clipped_line[0], clipped_line[1]], [clipped_line[2], clipped_line[3]]
            else: return
        pontos = line_dda(round(p1[0]), round(p1[1]), round(p2[0]), round(p2[1])) if algoritmo == 'DDA' else bresenham_geral(round(p1[0]), round(p1[1]), round(p2[0]), round(p2[1]))
        linha_info['pontos'] = pontos; linha_info['cor'] = cor; self.linhas.append(linha_info); self.tkExpose(None)
    def limpar_linhas(self): self.linhas = []; self.tkExpose(None)
    def set_clipping_info(self, enabled, rect): self.clipping_enabled.set(enabled); self.clipping_rect = rect; self.tkExpose(None)
    def _get_region_code(self, x, y):
        code = self.INSIDE
        if x < self.clipping_rect['xmin']: code |= self.LEFT
        elif x > self.clipping_rect['xmax']: code |= self.RIGHT
        if y < self.clipping_rect['ymin']: code |= self.BOTTOM
        elif y > self.clipping_rect['ymax']: code |= self.TOP
        return code
    def cohen_sutherland_clip(self, x1, y1, x2, y2):
        code1, code2, accept = self._get_region_code(x1, y1), self._get_region_code(x2, y2), False
        while True:
            if code1 == 0 and code2 == 0: accept = True; break
            elif (code1 & code2) != 0: break
            else:
                x, y = 0, 0; code_out = code1 if code1 != 0 else code2
                if y1 == y2: y_factor = float('inf')
                else: y_factor = (x2 - x1) / (y2 - y1)
                if x1 == x2: x_factor = float('inf')
                else: x_factor = (y2 - y1) / (x2 - x1)
                if code_out & self.TOP: x = x1 + y_factor * (self.clipping_rect['ymax']-y1); y = self.clipping_rect['ymax']
                elif code_out & self.BOTTOM: x = x1 + y_factor * (self.clipping_rect['ymin']-y1); y = self.clipping_rect['ymin']
                elif code_out & self.RIGHT: y = y1 + x_factor * (self.clipping_rect['xmax']-x1); x = self.clipping_rect['xmax']
                elif code_out & self.LEFT: y = y1 + x_factor * (self.clipping_rect['xmin']-x1); x = self.clipping_rect['xmin']
                if code_out == code1: x1, y1 = x, y; code1 = self._get_region_code(x1, y1)
                else: x2, y2 = x, y; code2 = self._get_region_code(x2, y2)
        if accept: return [x1, y1, x2, y2]
        return None

class CanvasImagem(OpenGLFrame):
    def __init__(self, master=None, **kwargs):
        super().__init__(master, **kwargs)
        self.pontos = []; self.pontos_originais = []
    def initgl(self):
        glClearColor(0.1, 0.1, 0.1, 1.0); glMatrixMode(GL_PROJECTION); glLoadIdentity()
        gluOrtho2D(-400, 400, -300, 300); glMatrixMode(GL_MODELVIEW)
    def redraw(self):
        glClear(GL_COLOR_BUFFER_BIT); glLoadIdentity()
        self.desenhar_plano(); self.desenhar_pontos(); glFlush()
    def carregar_imagem(self):
        caminho = filedialog.askopenfilename(filetypes=[("Imagens", "*.png *.jpg *.bmp")])
        if not caminho: return False
        try:
            imagem = Image.open(caminho).convert("1"); matriz = np.array(imagem)
            h, w = matriz.shape; escala = 0.5 # AJUSTE PARA IMAGEM MENOR
            self.pontos = [[(x - w / 2) * escala, (h / 2 - y) * escala] for y in range(h) for x in range(w) if matriz[y, x] == 0]
            self.pontos_originais = [p[:] for p in self.pontos]
            self.tkExpose(None); return True
        except Exception as e:
            messagebox.showerror("Erro ao Carregar", f"Não foi possível carregar a imagem.\nErro: {e}"); return False
    def aplicar_matriz(self, matriz):
        if not self.pontos: return
        pontos_homogeneos = np.c_[self.pontos, np.ones(len(self.pontos))]
        pontos_transformados = pontos_homogeneos @ matriz.T
        self.pontos = pontos_transformados[:, :2].tolist()
        self.tkExpose(None)
    def ponto_proximo_origem(self):
        if not self.pontos: return 0, 0
        return min(self.pontos, key=lambda p: p[0]**2 + p[1]**2)
    def aplicar_translacao(self, dx, dy):
        self.aplicar_matriz(np.array([[1, 0, dx], [0, 1, dy], [0, 0, 1]]))
    def aplicar_escala(self, sx, sy):
        px, py = self.ponto_proximo_origem()
        t1 = np.array([[1, 0, -px], [0, 1, -py], [0, 0, 1]]); s = np.array([[sx, 0, 0], [0, sy, 0], [0, 0, 1]])
        t2 = np.array([[1, 0, px], [0, 1, py], [0, 0, 1]]); matriz = t2 @ s @ t1; self.aplicar_matriz(matriz)
    def aplicar_rotacao(self, angulo):
        px, py = self.ponto_proximo_origem(); rad = math.radians(angulo); c, s = math.cos(rad), math.sin(rad)
        t1 = np.array([[1, 0, -px], [0, 1, -py], [0, 0, 1]]); r = np.array([[c, -s, 0], [s, c, 0], [0, 0, 1]])
        t2 = np.array([[1, 0, px], [0, 1, py], [0, 0, 1]]); matriz = t2 @ r @ t1; self.aplicar_matriz(matriz)
    def aplicar_cisalhamento(self, shx, shy):
        self.aplicar_matriz(np.array([[1, shx, 0], [shy, 1, 0], [0, 0, 1]]))
    def aplicar_reflexao(self, eixo):
        e = eixo.lower()
        if e == 'x': matriz = np.array([[1, 0, 0], [0, -1, 0], [0, 0, 1]])
        elif e == 'y': matriz = np.array([[-1, 0, 0], [0, 1, 0], [0, 0, 1]])
        elif e == 'origem': matriz = np.array([[-1, 0, 0], [0, -1, 0], [0, 0, 1]])
        elif e == 'reta y=x': matriz = np.array([[0, 1, 0], [1, 0, 0], [0, 0, 1]])
        else: return
        self.aplicar_matriz(matriz)
    def desenhar_plano(self):
        glColor3f(0.4, 0.4, 0.4); glBegin(GL_LINES)
        glVertex2f(-400, 0); glVertex2f(400, 0); glVertex2f(0, -300); glVertex2f(0, 300)
        glEnd()
    def desenhar_pontos(self):
        if not self.pontos: return
        glColor3f(0.0, 1.0, 1.0); glPointSize(1.0); glBegin(GL_POINTS) # Tamanho do ponto ajustado
        for x, y in self.pontos: glVertex2f(x, y)
        glEnd()
    def resetar(self): self.pontos = [p[:] for p in self.pontos_originais]; self.tkExpose(None)

class App(tk.Tk):
    def __init__(self):
        super().__init__(); self.title("Computação Gráfica: Projeto Final"); self.geometry("1400x800")
        self.painel_esquerdo = ttk.Frame(self, width=350, padding=10); self.painel_esquerdo.pack(side=tk.LEFT, fill=tk.Y, padx=5, pady=5)
        self.notebook = ttk.Notebook(self); self.notebook.pack(side=tk.RIGHT, fill=tk.BOTH, expand=True, padx=5, pady=5)
        
        frame_3d = ttk.Frame(self.notebook); frame_2d = ttk.Frame(self.notebook)
        frame_retas = ttk.Frame(self.notebook); frame_imagem = ttk.Frame(self.notebook)
        self.notebook.add(frame_3d, text='Transformações 3D'); self.notebook.add(frame_2d, text='Transformações 2D')
        self.notebook.add(frame_retas, text='Desenho de Retas'); self.notebook.add(frame_imagem, text='Imagem')
        
        self.canvas_3d = Canvas3D(frame_3d); self.canvas_3d.pack(fill=tk.BOTH, expand=True)
        self.canvas_2d = Canvas2D(frame_2d); self.canvas_2d.pack(fill=tk.BOTH, expand=True)
        self.canvas_retas = CanvasRetas(frame_retas); self.canvas_retas.pack(fill=tk.BOTH, expand=True)
        self.canvas_imagem = CanvasImagem(frame_imagem); self.canvas_imagem.pack(fill=tk.BOTH, expand=True)
        
        self.controles_3d = ttk.Frame(self.painel_esquerdo); self.controles_2d = ttk.Frame(self.painel_esquerdo)
        self.controles_retas = ttk.Frame(self.painel_esquerdo); self.controles_imagem = ttk.Frame(self.painel_esquerdo)
        
        self.criar_controles_3d(); self.criar_controles_2d(); self.criar_controles_retas(); self.criar_controles_imagem()
        self.notebook.bind("<<NotebookTabChanged>>", self.on_tab_changed)
        self.after(100, lambda: self.on_tab_changed(None))

    def on_tab_changed(self, event):
        for w in self.painel_esquerdo.winfo_children(): w.pack_forget()
        tab_selecionada = self.notebook.tab(self.notebook.select(), "text")
        if tab_selecionada == 'Transformações 3D': self.controles_3d.pack(fill=tk.X); self.canvas_3d.tkExpose(None)
        elif tab_selecionada == 'Transformações 2D': self.controles_2d.pack(fill=tk.X); self.canvas_2d.tkExpose(None)
        elif tab_selecionada == 'Desenho de Retas': self.controles_retas.pack(fill=tk.X); self.canvas_retas.tkExpose(None)
        elif tab_selecionada == 'Imagem': self.controles_imagem.pack(fill=tk.X); self.canvas_imagem.tkExpose(None)

    def criar_controles_imagem(self):
        self.entries_imagem = {}
        frame = self.controles_imagem
        ttk.Button(frame, text="Carregar Imagem", command=self.carregar_imagem_ui).pack(pady=10, fill=tk.X)
        ttk.Button(frame, text="Resetar Imagem", command=self.resetar_imagem_ui).pack(pady=(0,10), fill=tk.X)
        def _criar_controles_linha(parent, text, key1, val1, key2, val2, cmd):
            fr = ttk.LabelFrame(parent, text=text, padding=10); fr.pack(fill=tk.X, pady=5)
            ttk.Label(fr, text=f"{key1.replace('t','d').replace('s','').replace('sh','')}:").pack(side=tk.LEFT)
            e1 = ttk.Entry(fr, width=7); e1.insert(0, val1); e1.pack(side=tk.LEFT, fill=tk.X, expand=True, padx=(0, 5)); self.entries_imagem[key1] = e1
            if key2:
                ttk.Label(fr, text=f"{key2.replace('t','d').replace('s','').replace('sh','')}:").pack(side=tk.LEFT)
                e2 = ttk.Entry(fr, width=7); e2.insert(0, val2); e2.pack(side=tk.LEFT, fill=tk.X, expand=True, padx=(0, 5)); self.entries_imagem[key2] = e2
            ttk.Button(fr, text="Aplicar", command=cmd).pack(side=tk.LEFT)
        _criar_controles_linha(frame, "Translação", 'tx', "20.0", 'ty', "20.0", self.aplicar_translacao_imagem)
        _criar_controles_linha(frame, "Escala", 'sx', "1.2", 'sy', "1.2", self.aplicar_escala_imagem)
        _criar_controles_linha(frame, "Cisalhamento", 'shx', "0.2", 'shy', "0.1", self.aplicar_cisalhamento_imagem)
        _criar_controles_linha(frame, "Rotação", 'angulo', "15.0", None, None, self.aplicar_rotacao_imagem)
        f_ref = ttk.LabelFrame(frame, text="Reflexão", padding=10); f_ref.pack(fill=tk.X, pady=5)
        self.entries_imagem['reflexao_eixo'] = ttk.Combobox(f_ref, values=['x', 'y', 'origem', 'reta y=x'], state="readonly")
        self.entries_imagem['reflexao_eixo'].set('x'); self.entries_imagem['reflexao_eixo'].pack(side=tk.LEFT, fill=tk.X, expand=True, padx=(0, 5))
        ttk.Button(f_ref, text="Aplicar", command=self.aplicar_reflexao_imagem).pack(side=tk.LEFT)
        f_hist = ttk.LabelFrame(frame, text="Histórico de Transformações", padding=10); f_hist.pack(fill=tk.BOTH, expand=True, pady=10)
        self.hist_imagem_texto = tk.Text(f_hist, height=10, state='disabled'); self.hist_imagem_texto.pack(fill=tk.BOTH, expand=True)
    def _add_hist(self, text):
        self.hist_imagem_texto.config(state='normal')
        if self.hist_imagem_texto.get("1.0", "end-1c"): self.hist_imagem_texto.insert(tk.END, f"\n{text}")
        else: self.hist_imagem_texto.insert(tk.END, text)
        self.hist_imagem_texto.config(state='disabled')
    def carregar_imagem_ui(self):
        if self.canvas_imagem.carregar_imagem():
            self.hist_imagem_texto.config(state='normal'); self.hist_imagem_texto.delete(1.0, tk.END)
            self.hist_imagem_texto.insert(tk.END, "Imagem carregada."); self.hist_imagem_texto.config(state='disabled')
    def resetar_imagem_ui(self):
        self.canvas_imagem.resetar()
        self.hist_imagem_texto.config(state='normal'); self.hist_imagem_texto.delete(1.0, tk.END)
        self.hist_imagem_texto.config(state='disabled')
    def _get_float_img(self, key, default=0.0):
        try: return float(self.entries_imagem[key].get())
        except (ValueError, KeyError): messagebox.showerror("Erro", f"Valor inválido para {key}"); return default
    def aplicar_translacao_imagem(self):
        dx = self._get_float_img('tx'); dy = self._get_float_img('ty')
        self.canvas_imagem.aplicar_translacao(dx, dy); self._add_hist(f"Translação: dx={dx}, dy={dy}")
    def aplicar_escala_imagem(self):
        sx = self._get_float_img('sx', 1.0); sy = self._get_float_img('sy', 1.0)
        self.canvas_imagem.aplicar_escala(sx, sy); self._add_hist(f"Escala: sx={sx}, sy={sy}")
    def aplicar_rotacao_imagem(self):
        angulo = self._get_float_img('angulo'); self.canvas_imagem.aplicar_rotacao(angulo); self._add_hist(f"Rotação: {angulo}°")
    def aplicar_cisalhamento_imagem(self):
        shx = self._get_float_img('shx'); shy = self._get_float_img('shy')
        self.canvas_imagem.aplicar_cisalhamento(shx, shy); self._add_hist(f"Cisalhamento: shx={shx}, shy={shy}")
    def aplicar_reflexao_imagem(self):
        eixo = self.entries_imagem['reflexao_eixo'].get()
        self.canvas_imagem.aplicar_reflexao(eixo); self._add_hist(f"Reflexão: eixo {eixo}")

    def criar_controles_retas(self):
        self.entries_retas = {}; frame = self.controles_retas
        ttk.Button(frame, text="Limpar Tela", command=self.canvas_retas.limpar_linhas).pack(pady=10, fill=tk.X)
        def _criar_entry_reta(parent, label, key, val):
            ttk.Label(parent, text=label).pack(side=tk.LEFT, padx=(0,5)); e = ttk.Entry(parent, width=7); e.insert(0, val); e.pack(side=tk.LEFT, padx=(0,10)); self.entries_retas[key] = e
        f_p1 = ttk.LabelFrame(frame, text="Ponto Inicial (P1)", padding=10); f_p1.pack(fill=tk.X, pady=5)
        _criar_entry_reta(f_p1, "X0:", "x0", "-250"); _criar_entry_reta(f_p1, "Y0:", "y0", "-50")
        f_p2 = ttk.LabelFrame(frame, text="Ponto Final (P2)", padding=10); f_p2.pack(fill=tk.X, pady=5)
        _criar_entry_reta(f_p2, "X1:", "x1", "250"); _criar_entry_reta(f_p2, "Y1:", "y1", "180")
        f_algo = ttk.LabelFrame(frame, text="Algoritmo", padding=10); f_algo.pack(fill=tk.X, pady=5)
        self.entries_retas['algoritmo'] = ttk.Combobox(f_algo, values=['Bresenham', 'DDA'], state="readonly")
        self.entries_retas['algoritmo'].set('Bresenham'); self.entries_retas['algoritmo'].pack(fill=tk.X)
        ttk.Button(frame, text="Desenhar Reta", command=self.aplicar_desenho_reta).pack(pady=10, fill=tk.X)
        f_clip = ttk.LabelFrame(frame, text="Recorte (Cohen-Sutherland)", padding=10); f_clip.pack(fill=tk.X, pady=10)
        ttk.Checkbutton(f_clip, text="Habilitar Recorte", variable=self.canvas_retas.clipping_enabled, command=lambda: self.canvas_retas.tkExpose(None)).pack(anchor=tk.W)
        f_clip_coords = ttk.Frame(f_clip); f_clip_coords.pack(pady=5)
        def _criar_entry_clip(parent, label, key, val):
            ttk.Label(parent, text=label).pack(side=tk.LEFT); e = ttk.Entry(parent, width=6); e.insert(0, str(val)); e.pack(side=tk.LEFT, padx=(2, 8)); self.entries_retas[key] = e
        defaults = self.canvas_retas.clipping_rect
        _criar_entry_clip(f_clip_coords, "Xmin:", "xmin", defaults['xmin']); _criar_entry_clip(f_clip_coords, "Ymin:", "ymin", defaults['ymin'])
        _criar_entry_clip(f_clip_coords, "Xmax:", "xmax", defaults['xmax']); _criar_entry_clip(f_clip_coords, "Ymax:", "ymax", defaults['ymax'])
        ttk.Button(f_clip, text="Atualizar Janela de Recorte", command=self.aplicar_config_recorte).pack(pady=5, fill=tk.X)
    def aplicar_desenho_reta(self):
        try:
            x0 = int(self.entries_retas['x0'].get()); y0 = int(self.entries_retas['y0'].get())
            x1 = int(self.entries_retas['x1'].get()); y1 = int(self.entries_retas['y1'].get())
            algo = self.entries_retas['algoritmo'].get(); cor = tuple(np.random.rand(3))
            self.canvas_retas.adicionar_linha((x0,y0), (x1,y1), algo, cor)
        except ValueError: messagebox.showerror("Erro", "Coordenadas das retas devem ser números inteiros.")
    def aplicar_config_recorte(self):
        try:
            enabled = self.canvas_retas.clipping_enabled.get()
            rect = {'xmin': float(self.entries_retas['xmin'].get()), 'ymin': float(self.entries_retas['ymin'].get()), 'xmax': float(self.entries_retas['xmax'].get()), 'ymax': float(self.entries_retas['ymax'].get())}
            if rect['xmin'] >= rect['xmax'] or rect['ymin'] >= rect['ymax']: messagebox.showerror("Erro", "Coordenadas da janela inválidas."); return
            self.canvas_retas.set_clipping_info(enabled, rect)
        except ValueError: messagebox.showerror("Erro", "Coordenadas da janela devem ser números.")

    def criar_controles_3d(self):
        self.entries_3d = {}; frame = self.controles_3d
        def _criar_entry(parent, label, val):
            fr = ttk.Frame(parent); fr.pack(fill=tk.X, pady=2); ttk.Label(fr, text=label, width=8).pack(side=tk.LEFT); e = ttk.Entry(fr); e.pack(fill=tk.X, expand=True); e.insert(0, val); return e
        ttk.Button(frame, text="Resetar Cubo", command=self.resetar_3d).pack(pady=10, fill=tk.X)
        f_t = ttk.LabelFrame(frame, text="Translação", padding=10); f_t.pack(fill=tk.X, pady=5); self.entries_3d['tx'] = _criar_entry(f_t, "X:", "0.0"); self.entries_3d['ty'] = _criar_entry(f_t, "Y:", "0.0"); self.entries_3d['tz'] = _criar_entry(f_t, "Z:", "0.0")
        f_e = ttk.LabelFrame(frame, text="Escala", padding=10); f_e.pack(fill=tk.X, pady=5); self.entries_3d['sx'] = _criar_entry(f_e, "X:", "1.0"); self.entries_3d['sy'] = _criar_entry(f_e, "Y:", "1.0"); self.entries_3d['sz'] = _criar_entry(f_e, "Z:", "1.0")
        f_r = ttk.LabelFrame(frame, text="Rotação (Graus)", padding=10); f_r.pack(fill=tk.X, pady=5); self.entries_3d['rx'] = _criar_entry(f_r, "Eixo X:", "0.0"); self.entries_3d['ry'] = _criar_entry(f_r, "Eixo Y:", "0.0"); self.entries_3d['rz'] = _criar_entry(f_r, "Eixo Z:", "0.0")
        f_c = ttk.LabelFrame(frame, text="Cisalhamento", padding=10); f_c.pack(fill=tk.X, pady=5); self.entries_3d['sh_xy'] = _criar_entry(f_c, "XY:", "0.0"); self.entries_3d['sh_xz'] = _criar_entry(f_c, "XZ:", "0.0"); self.entries_3d['sh_yz'] = _criar_entry(f_c, "YZ:", "0.0")
        f_ref = ttk.LabelFrame(frame, text="Reflexão", padding=10); f_ref.pack(fill=tk.X, pady=5); self.entries_3d['reflexao_plano'] = ttk.Combobox(f_ref, values=['nenhuma', 'plano_xy', 'plano_yz', 'plano_xz'], state="readonly"); self.entries_3d['reflexao_plano'].set('nenhuma'); self.entries_3d['reflexao_plano'].pack(fill=tk.X)
        ttk.Button(frame, text="Aplicar Transformações 3D", command=self.aplicar_3d).pack(pady=20, fill=tk.X)
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
        except ValueError: messagebox.showerror("Erro", "Por favor, insira números válidos para todos os campos 3D.")

    def criar_controles_2d(self):
        self.entries_2d = {}; frame = self.controles_2d
        ttk.Button(frame, text="Resetar Quadrado", command=self.canvas_2d.resetar).pack(pady=10, fill=tk.X)
        def _criar_controles_linha(parent, text, key1, val1, key2, val2, cmd):
            fr = ttk.LabelFrame(parent, text=text, padding=10); fr.pack(fill=tk.X, pady=5); ttk.Label(fr, text=f"{key1.replace('t','d')}:").pack(side=tk.LEFT)
            e1 = ttk.Entry(fr, width=7); e1.insert(0, val1); e1.pack(side=tk.LEFT, fill=tk.X, expand=True, padx=(0, 5)); self.entries_2d[key1] = e1
            if key2:
                ttk.Label(fr, text=f"{key2.replace('t','d')}:").pack(side=tk.LEFT)
                e2 = ttk.Entry(fr, width=7); e2.insert(0, val2); e2.pack(side=tk.LEFT, fill=tk.X, expand=True, padx=(0, 5)); self.entries_2d[key2] = e2
            ttk.Button(fr, text="Aplicar", command=cmd).pack(side=tk.LEFT)
        _criar_controles_linha(frame, "Translação", 'tx', "10.0", 'ty', "10.0", self.aplicar_translacao_2d)
        _criar_controles_linha(frame, "Escala", 'sx', "1.2", 'sy', "1.2", self.aplicar_escala_2d)
        _criar_controles_linha(frame, "Cisalhamento", 'shx', "0.2", 'shy', "0.0", self.aplicar_cisalhamento_2d)
        f_r = ttk.LabelFrame(frame, text="Rotação", padding=10); f_r.pack(fill=tk.X, pady=5); ttk.Label(f_r, text="Ângulo:").pack(side=tk.LEFT)
        self.entries_2d['angulo'] = ttk.Entry(f_r, width=7); self.entries_2d['angulo'].insert(0, "15.0"); self.entries_2d['angulo'].pack(side=tk.LEFT, fill=tk.X, expand=True, padx=(0, 5))
        ttk.Button(f_r, text="Aplicar", command=self.aplicar_rotacao_2d).pack(side=tk.LEFT)
        f_ref = ttk.LabelFrame(frame, text="Reflexão", padding=10); f_ref.pack(fill=tk.X, pady=5)
        self.entries_2d['reflexao_eixo'] = ttk.Combobox(f_ref, values=['x', 'y', 'origem', 'reta y=x'], state="readonly"); self.entries_2d['reflexao_eixo'].set('x')
        self.entries_2d['reflexao_eixo'].pack(side=tk.LEFT, fill=tk.X, expand=True, padx=(0, 5)); ttk.Button(f_ref, text="Aplicar", command=self.aplicar_reflexao_2d).pack(side=tk.LEFT)
    def _get_float(self, entry_name):
        try: return float(self.entries_2d[entry_name].get())
        except (ValueError, KeyError): messagebox.showerror("Erro", f"Valor inválido no campo '{entry_name}'."); return None
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


if __name__ == '__main__':
    app = App()
    app.mainloop()
