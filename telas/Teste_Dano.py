import pygame
import sys
import random

# Inicializar o Pygame
pygame.init()

# Configurar tela
WIDTH, HEIGHT = 800, 600
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Jogo do Ano")

# Carregar imagem de fundo
background_image = pygame.image.load('Downloads/cenario.jpg').convert()  # Substitua 'cenario.jpg' pelo seu caminho e nome de arquivo
background_image = pygame.transform.scale(background_image, (WIDTH, HEIGHT))

# Definir cores
WHITE = (255, 255, 255)
GREEN = (0, 255, 0)
RED = (255, 0, 0)

# Variável de controle de fase
current_phase = 1

class Player(pygame.sprite.Sprite):
    def __init__(self):
        super().__init__()

        # Carregar imagens para a animação de ataque com fundo alfa
        self.attack_images = [
            pygame.image.load('Downloads/ataque1.png').convert_alpha(),
            pygame.image.load('Downloads/ataque2.png').convert_alpha()
            # Adicione mais imagens conforme necessário para sua animação de ataque
        ]

        self.image = self.attack_images[0]
        self.rect = self.image.get_rect()
        self.rect.center = (WIDTH // 4, HEIGHT // 2)

        # Velocidade do jogador
        self.speed = 2  # Velocidade de movimento do jogador

        # Atributos de vida
        self.max_health = 100
        self.health = self.max_health

        # Controle da animação de ataque
        self.is_attacking = False
        self.attack_index = 0  # Índice atual da animação de ataque
        self.attack_animation_speed = 10  # Velocidade da animação de ataque (quanto maior, mais lento)

        # Controle do tempo para a animação de ataque
        self.attack_frame_count = 1

    def update(self):
        # Atualizar a posição do jogador com base nas teclas pressionadas
        keys = pygame.key.get_pressed()
        if keys[pygame.K_a]:
            self.attack()

        # Movimento do jogador
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

    def attack(self):
        # Controla a velocidade da animação de ataque
        self.is_attacking = True
        self.attack_frame_count += 1
        if self.attack_frame_count >= self.attack_animation_speed:
            self.attack_frame_count = 0
            # Avança para o próximo frame da animação
            self.attack_index += 1
            if self.attack_index >= len(self.attack_images):
                self.attack_index = 0  # Reinicia a animação

            # Define a imagem atual da animação de ataque
            self.image = self.attack_images[self.attack_index]

            # Verifica colisão com o dragão durante o ataque
            if pygame.sprite.collide_rect(self, dragons[current_dragon]):
                dragons[current_dragon].take_damage()

        else:
            self.is_attacking = False

    def draw(self, screen):
        # Desenhar o jogador na tela
        screen.blit(self.image, self.rect)

    def draw_health_bar(self, screen):
        # Desenhar barra de vida do jogador
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

class Enemy(pygame.sprite.Sprite):
    def __init__(self, image_path, x, y):
        super().__init__()

        # Carregar imagem do inimigo (dragão)
        self.image = pygame.image.load(image_path).convert_alpha()
        self.rect = self.image.get_rect()
        self.rect.center = (x, y)

        # Velocidade do inimigo
        self.speed = 1  # Velocidade de movimento do inimigo

        # Atributos de vida do inimigo
        self.max_health = 50
        self.health = self.max_health

        # Tempo de ataque do inimigo
        self.attack_cooldown = 1  # Contador para o próximo ataque
        self.attack_timer = 0

    def update(self):
        # Movimento simples do inimigo
        self.rect.x -= self.speed

        # Verifica se o inimigo está atacando
        self.attack_timer += 1
        if self.attack_timer >= self.attack_cooldown:
            self.attack_timer = 0
            self.attack()

        # Verifica se o dragão chegou ao fim da tela
        if self.rect.right < 0:
            self.reset_position()

    def attack(self):
        # Simplesmente imprime uma mensagem de ataque
        print("O dragão atacou!")

    def draw(self, screen):
        # Desenhar o inimigo na tela
        screen.blit(self.image, self.rect)

    def draw_health_bar(self, screen):
        # Desenhar barra de vida do inimigo
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

    def take_damage(self):
        # Função para reduzir a vida do dragão quando ele é atacado pelo jogador
        self.health -= 10  # Ajuste conforme necessário

    def reset_position(self):
        # Função para reiniciar a posição do dragão quando chega ao fim da tela
        self.rect.right = WIDTH + random.randint(100, 300)  # Posição aleatória fora da tela
        self.rect.centery = random.randint(50, HEIGHT - 50)  # Posição vertical aleatória

# Função para mostrar "Fim de Jogo"
def show_game_over(screen):
    font = pygame.font.Font(None, 36)
    text = font.render("Fim de Jogo", True, WHITE)
    text_rect = text.get_rect(center=(WIDTH // 2, HEIGHT // 2))
    screen.blit(text, text_rect)

# Criar jogador
player = Player()

# Criar os dois inimigos (dragões) para a fase atual
dragon1 = Enemy('Downloads/drag.png', WIDTH - 100, HEIGHT // 2)  # Exemplo de posição e imagem do primeiro dragão
dragon2 = Enemy('Downloads/drag2.png', WIDTH - 100, random.randint(50, HEIGHT - 50))  # Exemplo de posição e imagem do segundo dragão

# Lista dos dragões disponíveis na fase atual
dragons = [dragon1, dragon2]
current_dragon = 0  # Começamos com o primeiro dragão

# Group para os sprites (jogador e inimigos)
all_sprites = pygame.sprite.Group()
all_sprites.add(player)
all_sprites.add(dragons[current_dragon])

# Loop principal do jogo
running = True
while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

    # Atualizar sprites
    all_sprites.update()

    # Verificar colisões (exemplo simples)
    if pygame.sprite.collide_rect(player, dragons[current_dragon]):
        player.health -= 1
        dragons[current_dragon].take_damage()

    # Verificar fim de jogo
    if player.health <= 0:
        show_game_over(screen)
        pygame.display.flip()
        pygame.time.delay(2000)  # Espera 2 segundos
        break

    # Verificar se o dragão atual foi derrotado
    if dragons[current_dragon].health <= 0:
        current_dragon += 1
        if current_dragon < len(dragons):
            all_sprites.add(dragons[current_dragon])  # Adiciona o próximo dragão ao grupo de sprites
        else:
            # Caso não haja mais dragões na lista, fase completada!
            current_phase += 1
            # Aqui você poderia configurar a lógica para passar para a próxima fase
            # ou finalizar o jogo se não houver mais fases

    # Desenhar elementos na tela
    screen.blit(background_image, (0, 0))  # Desenha o cenário de fundo na tela
    all_sprites.draw(screen)  # Desenha todos os sprites
    player.draw_health_bar(screen)  # Desenha a barra de vida do jogador
    dragons[current_dragon].draw_health_bar(screen)  # Desenha a barra de vida do dragão atual

    # Atualizar tela
    pygame.display.flip()

    # Controlar a taxa de atualização da tela
    pygame.time.Clock().tick(60)

# Finalizar o Pygame
pygame.quit()
sys.exit()
