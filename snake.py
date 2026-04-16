class SnakeGame:
    def __init__(self, width, height):
        self.snake = [(width // 2, height // 2)]
        self.direction = 'd'
    def move(self):
        x, y = self.snake[0]
        self.snake = [(x + 1, y)]