import pygame
import random

#Setting up the game
pygame.init()
WIDTH, HEIGHT = 800, 700
screen = pygame.display.set_mode((WIDTH, HEIGHT))
NAVY_BLUE = (0, 0, 139)
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
RED = (255, 0, 0)
spaceship_img = pygame.image.load('images/spaceship.png')
spaceship_img = pygame.transform.scale(spaceship_img, (50, 50))
asteroid_img = pygame.image.load('images/aesteroid.png')
asteroid_img = pygame.transform.scale(asteroid_img, (50, 50))
pygame.mixer.music.load('sound/Space Shooter Template Music.mp3')
bullet_sound = pygame.mixer.Sound('sound/background_music.mp3')
explosion_sound = pygame.mixer.Sound('sound/Explosion - Sound Effect.mp3')
font = pygame.font.SysFont(None, 36)
game_over_font = pygame.font.SysFont(None, 72)
pygame.mixer.music.play(-1)  

#Defining Classes

class Spaceship(pygame.sprite.Sprite):
    def __init__(self):
        super().__init__()
        self.image = spaceship_img
        self.rect = self.image.get_rect()
        self.rect.x = WIDTH // 2 - self.rect.width // 2
        self.rect.y = HEIGHT - 60
        self.speed_x = 5
    
    def update(self):
        keys = pygame.key.get_pressed()
        if keys[pygame.K_LEFT]:
            self.rect.x -= self.speed_x
        if keys[pygame.K_RIGHT]:
            self.rect.x += self.speed_x
        self.rect.x = max(0, min(self.rect.x, WIDTH - self.rect.width))
    
    def shoot(self):
        bullet = Bullet(self.rect.centerx, self.rect.top)
        all_sprites.add(bullet)
        bullets.add(bullet)
        bullet_sound.play()


class Asteroid(pygame.sprite.Sprite):
    def __init__(self):
        super().__init__()
        self.image = asteroid_img
        self.rect = self.image.get_rect()
        self.rect.x = random.randint(0, WIDTH - self.rect.width)
        self.rect.y = random.randint(-100, -40)
        self.speed_y = random.randint(2, 6)
    
    def update(self):
        self.rect.y += self.speed_y
        if self.rect.top > HEIGHT:
            self.rect.y = random.randint(-100, -40)
            self.rect.x = random.randint(0, WIDTH - self.rect.width)


class Bullet(pygame.sprite.Sprite):
    def __init__(self, x, y):
        super().__init__()
        self.image = pygame.Surface((5, 10))
        self.image.fill(RED)
        self.rect = self.image.get_rect()
        self.rect.centerx = x
        self.rect.bottom = y
        self.speed_y = -10

    def update(self):
        self.rect.y += self.speed_y
        if self.rect.bottom < 0:
            self.kill()

#Initializing Sprite Groups
all_sprites = pygame.sprite.Group()
asteroids = pygame.sprite.Group()
bullets = pygame.sprite.Group()
spaceship = Spaceship()
all_sprites.add(spaceship)

#Setting asteroids
for i in range(8):
    asteroid = Asteroid()
    all_sprites.add(asteroid)
    asteroids.add(asteroid)

clock = pygame.time.Clock()
score = 0
game_over = False
running = True

#Game loop
while running:
    clock.tick(60)  
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
        elif event.type == pygame.KEYDOWN:
            if event.key == pygame.K_SPACE:
                spaceship.shoot()

    if not game_over:
        all_sprites.update()
    
    #Check for collisions between bullets and asteroids
    hits = pygame.sprite.groupcollide(asteroids, bullets, True, True)
    
    #Handling collisions between bullets and asteroids
    for hit in hits:
        score += 10
        explosion_sound.play()
        asteroid = Asteroid()
        all_sprites.add(asteroid)
        asteroids.add(asteroid)
    
    #Handling collisions between asteroids and spaceship
    if pygame.sprite.spritecollideany(spaceship, asteroids):
        explosion_sound.play()
        game_over = True
    
    screen.fill(BLACK)
    all_sprites.draw(screen)
    score_text = font.render(f"Score: {score}", True, WHITE) #display score
    screen.blit(score_text, (10, 10))

    if game_over:
        game_over_text = game_over_font.render("Game Over", True, RED)
        screen.blit(game_over_text, (WIDTH // 2 - game_over_text.get_width() // 2, HEIGHT // 2 - game_over_text.get_height() // 2))
        keys = pygame.key.get_pressed()
        if keys[pygame.K_q]:
            running = False

    pygame.display.flip()

pygame.quit()