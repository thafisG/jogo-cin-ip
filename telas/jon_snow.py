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
background_image = pygame.image.load('D:/mapa.jpg').convert()
background_image = pygame.transform.scale(background_image, (WIDTH, HEIGHT))
tela_derrota_image = pygame.image.load('D:/tela_derrota.png').convert_alpha()
# Carregar imagem de tela de vitória
tela_vitoria_image = pygame.image.load('D:/tela_vitoria.png').convert_alpha()

# Carregar imagens das barras de vida
life_bar_images = {
    'full': pygame.image.load('D:/health_bar_full.png').convert_alpha(),
    'medium': pygame.image.load('D:/health_bar_half.png').convert_alpha(),
    'empty': pygame.image.load('D:/health_bar_low.png').convert_alpha()
}

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
        if weapon_type == "Sword":
            self.image = pygame.image.load('D:/true_sword.png').convert_alpha()
            self.image = pygame.transform.scale(self.image, (60, 60))  # Tamanho da espada
        self.rect = self.image.get_rect()
        self.rect.center = (x, y)

# Classe do jogador
class Player(pygame.sprite.Sprite):
    def __init__(self):
        super().__init__()
        self.attack_images = [
            pygame.image.load('D:/snow.png').convert_alpha(),
            pygame.image.load('D:/snow.png').convert_alpha()
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

        # Verificar se o jogador coleta itens colecionáveis
        collected_collectibles = pygame.sprite.spritecollide(self, collectibles, True)
        for collectible in collected_collectibles:
            if hasattr(collectible, 'item_type'):
                if collectible.item_type == "Fire Ball":
                    self.inventory["Fire Ball"] += 1

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
                    damage = self.current_weapon.damage * 2 if self.current_weapon else self.default_damage  # Dano aumentado se tiver espada
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
        # Determinar a imagem da barra de vida a ser usada
        health_percentage = self.health / self.max_health
        if health_percentage > 0.66:
            life_bar = life_bar_images['full']
        elif health_percentage > 0.33:
            life_bar = life_bar_images['medium']
        else:
            life_bar = life_bar_images['empty']

        # Reduzir a barra de vida para o tamanho pequeno desejado
        bar_width = 100
        bar_height = 10
        life_bar = pygame.transform.scale(life_bar, (bar_width, bar_height))
        bar_x = self.rect.centerx - bar_width // 2
        bar_y = self.rect.top - 20
        screen.blit(life_bar, (bar_x, bar_y))

    def draw_inventory(self, screen):
        font = pygame.font.Font(None, 24)
        text = font.render("Inventário:", True, WHITE)
        screen.blit(text, (10, 10))
        inventory_y = 30
        for item, count in self.inventory.items():
            item_text = font.render(f"{item}: {count}", True, WHITE)
            screen.blit(item_text, (10, inventory_y))
            inventory_y += 20

    def check_death(self):
        if self.health <= 0:
            return True
        return False

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
        self.item_type = item_type  # Atribuição do atributo item_type
        if item_type == "Fire Ball":
            try:
                self.image = pygame.image.load('D:/colecio.png').convert_alpha()
                self.image = pygame.transform.scale(self.image, (30, 30))
            except pygame.error as e:
                print(f"Erro ao carregar a imagem 'colecio.png': {e}")
                self.image = pygame.Surface((30, 30))
                self.image.fill(RED)
        elif item_type == "Sword":
            try:
                self.image = pygame.image.load('D:/true_sword.png').convert_alpha()
                self.image = pygame.transform.scale(self.image, (60, 60))
            except pygame.error as e:
                print(f"Erro ao carregar a imagem 'true_sword.png': {e}")
                self.image = pygame.Surface((60, 60))
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
            self.image = pygame.image.load('D:/ball_fire_attack.png').convert_alpha()
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

# Função para criar itens colecionáveis
def create_collectible(x, y, item_type):
    collectible = Collectible(x, y, item_type)
    collectibles.add(collectible)
    all_sprites.add(collectible)

# Função para exibir a tela de Game Over
def game_over_screen():
    screen.blit(tela_derrota_image, (0, 0))
    pygame.display.flip()
    pygame.time.wait(5000)  # Exibir tela de Game Over por 2 segundos
    pygame.quit()
    sys.exit()

# Função para exibir a tela de vitória
def victory_screen():
    screen.blit(tela_vitoria_image, (0, 0))
    pygame.display.flip()
    pygame.time.wait(5000)  # Exibir tela de vitória por 2 segundos
    pygame.quit()
    sys.exit()


# Grupos de sprites
all_sprites = pygame.sprite.Group()
weapons = pygame.sprite.Group()
dragons = pygame.sprite.Group()
fireballs = pygame.sprite.Group()
collectibles = pygame.sprite.Group()

# Criar jogador
player = Player()
all_sprites.add(player)

# Adicionar a true_sword no início
initial_sword = Weapon(WIDTH // 2, HEIGHT // 2, "Sword", 10)
weapons.add(initial_sword)
all_sprites.add(initial_sword)

# Criar inimigos (agora 2 dragões)
for i in range(2):
    enemy = Enemy('D:/dragao.png', random.randint(600, 800), random.randint(50, HEIGHT - 50))
    all_sprites.add(enemy)
    dragons.add(enemy)

# Main loop
# Main loop
clock = pygame.time.Clock()
while True:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            sys.exit()

    # Atualizar sprites
    all_sprites.update()

    # Verificar colisão do jogador com bolas de fogo e dragões
    hits = pygame.sprite.spritecollide(player, fireballs, True)
    for hit in hits:
        player.health -= 10  # Ajuste o dano conforme necessário
        if player.health <= 0:
            player.health = 0

    for dragon in dragons:
        if pygame.sprite.collide_rect(player, dragon):
            player.health -= 1  # Dano ainda mais reduzido ao contato com dragão
            if player.health <= 0:
                player.health = 0

    # Atualizar o inventário do jogador
    player.update()

    # Verificar se o jogador morreu
    if player.check_death():
        game_over_screen()

    # Verificar se todos os dragões foram derrotados
    if len(dragons) == 0:
        victory_screen()

    # Desenhar fundo e sprites
    screen.blit(background_image, (0, 0))
    all_sprites.draw(screen)

    # Desenhar barras de vida
    player.draw_health_bar(screen)
    for dragon in dragons:
        dragon.draw_health_bar(screen)

    # Desenhar inventário
    player.draw_inventory(screen)

    # Atualizar a tela
    pygame.display.flip()
    clock.tick(60)
