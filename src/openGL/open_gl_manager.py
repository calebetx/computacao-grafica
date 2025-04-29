import threading

import numpy as np
from openGL.draw_square import draw_square
from openGL.functions.algorithms2d.reflexao2d import reflexao2d
from openGL.functions.algorithms2d.escala2d import escala2d
from openGL.functions.algorithms2d.rotacao2d import rotacao2d
from openGL.functions.algorithms2d.translacao2d import translacao2d
from openGL.functions.algorithms2d.cisalhamento2d import cisalhamento2d

import time

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
            print("\n=== Menu Principal ===")
            print("1 - Reflexão")
            print("2 - Translação")
            print("3 - Rotação")
            print("4 - Escala")
            print("5 - Cisalhamento")
            print("0 - Resetar para Original")
            print("q - Sair")

            escolha = input("Digite o tipo de transformação: ").strip()

            if escolha == '1':
                self.menu_reflexao()
            elif escolha == '2':
                self.menu_translacao()
            elif escolha == '3':
                self.menu_rotacao()
            elif escolha == '4':
                self.menu_escala()
            elif escolha == '5':
                self.menu_cisalhamento()
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
                print("Opção inválida. Tente novamente.")

    def menu_reflexao(self):
        print("\n--- Reflexão ---")
        print("1 - Eixo X")
        print("2 - Eixo Y")
        print("3 - Origem")
        print("4 - Reta Y = X")

        escolha = input("Digite a reflexão desejada: ").strip()

        if escolha == '1':
            self.square_points = reflexao2d(self.square_points, 'x')
        elif escolha == '2':
            self.square_points = reflexao2d(self.square_points, 'y')
        elif escolha == '3':
            self.square_points = reflexao2d(self.square_points, 'origem')
        elif escolha == '4':
            self.square_points = reflexao2d(self.square_points, 'xy')
        else:
            print("Opção inválida para reflexão.")

    def menu_translacao(self):
        print("\n--- Translação ---")
        try:
            dx = float(input("Digite o valor de deslocamento em X: "))
            dy = float(input("Digite o valor de deslocamento em Y: "))
            self.square_points = translacao2d(self.square_points, dx, dy)
        except ValueError:
            print("Entrada inválida. Digite números.")

    def menu_rotacao(self):
        print("\n--- Rotação ---")
        try:
            angulo = float(input("Digite o ângulo de rotação (em graus): "))
            self.square_points = rotacao2d(self.square_points, angulo)
        except ValueError:
            print("Entrada inválida. Digite um número.")

    def menu_escala(self):
        print("\n--- Escala ---")
        try:
            sx = float(input("Digite o fator de escala em X: "))
            sy = float(input("Digite o fator de escala em Y: "))
            self.square_points = escala2d(self.square_points, sx, sy)
        except ValueError:
            print("Entrada inválida. Digite números.")

    def menu_cisalhamento(self):
        print("\n--- Cisalhamento ---")
        try:
            shx = float(input("Digite o valor de cisalhamento em X: "))
            shy = float(input("Digite o valor de cisalhamento em Y: "))
            self.square_points = cisalhamento2d(self.square_points, shx, shy)
        except ValueError:
            print("Entrada inválida. Digite números.")                        

    def start_menu_thread(self):
        menu_thread = threading.Thread(target=self.menu)
        menu_thread.daemon = True
        menu_thread.start()

    def draw(self):
        draw_square(self.square_points)