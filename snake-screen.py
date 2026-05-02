import pygame
from snake import SnakeGame, Renderer

game = SnakeGame(20, 10)
renderer = Renderer(32, 20, 10)

clock = pygame.time.Clock()

running = True
while running:
    for event in pygame.event.get():

        if event.type == pygame.QUIT:
            running = False

        if event.type == pygame.KEYDOWN:
            
            if event.key == pygame.K_ESCAPE:
                running = False

            if event.key == pygame.K_p and not game.game_over:
                game.paused = not game.paused

            # RESTART
            elif game.game_over:
                if event.key == pygame.K_r:
                    game.reset()

            elif not game.game_over:
                if event.key == pygame.K_w: game.update_direction('w')
                if event.key == pygame.K_s: game.update_direction('s')
                if event.key == pygame.K_a: game.update_direction('a')
                if event.key == pygame.K_d: game.update_direction('d')

    if game.game_over:
        renderer.draw_game_over()
    elif game.paused:
        renderer.draw(game) # desenha o jogo congelado
        renderer.draw_pause() # overlay por cima
    else:
        renderer.draw(game)
    
    if not game.game_over and not game.paused:
        game.move()

    clock.tick(10)