class Camera:
    def __init__(self, width, height, map_width, map_height):
        self.width = width
        self.height = height
        self.map_width = map_width
        self.map_height = map_height
        self.x = 0
        self.y = 0

    def apply(self, entity):
        return entity.rect.move(self.x, self.y)

    def update(self, target):
        # Center the camera on the target
        self.x = target.x - self.width // 2
        self.y = target.y - self.height // 2

        # Keep the camera within the map bounds
        self.x = max(0, min(self.x, self.map_width - self.width))
        self.y = max(0, min(self.y, self.map_height - self.height))
