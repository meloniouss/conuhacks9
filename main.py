import pygame
import random

# Initialize Pygame
pygame.init()

# Screen dimensions
WIDTH, HEIGHT = 800, 600
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Top-Down Shooter")

# Colors
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
RED = (255, 0, 0)
BLUE = (0, 0, 255)

# Player settings
player_size = 50
player_x = WIDTH // 2 - player_size // 2
player_y = HEIGHT // 2 - player_size // 2
player_speed = 5

# Projectile settings
projectile_speed = 7
projectiles = []

# Enemy settings
enemy_size = 40
enemy_speed = 3
enemies = []
enemy_spawn_delay = 60
enemy_spawn_counter = 0

# Clock
clock = pygame.time.Clock()

# Function to draw the player
def draw_player(x, y):
    pygame.draw.rect(screen, BLUE, (x, y, player_size, player_size))

# Function to draw projectiles
def draw_projectiles():
    for projectile in projectiles:
        pygame.draw.rect(screen, RED, projectile)

# Function to draw enemies
def draw_enemies():
    for enemy in enemies:
        pygame.draw.rect(screen, BLACK, enemy)

def move_projectiles():
    for projectile in projectiles:
        projectile.y -= projectile_speed
        if projectile.y < 0:
            projectiles.remove(projectile)

def move_enemies():
    for enemy in enemies:
        enemy.y += enemy_speed
        if enemy.y > HEIGHT:
            enemies.remove(enemy)

# Function to check for collisions
def check_collisions():
    for enemy in enemies:
        for projectile in projectiles:
            if projectile.colliderect(enemy):
                enemies.remove(enemy)
                projectiles.remove(projectile)
                break

# Game loop
running = True
while running:
    screen.fill(WHITE)

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_SPACE:
                projectiles.append(pygame.Rect(player_x + player_size // 2 - 5, player_y, 10, 20))

    # Player movement
    keys = pygame.key.get_pressed()
    if keys[pygame.K_LEFT] and player_x > 0:
        player_x -= player_speed
    if keys[pygame.K_RIGHT] and player_x < WIDTH - player_size:
        player_x += player_speed
    if keys[pygame.K_UP] and player_y > 0:
        player_y -= player_speed
    if keys[pygame.K_DOWN] and player_y < HEIGHT - player_size:
        player_y += player_speed

    # Spawn enemies
    enemy_spawn_counter += 1
    if enemy_spawn_counter >= enemy_spawn_delay:
        enemy_x = random.randint(0, WIDTH - enemy_size)
        enemies.append(pygame.Rect(enemy_x, 0, enemy_size, enemy_size))
        enemy_spawn_counter = 0

    # Move projectiles and enemies
    move_projectiles()
    move_enemies()

    # Check for collisions
    check_collisions()

    # Draw everything
    draw_player(player_x, player_y)
    draw_projectiles()
    draw_enemies()

    # Update the display
    pygame.display.flip()

    # Cap the frame rate
    clock.tick(60)

# Quit Pygame
pygame.quit()