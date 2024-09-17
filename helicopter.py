import math
import pygame
from projectile import Bullet, Missile
from pygame.surface import Surface


class Helicopter:
    def __init__(self, width, height, x, y):
        self.width = width
        self.height = height
        self.x = x
        self.y = y
        self.angle = 0
        self.vx = 0
        self.vy = 0
        self.max_speed = 5
        self.acceleration = 0.1
        self.deceleration = 0.05
        self.projectiles = []
        self.bullet_cooldown = 0
        self.bullet_delay = 5  # frames between shots
        self.missile_cooldown = 0
        self.missile_delay = 30  # Longer delay between missile shots

    def rotate(self, direction):
        self.angle += direction * 3
        self.angle %= 360

    def accelerate(self):
        acceleration_x = self.acceleration * math.cos(math.radians(self.angle))
        acceleration_y = -self.acceleration * math.sin(math.radians(self.angle))
        self.vx += acceleration_x
        self.vy += acceleration_y
        speed = math.sqrt(self.vx**2 + self.vy**2)
        if speed > self.max_speed:
            scale = self.max_speed / speed
            self.vx *= scale
            self.vy *= scale

    def decelerate(self):
        speed = math.sqrt(self.vx**2 + self.vy**2)
        if speed > 0:
            scale = max(0, speed - self.deceleration) / speed
            self.vx *= scale
            self.vy *= scale

    def shoot(self):
        if self.bullet_cooldown == 0:
            projectile_x = self.x + 30 * math.cos(math.radians(self.angle))
            projectile_y = self.y - 30 * math.sin(math.radians(self.angle))
            self.projectiles.append(Bullet(projectile_x, projectile_y, self.angle))
            self.bullet_cooldown = self.bullet_delay

    def shoot_missile(self):
        if self.missile_cooldown == 0:
            projectile_x = self.x + 30 * math.cos(math.radians(self.angle))
            projectile_y = self.y - 30 * math.sin(math.radians(self.angle))
            self.projectiles.append(Missile(projectile_x, projectile_y, self.angle))
            self.missile_cooldown = self.missile_delay

    def update(self):
        self.x += self.vx
        self.y += self.vy

        # Ensure the helicopter stays within the screen bounds
        self.x = max(0, min(self.x, self.width))
        self.y = max(0, min(self.y, self.height))

        if self.bullet_cooldown > 0:
            self.bullet_cooldown -= 1

        if self.missile_cooldown > 0:
            self.missile_cooldown -= 1

        for projectile in self.projectiles[:]:
            projectile.update()
            if projectile.lifetime <= 0:
                self.projectiles.remove(projectile)

    def draw(self, surface: Surface, position: tuple[int, int]):
        pygame.draw.circle(surface, (255, 255, 255), position, 20)
        end_x = position[0] + 30 * math.cos(math.radians(self.angle))
        end_y = position[1] - 30 * math.sin(math.radians(self.angle))
        pygame.draw.line(surface, (255, 255, 255), position, (end_x, end_y), 3)
