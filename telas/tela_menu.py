import pygame
import sys

# Inicialização do Pygame
pygame.init()

# Cores
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
GOLD = (212, 175, 55)

# Dimensões da tela
SCREEN_WIDTH = 800
SCREEN_HEIGHT = 600

# Configuração da tela
screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
pygame.display.set_caption("Menu - A Guerra dos Tronos")

# Carregar imagem de fundo
background = pygame.image.load("Downloads/tela_menu_figma.png")
background = pygame.transform.scale(background, (SCREEN_WIDTH, SCREEN_HEIGHT))

# Fonte
font = pygame.font.Font(None, 74)

def main_menu():
    click = False
    while True:
        screen.blit(background, (0, 0))

        mx, my = pygame.mouse.get_pos()

        # Áreas dos botões na imagem de fundo
        button_start_area = pygame.Rect(275, 300, 200, 50)
        button_menu_area = pygame.Rect(200, 400, 250, 50)

        # Verificar cliques nas áreas dos botões
        if button_start_area.collidepoint((mx, my)):
            if click:
                screen.fill(BLACK)
                text = font.render('Jogo Iniciado!', True, GOLD)
                text_rect = text.get_rect(center=(SCREEN_WIDTH // 2, SCREEN_HEIGHT // 2))
                screen.blit(text, text_rect)
                pygame.display.update()
                pygame.time.delay(2000)
                return

        if button_menu_area.collidepoint((mx, my)):
            if click:
                print("Ir para o Menu")
                #  ação para mudar para a tela de menu

        click = False  # Resetar click a cada iteração do loop
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            if event.type == pygame.MOUSEBUTTONDOWN:
                if event.button == 1:
                    click = True

        pygame.display.update()

# Executar o menu principal
main_menu()
