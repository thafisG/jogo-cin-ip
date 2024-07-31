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
background_image = pygame.image.load('Downloads/mapa.jpg').convert()
background_image = pygame.transform.scale(background_image, (WIDTH, HEIGHT))

# Definir cores
WHITE = (255, 255, 255)
GREEN = (0, 255, 0)
RED = (255, 0, 0)
BLUE = (0, 0, 255)

# Variável de controle de fase
current_phase = 1

# Classe para as armas
class Weapon(pygame.sprite.Sprite):
    def __init__(self, x, y, weapon_type, damage):
        super().__init__()
        self.weapon_type = weapon_type
        self.damage = damage
        if weapon_type == "Sword":
            self.image = pygame.image.load('Downloads/true_sword.png').convert_alpha()
            self.image = pygame.transform.scale(self.image, (60, 60))  # Tamanho da espada
        self.rect = self.image.get_rect()
        self.rect.center = (x, y)

# Classe do jogador
class Player(pygame.sprite.Sprite):
    def __init__(self):
        super().__init__()
        self.attack_images = [
            pygame.image.load('Downloads/snow.png').convert_alpha(),
            pygame.image.load('Downloads/snow.png').convert_alpha()
        ]
        self.image = self.attack_images[0]
        self.rect = self.image.get_rect()
        self.rect.center = (WIDTH // 4, HEIGHT // 2)
        self.speed = 1
        self.max_health = 100
        self.health = self.max_health
        self.is_attacking = False
        self.attack_index = 0
        self.attack_animation_speed = 10
        self.attack_frame_count = 1
        self.inventory = {
            "Fire Ball": 0,
            "Sword": 0
        }
        self.current_weapon = None
        self.default_damage = 5

    def update(self):
        keys = pygame.key.get_pressed()
        if keys[pygame.K_LEFT]:
            self.rect.x -= self.speed
        if keys[pygame.K_RIGHT]:
            self.rect.x += self.speed
        if keys[pygame.K_UP]:
            self.rect.y -= self.speed
        if keys[pygame.K_DOWN]:
            self.rect.y += self.speed

        self.rect.x = max(0, min(WIDTH - self.rect.width, self.rect.x))
        self.rect.y = max(0, min(HEIGHT - self.rect.height, self.rect.y))

        if keys[pygame.K_k]:
            self.attack()

        # Verificar se o jogador coleta armas
        collected_weapons = pygame.sprite.spritecollide(self, weapons, True)
        for weapon in collected_weapons:
            if weapon.weapon_type == "Sword":
                self.inventory["Sword"] += 1
                self.current_weapon = weapon

    def attack(self):
        self.is_attacking = True
        self.attack_frame_count += 1
        if self.attack_frame_count >= self.attack_animation_speed:
            self.attack_frame_count = 0
            self.attack_index += 1
            if self.attack_index >= len(self.attack_images):
                self.attack_index = 0
            self.image = self.attack_images[self.attack_index]

            dragons_to_remove = []
            for dragon in dragons:
                if pygame.sprite.collide_rect(self, dragon):
                    damage = self.current_weapon.damage if self.current_weapon else self.default_damage
                    dragon.take_damage(damage)
                    if dragon.health <= 0:
                        create_collectible(dragon.rect.centerx, dragon.rect.bottom, "Fire Ball")
                        dragons_to_remove.append(dragon)
            
            for dragon in dragons_to_remove:
                dragons.remove(dragon)
                all_sprites.remove(dragon)
        else:
            self.is_attacking = False

    def draw(self, screen):
        screen.blit(self.image, self.rect)

    def draw_health_bar(self, screen):
        bar_width = 100
        bar_height = 10
        bar_x = self.rect.centerx - bar_width // 2
        bar_y = self.rect.top - 20
        health_ratio = self.health / self.max_health
        health_bar_width = int(bar_width * health_ratio)
        pygame.draw.rect(screen, RED, (bar_x, bar_y, bar_width, bar_height))
        pygame.draw.rect(screen, GREEN, (bar_x, bar_y, health_bar_width, bar_height))

    def draw_inventory(self, screen):
        font = pygame.font.Font(None, 24)
        text = font.render("Inventário:", True, WHITE)
        screen.blit(text, (10, 10))
        inventory_y = 30
        for item, count in self.inventory.items():
            item_text = font.render(f"{item}: {count}", True, WHITE)
            screen.blit(item_text, (10, inventory_y))
            inventory_y += 20

# Classe para o inimigo (dragão)
class Enemy(pygame.sprite.Sprite):
    def __init__(self, image_path, x, y):
        super().__init__()
        self.image = pygame.image.load(image_path).convert_alpha()
        self.image = pygame.transform.scale(self.image, (100, 100))  # Tamanho médio do dragão
        self.rect = self.image.get_rect()
        self.rect.center = (x, y)
        self.speed = 1
        self.max_health = 50
        self.health = self.max_health
        self.attack_cooldown = 100
        self.attack_timer = 0

    def update(self):
        self.rect.x -= self.speed
        if self.rect.right < 0:  # Quando o dragão sair pelo lado esquerdo da tela
            self.rect.left = WIDTH  # Reposiciona o dragão na borda direita
        self.attack_timer += 1
        if self.attack_timer >= self.attack_cooldown:
            self.attack()
            self.attack_timer = 0

    def attack(self):
        fireball = FireballAttack(self.rect.centerx - 20, self.rect.centery)
        fireballs.add(fireball)
        all_sprites.add(fireball)

    def draw(self, screen):
        screen.blit(self.image, self.rect)

    def draw_health_bar(self, screen):
        bar_width = 100
        bar_height = 10
        bar_x = self.rect.centerx - bar_width // 2
        bar_y = self.rect.top - 20
        health_ratio = self.health / self.max_health
        health_bar_width = int(bar_width * health_ratio)
        pygame.draw.rect(screen, RED, (bar_x, bar_y, bar_width, bar_height))
        pygame.draw.rect(screen, GREEN, (bar_x, bar_y, health_bar_width, bar_height))

    def take_damage(self, damage):
        self.health -= damage
        if self.health <= 0:
            self.health = 0

# Classe para itens colecionáveis
class Collectible(pygame.sprite.Sprite):
    def __init__(self, x, y, item_type):
        super().__init__()
        if item_type == "Fire Ball":
            try:
                self.image = pygame.image.load('Downloads/colecio.png').convert_alpha()
                self.image = pygame.transform.scale(self.image, (30, 30))
            except pygame.error as e:
                print(f"Erro ao carregar a imagem 'colecio.png': {e}")
                self.image = pygame.Surface((30, 30))
                self.image.fill(RED)
        self.rect = self.image.get_rect()
        self.rect.center = (x, y)
        self.time_to_live = 5000
        self.creation_time = pygame.time.get_ticks()

    def update(self):
        current_time = pygame.time.get_ticks()
        if current_time - self.creation_time > self.time_to_live:
            self.kill()

    def draw(self, screen):
        screen.blit(self.image, self.rect)

# Classe para o ataque de bola de fogo
class FireballAttack(pygame.sprite.Sprite):
    def __init__(self, x, y):
        super().__init__()
        try:
            self.image = pygame.image.load('Downloads/ball_fire_attack.png').convert_alpha()
            self.image = pygame.transform.scale(self.image, (30, 30))
        except pygame.error as e:
            print(f"Erro ao carregar a imagem 'ball_fire_attack.png': {e}")
            self.image = pygame.Surface((30, 30))
            self.image.fill(RED)
        self.rect = self.image.get_rect()
        self.rect.center = (x, y)
        self.speed = 10

    def update(self):
        self.rect.x -= self.speed
        if self.rect.right < 0:
            self.kill()

    def draw(self, screen):
        screen.blit(self.image, self.rect)

# Função para criar um novo item colecionável na tela
def create_collectible(x, y, item_type):
    collectible = Collectible(x, y, item_type)
    collectibles.add(collectible)
    all_sprites.add(collectible)

# Função para criar uma nova arma na tela
def create_weapon(x, y, weapon_type, damage):
    weapon = Weapon(x, y, weapon_type, damage)
    weapons.add(weapon)
    all_sprites.add(weapon)

# Função para mostrar "Fim de Jogo"
def show_game_over(screen):
    font = pygame.font.Font(None, 36)
    text = font.render("Fim de Jogo", True, WHITE)
    text_rect = text.get_rect(center=(WIDTH // 2, HEIGHT // 2))
    screen.blit(text, text_rect)

# Criar jogador
player = Player()

# Criar inimigos
dragon1 = Enemy('Downloads/dragao.png', WIDTH - 100, HEIGHT // 2)
dragon2 = Enemy('Downloads/dragao2.png', WIDTH - 100, random.randint(50, HEIGHT - 50))

# Lista dos dragões
dragons = pygame.sprite.Group()
dragons.add(dragon1, dragon2)

# Grupo para os sprites
all_sprites = pygame.sprite.Group()
all_sprites.add(player)
all_sprites.add(dragons)

# Grupo para os itens colecionáveis
collectibles = pygame.sprite.Group()

# Grupo para as armas
weapons = pygame.sprite.Group()

# Grupo para os ataques de bola de fogo
fireballs = pygame.sprite.Group()

# Exemplo de criar uma arma no chão
create_weapon(WIDTH // 2, HEIGHT // 2, "Sword", 20)

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
            if item.image.get_at((0, 0)) == RED:
                continue
            player.inventory["Fire Ball"] += 1

    # Verificar colisões entre o jogador e os ataques de bola de fogo
    for fireball in fireballs:
        if pygame.sprite.collide_rect(player, fireball):
            player.health -= 5
            fireball.kill()

    # Verificar fim de jogo
    if player.health <= 0:
        show_game_over(screen)
        pygame.display.flip()
        pygame.time.delay(2000)
        

    # Desenhar elementos na tela
    screen.blit(background_image, (0, 0))
    all_sprites.draw(screen)
    player.draw_health_bar(screen)
    player.draw_inventory(screen)
    for dragon in dragons:
        dragon.draw_health_bar(screen)

    pygame.display.flip()
    pygame.time.Clock().tick(60)

pygame.quit()
sys.exit()
