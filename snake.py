import random

class SnakeGame:
    def __init__(self, width, height):
        self.width = width
        self.height = height
        self.snake = [(width // 2, height // 2)]
        self.direction = 'd'
        self.game_over = False
        self.fruits = []
        self.spawn_fruits()

    def update_direction(self, new_dir):
        self.direction = new_dir

    def required_fruits(self):
        return (len(self.snake) // 10) + 1
    
    def _get_movement_vector(self):
        move_map = {'w': (0, -1), 's': (0, 1), 'a': (-1, 0), 'd': (1, 0)}
        return move_map.get(self.direction, (0, 0))
    
    def spawn_fruits(self):
       while len(self.fruits) < self.required_fruits():
            new_fruit = (
                random.randint(0, self.width - 1), 
                random.randint(0, self.height - 1)
            )
            # Verifica se a posição é válida antes de adicionar
            if new_fruit not in self.snake and new_fruit not in self.fruits:
                self.fruits.append(new_fruit)
    def move(self):
        if self.game_over:
            return


        dx, dy = self._get_movement_vector()
        hx, hy = self.snake[0]

        new_head = ((hx + dx) % self.width, (hy + dy) % self.height)

        if new_head in self.snake:
            self.game_over = True
            return

        self.snake.insert(0, new_head)
        if new_head in self.fruits:
            self.fruits.remove(new_head)
            self.spawn_fruits()
        else:
            self.snake.pop()

