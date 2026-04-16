import pytest
from snake import SnakeGame


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
