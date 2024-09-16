import pygame
from helicopter import Helicopter

# Initialize Pygame
pygame.init()

# Set up the display
WIDTH, HEIGHT = 800, 600
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Desert Strike Clone")

# Colors
BLACK = (0, 0, 0)

# Create helicopter
heli = Helicopter(WIDTH, HEIGHT)

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
        heli.rotate(1)
    if keys[pygame.K_RIGHT]:
        heli.rotate(-1)
    if keys[pygame.K_UP]:
        heli.accelerate()
    else:
        heli.decelerate()
    if keys[pygame.K_SPACE]:
        heli.shoot()

    # Update game state
    heli.update()

    # Draw
    screen.fill(BLACK)
    heli.draw(screen)
    pygame.display.flip()

    # Cap the frame rate
    clock.tick(60)

pygame.quit()
