import math
import pygame
from pygame.surface import Surface


class Projectile(pygame.sprite.Sprite):
    def __init__(
        self,
        x,
        y,
        angle,
        speed,
        color,
        initial_vx,
        initial_vy,
        size,
        damage,
        lifetime,
    ):
        super().__init__()
        self.x = x
        self.y = y
        self.angle = angle
        self.speed = speed
        self.color = color
        self.size = size
        self.damage = damage
        self.vx = initial_vx + speed * math.cos(math.radians(angle))
        self.vy = initial_vy - speed * math.sin(math.radians(angle))
        self.lifetime = lifetime

    def update(self):
        self.x += self.vx
        self.y += self.vy
        self.lifetime -= 1

    def draw(self, surface: Surface, position: tuple[int, int]):
        raise NotImplementedError("Subclasses must implement draw method")


class Bullet(Projectile):
    def __init__(self, x, y, angle, initial_vx, initial_vy):
        super().__init__(
            x, y, angle, 10, (255, 255, 0), initial_vx, initial_vy, 4, 2, 120
        )
        self.image = pygame.Surface((4, 4))
        self.image.fill((255, 255, 0))  # Yellow color
        self.rect = self.image.get_rect(center=(self.x, self.y))

    def update(self):
        super().update()
        self.rect.center = (self.x, self.y)

    def draw(self, surface: Surface, position: tuple[int, int]):
        pygame.draw.circle(surface, self.color, position, self.size)


class Missile(Projectile):
    def __init__(self, x, y, angle, initial_vx, initial_vy):
        super().__init__(
            x, y, angle, 5, (255, 0, 0), initial_vx, initial_vy, 8, 20, 120
        )
        self.image = pygame.Surface((8, 8))
        self.image.fill((255, 0, 0))  # Red color
        self.rect = self.image.get_rect(center=(self.x, self.y))

    def update(self):
        super().update()
        self.rect.center = (self.x, self.y)

    def draw(self, surface: Surface, position: tuple[int, int]):
        pygame.draw.rect(
            surface,
            self.color,
            (
                position[0] - self.size // 2,
                position[1] - self.size // 2,
                self.size,
                self.size,
            ),
        )
