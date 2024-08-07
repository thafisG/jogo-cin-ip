import pygame
import sys
import random

# Inicializar o Pygame
pygame.init()

# Configurar tela
WIDTH, HEIGHT = 800, 600
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("A Guerra dos Tronos")

# Carregar imagem de fundo
background_image = pygame.image.load('Downloads/mapa.jpg').convert()
background_image = pygame.transform.scale(background_image, (WIDTH, HEIGHT))
tela_derrota_image = pygame.image.load('Downloads/tela_derrota.png').convert_alpha()
tela_vitoria_image = pygame.image.load('Downloads/tela_vitoria.png').convert_alpha()
# Definir cores
WHITE = (255, 255, 255)
GREEN = (0, 255, 0)
RED = (255, 0, 0)
BLUE = (0, 0, 255)

# Carregar imagens da barra de vida
life_bar_images = {
    'full': pygame.image.load('Downloads/health_bar_full.png').convert_alpha(),
    'medium': pygame.image.load('Downloads/health_bar_half.png').convert_alpha(),
    'empty': pygame.image.load('Downloads/health_bar_low.png').convert_alpha()
}

# Redimensionar imagens da barra de vida
bar_width, bar_height = 60, 6
for key in life_bar_images:
    life_bar_images[key] = pygame.transform.scale(life_bar_images[key], (bar_width, bar_height))

class Player(pygame.sprite.Sprite):
    def __init__(self):
        super().__init__()
        self.attack_images = [
            pygame.image.load('Downloads/draca.png').convert_alpha(),
            pygame.image.load('Downloads/draca.png').convert_alpha()
        ]
        self.image = self.attack_images[0]
        self.rect = self.image.get_rect()
        self.rect.center = (WIDTH // 4, HEIGHT // 2)
        self.speed = 2
        self.max_health = 25
        self.health = self.max_health
        self.is_attacking = False
        self.attack_index = 0
        self.attack_animation_speed = 10
        self.attack_frame_count = 1
        self.inventory = {"Fire Ball": 0, "Ovo": 0}  # Adicionando "Ovo" ao inventário
        self.fireball_cooldown = 500  # Cooldown inicial em milissegundos
        self.fireball_timer = 0  # Temporizador para controle de cooldown
        self.double_shoot = False  # Flag para controle do disparo duplo

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

        # Disparar projéteis somente quando a tecla 'K' é pressionada
        if keys[pygame.K_k]:
            self.shoot()
        
        if keys[pygame.K_a]:
            self.attack()

        # Verificar colisão com inimigos
        self.check_collision_with_enemies()

    def attack(self):
        self.is_attacking = True
        self.attack_frame_count += 1
        if self.attack_frame_count >= self.attack_animation_speed:
            self.attack_frame_count = 0
            self.attack_index += 1
            if self.attack_index >= len(self.attack_images):
                self.attack_index = 0
            self.image = self.attack_images[self.attack_index]
            # Verificar se há colisão com dragões
            dragons_hit = pygame.sprite.spritecollide(self, dragons, False)
            for dragon in dragons_hit:
                dragon.take_damage()
                # Criar item "Fire Ball" quando o dragão é atacado
                create_collectible(dragon.rect.centerx, dragon.rect.bottom, "Fire Ball")
        else:
            self.is_attacking = False

    def shoot(self):
        current_time = pygame.time.get_ticks()
        if current_time - self.fireball_timer >= self.fireball_cooldown:
            if self.double_shoot:
                # Disparar dois projéteis
                fireball1 = FireballAttack(self.rect.right, self.rect.centery - 15, "player")
                fireball2 = FireballAttack(self.rect.right, self.rect.centery + 15, "player")
                fireballs.add(fireball1)
                fireballs.add(fireball2)
                all_sprites.add(fireball1)
                all_sprites.add(fireball2)
            else:
                # Disparar um projétil
                fireball = FireballAttack(self.rect.right, self.rect.centery, "player")
                fireballs.add(fireball)
                all_sprites.add(fireball)
            self.fireball_timer = current_time  # Atualiza o temporizador para o último disparo

    def draw(self, screen):
        screen.blit(self.image, self.rect)

    def draw_health_bar(self, screen):
        bar_x = self.rect.centerx - bar_width // 2
        bar_y = self.rect.top - 20

        # Determinar a imagem da barra de vida com base no nível de saúde
        if self.health > 0.66 * self.max_health:
            life_bar_image = life_bar_images['full']
        elif self.health > 0.33 * self.max_health:
            life_bar_image = life_bar_images['medium']
        else:
            life_bar_image = life_bar_images['empty']

        # Ajustar a posição e desenhar a imagem da barra de vida
        screen.blit(life_bar_image, (bar_x, bar_y))

    def draw_inventory(self, screen):
        font = pygame.font.Font(None, 24)
        text = font.render("Inventário:", True, WHITE)
        screen.blit(text, (10, 10))
        inventory_y = 30
        for item, count in self.inventory.items():
            item_text = font.render(f"{item}: {count}", True, WHITE)
            screen.blit(item_text, (10, inventory_y))
            inventory_y += 20

    def increase_fireball_speed(self):
        # Reduz o tempo de cooldown
        self.fireball_cooldown = max(100, self.fireball_cooldown - 100)  # O cooldown não pode ser menor que 100 ms

    def enable_double_shoot(self):
        # Ativa o disparo duplo
        self.double_shoot = True

    def check_collision_with_enemies(self):
        enemies_hit = pygame.sprite.spritecollide(self, dragons, False)
        for enemy in enemies_hit:
            self.take_damage()

    def take_damage(self):
        self.health -= 5  # Define o valor de dano a ser aplicado
        if self.health <= 0:
            self.health = 0  # Garantir que a saúde não fique negativa

class Enemy(pygame.sprite.Sprite):
    def __init__(self, image_path, x, y):
        super().__init__()
        self.image = pygame.image.load(image_path).convert_alpha()
        self.image = pygame.transform.scale(self.image, (150, 150))  # Redimensionar para tamanho médio
        self.rect = self.image.get_rect()
        self.rect.center = (x, y)
        self.speed = 1
        self.max_health = 50
        self.health = self.max_health
        self.attack_cooldown = 100
        self.attack_timer = 0
        self.reappearance_delay = 10000  # Tempo de reaparecimento em milissegundos
        self.reappearance_timer = 0
        self.is_reappearing = False

    def update(self):
        # Recolocar o dragão se sair da tela
        if self.rect.right < 0:
            self.rect.left = WIDTH
        elif self.rect.left > WIDTH:
            self.rect.right = 0
        elif self.rect.bottom < 0:
            self.rect.top = HEIGHT
        elif self.rect.top > HEIGHT:
            self.rect.bottom = 0

        # Mover e atacar
        self.rect.x -= self.speed
        self.attack_timer += 1
        if self.attack_timer >= self.attack_cooldown:
            self.attack()
            self.attack_timer = 0

    def attack(self):
        fireball = FireballAttack(self.rect.centerx - 20, self.rect.centery, "enemy")
        fireballs.add(fireball)
        all_sprites.add(fireball)

    def draw(self, screen):
        screen.blit(self.image, self.rect)

    def draw_health_bar(self, screen):
        bar_x = self.rect.centerx - bar_width // 2
        bar_y = self.rect.top - 20
        health_ratio = self.health / self.max_health
        health_bar_width = int(bar_width * health_ratio)
        pygame.draw.rect(screen, RED, (bar_x, bar_y, bar_width, bar_height))
        pygame.draw.rect(screen, GREEN, (bar_x, bar_y, health_bar_width, bar_height))

    def take_damage(self):
        self.health -= 10
        if self.health <= 0:
            self.kill()
            # Criar item "Fire Ball" quando o dragão é derrotado
            create_collectible(self.rect.centerx, self.rect.bottom, "Fire Ball")
            # Não reaparecer se a vida chegar a 0
            self.reappearance_delay = 0

class Collectible(pygame.sprite.Sprite):
    def __init__(self, x, y, item_type):
        super().__init__()
        self.item_type = item_type
        if item_type == "Fire Ball":
            try:
                self.image = pygame.image.load('Downloads/colecio.png').convert_alpha()
                self.image = pygame.transform.scale(self.image, (30, 30))
            except pygame.error as e:
                print(f"Erro ao carregar a imagem 'fireball.png': {e}")
                self.image = pygame.Surface((30, 30))
                self.image.fill(RED)
        elif item_type == "Ovo":
            try:
                self.image = pygame.image.load('Downloads/ovo.png').convert_alpha()
                self.image = pygame.transform.scale(self.image, (30, 30))
            except pygame.error as e:
                print(f"Erro ao carregar a imagem 'ovo.png': {e}")
                self.image = pygame.Surface((30, 30))
                self.image.fill(BLUE)
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

class FireballAttack(pygame.sprite.Sprite):
    def __init__(self, x, y, source):
        super().__init__()
        self.source = source
        try:
            self.image = pygame.image.load('Downloads/ball_fire_attack.png').convert_alpha()
            self.image = pygame.transform.scale(self.image, (30, 30))
        except pygame.error as e:
            print(f"Erro ao carregar a imagem 'fireball.png': {e}")
            self.image = pygame.Surface((30, 30))
            self.image.fill(RED)
        self.rect = self.image.get_rect()
        self.rect.center = (x, y)
        self.speed = 5

    def update(self):
        if self.source == "player":
            self.rect.x += self.speed
        else:
            self.rect.x -= self.speed
        if self.rect.right < 0 or self.rect.left > WIDTH:
            self.kill()

    def draw(self, screen):
        screen.blit(self.image, self.rect)

def create_collectible(x, y, item_type):
    collectible = Collectible(x, y, item_type)
    collectibles.add(collectible)
    all_sprites.add(collectible)

def tela_derrota(screen):
    screen.blit(tela_derrota_image, (0, 0))
    pygame.display.flip()
    waiting = True
    while waiting:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_ESCAPE:
                    pygame.quit()
                    sys.exit()

def tela_vitoria(screen):
    screen.blit(tela_vitoria_image, (0, 0))
    pygame.display.flip()
    waiting = True
    while waiting:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_ESCAPE:
                    pygame.quit()
                    sys.exit()
                elif event.key == pygame.K_RETURN:  # Pressione Enter para sair da tela de vitória
                    waiting = False

player = Player()

dragon1 = Enemy('Downloads/dragao.png', WIDTH - 100, HEIGHT // 2)
dragon2 = Enemy('Downloads/dragao2.png', WIDTH - 100, random.randint(50, HEIGHT - 50))

dragons = pygame.sprite.Group()
dragons.add(dragon1, dragon2)

all_sprites = pygame.sprite.Group()
all_sprites.add(player)
all_sprites.add(dragon1)
all_sprites.add(dragon2)

collectibles = pygame.sprite.Group()
fireballs = pygame.sprite.Group()

# Criar item "Ovo" no início do jogo
create_collectible(WIDTH // 2, HEIGHT // 2, "Ovo")
# Adicione uma variável para controlar se a tela de vitória foi exibida
victory_screen_shown = False

running = True
while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

    all_sprites.update()

    collected_items = pygame.sprite.spritecollide(player, collectibles, True)
    for item in collected_items:
        if isinstance(item, Collectible):
            if item.item_type == "Fire Ball":
                player.inventory["Fire Ball"] += 1
            elif item.item_type == "Ovo":
                player.inventory["Ovo"] += 1
                player.enable_double_shoot()  # Habilita o disparo duplo após pegar o item "Ovo"
                player.increase_fireball_speed()  # Aumenta a velocidade do disparo

    # Verificar a condição de vitória após a coleta de itens
    if not victory_screen_shown and (player.inventory["Fire Ball"] >= 2 or player.inventory["Ovo"] > 1):
        tela_vitoria(screen)
        victory_screen_shown = True  # Evita que a tela de vitória seja exibida repetidamente
        running = False  # Finaliza o loop para mostrar a tela de vitória

    for fireball in fireballs.copy():
        if fireball.source == "player":
            dragons_hit = pygame.sprite.spritecollide(fireball, dragons, False)
            for dragon in dragons_hit:
                dragon.take_damage()
                fireball.kill()
        elif fireball.source == "enemy":
            if pygame.sprite.collide_rect(player, fireball):
                player.take_damage()
                fireball.kill()

    if player.health <= 0:
        tela_derrota(screen)
        running = False

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
