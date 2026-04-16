import pytest
from snake import SnakeGame


#Teste 1 -> Posição inicial
def test_cobra_deve_ter_posicao_inicial():
    game = SnakeGame(width=10, height=10)
    assert len(game.snake) == 1
    assert game.snake[0] == (5, 5)