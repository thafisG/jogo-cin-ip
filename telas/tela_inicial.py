import pygame
import sys

# Inicialização do Pygame
pygame.init()

# Cores
BRANCO = (255, 255, 255)
PRETO = (0, 0, 0)
OURO = (212, 175, 55)

# Dimensões da tela
LARGURA_TELA = 800
ALTURA_TELA = 600

# Configuração da tela
tela = pygame.display.set_mode((LARGURA_TELA, ALTURA_TELA))
pygame.display.set_caption("Menu - A Guerra dos Tronos")

# Carregar imagens de fundo
fundo_menu = pygame.image.load("Downloads/tela_menu_figma.png").convert()
fundo_menu = pygame.transform.scale(fundo_menu, (LARGURA_TELA, ALTURA_TELA))
fundo_menu_in = pygame.image.load("Downloads/escolhas_de_personagens.png").convert()
fundo_menu_in = pygame.transform.scale(fundo_menu_in, (LARGURA_TELA, ALTURA_TELA))

# Fonte
fonte = pygame.font.Font(None, 74)

def menu_principal():
    fundo_atual = fundo_menu  # Começa com o fundo do menu principal
    clicou = False
    
    while True:
        tela.blit(fundo_atual, (0, 0))

        mx, my = pygame.mouse.get_pos()

        # Áreas dos botões no menu principal
        area_botao_iniciar = pygame.Rect(275, 300, 200, 50)
        area_botao_menu = pygame.Rect(200, 400, 250, 50)

        # Verificar cliques nos botões
        if area_botao_iniciar.collidepoint((mx, my)):
            if clicou:
                # chamando a tela da escolha dos tronos 
                fundo_atual = fundo_menu_in
            clicou = False
        # verificando click in menu
        if area_botao_menu.collidepoint((mx, my)):
            if clicou:
                print("clica mt no menu")

        clicou = False
        
        # Tratamento de eventos
        for evento in pygame.event.get():
            if evento.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            if evento.type == pygame.MOUSEBUTTONDOWN:
                if evento.button == 1:
                    clicou = True

        pygame.display.update()

# Executar a função do menu principal
menu_principal()
