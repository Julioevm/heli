import random
import pygame
from pygame.surface import Surface


class Enemy:
    def __init__(self, width, height, size, health, color, damage):
        self.width = width
        self.height = height
        self.x = random.randint(0, width)
        self.y = random.randint(0, height)
        self.size = size
        self.health = health
        self.color = color
        self.damage = damage

    def update(self):
        # Simple movement: random walk
        self.x += random.randint(-2, 2)
        self.y += random.randint(-2, 2)
        self.x = max(0, min(self.x, self.width))
        self.y = max(0, min(self.y, self.height))

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

    def take_damage(self, damage):
        self.health -= damage
        return self.health <= 0


class Soldier(Enemy):
    def __init__(self, width, height):
        super().__init__(width, height, size=10, health=2, color=(0, 255, 0), damage=1)


class Tank(Enemy):
    def __init__(self, width, height):
        super().__init__(width, height, size=25, health=50, color=(0, 0, 255), damage=3)
