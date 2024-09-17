from helicopter import Helicopter
from enemy import Soldier, Tank
from pytmx.util_pygame import load_pygame
from camera import Camera


class GameMap:
    def __init__(self, width, height):
        self.width = width
        self.height = height
        self.helicopter = Helicopter(
            width, height, width // 2, height // 2
        )  # Start at center
        self.camera = Camera(width, height)
        self.enemies = []
        self.spawn_enemies()
        self.tmx_data = load_pygame("assets/maps/test map.tmx")
        self.map_data = self.tmx_data.get_layer_by_name("Tile Layer 1")
        self.tileset = self.tmx_data.get_tileset_from_gid(1)
        self.tile_width = self.tileset.tilewidth
        self.tile_height = self.tileset.tileheight

    def spawn_enemies(self):
        for _ in range(8):  # Create 8 soldiers
            self.enemies.append(Soldier(self.width, self.height))
        for _ in range(3):  # Create 3 tanks
            self.enemies.append(Tank(self.width, self.height))

    def update(self):
        self.helicopter.update()
        self.camera.update(self.helicopter)

        for enemy in self.enemies[:]:
            enemy.update()
            for projectile in self.helicopter.projectiles[:]:
                if self.check_collision(projectile, enemy):
                    if enemy.take_damage(projectile.damage):
                        self.enemies.remove(enemy)
                    self.helicopter.projectiles.remove(projectile)

    def draw(self, surface):
        # Draw the tilemap in isometric view
        for x, y, gid in self.map_data:
            tile = self.tmx_data.get_tile_image_by_gid(gid)
            if tile:
                # Calculate isometric position
                iso_x = (x - y) * self.tile_width // 2
                iso_y = (x + y) * self.tile_height // 4

                # Apply camera offset
                screen_x = iso_x + self.camera.x
                screen_y = iso_y + self.camera.y

                # Draw the tile if it's on screen
                if (
                    -self.tile_width <= screen_x <= self.width
                    and -self.tile_height <= screen_y <= self.height
                ):
                    surface.blit(tile, (screen_x, screen_y))

        # Draw enemies
        for enemy in self.enemies:
            enemy_pos = (enemy.x + self.camera.x, enemy.y + self.camera.y)
            enemy.draw(surface, enemy_pos)

        # Draw helicopter projectiles
        for projectile in self.helicopter.projectiles:
            projectile_pos = (
                projectile.x + self.camera.x,
                projectile.y + self.camera.y,
            )
            projectile.draw(surface, projectile_pos)

        # Draw helicopter
        heli_pos = (
            self.helicopter.x + self.camera.x,
            self.helicopter.y + self.camera.y,
        )
        self.helicopter.draw(surface, heli_pos)

    @staticmethod
    def check_collision(projectile, enemy):
        return (
            abs(projectile.x - enemy.x) < enemy.size // 2
            and abs(projectile.y - enemy.y) < enemy.size // 2
        )
