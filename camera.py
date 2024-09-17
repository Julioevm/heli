class Camera:
    def __init__(self, width, height):
        self.width = width
        self.height = height
        self.x = 0
        self.y = 0

    def apply(self, entity):
        return entity.rect.move(self.x, self.y)

    def update(self, target):
        x = -target.x + self.width // 2
        y = -target.y + self.height // 2
        self.x = x
        self.y = y
