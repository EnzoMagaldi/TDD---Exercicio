class SnakeGame:
    def __init__(self, width, height):
        self.snake = [(width // 2, height // 2)]
        self.direction = 'd'
    def move(self):
        x, y = self.snake[0]
        move_map = {'w': (0, -1), 's': (0, 1), 'a': (-1, 0), 'd': (1, 0)}
        self.snake = [(x + 1, y)]