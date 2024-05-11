import random
import time
import pygame

import tetris_init
from tetris_init import *


def tetris_game():

    running = True
    score = tetris_init.score
    current_shape = tetris_init.current_shape
    x_move = tetris_init.x_move
    y_move = tetris_init.y_move
    color = tetris_init.color
    next_figure = tetris_init.next_figure
    frequency_counter = tetris_init.frequency_counter

    while running:
        score = delete_line(score)

        keys = pygame.key.get_pressed()

        if keys[pygame.K_UP]:
            current_shape = rotate(keys, current_shape, None)
            clock.tick(10)

        if keys[pygame.K_DOWN]:
            frequency = 2
        else:
            frequency = current_frequency

        tetramino = create_tetramino(current_shape, (y_move, x_move), color)

        x_move = control(keys, tetramino[1], x_move)

        for i in range(len(tetramino[0])):
            bg.blit(tetramino[0][i], tetramino[1][i])

        print_main_elements()
        print_next_figure(next_figure)

        if is_need_to_add_shape(tetramino):
            x_move = int(len(grid[0]) / 2)
  
            y_move = 0

            current_shape = next_figure[0]
            color = next_figure[1]

            next_figure = get_next_figure()

            add_tetramino_to_field(tetramino)

        if frequency_counter >= frequency:
            y_move += 1
            frequency_counter = 0

        frequency_counter += 1

        # not logic
        pygame.display.update()

        clock.tick(fps)

        running = not stop()


def stop_game():
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            return True
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_x:
                return True
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_r:
                tetris_game()
                return False


pygame.init()

menu_screen = pygame.display.set_mode((tetris_init.x, tetris_init.y))
menu_screen.fill('Black')

icon = pygame.image.load('Images/Icon.png').convert()
pygame.display.set_caption('Tetris')
pygame.display.set_icon(icon)

my_font = pygame.font.Font('font/PIXY.ttf', 20)
restart = my_font.render('R to restart or start', True, 'White', 'Black')
exit = my_font.render('X to exit', True, 'White', 'Black')

while True:
    menu_screen.blit(restart, (20, 300))
    menu_screen.blit(exit, (20, 340))
    pygame.display.update()
    if stop_game():
        break

pygame.quit()
