import pygame
import sys

# Inicializar o Pygame
pygame.init()

# Configurar tela
WIDTH, HEIGHT = 800, 600
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Jogo do Ano")

# Carregar imagem de fundo
background_image = pygame.image.load('cenario.jpg').convert()  # Substitua 'cenario.jpg' pelo seu caminho e nome de arquivo
background_image = pygame.transform.scale(background_image, (WIDTH, HEIGHT))

# Definir cores
WHITE = (255, 255, 255)
GREEN = (0, 255, 0)
RED = (255, 0, 0)

class Player(pygame.sprite.Sprite):
    def __init__(self):
        super().__init__()

        # Carregar imagens para a animação de ataque
        self.attack_images = [
            pygame.image.load('ataque1.png').convert_alpha(),  # Substitua 'ataque1.png' pelo seu caminho e nome de arquivo
            pygame.image.load('ataque2.png').convert_alpha()   # Substitua 'ataque2.png' pelo seu caminho e nome de arquivo
            # Adicione mais imagens conforme necessário para sua animação de ataque
        ]
        
        self.image = self.attack_images[0]  # Inicia com a primeira imagem da animação
        self.rect = self.image.get_rect()

        # Definir posição inicial
        self.rect.center = (WIDTH // 2, HEIGHT // 2)

        # Velocidade do jogador
        self.speed = 5  # Velocidade de movimento do jogador

        # Atributos de vida
        self.max_health = 100
        self.health = self.max_health

        # Controle da animação de ataque
        self.attack_index = 0  # Índice atual da animação de ataque
        self.attack_animation_speed = 5  # Velocidade da animação de ataque (quanto maior, mais lento)

    def update(self):
        # Atualizar a posição do jogador com base nas teclas pressionadas
        keys = pygame.key.get_pressed()
        if keys[pygame.K_LEFT]:
            self.rect.x -= self.speed
        if keys[pygame.K_RIGHT]:
            self.rect.x += self.speed
        if keys[pygame.K_UP]:
            self.rect.y -= self.speed
        if keys[pygame.K_DOWN]:
            self.rect.y += self.speed

        # Limitar o jogador dentro dos limites da tela
        self.rect.x = max(0, min(WIDTH - self.rect.width, self.rect.x))
        self.rect.y = max(0, min(HEIGHT - self.rect.height, self.rect.y))

        # Verificar o ataque (tecla 'K')
        if keys[pygame.K_k]:
            self.attack()

    def attack(self):
        # Executar a animação de ataque
        self.image = self.attack_images[self.attack_index]
        self.attack_index += 1
        if self.attack_index >= len(self.attack_images):
            self.attack_index = 0

    def draw(self, screen):
        # Desenhar o jogador na tela
        screen.blit(self.image, self.rect)

    def draw_health_bar(self, screen):
        # Desenhar barra de vida
        bar_width = 100
        bar_height = 10
        bar_x = self.rect.centerx - bar_width // 2
        bar_y = self.rect.top - 20

        # Calcula a largura proporcional da barra de vida baseada na vida atual
        health_ratio = self.health / self.max_health
        health_bar_width = int(bar_width * health_ratio)

        # Desenha a barra de fundo (vermelha)
        pygame.draw.rect(screen, RED, (bar_x, bar_y, bar_width, bar_height))
        # Desenha a barra de vida (verde) por cima da barra de fundo
        pygame.draw.rect(screen, GREEN, (bar_x, bar_y, health_bar_width, bar_height))

# Criar jogador
player = Player()

# Loop principal do jogo
running = True
while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

    # Atualizar jogador
    player.update()

    # Desenhar elementos na tela
    screen.blit(background_image, (0, 0))  # Desenha o cenário de fundo na tela
    player.draw(screen)  # Desenha o jogador na tela
    player.draw_health_bar(screen)  # Desenha a barra de vida do jogador

    # Atualizar tela
    pygame.display.flip()

# Finalizar o Pygame
pygame.quit()
sys.exit()
