import math
import pygame


class Projectile:
    def __init__(self, x, y, angle, speed, lifetime, color, size, damage):
        self.x = x
        self.y = y
        self.angle = angle
        self.speed = speed
        self.lifetime = lifetime
        self.color = color
        self.size = size
        self.damage = damage

    def update(self):
        self.x += self.speed * math.cos(math.radians(self.angle))
        self.y -= self.speed * math.sin(math.radians(self.angle))
        self.lifetime -= 1

    def draw(self, surface):
        raise NotImplementedError("Subclasses must implement draw method")


class Bullet(Projectile):
    def __init__(self, x, y, angle):
        super().__init__(
            x, y, angle, speed=10, lifetime=60, color=(255, 255, 0), size=3, damage=2
        )

    def draw(self, surface):
        pygame.draw.circle(surface, self.color, (int(self.x), int(self.y)), self.size)


class Missile(Projectile):
    def __init__(self, x, y, angle):
        super().__init__(
            x, y, angle, speed=5, lifetime=120, color=(255, 0, 0), size=6, damage=20
        )

    def draw(self, surface):
        pygame.draw.rect(
            surface,
            self.color,
            (
                int(self.x) - self.size // 2,
                int(self.y) - self.size // 2,
                self.size,
                self.size,
            ),
        )
