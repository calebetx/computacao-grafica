def menu_transformacoes():
    print("\nEscolha a transformação a ser aplicada:")
    print("1 - Escala")
    print("2 - Translação")
    print("3 - Reflexão")
    print("4 - Cisalhamento")
    print("5 - Rotação")
    print("0 - Nenhuma (reinicia cubo)")
    print("S - Sair do menu")

    opcao = input("Opção: ").strip().lower()

    if opcao == '1':
        sx = float(input("Fator de escala em X: "))
        sy = float(input("Fator de escala em Y: "))
        sz = float(input("Fator de escala em Z: "))
        return ('escala', (sx, sy, sz))

    elif opcao == '2':
        tx = float(input("Translação em X: "))
        ty = float(input("Translação em Y: "))
        tz = float(input("Translação em Z: "))
        return ('translacao', (tx, ty, tz))

    elif opcao == '3':
        plano = input("Plano de reflexão (xy, yz, xz): ").lower()
        return ('reflexao', plano)

    elif opcao == '4':
        sh_xy = float(input("Cisalhamento em XY: "))
        sh_xz = float(input("Cisalhamento em XZ: "))
        sh_yz = float(input("Cisalhamento em YZ: "))
        return ('cisalhamento', (sh_xy, sh_xz, sh_yz))

    elif opcao == '5':
        angulo = float(input("Ângulo de rotação (graus): "))
        eixo = input("Eixo de rotação (x, y ou z): ").lower()
        return ('rotacao', (angulo, eixo))

    elif opcao == '0':
        from main import transformacoes
        transformacoes.clear()
        print("[INFO] Transformações reiniciadas.")
        return ('nenhuma', None)

    elif opcao == 's':
        return ('sair', None)

    else:
        print("Opção inválida.")
        return ('nenhuma', None)
