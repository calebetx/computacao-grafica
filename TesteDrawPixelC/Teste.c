#include <Windows.h>
#include <GL/gl.h>
#include <stdio.h>
#include <stdlib.h>
#include <math.h>

#define WIDTH 1920
#define HEIGHT 1080

// Função para inicializar o OpenGL
void initOpenGL(HDC hdc) {
    PIXELFORMATDESCRIPTOR pfd;
    int pixelFormat;

    // Prepara o formato de pixel (para renderização com OpenGL)
    ZeroMemory(&pfd, sizeof(pfd));
    pfd.nSize = sizeof(pfd);
    pfd.nVersion = 1;
    pfd.dwFlags = PFD_SUPPORT_OPENGL | PFD_DOUBLEBUFFER | PFD_DRAW_TO_WINDOW;
    pfd.iPixelType = PFD_TYPE_RGBA;
    pfd.cColorBits = 32;
    pfd.cRedBits = 8;
    pfd.cGreenBits = 8;
    pfd.cBlueBits = 8;
    pfd.cAlphaBits = 8;

    // Escolhe um formato de pixel adequado
    pixelFormat = ChoosePixelFormat(hdc, &pfd);
    SetPixelFormat(hdc, pixelFormat, &pfd);

    // Cria o contexto OpenGL
    HGLRC hglrc = wglCreateContext(hdc);
    wglMakeCurrent(hdc, hglrc);
}

// Função para desenhar um pixel na tela nas coordenadas fornecidas
void drawPixel(float x, float y) {
    glPointSize(1.0f);  // Define o tamanho do ponto (pixel)
    glBegin(GL_POINTS);
    glVertex2f(x, y);  // Desenha o ponto nas coordenadas (x, y)
    glEnd();
}

// Função para mapear as coordenadas do mundo para as coordenadas normalizadas do dispositivo (NDC)
void worldToNDC(float x, float y, float xmin, float xmax, float ymin, float ymax, float* ndcx, float* ndcy) {
    *ndcx = (x - xmin) / (xmax - xmin);  // Mapeamento X para NDC
    *ndcy = (y - ymin) / (ymax - ymin);  // Mapeamento Y para NDC
}

// Função para mapear as coordenadas normalizadas do dispositivo para as coordenadas do dispositivo
void NDCtoDevice(float ndcx, float ndcy, int width, int height, int* dcx, int* dcy) {
    *dcx = round(ndcx * (width - 1));  // Mapeamento X para coordenadas do dispositivo
    *dcy = round(ndcy * (height - 1)); // Mapeamento Y para coordenadas do dispositivo
}

// Função para criar a janela
HWND createWindow(HINSTANCE hInstance) {
    WNDCLASS wc = {0};
    wc.lpfnWndProc = DefWindowProc;
    wc.hInstance = hInstance;
    wc.lpszClassName = "OpenGL_Window";

    if (!RegisterClass(&wc)) {
        printf("Erro ao registrar a classe da janela.\n");
        exit(EXIT_FAILURE);
    }

    HWND hwnd = CreateWindow(
        wc.lpszClassName,
        "Coordenadas do Mundo",
        WS_OVERLAPPEDWINDOW | WS_VISIBLE,
        100, 100, WIDTH, HEIGHT,
        NULL, NULL, hInstance, NULL
    );

    if (!hwnd) {
        printf("Erro ao criar a janela.\n");
        exit(EXIT_FAILURE);
    }

    return hwnd;
}

int main(void) {
    HINSTANCE hInstance = GetModuleHandle(NULL);
    HWND hwnd = createWindow(hInstance);

    HDC hdc = GetDC(hwnd);
    initOpenGL(hdc);

    // Resolução do dispositivo (tela)
    int screenWidth = 1920;
    int screenHeight = 1080;

    // Intervalo do mundo/usuário
    float xmin = -10.0f, xmax = 10.0f;
    float ymin = -10.0f, ymax = 10.0f;

    float x, y;
    printf("Digite a coordenada X do mundo: ");
    scanf("%f", &x);
    printf("Digite a coordenada Y do mundo: ");
    scanf("%f", &y);

    // Variáveis para coordenadas normalizadas e coordenadas do dispositivo
    float ndcx, ndcy;
    int dcx, dcy;

    // Transformação do mundo para NDC
    worldToNDC(x, y, xmin, xmax, ymin, ymax, &ndcx, &ndcy);

    // Transformação de NDC para coordenadas do dispositivo
    NDCtoDevice(ndcx, ndcy, screenWidth, screenHeight, &dcx, &dcy);

    // Loop principal para renderizar a janela
    MSG msg;
    while (1) {
        if (PeekMessage(&msg, NULL, 0, 0, PM_REMOVE)) {
            if (msg.message == WM_QUIT) break;
            TranslateMessage(&msg);
            DispatchMessage(&msg);
        }

        glClear(GL_COLOR_BUFFER_BIT);

        // Definindo a cor do ponto (pixel)
        glColor3f(1.0f, 0.0f, 0.0f); // Red (vermelho)

        // Desenhando o ponto nas coordenadas do dispositivo
        drawPixel((float)dcx / screenWidth * 2 - 1, (float)dcy / screenHeight * 2 - 1);

        SwapBuffers(hdc);  // Troca os buffers para renderização

        // Espera um pouco para simular a renderização
        Sleep(10);
    }

    // Cleanup
    ReleaseDC(hwnd, hdc);
    PostQuitMessage(0);

    return 0;
}
