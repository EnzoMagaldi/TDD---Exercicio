class SnakeGame:
    def __init__(self, width, height):
        self.snake = [(width // 2, height // 2)]
        self.direction = 'd'
    def update_direction(self, new_dir):
        self.direction = new_dir
    
    def move(self):
        hx, hy = self.snake[0]
        move_map = {'w': (0, -1), 's': (0, 1), 'a': (-1, 0), 'd': (1, 0)}
        dx, dy = move_map[self.direction]
        self.snake = [(hx + dx, hy + dy)]
