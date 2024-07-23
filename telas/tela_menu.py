import pygame
import sys

# Inicialização do Pygame
pygame.init()

# Cores
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
RED = (255, 0, 0)
GOLD = (212, 175, 55)

# Dimensões da tela
SCREEN_WIDTH = 800
SCREEN_HEIGHT = 600

# Configuração da tela
screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
pygame.display.set_caption("Menu - Game of Thrones")

# Fonte
font = pygame.font.Font(None, 74)
font_small = pygame.font.Font(None, 36)

# Carregar imagem de fundo (opcional)
background = pygame.image.load("Downloads\got_background.jpg")
background = pygame.transform.scale(background, (SCREEN_WIDTH, SCREEN_HEIGHT))

def draw_text(text, font, color, surface, x, y):
    textobj = font.render(text, True, color)
    textrect = textobj.get_rect()
    textrect.topleft = (x, y)
    surface.blit(textobj, textrect)

def main_menu():
    while True:
        screen.blit(background, (0, 0))

        draw_text('Game of Thrones', font, GOLD, screen, 200, 50)

        mx, my = pygame.mouse.get_pos()

        button_1 = pygame.Rect(300, 200, 200, 50)
        button_2 = pygame.Rect(300, 300, 200, 50)

        if button_1.collidepoint((mx, my)):
            if click:
                start_game()
        if button_2.collidepoint((mx, my)):
            if click:
                how_to_play()

        pygame.draw.rect(screen, RED, button_1)
        pygame.draw.rect(screen, RED, button_2)

        draw_text('Comece a Batalha!', font_small, WHITE, screen, 320, 210)
        draw_text('Como Jogar', font_small, WHITE, screen, 340, 310)

        click = False
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            if event.type == pygame.MOUSEBUTTONDOWN:
                if event.button == 1:
                    click = True

        pygame.display.update()

def start_game():
    running = True
    while running:
        screen.fill(BLACK)
        draw_text('Jogo Iniciado!', font, GOLD, screen, 200, 250)
        
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_ESCAPE:
                    running = False

        pygame.display.update()

def how_to_play():
    running = True
    while running:
        screen.fill(BLACK)
        draw_text('Instruções de Como Jogar', font, GOLD, screen, 100, 250)
        
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_ESCAPE:
                    running = False

        pygame.display.update()

main_menu()
