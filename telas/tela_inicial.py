import pygame
import sys

# Inicialização do Pygame
pygame.init()

# Cores
BRANCO = (255, 255, 255)
PRETO = (0, 0, 0)

# Dimensões da tela
LARGURA_TELA = 800
ALTURA_TELA = 600

# Configuração da tela
tela = pygame.display.set_mode((LARGURA_TELA, ALTURA_TELA))
pygame.display.set_caption("Menu - A Guerra dos Tronos")

# Carregar imagens de fundo
fundo_menu = pygame.image.load("Downloads/tela_menu_figma.png").convert()
fundo_menu = pygame.transform.scale(fundo_menu, (LARGURA_TELA, ALTURA_TELA))
fundo_menu_in = pygame.image.load("Downloads/escolhas_personagens.png").convert()
fundo_menu_in = pygame.transform.scale(fundo_menu_in, (LARGURA_TELA, ALTURA_TELA))
tela_historia = pygame.image.load("Downloads/tela_ifmenu.png").convert()
tela_historia = pygame.transform.scale(tela_historia, (LARGURA_TELA, ALTURA_TELA))

# função para inicio do jogo (trocar para a tela das fases para implementação)
def iniciar_jogo():
    # Função para iniciar o jogo
    fundo_jogo_iniciado = pygame.image.load("Downloads/tela_jogo_iniciado.png").convert()
    fundo_jogo_iniciado = pygame.transform.scale(fundo_jogo_iniciado, (LARGURA_TELA, ALTURA_TELA))

    # Exibir a tela do jogo iniciado por 5 segundos
    tela.blit(fundo_jogo_iniciado, (0, 0))
    pygame.display.update()
    pygame.time.wait(5000)  # Espera 5 segundos para que o jogador veja a mensagem

def menu_principal():
    tela_atual = 'menu_principal'
    clicado = False
    tela_inicial = True
    
    while tela_inicial:
        tela.fill(BRANCO)
        
        if tela_atual == 'menu_principal':
            tela.blit(fundo_menu, (0, 0))
            mx, my = pygame.mouse.get_pos()
            
            # Áreas dos botões no menu principal
            area_botao_iniciar = pygame.Rect(280, 310, 250, 50)
            area_botao_menu = pygame.Rect(350, 390, 100, 50)
            
            if area_botao_iniciar.collidepoint((mx, my)) and pygame.mouse.get_pressed()[0] and not clicado:
                tela_atual = 'escolha_personagem'
                clicado = True
            
            if area_botao_menu.collidepoint((mx, my)) and pygame.mouse.get_pressed()[0] and not clicado:
                tela_atual = 'tela_historia'
                clicado = True
        # direcionamento da tela para escolha dos personagens
        elif tela_atual == 'escolha_personagem':
            tela.blit(fundo_menu_in, (0, 0))
            mx, my = pygame.mouse.get_pos()
            
            # Áreas dos botões de personagens
            area_botao_personagem1 = pygame.Rect(60, 200, 180, 200)
            area_botao_personagem2 = pygame.Rect(300, 200, 200, 200)
            area_botao_personagem3 = pygame.Rect(550, 200, 200, 200)
            
            if area_botao_personagem1.collidepoint((mx, my)) and pygame.mouse.get_pressed()[0] and not clicado:
                print("Daenerys escolhida")
                iniciar_jogo()
                tela_inicial = not tela_inicial

            if area_botao_personagem2.collidepoint((mx, my)) and pygame.mouse.get_pressed()[0] and not clicado:
                print("Jon escolhido")
                iniciar_jogo()
                tela_inicial = not tela_inicial

            if area_botao_personagem3.collidepoint((mx, my)) and pygame.mouse.get_pressed()[0] and not clicado:
                print("Stannis escolhido")
                iniciar_jogo()
                tela_inicial = not tela_inicial
        
        elif tela_atual == "tela_historia":
            area_botao_historia = pygame.Rect(350, 390, 100, 50)
            if area_botao_historia.collidepoint((mx, my)) and pygame.mouse.get_pressed()[0] and not clicado:
                menu_principal()
                tela_inicial = not tela_inicial
        # Tratamento de eventos
        for evento in pygame.event.get():
            if evento.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            if evento.type == pygame.MOUSEBUTTONDOWN:
                if evento.button == 1:
                    clicado = False  # Resetar clicado quando o botão do mouse é pressionado
                    
        pygame.display.update()

# Executar a função do menu principal
menu_principal()
