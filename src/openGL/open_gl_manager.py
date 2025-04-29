import threading

import numpy as np
from openGL.draw_square import draw_square
from openGL.functions.algorithms2d.reflexao2d import reflexao2d

class OpenGLManager:
    def __init__(self):
        self.running = True
        self.square_points = np.array([
            [0, 0],
            [0, 150],
            [150, 150],
            [150, 0]
        ])

    def menu(self):
        while self.running:
            print("\nEscolha o tipo de reflexão:")
            print("1 - Reflexão em relação ao eixo X")
            print("2 - Reflexão em relação ao eixo Y")
            print("3 - Reflexão em relação à Origem")
            print("4 - Reflexão na linha Y = X")
            print("0 - Sem reflexão (normal)")
            print("q - Sair")

            escolha = input("Digite sua opção: ").strip()

            if escolha == '1':
                self.square_points = reflexao2d(self.square_points, 'x')
            elif escolha == '2':
                self.square_points = reflexao2d(self.square_points, 'y')
            elif escolha == '3':
                self.square_points = reflexao2d(self.square_points, 'origem')
            elif escolha == '4':
                self.square_points = reflexao2d(self.square_points, 'xy')
            elif escolha == '0':
                self.square_points = np.array([
                    [0, 0],
                    [0, 150],
                    [150, 150],
                    [150, 0]
                ]) 
            elif escolha.lower() == 'q':
                self.running = False
                break
            else:
                print("Opção inválida. Nenhuma transformação aplicada.")                        

    def start_menu_thread(self):
        menu_thread = threading.Thread(target=self.menu)
        menu_thread.daemon = True
        menu_thread.start()

    def draw(self):
        draw_square(self.square_points)