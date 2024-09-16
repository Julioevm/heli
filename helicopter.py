import math
import pygame


class Bullet:
    def __init__(self, x, y, angle):
        self.x = x
        self.y = y
        self.angle = angle
        self.speed = 10
        self.lifetime = 60  # frames

    def update(self):
        self.x += self.speed * math.cos(math.radians(self.angle))
        self.y -= self.speed * math.sin(math.radians(self.angle))
        self.lifetime -= 1

    def draw(self, surface):
        pygame.draw.circle(surface, (255, 255, 0), (int(self.x), int(self.y)), 3)


class Helicopter:
    def __init__(self, width, height):
        self.width = width
        self.height = height
        self.x = width // 2
        self.y = height // 2
        self.angle = 0
        self.vx = 0
        self.vy = 0
        self.max_speed = 5
        self.acceleration = 0.1
        self.deceleration = 0.05
        self.bullets = []
        self.shoot_cooldown = 0
        self.shoot_delay = 5  # frames between shots

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
        if self.shoot_cooldown == 0:
            bullet_x = self.x + 30 * math.cos(math.radians(self.angle))
            bullet_y = self.y - 30 * math.sin(math.radians(self.angle))
            self.bullets.append(Bullet(bullet_x, bullet_y, self.angle))
            self.shoot_cooldown = self.shoot_delay

    def update(self):
        self.x += self.vx
        self.y += self.vy

        # Ensure the helicopter stays within the screen bounds
        self.x = max(0, min(self.x, self.width))
        self.y = max(0, min(self.y, self.height))

        if self.shoot_cooldown > 0:
            self.shoot_cooldown -= 1

        for bullet in self.bullets[:]:
            bullet.update()
            if bullet.lifetime <= 0:
                self.bullets.remove(bullet)

    def draw(self, surface):
        pygame.draw.circle(surface, (255, 255, 255), (int(self.x), int(self.y)), 20)
        end_x = self.x + 30 * math.cos(math.radians(self.angle))
        end_y = self.y - 30 * math.sin(math.radians(self.angle))
        pygame.draw.line(surface, (255, 255, 255), (self.x, self.y), (end_x, end_y), 3)
        for bullet in self.bullets:
            bullet.draw(surface)
