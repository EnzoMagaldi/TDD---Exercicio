import random

def direction(a, b, width, height):
    ax, ay = a
    bx, by = b

    dx = bx - ax
    dy = by - ay

    #corrigir wrap horizontal
    if dx > 1:
        dx = -1
    elif dx < -1:
       dx = 1

    # corrigir wrap vertical
    if dy > 1:
        dy = -1
    elif dy < -1:
        dy = 1

    if dx == 1: 
        return 'right'
    if dx == -1: 
        return 'left'
    if dy == 1: 
        return 'down'
    if dy == -1: 
        return 'up'
    
def is_straight(d1, d2):
    return (
        d1 == d2 or
        {d1, d2} == {'up', 'down'} or
        {d1, d2} == {'left', 'right'}
    )

class SnakeGame:
    def __init__(self, width, height):
        self.width = width
        self.height = height
        self.snake = [(width // 2, height // 2)]
        self.direction = 'd'
        self.game_over = False
        self.fruits = []
        self.spawn_fruits()
        self.paused = False

    def update_direction(self, new_dir):
        opposites = {'w': 's', 's': 'w', 'a': 'd', 'd': 'a'}
        if new_dir in opposites and opposites[new_dir] != self.direction:
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
        if self.game_over or self.paused:
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

