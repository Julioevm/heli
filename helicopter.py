import math
import pygame
import os
from projectile import Bullet, Missile
from pygame.surface import Surface


class SpriteSheet:
    def __init__(self, folder_path):
        self.images = []
        try:
            for i in range(26):
                image_path = os.path.join(folder_path, f"capture_{i}.png")
                image = pygame.image.load(image_path).convert_alpha()
                self.images.append(image)
        except pygame.error as e:
            print(f"Unable to load image: {image_path}")
            raise SystemExit(e)


class Helicopter(pygame.sprite.Sprite):
    def __init__(self, x, y, angle):
        super().__init__()
        self.x = x
        self.y = y
        self.angle = angle
        self.vx = 0
        self.vy = 0
        self.max_speed = 5
        self.acceleration = 0.1
        self.deceleration = 0.05
        self.projectiles = []
        self.bullet_cooldown = 0
        self.bullet_delay = 5
        self.missile_cooldown = 0
        self.missile_delay = 30

        # Load images
        self.spritesheet = SpriteSheet("assets/helicopter")
        self.images = self.spritesheet.images

        self.image = self.images[0]
        self.rect = self.image.get_rect()

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
            # Add helicopter's velocity to the bullet's initial velocity
            initial_vx = self.vx + 10 * math.cos(math.radians(self.angle))
            initial_vy = self.vy - 10 * math.sin(math.radians(self.angle))
            self.projectiles.append(
                Bullet(projectile_x, projectile_y, self.angle, initial_vx, initial_vy)
            )
            self.bullet_cooldown = self.bullet_delay

    def shoot_missile(self):
        if self.missile_cooldown == 0:
            projectile_x = self.x + 30 * math.cos(math.radians(self.angle))
            projectile_y = self.y - 30 * math.sin(math.radians(self.angle))
            # Add helicopter's velocity to the missile's initial velocity
            initial_vx = self.vx + 5 * math.cos(math.radians(self.angle))
            initial_vy = self.vy - 5 * math.sin(math.radians(self.angle))
            self.projectiles.append(
                Missile(projectile_x, projectile_y, self.angle, initial_vx, initial_vy)
            )
            self.missile_cooldown = self.missile_delay

    def update(self):
        self.x += self.vx
        self.y += self.vy

        if self.bullet_cooldown > 0:
            self.bullet_cooldown -= 1

        if self.missile_cooldown > 0:
            self.missile_cooldown -= 1

        for projectile in self.projectiles[:]:
            projectile.update()
            if projectile.lifetime <= 0:
                self.projectiles.remove(projectile)

        # Update the helicopter's image based on its angle
        image_index = (round(self.angle / (360 / 26)) + 7) % 26
        self.image = self.images[image_index]

    def draw(self, surface: Surface, position: tuple[int, int]):
        # Draw shadow under the helicopter
        shadow_x = position[0] - 20  # Offset to the right
        shadow_y = position[1] + 40  # Offset down
        pygame.draw.ellipse(
            surface,
            (128, 128, 128),  # Gray color for shadow
            [shadow_x, shadow_y, 40, 20],
        )
        # Draw the helicopter sprite
        surface.blit(
            self.image,
            (
                position[0] - self.image.get_width() // 2,
                position[1] - self.image.get_height() // 2,
            ),
        )
