import pygame


class MiniMap:
    def __init__(self, map_width, map_height, mini_map_size):
        self.map_width = map_width
        self.map_height = map_height
        self.mini_map_size = mini_map_size
        self.surface = pygame.Surface((mini_map_size, mini_map_size))
        self.scale_x = mini_map_size / map_width
        self.scale_y = mini_map_size / map_height

    def update(self, helicopter_x, helicopter_y):
        self.surface.fill((0, 0, 0))  # Black background
        pygame.draw.rect(
            self.surface,
            (255, 255, 255),
            (0, 0, self.mini_map_size, self.mini_map_size),
            1,
        )  # White border

        # Draw helicopter position
        mini_heli_x = int(helicopter_x * self.scale_x)
        mini_heli_y = int(helicopter_y * self.scale_y)
        pygame.draw.circle(self.surface, (0, 255, 0), (mini_heli_x, mini_heli_y), 2)

    def draw(self, screen, x, y):
        screen.blit(self.surface, (x, y))
