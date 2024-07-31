import pygame
import sys

# Inicialização do Pygame
pygame.init()

# Cores
BRANCO = (255, 255, 255)

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
tela_historia = pygame.image.load("Downloads/tela_ifmenu.png").convert()
tela_historia = pygame.transform.scale(tela_historia, (LARGURA_TELA, ALTURA_TELA))

# Função para iniciar o jogo
def iniciar_jogo(personagem):
    if personagem == "Daenerys":
        import draca
        draca.main()
    elif personagem == "Jon":
        import jogo_do_ano
        jogo_do_ano.main()
    elif personagem == "Stannis":
        import tela3
        tela3.main()

def menu_principal():
    tela_atual = 'menu_principal'
    clicado = False
    tela_inicial = True

    while tela_inicial:
        mx, my = pygame.mouse.get_pos()
        tela.fill(BRANCO)
        
        if tela_atual == 'menu_principal':
            tela.blit(fundo_menu, (0, 0))
            area_botao_iniciar = pygame.Rect(280, 310, 250, 50)
            area_botao_menu = pygame.Rect(350, 390, 100, 50)
            
            if area_botao_iniciar.collidepoint((mx, my)) and pygame.mouse.get_pressed()[0] and not clicado:
                tela_atual = 'escolha_personagem'
                clicado = True
            
            if area_botao_menu.collidepoint((mx, my)) and pygame.mouse.get_pressed()[0] and not clicado:
                tela_atual = 'tela_historia'
                clicado = True
        
        elif tela_atual == 'escolha_personagem':
            tela.blit(fundo_menu_in, (0, 0))
            area_botao_personagem1 = pygame.Rect(60, 200, 180, 200)
            area_botao_personagem2 = pygame.Rect(300, 200, 200, 200)
            area_botao_personagem3 = pygame.Rect(550, 200, 200, 200)
            area_botao_historia = pygame.Rect(51, 520, 60, 45)

            if area_botao_historia.collidepoint((mx, my)) and pygame.mouse.get_pressed()[0] and not clicado:
                tela_atual = 'menu_principal'
                clicado = True
            elif area_botao_personagem1.collidepoint((mx, my)) and pygame.mouse.get_pressed()[0] and not clicado:
                print("Daenerys escolhida")
                iniciar_jogo("Daenerys")
                tela_inicial = False  # Exit loop

            elif area_botao_personagem2.collidepoint((mx, my)) and pygame.mouse.get_pressed()[0] and not clicado:
                print("Jon escolhido")
                iniciar_jogo("Jon")
                tela_inicial = False  # Exit loop

            elif area_botao_personagem3.collidepoint((mx, my)) and pygame.mouse.get_pressed()[0] and not clicado:
                print("Stannis escolhido")
                iniciar_jogo("Stannis")
                tela_inicial = False  # Exit loop
        
        elif tela_atual == "tela_historia":
            tela.blit(tela_historia, (0, 0))
            area_botao_historia = pygame.Rect(51, 520, 60, 45)
            if area_botao_historia.collidepoint((mx, my)) and pygame.mouse.get_pressed()[0] and not clicado:
                tela_atual = 'menu_principal'
                clicado = True
        
        # Tratamento de eventos
        for evento in pygame.event.get():
            if evento.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            if evento.type == pygame.MOUSEBUTTONDOWN:
                if evento.button == 1:
                    clicado = False  # Resetar clicado quando o botão do mouse é pressionado
                    
            if evento.type == pygame.MOUSEBUTTONUP:
                if evento.button == 1:
                    clicado = True  # Permitir nova detecção de clique
                    
        pygame.display.update()

# Executar a função do menu principal
menu_principal()
