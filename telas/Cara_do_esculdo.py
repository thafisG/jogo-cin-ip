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
background_image = pygame.image.load('Downloads/cenario.jpg').convert()
background_image = pygame.transform.scale(background_image, (WIDTH, HEIGHT))

# Definir cores
WHITE = (255, 255, 255)
GREEN = (0, 255, 0)
RED = (255, 0, 0)
BLUE = (0, 0, 255)

# Classe para as armas
class Weapon(pygame.sprite.Sprite):
    def __init__(self, x, y, weapon_type, damage):
        super().__init__()
        self.weapon_type = weapon_type
        self.damage = damage
        if weapon_type == "Shield":
            self.image = pygame.image.load('Downloads/true_shield1.png').convert_alpha()
            self.image = pygame.transform.scale(self.image, (60, 60))
        self.rect = self.image.get_rect()
        self.rect.center = (x, y)

# Classe do jogador
class Player(pygame.sprite.Sprite):
    def __init__(self):
        super().__init__()
        self.image = pygame.image.load('Downloads/anao.png').convert_alpha()
        self.rect = self.image.get_rect()
        self.rect.center = (WIDTH // 4, HEIGHT // 2)
        self.speed = 5
        self.max_health = 100
        self.health = self.max_health
        self.is_attacking = False
        self.has_shield = False
        self.inventory = {
            "Fire Ball": 0,
            "Shield": 0
        }
        self.current_weapon = None

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

        if keys[pygame.K_SPACE]:
            self.shoot()

        # Verificar se o jogador coleta armas
        collected_weapons = pygame.sprite.spritecollide(self, weapons, True)
        for weapon in collected_weapons:
            if weapon.weapon_type == "Shield":
                self.inventory["Shield"] += 1
                self.has_shield = True
                self.current_weapon = weapon

    def shoot(self):
        if self.inventory["Fire Ball"] > 0:
            fireball = FireballAttack(self.rect.right, self.rect.centery, "player")
            fireballs.add(fireball)
            all_sprites.add(fireball)
            self.inventory["Fire Ball"] -= 1

    def reflect_attack(self):
        if self.has_shield:
            reflected_fireballs = pygame.sprite.spritecollide(self, fireballs, False)
            for fireball in reflected_fireballs:
                if fireball.source == "enemy":
                    reflected_fireball = FireballAttack(self.rect.left, self.rect.centery, "player")
                    reflected_fireball.rect.center = fireball.rect.center
                    reflected_fireball.speed = -reflected_fireball.speed  # Inverter a direção
                    fireballs.add(reflected_fireball)
                    all_sprites.add(reflected_fireball)
                    fireball.kill()

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
        font = pygame.font.Font(None, 36)
        inventory_text = f"Fire Balls: {self.inventory['Fire Ball']}"
        inventory_surface = font.render(inventory_text, True, WHITE)
        screen.blit(inventory_surface, (10, 10))

# Classe para os inimigos
class Enemy(pygame.sprite.Sprite):
    def __init__(self, image_path, x, y):
        super().__init__()
        self.image = pygame.image.load(image_path).convert_alpha()
        self.rect = self.image.get_rect()
        self.rect.center = (x, y)
        self.speed = 1
        self.max_health = 50
        self.health = self.max_health
        self.attack_cooldown = 100
        self.attack_timer = 0

    def update(self):
        self.rect.x -= self.speed
        self.attack_timer += 1
        if self.attack_timer >= self.attack_cooldown:
            self.attack()
            self.attack_timer = 0

    def attack(self):
        fireball = FireballAttack(self.rect.centerx - 20, self.rect.centery, "enemy")
        fireballs.add(fireball)
        all_sprites.add(fireball)

    def take_damage(self, damage):
        self.health -= damage
        if self.health <= 0:
            self.kill()

    def draw_health_bar(self, screen):
        bar_width = 100
        bar_height = 10
        bar_x = self.rect.centerx - bar_width // 2
        bar_y = self.rect.top - 20
        health_ratio = self.health / self.max_health
        health_bar_width = int(bar_width * health_ratio)
        pygame.draw.rect(screen, RED, (bar_x, bar_y, bar_width, bar_height))
        pygame.draw.rect(screen, GREEN, (bar_x, bar_y, health_bar_width, bar_height))

# Classe para a bola de fogo
class FireballAttack(pygame.sprite.Sprite):
    def __init__(self, x, y, source):
        super().__init__()
        self.source = source
        try:
            self.image = pygame.image.load('Downloads/ball_fire_attack.png').convert_alpha()
            self.image = pygame.transform.scale(self.image, (30, 30))
        except pygame.error as e:
            print(f"Erro ao carregar a imagem 'ball_fire_attack.png': {e}")
            self.image = pygame.Surface((30, 30))
            self.image.fill(RED)
        self.rect = self.image.get_rect()
        self.rect.center = (x, y)
        self.speed = 10 if source == "player" else -5  # A direção negativa para inimigos

    def update(self):
        self.rect.x += self.speed
        if self.rect.right < 0 or self.rect.left > WIDTH:
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

# Exemplo de criar um escudo no chão
create_weapon(WIDTH // 2, HEIGHT // 2, "Shield", 0)

# Loop principal do jogo
clock = pygame.time.Clock()
running = True
while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

    # Atualizar sprites
    all_sprites.update()
    fireballs.update()
    collectibles.update()

    # Verificar colisões entre o jogador e os itens colecionáveis
    collected_items = pygame.sprite.spritecollide(player, collectibles, True)
    for item in collected_items:
        if isinstance(item, Collectible):
            if item.image.get_at((0, 0)) == RED:
                continue
            player.inventory["Fire Ball"] += 1

    # Verificar colisões entre o jogador e os dragões
    dragons_to_remove = []
    for dragon in dragons:
        if pygame.sprite.collide_rect(player, dragon):
            if not player.has_shield:
                player.health -= 1
            dragon.take_damage(player.current_weapon.damage if player.current_weapon else player.default_damage)
            if dragon.health <= 0:
                create_collectible(dragon.rect.centerx, dragon.rect.bottom, "Fire Ball")
                dragons_to_remove.append(dragon)
    
    for dragon in dragons_to_remove:
        dragons.remove(dragon)
        all_sprites.remove(dragon)

    # Verificar colisões entre o jogador e os ataques de bola de fogo
    player.reflect_attack()
    for fireball in fireballs:
        if pygame.sprite.collide_rect(player, fireball):
            if player.has_shield:
                player.health -= 1  # Dano reduzido ao jogador com o escudo
            else:
                player.health -= 5
            fireball.kill()

    # Verificar fim de jogo
    if player.health <= 0:
        show_game_over(screen)
        pygame.display.flip()
        pygame.time.delay(2000)
        break

    # Desenhar elementos na tela
    screen.blit(background_image, (0, 0))
    all_sprites.draw(screen)
    player.draw_health_bar(screen)
    player.draw_inventory(screen)
    for dragon in dragons:
        dragon.draw_health_bar(screen)

    pygame.display.flip()
    clock.tick(60)

pygame.quit()
sys.exit()
