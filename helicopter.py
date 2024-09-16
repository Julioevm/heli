import math
import pygame


class Projectile:
    def __init__(self, x, y, angle, speed, lifetime, color, size):
        self.x = x
        self.y = y
        self.angle = angle
        self.speed = speed
        self.lifetime = lifetime
        self.color = color
        self.size = size

    def update(self):
        self.x += self.speed * math.cos(math.radians(self.angle))
        self.y -= self.speed * math.sin(math.radians(self.angle))
        self.lifetime -= 1

    def draw(self, surface):
        raise NotImplementedError("Subclasses must implement draw method")


class Bullet(Projectile):
    def __init__(self, x, y, angle):
        super().__init__(
            x, y, angle, speed=10, lifetime=60, color=(255, 255, 0), size=3
        )

    def draw(self, surface):
        pygame.draw.circle(surface, self.color, (int(self.x), int(self.y)), self.size)


class Missile(Projectile):
    def __init__(self, x, y, angle):
        super().__init__(x, y, angle, speed=5, lifetime=120, color=(255, 0, 0), size=6)
        self.damage = 3  # More damage than bullets

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

    def draw(self, surface):
        pygame.draw.circle(surface, (255, 255, 255), (int(self.x), int(self.y)), 20)
        end_x = self.x + 30 * math.cos(math.radians(self.angle))
        end_y = self.y - 30 * math.sin(math.radians(self.angle))
        pygame.draw.line(surface, (255, 255, 255), (self.x, self.y), (end_x, end_y), 3)
        for projectile in self.projectiles:
            projectile.draw(surface)
