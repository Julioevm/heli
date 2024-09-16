import pygame
from game_map import GameMap

# Initialize Pygame
pygame.init()

# Set up the display
WIDTH, HEIGHT = 800, 600
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Desert Strike Clone")

# Colors
BLACK = (0, 0, 0)
WHITE = (255, 255, 255)

# Create game map
game_map = GameMap(WIDTH, HEIGHT)

# Game loop
running = True
clock = pygame.time.Clock()

while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

    # Handle input
    keys = pygame.key.get_pressed()
    if keys[pygame.K_LEFT]:
        game_map.helicopter.rotate(1)
    if keys[pygame.K_RIGHT]:
        game_map.helicopter.rotate(-1)
    if keys[pygame.K_UP]:
        game_map.helicopter.accelerate()
    else:
        game_map.helicopter.decelerate()
    if keys[pygame.K_SPACE]:
        game_map.helicopter.shoot()
    if keys[pygame.K_LCTRL] or keys[pygame.K_RCTRL]:
        game_map.helicopter.shoot_missile()
    if keys[pygame.K_ESCAPE]:
        running = False

    # Update game state
    game_map.update()

    # Draw
    screen.fill(BLACK)
    game_map.draw(screen)

    # Display enemy count
    font = pygame.font.Font(None, 36)
    enemy_count = font.render(f"Enemies: {len(game_map.enemies)}", True, WHITE)
    screen.blit(enemy_count, (10, 10))

    pygame.display.flip()

    # Cap the frame rate
    clock.tick(60)

pygame.quit()
