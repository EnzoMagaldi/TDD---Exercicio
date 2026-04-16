import os
import keyboard
import time
from snake import SnakeGame


class io_handler:
    
    x_size: int
    y_size: int
    game_speed = float
    last_input: str
    matrix = []

    def __init__(self, dim, speed):
        self.x_size = dim[0]
        self.y_size = dim[1]
        
        self.game_speed = speed
        self.last_input = 'w'

        for i in range (self.y_size): 
            self.matrix.append([0]*self.x_size)

    def record_inputs(self):
        keyboard.add_hotkey('w', lambda: setattr(self, "last_input", 'w'))
        keyboard.add_hotkey('a', lambda: setattr(self, "last_input", 'a'))
        keyboard.add_hotkey('s', lambda: setattr(self, "last_input", 's'))
        keyboard.add_hotkey('d', lambda: setattr(self, "last_input", 'd'))
        keyboard.add_hotkey('esc', lambda: setattr(self, "last_input", 'end'))

    def display(self):
        def display_h_line(self):
            print ('+', end='')
            print ('--'* len(self.matrix[0]), end='')
            print ('+')
        
        def display_content_line(line):
            print ('|', end='')
            for item in line: 
                if item == 1:
                    print ('[]', end='')
                elif item == 2:
                    print ('<>', end='')
                elif item == 3:
                    print ('()', end='')
                else:
                    print ('  ', end='')

            print ('|')

        os.system('cls' if os.name == 'nt' else 'clear')
        display_h_line(self)
        for line in self.matrix:
            display_content_line(line)
        display_h_line(self)

instance = io_handler((20, 10), 0.2)
game = SnakeGame(20, 10)

def game_loop():
    instance.record_inputs()
    while True:
        game.update_direction(instance.last_input)
        game.move()
        
        if game.game_over:
            print("GAME OVER! A cobra se mordeu.")
            break

        instance.matrix = [[0 for _ in range(instance.x_size)] for _ in range(instance.y_size)]
        
        for fx, fy in game.fruits:
            instance.matrix[fy][fx] = 3
    
        for bx, by in game.snake[1:]:
            instance.matrix[by][bx] = 1
            
        hx, hy = game.snake[0]
        instance.matrix[hy][hx] = 2

        instance.display()
        print(f"Tamanho: {len(game.snake)} | Frutas: {len(game.fruits)}")
        print("mova com WASD, saia com esc. Ultimo botão:", end=' ')
        print(instance.last_input)
        
        if(instance.last_input == 'end'):
            exit()
        time.sleep(instance.game_speed)

game_loop()
