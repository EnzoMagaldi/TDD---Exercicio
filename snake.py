import random
import pygame

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



class Renderer:
    def __init__(self, cell_size, width, height):
        pygame.init()
        self.cell = cell_size
        self.screen = pygame.display.set_mode(
            (width * cell_size, height * cell_size)
        )

        self.sprites = {
            "head_up": pygame.image.load("Graphics/head_up.png"),
            "head_down": pygame.image.load("Graphics/head_down.png"),
            "head_left": pygame.image.load("Graphics/head_left.png"),
            "head_right": pygame.image.load("Graphics/head_right.png"),

            "tail_up": pygame.image.load("Graphics/tail_up.png"),
            "tail_down": pygame.image.load("Graphics/tail_down.png"),
            "tail_left": pygame.image.load("Graphics/tail_left.png"),
            "tail_right": pygame.image.load("Graphics/tail_right.png"),

            "body_h": pygame.image.load("Graphics/body_horizontal.png"),
            "body_v": pygame.image.load("Graphics/body_vertical.png"),

            "curve_ur": pygame.image.load("Graphics/body_bottomright.png"),
            "curve_rd": pygame.image.load("Graphics/body_bottomleft.png"),
            "curve_dl": pygame.image.load("Graphics/body_topleft.png"),
            "curve_lu": pygame.image.load("Graphics/body_topright.png"),

            "apple": pygame.image.load("Graphics/apple.png")
        }

    def draw(self, game):
        self.screen.fill((0, 0, 0))
        snake = game.snake

        dir_map = {'w': 'up', 's': 'down', 'a': 'left', 'd': 'right'}

        # ===== cabeça =====
        head_dir = dir_map[game.direction]
        sprite = self.sprites[f"head_{head_dir}"]
        self._blit(sprite, snake[0])

        # ===== corpo =====
        for i in range(1, len(snake)-1):
            prev = snake[i-1]
            curr = snake[i]
            next = snake[i+1]

            d1 = direction(prev, curr, game.width, game.height)
            d2 = direction(curr, next, game.width, game.height)

            if is_straight(d1, d2):
                if d1 in ['left', 'right'] or d2 in ['left', 'right']:
                    sprite = self.sprites["body_h"]
                else:
                    sprite = self.sprites["body_v"]
            else:
                sprite = self._get_curve_sprite(d1, d2)

            self._blit(sprite, curr)

        # ===== cauda =====
        if len(snake) > 1:
            tail_dir = direction(snake[-2], snake[-1], game.width, game.height)
            sprite = self.sprites[f"tail_{tail_dir}"]
            self._blit(sprite, snake[-1])

        # ===== frutas =====
        for f in game.fruits:
            self._blit(self.sprites["apple"], f)

        pygame.display.flip()

    def _get_curve_sprite(self, d1, d2):
        combos = {
            ('up','right'): "curve_ur",
            ('right','down'): "curve_rd",
            ('down','left'): "curve_dl",
            ('left','up'): "curve_lu",

            ('right','up'): "curve_dl",
            ('down','right'): "curve_lu",
            ('left','down'): "curve_ur",
            ('up','left'): "curve_rd",
        }
        return self.sprites[combos[(d1, d2)]]

    def draw_pause(self):
        # overlay escuro
            overlay = pygame.Surface(self.screen.get_size())
            overlay.set_alpha(150)
            overlay.fill((0, 0, 0))
            self.screen.blit(overlay, (0, 0))

            font_big = pygame.font.Font(None, 72)
            font_small = pygame.font.Font(None, 36)

            text1 = font_big.render("PAUSADO", True, (255, 255, 0))
            text2 = font_small.render("Pressione P para continuar", True, (255, 255, 255))

            rect1 = text1.get_rect(center=(self.screen.get_width()//2, self.screen.get_height()//2 - 30))
            rect2 = text2.get_rect(center=(self.screen.get_width()//2, self.screen.get_height()//2 + 30))

            self.screen.blit(text1, rect1)
            self.screen.blit(text2, rect2)

            pygame.display.flip()