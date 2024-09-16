from helicopter import Helicopter
from enemy import Soldier, Tank


class GameMap:
    def __init__(self, width, height):
        self.width = width
        self.height = height
        self.helicopter = Helicopter(width, height)
        self.enemies = []
        self.spawn_enemies()

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
        # Draw enemies
        for enemy in self.enemies:
            enemy.draw(surface)

        # Draw helicopter projectiles
        for projectile in self.helicopter.projectiles:
            projectile.draw(surface)

        # Draw helicopter
        self.helicopter.draw(surface)

    @staticmethod
    def check_collision(projectile, enemy):
        return (
            abs(projectile.x - enemy.x) < enemy.size // 2
            and abs(projectile.y - enemy.y) < enemy.size // 2
        )
