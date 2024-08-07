import pygame
import random
import sys

# Inicializar o Pygame
pygame.init()

# Configurar tela
WIDTH, HEIGHT = 800, 600
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("A Guerra dos Tronos")

# Carregar imagem de fundo
background_image = pygame.image.load('D:/Users/tffg/Downloads/jogo-cin-ip-main/jogo-cin-ip-main/assets/fase_1/mapa.jpg').convert()
background_image = pygame.transform.scale(background_image, (WIDTH, HEIGHT))
tela_derrota_image = pygame.image.load('D:/Users/tffg/Downloads/jogo-cin-ip-main/jogo-cin-ip-main/assets/resultados/tela_derrota.png').convert_alpha()
tela_vitoria_image = pygame.image.load('D:/Users/tffg/Downloads/jogo-cin-ip-main/jogo-cin-ip-main/assets/resultados/tela_vitoria.png').convert_alpha()

# Carregar imagens da barra de vida
health_bar_full = pygame.image.load('D:/Users/tffg/Downloads/jogo-cin-ip-main/jogo-cin-ip-main/assets/fase_1/health_bar_full.png').convert_alpha()
health_bar_half = pygame.image.load('D:/Users/tffg/Downloads/jogo-cin-ip-main/jogo-cin-ip-main/assets/fase_1/health_bar_half.png').convert_alpha()
health_bar_low = pygame.image.load('D:/Users/tffg/Downloads/jogo-cin-ip-main/jogo-cin-ip-main/assets/fase_1/health_bar_low.png').convert_alpha()

# Redimensionar as imagens da barra de vida para o tamanho adequado
health_bar_full = pygame.transform.scale(health_bar_full, (60, 6))
health_bar_half = pygame.transform.scale(health_bar_half, (60, 6))
health_bar_low = pygame.transform.scale(health_bar_low, (60, 6))

# Definir cores
WHITE = (255, 255, 255)
GREEN = (0, 255, 0)
YELLOW = (255, 255, 0)
RED = (255, 0, 0)

# Classe para as armas
class Weapon(pygame.sprite.Sprite):
    def __init__(self, x, y, weapon_type, damage):
        super().__init__()
        self.weapon_type = weapon_type
        self.damage = damage
        if weapon_type == "True Shield":
            self.image = pygame.image.load('D:/Users/tffg/Downloads/jogo-cin-ip-main/jogo-cin-ip-main/assets/fase_1/true_shield.png').convert_alpha()
            self.image = pygame.transform.scale(self.image, (60, 60))  # Tamanho do escudo
        self.rect = self.image.get_rect()
        self.rect.center = (x, y)

# Classe do jogador
class Player(pygame.sprite.Sprite):
    def __init__(self):
        super().__init__()
        self.attack_images = [
            pygame.image.load('D:/Users/tffg/Downloads/jogo-cin-ip-main/jogo-cin-ip-main/assets/fase_1/Stannis baratheon.png').convert_alpha(),
            pygame.image.load('D:/Users/tffg/Downloads/jogo-cin-ip-main/jogo-cin-ip-main/assets/fase_1/Stannis baratheon.png').convert_alpha()
        ]
        self.image = self.attack_images[0]
        self.rect = self.image.get_rect()
        self.rect.center = (WIDTH // 4, HEIGHT // 2)
        self.speed = 2
        self.max_health = 100
        self.health = self.max_health
        self.is_attacking = False
        self.attack_index = 0
        self.attack_animation_speed = 10
        self.attack_frame_count = 1
        self.inventory = {
            "Fire Ball": 0,
            "True Shield": 0
        }
        self.current_weapon = None
        self.shield_active = False  # Controla se o escudo está ativo
        self.shield = None  # Guarda a instância do escudo

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

        # Atualiza a animação de ataque
        if self.is_attacking:
            self.attack()

        # Refletir projéteis se o escudo estiver ativo
        if self.shield_active:
            for fireball in fireballs:
                if pygame.sprite.collide_rect(self, fireball) and not fireball.reflected:
                    # Criar um novo projétil refletido
                    reflected_fireball = FireballAttack(fireball.rect.right, fireball.rect.centery, direction=1, reflected=True)
                    fireballs.add(reflected_fireball)
                    all_sprites.add(reflected_fireball)
                    fireball.kill()  # Remove o projétil original

                    # Contra-ataque: Atacar inimigos próximos
                    self.counter_attack()

        # Verificar se o jogador coleta armas
        collected_weapons = pygame.sprite.spritecollide(self, weapons, True)
        for weapon in collected_weapons:
            if weapon.weapon_type == "True Shield":
                self.inventory["True Shield"] += 1
                self.shield_active = True
                self.shield = weapon

        # Verificar se o jogador coleta itens colecionáveis
        collected_items = pygame.sprite.spritecollide(self, collectibles, True)
        for item in collected_items:
            if isinstance(item, Collectible):
                if item.item_type == "Fire Ball":
                    self.inventory["Fire Ball"] += 1
                elif item.item_type == "True Shield":
                    self.inventory["True Shield"] += 1
                    self.shield_active = True
                    self.shield = item

        # Atualizar a posição do escudo se estiver ativo
        if self.shield_active and self.shield:
            self.shield.rect.center = self.rect.center

        # Verificar colisão com projéteis
        for fireball in fireballs:
            if pygame.sprite.collide_rect(self, fireball):
                self.take_damage(10)  # Ajuste o dano conforme necessário
                fireball.kill()  # Remove o projétil após o impacto

        # Verificar colisão com dragões
        for dragon in dragons:
            if pygame.sprite.collide_rect(self, dragon):
                self.take_damage(10)  # Ajuste o dano conforme necessário

    def attack(self):
        # O jogador não causa dano
        self.is_attacking = True
        self.attack_frame_count += 1
        if self.attack_frame_count >= self.attack_animation_speed:
            self.attack_frame_count = 0
            self.attack_index += 1
            if self.attack_index >= len(self.attack_images):
                self.attack_index = 0
            self.image = self.attack_images[self.attack_index]
            self.is_attacking = False

    def counter_attack(self):
        # Realiza um contra-ataque em inimigos próximos
        for enemy in dragons:
            if self.rect.colliderect(enemy.rect.inflate(100, 100)):  # Área de ataque
                enemy.take_damage(10)  # Ajuste o dano conforme necessário

    def take_damage(self, damage):
        self.health -= damage
        if self.health <= 0:
            self.health = 0
            # Aqui você pode adicionar lógica para o fim do jogo
            # Por exemplo, você pode chamar uma função para mostrar "Game Over" e sair do jogo
            tela_derrota(screen)
            pygame.display.flip()
            pygame.time.delay(2000)
            pygame.quit()
            sys.exit()

    def draw(self, screen):
        screen.blit(self.image, self.rect)
        # Desenhar o escudo se estiver ativo
        if self.shield_active and self.shield:
            screen.blit(self.shield.image, self.shield.rect)

    def draw_health_bar(self, screen):
        bar_width = 60
        bar_height = 6
        bar_x = self.rect.centerx - bar_width // 2
        bar_y = self.rect.top - 20
        health_ratio = self.health / self.max_health

        # Usar a barra de vida padrão para o jogador
        if health_ratio > 0.66:
            screen.blit(health_bar_full, (bar_x, bar_y))
        elif health_ratio > 0.33:
            screen.blit(health_bar_half, (bar_x, bar_y))
        else:
            screen.blit(health_bar_low, (bar_x, bar_y))

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
            self.breath_fire()
            self.attack_timer = 0

    def breath_fire(self):
        fireball = FireballAttack(self.rect.left, self.rect.centery, direction=-1)  # Ajusta a posição para a boca do dragão
        fireballs.add(fireball)
        all_sprites.add(fireball)

    def draw(self, screen):
        screen.blit(self.image, self.rect)

    def draw_health_bar(self, screen):
        bar_width = 60
        bar_height = 6
        bar_x = self.rect.centerx - bar_width // 2
        bar_y = self.rect.top - 20
        health_ratio = self.health / self.max_health
        health_bar_width = int(bar_width * health_ratio)

        # Desenhar a barra de vida do dragão
        pygame.draw.rect(screen, RED, (bar_x, bar_y, bar_width, bar_height))  # Fundo vermelho
        pygame.draw.rect(screen, GREEN, (bar_x, bar_y, health_bar_width, bar_height))  # Vida restante verde


    def take_damage(self, damage):
        self.health -= damage
        if self.health <= 0:
            self.health = 0
            self.kill()  # Remove o dragão quando sua saúde chega a 0
            # Criar um item colecionável do tipo "Fire Ball" ao derrotar o dragão
            create_collectible(self.rect.centerx, self.rect.centery, "Fire Ball")

# Classe para itens colecionáveis
class Collectible(pygame.sprite.Sprite):
    def __init__(self, x, y, item_type):
        super().__init__()
        self.item_type = item_type
        if item_type == "Fire Ball":
            self.image = pygame.image.load('D:/Users/tffg/Downloads/jogo-cin-ip-main/jogo-cin-ip-main/assets/fase_1/colecio.png').convert_alpha()
            self.image = pygame.transform.scale(self.image, (30, 30))
        elif item_type == "True Shield":
            self.image = pygame.image.load('D:/Users/tffg/Downloads/jogo-cin-ip-main/jogo-cin-ip-main/assets/fase_1/true_shield.png').convert_alpha()
            self.image = pygame.transform.scale(self.image, (60, 60))  # Tamanho do escudo
        self.rect = self.image.get_rect()
        self.rect.center = (x, y)

# Classe para ataques de bola de fogo
class FireballAttack(pygame.sprite.Sprite):
    def __init__(self, x, y, direction, reflected=False):
        super().__init__()
        self.image = pygame.image.load('D:/Users/tffg/Downloads/jogo-cin-ip-main/jogo-cin-ip-main/assets/fase_1/ball_fire_attack.png').convert_alpha()
        self.image = pygame.transform.scale(self.image, (30, 30))
        self.rect = self.image.get_rect()
        self.rect.center = (x, y)
        self.speed = direction * 10  # Define a velocidade com base na direção
        self.reflected = reflected  # Adiciona um atributo para saber se o projétil é refletido

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

# Função para mostrar a tela de derrota
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

# Função para mostrar a tela de vitória
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


# Criar jogador
player = Player()

# Criar inimigos
dragon1 = Enemy('D:/Users/tffg/Downloads/jogo-cin-ip-main/jogo-cin-ip-main/assets/fase_1/dragao.png', WIDTH - 100, HEIGHT // 2)
dragon2 = Enemy('D:/Users/tffg/Downloads/jogo-cin-ip-main/jogo-cin-ip-main/assets/fase_1/dragao.png', WIDTH - 100, random.randint(50, HEIGHT - 50))

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

# Adicionar uma arma de escudo ao jogo
create_weapon(WIDTH // 2 + 50, HEIGHT // 2, "True Shield", 0)

# Loop principal do jogo
running = True
while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

    # Atualizar sprites
    all_sprites.update()

    # Verificar colisões entre projéteis refletidos e os dragões
    for fireball in fireballs:
        if fireball.reflected:
            collided_dragons = pygame.sprite.spritecollide(fireball, dragons, False)
            for dragon in collided_dragons:
                dragon.take_damage(10)  # Dano causado ao dragão
                fireball.kill()  # Remove o projétil refletido após colidir

    # Verificar fim de jogo
    if player.health <= 0:
        tela_derrota(screen)
        pygame.display.flip()
        pygame.time.delay(2000)
        running = False

    # Verificar vitória
    if player.inventory["Fire Ball"] >= 2 and player.inventory["True Shield"] >= 1:
        tela_vitoria(screen)
        pygame.display.flip()
        pygame.time.delay(2000)
        running = False

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
