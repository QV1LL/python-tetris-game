import random
import time

import pygame

def tetris_game():

    # Set icon and caption
    icon = pygame.image.load('Images/Icon.png')
    pygame.display.set_caption('Tetris')
    pygame.display.set_icon(icon)

    # Font styles
    my_font = pygame.font.Font('font/PIXY.ttf', 40)

    # Main screen settings
    x, y = 450, 675
    screen = pygame.display.set_mode((x, y))
    screen.fill('Red')

    clock = pygame.time.Clock()
    fps = 30

    # Background
    bg = pygame.Surface((x, y - y / 5))
    bg.fill((0, 0, 0))

    bg_fill = pygame.Surface((x, y))
    bg_fill.fill((0, 0, 0))

    # Banner with score and settings
    banner = pygame.image.load('Images/Images.jpg').convert()
    banner = pygame.transform.scale(banner, (x, y / 5))

    score: int = 0
    best_score: int
    with open('best score.txt', 'r') as bst_score:
        best_score = int(bst_score.read())

    cell_size = 30

    # Tetromino shape list
    shapes_data = (
        ((-1, -1), (0, -1), (1, -1), (2, -1)),

        ((-1, -1), (0, -1), (1, -1), (-1, 0)),

        ((-1, -1), (0, -1), (1, -1), (1, 0)),

        ((0, -1), (1, -1), (0, 0), (1, 0)),

        ((-1, -1), (0, -1), (0, 0), (1, 0)),

        ((-1, -1), (0, -1), (1, -1), (0, 0)),

        ((0, -1), (1, -1), (-1, 0), (0, 0)))

    # game settings
    running = True
    fps = 60


    # creates blocks
    def create_block(size: int = cell_size, color: tuple = (0, 0, 0)):
        block = pygame.Surface((size, size))
        block.fill(color)
        return block


    # creates random color
    def random_color() -> tuple:
        color = (random.randint(50, 255), random.randint(50, 255), random.randint(50, 255))
        return color


    # create game field (containes cordinates of each cell)
    grid = [[(i * cell_size, g * cell_size) for i in range(int(x / cell_size))] for g in range(int(y * 0.8 / cell_size))]

    # create a list which containes blocks
    blocks = []
    positions = []

    # Print current score of the game
    def print_score(score: int):
        my_score = my_font.render(f'Рахунок: {score}', True, 'White', 'Black').convert()
        my_score = pygame.transform.scale(my_score, (banner.get_size()[0] / 4, banner.get_size()[1] / 4))
        return my_score


    def print_best_score(score: int):
        my_best_score = my_font.render(f'Найкращий рахунок: {best_score}', True, 'White', 'Black').convert()
        my_best_score = pygame.transform.scale(my_best_score, (banner.get_size()[0] / 3, banner.get_size()[1] / 4))
        return my_best_score




    # Print tetramino
    def create_tetramino(shape, offset: tuple = (0, 0), color=random_color()):
        return_positions = []
        return_blocks = []

        for i in range(len(shape)):
            block = create_block(color=color)
            position = ((shape[i][0] + 1 + offset[1]) * cell_size, (shape[i][1] + 1 + offset[0]) * cell_size)

            return_positions.append(position)
            return_blocks.append(block)

        return [return_blocks, return_positions]


    # adding blocks from shape to game field
    def add_tetramino_to_field(blocks_info: list):
        for i in range(len(blocks_info[0])):
            blocks.append(blocks_info[0][i])
            positions.append(blocks_info[1][i])


    # adding the blocks from tetramino to list of statics blocks in field
    def is_need_to_add_shape(blocks_info: list[list]):
        for i in range(len(blocks_info[0])):
            if blocks_info[1][i][1] / cell_size >= len(grid) - 1:
                return True
            elif (blocks_info[1][i][0], blocks_info[1][i][1] + cell_size) in positions:
                return True
        return False


    # Prints banner, score and etc...
    def print_main_elements():
        screen.blit(bg, (0, y / 5))
        bg.blit(bg_fill, (0, 0))
        screen.blit(banner, (0, 0))

        banner.blit(print_score(score), (10, 10))
        banner.blit(print_best_score(score), (10, 50))

        for i in range(len(blocks)):
            block = blocks[i]
            pos = positions[i]
            bg.blit(block, pos)




    # game control
    y_move = 0
    x_move = 0

    current_frequency = 27

    frequency = current_frequency
    frequency_counter = 0

    # checks the admissibility of right, left move or rotation
    def check_borders(tetramino_position: list) -> list:
        tetramino_pos_x = []
        for i in range(len(tetramino_position)):
            tetramino_pos_x.append(tetramino_position[i][0])

        right_move = True
        left_move = True
        for i in range(len(tetramino_position)):
            if not tetramino_pos_x[i] < x - cell_size or (
            tetramino_position[i][0] + cell_size, tetramino_position[i][1]) in positions:
                right_move = False
            if not tetramino_pos_x[i] > 0 or (
            tetramino_position[i][0] - cell_size, tetramino_position[i][1]) in positions:
                left_move = False

        return [right_move, left_move]


    # basic control of our shape, includes x move and rotate
    def control(keys_events: list, tetramino_position: list, x):

        checked_borders = check_borders(tetramino_position)

        if keys_events[pygame.K_RIGHT] and checked_borders[0]:
            x += 1
            clock.tick(15)
        elif keys_events[pygame.K_LEFT] and checked_borders[1]:
            x -= 1
            clock.tick(15)

        return x


    #returnes the admissibly of rotate
    def can_rotate(keys, current_shape) -> bool:
        rotate_shape = rotate(keys, current_shape, can_rotate)

        test_tetramino = create_tetramino(rotate_shape, (y_move, x_move), 'Red')

        for pos in test_tetramino[1]:
            if pos in positions or pos[0] < 0 or pos[0] > x - cell_size:
                return False
        return True


    # Rotate tetramino
    def rotate(keys_events, current_shape, func):
        new_shape = []
        for pos in current_shape:
            new_pos = (pos[1], -pos[0])
            new_shape.append(new_pos)
        if func == can_rotate:
            return tuple(new_shape)
        return tuple(new_shape) if can_rotate(keys_events, current_shape) else current_shape



    # Is the game stop?
    def stop():
        def overwrite_best_score():
            with open('best score.txt', 'w') as bst_score:
                if score > best_score:
                    bst_score.write(str(score))
                else:
                    bst_score.write(str(best_score))

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                overwrite_best_score()
                return True
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_x:
                    overwrite_best_score()
                    return True

        for position in positions:
            if position[1] <= cell_size * 2:
                overwrite_best_score()
                return True
        return False


    # deletes full line
    def delete_line(score):
        def replacing_number(count: int, numbers: list) -> int:
            numbers_dict: dict = {}
            for i in range(len(numbers)):
                numbers_dict[str(numbers[i])] = 0

            for number in numbers:
                numbers_dict[str(number)] += 1

            for key in numbers_dict:
                if numbers_dict[key] == count:
                    return key

        y_pos = []
        for pos in positions:
            y_pos.append(pos[1])

        if num := replacing_number(x / cell_size, y_pos):
            score += 100

            i = 0
            while i < len(positions):
                if positions[i][1] == int(num):
                    blocks.pop(i)
                    positions.pop(i)
                    continue
                i += 1

            for i in range(len(positions)):
                if positions[i][1] < int(num):
                    positions[i] = (positions[i][0], positions[i][1] + cell_size)
        return score

    # random settings to figure like a color and shape of tetramino
    figure = random.randint(0, len(shapes_data) - 1)
    current_shape = shapes_data[figure]
    color = random_color()

    # choice the next figure
    def get_next_figure():
        figure = random.randint(0, len(shapes_data) - 1)
        current_shape = shapes_data[figure]
        color = random_color()
        return current_shape, color

    next_figure = get_next_figure()


    #blit the next figure
    def print_next_figure(next_figure):
        next_tetramino = create_tetramino(next_figure[0], (0, 0), next_figure[1])

        for i in range(len(next_tetramino[1])):
            screen.blit(next_tetramino[0][i], (next_tetramino[1][i][0] + 170, next_tetramino[1][i][1] + 30))


    # Main run
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

menu_screen = pygame.display.set_mode((360, 600))
menu_screen.fill('Black')

icon = pygame.image.load('Images/Icon.png').convert()
pygame.display.set_caption('Tetris')
pygame.display.set_icon(icon)

my_font = pygame.font.Font('font/PIXY.ttf', 20)
restart = my_font.render('Нажмiть R, запустити гру', True, 'White', 'Black')
exit = my_font.render('Натиснiть Х для виходу', True, 'White', 'Black')

while True:
    menu_screen.blit(restart, (20, 300))
    menu_screen.blit(exit, (20, 340))
    pygame.display.update()
    if stop_game():
        break

pygame.quit()
