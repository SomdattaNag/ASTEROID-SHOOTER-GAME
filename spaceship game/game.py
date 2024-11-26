import pygame
import random


# Initialize Pygame
pygame.init()

# Screen dimensions
WIDTH, HEIGHT = 800, 700
screen = pygame.display.set_mode((WIDTH, HEIGHT))
NAVY_BLUE = (0, 0, 139)

# Load and scale the background image


# Colors
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
RED = (255, 0, 0)

# Load spaceship image
spaceship_img = pygame.image.load('spaceship.png')
spaceship_img = pygame.transform.scale(spaceship_img, (50, 50))

# Load asteroid image
asteroid_img = pygame.image.load('aesteroid.png')
asteroid_img = pygame.transform.scale(asteroid_img, (50, 50))

# Load sounds
pygame.mixer.music.load('Space Shooter Template Music.mp3')
bullet_sound = pygame.mixer.Sound('background_music.mp3')
explosion_sound = pygame.mixer.Sound('Explosion - Sound Effect.mp3')

# Fonts for text
font = pygame.font.SysFont(None, 36)
game_over_font = pygame.font.SysFont(None, 72)

# Background music
pygame.mixer.music.play(-1)  # Loop forever

# Sprite for the spaceship
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

# Sprite for the asteroids
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

# Sprite for bullets
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

# Initialize game variables
all_sprites = pygame.sprite.Group()
asteroids = pygame.sprite.Group()
bullets = pygame.sprite.Group()

spaceship = Spaceship()
all_sprites.add(spaceship)

for i in range(8):
    asteroid = Asteroid()
    all_sprites.add(asteroid)
    asteroids.add(asteroid)

clock = pygame.time.Clock()
score = 0
game_over = False
running = True

# Game loop
while running:
    clock.tick(60)  # Limit frame rate to 60 FPS

    # Event handling
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
        elif event.type == pygame.KEYDOWN:
            if event.key == pygame.K_SPACE:
                spaceship.shoot()

    # Update game objects
    if not game_over:
        all_sprites.update()

    # Collision detection between bullets and asteroids
    hits = pygame.sprite.groupcollide(asteroids, bullets, True, True)
    for hit in hits:
        score += 10
        explosion_sound.play()
        asteroid = Asteroid()
        all_sprites.add(asteroid)
        asteroids.add(asteroid)

    # Check if an asteroid hits the spaceship
    if pygame.sprite.spritecollideany(spaceship, asteroids):
        explosion_sound.play()
        game_over = True

    
    screen.fill(BLACK)
    # Draw all the sprites (spaceship, asteroids, bullets, etc.)
    all_sprites.draw(screen)

    # Draw score
    score_text = font.render(f"Score: {score}", True, WHITE)
    screen.blit(score_text, (10, 10))

    if game_over:
        # Display "Game Over" message
        game_over_text = game_over_font.render("Game Over", True, RED)
        screen.blit(game_over_text, (WIDTH // 2 - game_over_text.get_width() // 2, HEIGHT // 2 - game_over_text.get_height() // 2))

        # Wait for the player to quit by pressing 'Q'
        keys = pygame.key.get_pressed()
        if keys[pygame.K_q]:
            running = False

    # Flip the display to show everything
    pygame.display.flip()

# Quit Pygame
pygame.quit()
