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
background_image = pygame.image.load('D:/cenario.jpg').convert()  # Ajuste o caminho conforme necessário
background_image = pygame.transform.scale(background_image, (WIDTH, HEIGHT))

# Definir cores
WHITE = (255, 255, 255)
GREEN = (0, 255, 0)
RED = (255, 0, 0)
BLUE = (0, 0, 255)

# Variável de controle de fase
current_phase = 1

class Player(pygame.sprite.Sprite):
    def __init__(self):
        super().__init__()

        # Carregar imagens para a animação de ataque com fundo alfa
        self.attack_images = [
            pygame.image.load('D:/draca.png').convert_alpha(),
            pygame.image.load('D:/draca.png').convert_alpha()
            # Adicione mais imagens conforme necessário para sua animação de ataque
        ]

        self.image = self.attack_images[0]
        self.rect = self.image.get_rect()
        self.rect.center = (WIDTH // 4, HEIGHT // 2)

        # Velocidade do jogador
        self.speed = 7  # Ajuste a velocidade conforme necessário

        # Atributos de vida
        self.max_health = 100
        self.health = self.max_health

        # Controle da animação de ataque
        self.is_attacking = False
        self.attack_index = 0  # Índice atual da animação de ataque
        self.attack_animation_speed = 10  # Velocidade da animação de ataque (quanto maior, mais lento)

        # Controle do tempo para a animação de ataque
        self.attack_frame_count = 1

        # Inventário para os itens colecionáveis
        self.inventory = {
            "Fire Ball": 0
        }

    def update(self):
        # Atualizar a posição do jogador com base nas teclas pressionadas
        keys = pygame.key.get_pressed()

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

        # Verificar se o jogador está atacando
        if keys[pygame.K_a]:
            self.attack()

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
            if pygame.sprite.spritecollide(self, dragons, False):
                for dragon in dragons.copy():  # Usamos copy() para iterar sobre uma cópia, pois vamos modificar o original
                    if pygame.sprite.collide_rect(self, dragon):
                        dragon.take_damage()
                        # Após derrotar o dragão, criar um item colecionável
                        create_collectible(dragon.rect.centerx, dragon.rect.bottom, "Fire Ball")
                        dragons.remove(dragon)  # Remove o dragão derrotado do grupo
                        all_sprites.remove(dragon)  # Remove também do grupo de todos os sprites

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

    def draw_inventory(self, screen):
        # Desenhar o inventário na tela
        font = pygame.font.Font(None, 24)
        text = font.render("Inventário:", True, WHITE)
        screen.blit(text, (10, 10))
        inventory_y = 30
        for item, count in self.inventory.items():
            item_text = font.render(f"{item}: {count}", True, WHITE)
            screen.blit(item_text, (10, inventory_y))
            inventory_y += 20

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

        # Controle de ataque do inimigo
        self.attack_cooldown = 100  # Tempo entre ataques em frames
        self.attack_timer = 0

    def update(self):
        # Movimento simples do inimigo
        self.rect.x -= self.speed

        # Atualiza o tempo do cooldown do ataque
        self.attack_timer += 1
        if self.attack_timer >= self.attack_cooldown:
            self.attack()
            self.attack_timer = 0

    def attack(self):
        # Cria uma nova bola de fogo (ataque)
        fireball = FireballAttack(self.rect.centerx - 20, self.rect.centery)  # Ajuste a posição inicial do ataque
        fireballs.add(fireball)
        all_sprites.add(fireball)

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

# Classe para os itens colecionáveis
class Collectible(pygame.sprite.Sprite):
    def __init__(self, x, y, item_type):
        super().__init__()

        # Carregar imagem do item colecionável
        if item_type == "Fire Ball":
            try:
                self.image = pygame.image.load('D:/colecio.png').convert_alpha()  # Ajuste o caminho conforme necessário
                # Redimensionar a imagem para um tamanho menor
                self.image = pygame.transform.scale(self.image, (30, 30))  # Ajuste o tamanho conforme necessário
            except pygame.error as e:
                print(f"Erro ao carregar a imagem 'fire_ball.webp': {e}")
                self.image = pygame.Surface((30, 30))  # Substitui a imagem com um retângulo simples
                self.image.fill(RED)  # Preenche com vermelho para indicar um erro visualmente

        self.rect = self.image.get_rect()
        self.rect.center = (x, y)
        self.time_to_live = 5000  # Tempo em milissegundos que o item permanecerá visível
        self.creation_time = pygame.time.get_ticks()

    def update(self):
        # Atualiza o tempo de vida do item
        current_time = pygame.time.get_ticks()
        if current_time - self.creation_time > self.time_to_live:
            self.kill()  # Remove o item da tela após o tempo de vida

    def draw(self, screen):
        # Desenhar o item colecionável na tela
        screen.blit(self.image, self.rect)

# Classe para o ataque de bola de fogo
class FireballAttack(pygame.sprite.Sprite):
    def __init__(self, x, y):
        super().__init__()
        # Carregar imagem da bola de fogo
        try:
            self.image = pygame.image.load('D:/ball_fire_attack.png').convert_alpha()  # Ajuste o caminho conforme necessário
            self.image = pygame.transform.scale(self.image, (30, 30))  # Ajuste o tamanho conforme necessário
        except pygame.error as e:
            print(f"Erro ao carregar a imagem 'fireball.png': {e}")
            self.image = pygame.Surface((30, 30))  # Substitui a imagem com um retângulo simples
            self.image.fill(RED)  # Preenche com vermelho para indicar um erro visualmente

        self.rect = self.image.get_rect()
        self.rect.center = (x, y)
        self.speed = 10  # Velocidade do ataque

    def update(self):
        # Movimento do ataque
        self.rect.x -= self.speed
        # Remove o ataque se sair da tela
        if self.rect.right < 0:
            self.kill()

    def draw(self, screen):
        # Desenhar o ataque na tela
        screen.blit(self.image, self.rect)

# Função para criar um novo item colecionável na tela
def create_collectible(x, y, item_type):
    collectible = Collectible(x, y, item_type)
    collectibles.add(collectible)
    all_sprites.add(collectible)

# Função para mostrar "Fim de Jogo"
def show_game_over(screen):
    font = pygame.font.Font(None, 36)
    text = font.render("Fim de Jogo", True, WHITE)
    text_rect = text.get_rect(center=(WIDTH // 2, HEIGHT // 2))
    screen.blit(text, text_rect)

# Criar jogador
player = Player()

# Criar os dois inimigos (dragões) para a fase atual
dragon1 = Enemy('D:/dragao.png', WIDTH - 100, HEIGHT // 2)  # Exemplo de posição e imagem do primeiro dragão
dragon2 = Enemy('D:/dragao2.png', WIDTH - 100, random.randint(50, HEIGHT - 50))  # Exemplo de posição e imagem do segundo dragão

# Lista dos dragões disponíveis na fase atual
dragons = pygame.sprite.Group()
dragons.add(dragon1, dragon2)

# Group para os sprites (jogador, inimigos e itens colecionáveis)
all_sprites = pygame.sprite.Group()
all_sprites.add(player)
all_sprites.add(dragons)

# Group para os itens colecionáveis
collectibles = pygame.sprite.Group()

# Group para os ataques de bola de fogo
fireballs = pygame.sprite.Group()

# Loop principal do jogo
running = True
while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

    # Atualizar sprites
    all_sprites.update()

    # Verificar colisões entre o jogador e os itens colecionáveis
    collected_items = pygame.sprite.spritecollide(player, collectibles, True)
    for item in collected_items:
        if isinstance(item, Collectible):
            if item.image.get_at((0, 0)) == RED:  # Verifica se a cor é a do item de erro (alternativa)
                continue
            player.inventory["Fire Ball"] += 1

    # Verificar colisões entre o jogador e os dragões
    if pygame.sprite.spritecollide(player, dragons, False):
        for dragon in dragons:
            if pygame.sprite.collide_rect(player, dragon):
                player.health -= 1
                dragon.take_damage()

    # Verificar colisões entre o jogador e os ataques de bola de fogo
    for fireball in fireballs:
        if pygame.sprite.collide_rect(player, fireball):
            player.health -= 5  # Ajuste o dano conforme necessário
            fireball.kill()  # Remove a bola de fogo após o impacto

    # Verificar fim de jogo
    if player.health <= 0:
        show_game_over(screen)
        pygame.display.flip()
        pygame.time.delay(2000)  # Espera 2 segundos
        break

    # Verificar se todos os dragões foram derrotados
    for dragon in dragons.copy():  # Usamos copy() para iterar sobre uma cópia, pois vamos modificar o original
        if dragon.health <= 0:
            dragons.remove(dragon)  # Remove o dragão derrotado do grupo
            all_sprites.remove(dragon)  # Remove também do grupo de todos os sprites
            create_collectible(dragon.rect.centerx, dragon.rect.bottom, "Fire Ball")  # Criar um item colecionável na posição do dragão

    # Desenhar elementos na tela
    screen.blit(background_image, (0, 0))  # Desenha o cenário de fundo na tela
    all_sprites.draw(screen)  # Desenha todos os sprites
    player.draw_health_bar(screen)  # Desenha a barra de vida do jogador
    player.draw_inventory(screen)  # Desenha o inventário do jogador

    for dragon in dragons:
        dragon.draw_health_bar(screen)  # Desenha a barra de vida dos dragões

    # Atualizar tela
    pygame.display.flip()

    # Controlar a taxa de atualização da tela
    pygame.time.Clock().tick(60)

# Finalizar o Pygame
pygame.quit()
sys.exit()
