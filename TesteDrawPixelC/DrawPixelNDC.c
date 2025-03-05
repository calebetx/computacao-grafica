#include <GL/glew.h>
#include <GLFW/glfw3.h>
#include <stdio.h>
#include <stdlib.h>
#include <math.h>

// Função para inicializar o OpenGL
void initOpenGL() {
    if (!glfwInit()) {
        fprintf(stderr, "Erro ao inicializar GLFW\n");
        exit(EXIT_FAILURE);
    }

    glfwWindowHint(GLFW_CONTEXT_VERSION_MAJOR, 3);
    glfwWindowHint(GLFW_CONTEXT_VERSION_MINOR, 3);
    
    GLFWwindow* window = glfwCreateWindow(1920, 1080, "Coordenadas do Mundo", NULL, NULL);
    if (!window) {
        fprintf(stderr, "Erro ao criar a janela GLFW\n");
        glfwTerminate();
        exit(EXIT_FAILURE);
    }

    glfwMakeContextCurrent(window);
    glfwSwapInterval(1);

    if (glewInit() != GLEW_OK) {
        fprintf(stderr, "Erro ao inicializar GLEW\n");
        exit(EXIT_FAILURE);
    }
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

int main(void) {
    initOpenGL();

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

    // Loop principal do OpenGL para renderizar a janela
    GLFWwindow* window = glfwGetCurrentContext();
    while (!glfwWindowShouldClose(window)) {
        glClear(GL_COLOR_BUFFER_BIT);

        // Definindo a cor do ponto (pixel)
        glColor3f(1.0f, 0.0f, 0.0f); // Red (vermelho)

        // Desenhando o ponto nas coordenadas do dispositivo
        drawPixel((float)dcx / screenWidth * 2 - 1, (float)dcy / screenHeight * 2 - 1);

        // Trocar os buffers e processar eventos
        glfwSwapBuffers(window);
        glfwPollEvents();
    }

    glfwDestroyWindow(window);
    glfwTerminate();

    return 0;
}

