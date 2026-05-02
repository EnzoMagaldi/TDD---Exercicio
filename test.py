import pytest
from snake import SnakeGame, direction, is_straight
from unittest.mock import patch
from snake import Renderer

#Teste 1 -> Posição inicial
def test_cobra_deve_ter_posicao_inicial():
    game = SnakeGame(width=10, height=10)
    assert len(game.snake) == 1
    assert game.snake[0] == (5, 5)

#Teste 2 -> Movimentação
def test_movimento_para_direita():
    game = SnakeGame(width=10, height=10)
    game.update_direction('d')
    game.move()
    assert game.snake[0] == (6, 5)

def test_movimento_para_esquerda():
    game = SnakeGame(width=10, height=10)
    game.direction = 'w'
    game.update_direction('a')
    game.move()
    assert game.snake[0] == (4, 5)

def test_movimento_para_cima():
    game = SnakeGame(width=10, height=10)
    game.update_direction('w')
    game.move()
    assert game.snake[0] == (5, 4)


def test_movimento_para_baixo():
    game = SnakeGame(width=10, height=10)
    game.update_direction('s')
    game.move()
    assert game.snake[0] == (5, 6)

#Teste 3 -> Atravessar paredes
def test_atravessar_parede_direita_leste():
    game = SnakeGame(width=10, height=10)
    game.snake = [(9, 5)] 
    game.direction = 'd'
    game.move()
    assert game.snake[0] == (0, 5)

def test_atravessar_parede_esquerda_oeste():
    game = SnakeGame(width=10, height=10)
    game.snake = [(0, 5)]
    game.direction = 'a'
    game.move()
    assert game.snake[0] == (9, 5)

def test_atravessar_parede_cima_norte():
    game = SnakeGame(width=10, height=10)
    game.snake = [(5, 0)]
    game.direction = 'w'
    game.move()
    assert game.snake[0] == (5, 9)

def test_atravessar_parede_baixo_sul():
    game = SnakeGame(width=10, height=10)
    game.snake = [(5, 9)]
    game.direction = 's'
    game.move()
    assert game.snake[0] == (5, 0)

#Teste 4 -> Frutas
def test_comer_fruta_aumenta_tamanho():
    game = SnakeGame(10, 10)
    game.fruits = [(6, 5)]
    game.move() # Move para (6,5) onde está a fruta
    assert len(game.snake) == 2

def test_quantidade_de_frutas_baseado_no_tamanho():
    game = SnakeGame(10, 10)
    # Simula tamanho 10
    game.snake = [(i, 0) for i in range(10)]
    assert game.required_fruits() == 2

# Teste 5 -> Bloqueiar movimentação 180°
def test_impedir_virada_180_graus_horizontal():
    game = SnakeGame(10, 10)
    game.direction = 'd' 
    game.update_direction('a') 
    assert game.direction == 'd' 

def test_impedir_virada_180_graus_vertical():
    game = SnakeGame(10, 10)
    game.direction = 'w'
    game.update_direction('s') 
    assert game.direction == 'w'

# Teste 6 -> colisões com as paredes usando nova lógica de movimento
def test_direction_wrap_around_horizontal():
    a = (9, 5)
    b = (0, 5)
    d = direction(a, b, 10, 10)

    assert d == 'right'

def test_direction_wrap_around_horizontal():
    a = (5, 9)
    b = (5, 0)
    d = direction(a, b, 10, 10)

    assert d == 'down'

# Teste 7 -> Cobra no estado normal
def test_straight_horizontal():
    assert is_straight('left', 'right') is True

def test_straight_vertical():
    assert is_straight('up', 'down') is True

def test_not_straight():
    assert is_straight('up', 'right') is False

# Teste 8 -> Jogo pausado
def test_pause_does_not_move():
    game = SnakeGame(10, 10)
    game.paused = True

    original = game.snake.copy()
    game.move()

    assert game.snake == original

def test_carrega_todas_as_imagens():
    with patch("pygame.image.load") as mock_load:
        with patch("pygame.display.set_mode"):
            with patch("pygame.init"):
                
                Renderer(32, 10, 10)

                expected_calls = [
                    "Graphics/head_up.png",
                    "Graphics/head_down.png",
                    "Graphics/head_left.png",
                    "Graphics/head_right.png",

                    "Graphics/tail_up.png",
                    "Graphics/tail_down.png",
                    "Graphics/tail_left.png",
                    "Graphics/tail_right.png",

                    "Graphics/body_horizontal.png",
                    "Graphics/body_vertical.png",

                    "Graphics/body_bottomright.png",
                    "Graphics/body_bottomleft.png",
                    "Graphics/body_topleft.png",
                    "Graphics/body_topright.png",

                    "Graphics/apple.png"
                ]

                loaded_paths = [call.args[0] for call in mock_load.call_args_list]

                for path in expected_calls:
                    assert path in loaded_paths