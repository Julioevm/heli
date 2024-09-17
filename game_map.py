import pygame
from helicopter import Helicopter
from enemy import Soldier, Tank
from pytmx.util_pygame import load_pygame


class GameMap:
    def __init__(self, width, height):
        self.width = width
        self.height = height
        self.helicopter = Helicopter(width, height)
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

                # Center the map
                center_offset_x = self.width // 2 - self.tile_width // 2
                center_offset_y = self.tile_height

                # Draw the tile
                surface.blit(tile, (iso_x + center_offset_x, iso_y + center_offset_y))

        # Draw enemies (you may need to adjust their positions for isometric view)
        for enemy in self.enemies:
            enemy.draw(surface)

        # Draw helicopter projectiles (may need position adjustment)
        for projectile in self.helicopter.projectiles:
            projectile.draw(surface)

        # Draw helicopter (may need position adjustment)
        self.helicopter.draw(surface)

    @staticmethod
    def check_collision(projectile, enemy):
        return (
            abs(projectile.x - enemy.x) < enemy.size // 2
            and abs(projectile.y - enemy.y) < enemy.size // 2
        )
