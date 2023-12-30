import pygame
import sys
import random
import math
import time


def main():
    # Initializes the game window and fetches the rectangles drawn
    play_btn = window_init()

    play_pressed(play_btn)

    # Generate a 9x9 board
    alpha = 3  # alpha is the gap between cells, in pixels
    mine_locations, screen = board_drawer(9, alpha, 10)

    # "Place" the mines based on their locations by implementing the number logic
    numbered_board = place_mines(mine_locations)
    print(numbered_board)

    # Show remaining mines:
    mine_counter(screen)

    # Run the game normally
    running(alpha, numbered_board, screen)

    pygame.quit()
    sys.exit()


def mine_counter(screen, num=0):
    bg_color = (70, 80, 90)
    pygame.draw.rect(screen, bg_color, (450, 0, 150, 40))
    count = 10 + num

    counter_font = pygame.font.Font("static/Seven-Segment.ttf", 32)
    counter_text = counter_font.render("Mines:" + str(count), False, (255, 0, 0))
    screen.blit(counter_text, (450, 0))
    pygame.display.flip()


def window_init():
    # Initialize pygame's window
    pygame.init()

    bg_color = (70, 80, 90)
    screen = pygame.display.set_mode((600, 500))
    pygame.display.set_caption("Minesweeper")

    # Show title

    # Minesweeper font, size 52
    title_font = pygame.font.Font("static/mine-sweeper.ttf", 42)

    # Render the "MINESWEEPER" text, white
    title_text = title_font.render("MINESWEEPER", False, (255, 255, 255))

    # Center the text
    title_rect = title_text.get_rect(center=(300, 50))

    # Show that part of the screen
    screen.fill(bg_color)
    screen.blit(title_text, title_rect)

    # Draw rectangle objects to start playing
    play = pygame.Rect(50, 150, 500, 100)

    darker_gray = (39, 39, 39)

    play_button(screen, (245, 230, 232), play, "Play", darker_gray)

    pygame.display.flip()
    return play


def play_pressed(btn):
    # Prompt the user for a difficulty level

    while True:

        for event in pygame.event.get():

            # Check for events

            if event.type == pygame.QUIT:
                raise SystemExit

            elif event.type == pygame.MOUSEBUTTONDOWN:
                if event.button == 1:

                    # Get position of the mouseclick and return if it collides with the button (i.e. button is pressed)
                    mouse_x, mouse_y = pygame.mouse.get_pos()

                    if btn.collidepoint(mouse_x, mouse_y):
                        return


def running(alpha, numbered_board, screen):
    runs = True
    flagged = []
    clicked = []
    ct = 0
    time_start = time.time()
    while runs:

        for event in pygame.event.get():
            print(len(clicked))

            if event.type == pygame.QUIT:
                runs = False

            elif event.type == pygame.MOUSEBUTTONDOWN:

                mouse_x, mouse_y = pygame.mouse.get_pos()

                if 390 - alpha >= mouse_x >= 10 and 390 - alpha >= mouse_y >= 10:

                    column = get_cell(mouse_x, alpha)
                    row = get_cell(mouse_y, alpha)

                    if event.button == 1:
                        if [row, column] not in clicked:
                            if [row, column] in flagged:
                                flagged.remove([row, column])
                                remove_flag(row, column, alpha, screen)
                            continue_game = show_cell(row, column, alpha, screen, numbered_board, clicked)
                            if not continue_game:
                                runs = False
                            else:
                                if [row, column] not in clicked:
                                    clicked.append([row, column])
                        if [row, column] in clicked:
                            clicked = chord(row, column, alpha, numbered_board, screen, flagged, clicked)
                            if len(clicked) >= 71:
                                time_end = time.time()
                                time_elapsed = time_end - time_start
                                win(screen, time_elapsed)

                    elif event.button == 3:
                        if [row, column] in flagged:
                            flagged.remove([row, column])
                            remove_flag(row, column, alpha, screen)
                            ct += 1
                            mine_counter(screen, ct)
                        elif [row, column] in clicked:
                            pass
                        elif len(flagged) < 10:
                            flagged.append([row, column])
                            place_flag(row, column, alpha, screen)
                            ct -= 1
                            mine_counter(screen, ct)


def chord(row, column, alpha, numbered_board, screen, flagged, clicked):
    close_flags = 0

    for i in range(-1, 2):
        for j in range(-1, 2):
            if not (i == 0 and j == 0):
                if [row + i, column + j] in flagged and (row + i >= 0 and column + j >= 0) and (
                        row + i < 9 and column + j < 9):
                    close_flags += 1

    if numbered_board[(row, column)] == close_flags and numbered_board[(row, column)] != 0:
        for i in range(-1, 2):
            for j in range(-1, 2):
                if not (i == 0 and j == 0):
                    if [row + i, column + j] not in clicked and [row + i, column + j] not in flagged and (
                            row + i >= 0 and column + j >= 0) and (row + i < 9 and column + j < 9):
                        show_cell(row + i, column + j, alpha, screen, numbered_board, clicked)
                        clicked.append([row + i, column + j])
    return clicked


def win(screen, time_elapsed):
    font = pygame.font.Font("static/mine-sweeper.ttf", 55)
    text = font.render("YOU WIN!!!", False, (255, 223, 0))
    font = pygame.font.Font("static/mine-sweeper.ttf", 25)
    thanks = font.render("Thank you for playing!", False, (255, 255, 255))
    font = pygame.font.Font("static/mine-sweeper.ttf", 15)
    stats = font.render(f"You defused the mines in {time_elapsed:.1f} seconds!", False, (32, 255, 255))
    screen.blit(text, (100, 200))
    screen.blit(thanks, (40, 350))
    screen.blit(stats, (20, 450))
    pygame.display.flip()

    while True:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                raise SystemExit


def get_cell(pos: int, alpha: int) -> int:
    return math.floor((9 * (pos - 10)) / (380 - alpha))


def place_flag(row, column, alpha, screen):
    flag = pygame.image.load("static/flag.png").convert()

    size = get_size()

    scaled_image = pygame.transform.scale(flag, size)

    x = 10 + column * (size[0] + alpha)
    y = 10 + row * (size[1] + alpha)

    screen.blit(scaled_image, (x, y))
    pygame.display.flip()


def remove_flag(row, column, alpha, screen):
    size = get_size()

    x = 10 + column * (size[0] + alpha)
    y = 10 + row * (size[1] + alpha)

    # Draw a rectangle of area size^2 in the x,y position, gray
    pygame.draw.rect(screen, (198, 198, 198), (x, y, size[0], size[1]))
    pygame.display.flip()


def show_cell(row, column, alpha, screen, numbered_board, clicked):
    colors = [
        (0, 0, 255),
        (0, 128, 0),
        (255, 0, 0),
        (0, 0, 128),
        (128, 0, 0),
        (0, 128, 128),
        (0, 0, 0),
        (128, 128, 128),
    ]

    if numbered_board[(row, column)] == -1:
        game_over(row, column, alpha, screen, numbered_board, clicked)
        return False
    elif numbered_board[(row, column)] != 0:
        num_font = pygame.font.Font("static/mine-sweeper.ttf", 7 * alpha)
        mine_count = num_font.render(f"{numbered_board[(row, column)]}", False,
                                     colors[numbered_board[(row, column)] - 1])

        size = get_size()

        x = 10 + 3.5 * alpha + column * (size[0] + alpha)
        y = 10 + 2 * alpha + row * (size[1] + alpha)

        screen.blit(mine_count, (x, y))
        pygame.display.flip()
        return True
    else:
        clicked = cascading_0s(row, column, alpha, screen, numbered_board, clicked)

    return clicked


def cascading_0s(row, column, alpha, screen, numbered_board, clicked):
    if [row, column] not in clicked:
        clicked.append([row, column])

        size = get_size()

        x = 10 + column * (size[0] + alpha)
        y = 10 + row * (size[1] + alpha)

        # Draw a rectangle of area size^2 in the x,y position, gray
        pygame.draw.rect(screen, (128, 128, 128), (x, y, size[0], size[1]))

        # Check all surrounding squares for non-mines
        for i in range(-1, 2):
            for j in range(-1, 2):
                if (not (i == 0 and j == 0) and 0 <= row + i < 9 and 0 <= column + j < 9 and
                        [row + i, column + j] not in clicked):
                    # If it's a zero, keep checking (by calling the function again)
                    if numbered_board[(row + i, column + j)] == 0:
                        cascading_0s(row + i, column + j, alpha, screen, numbered_board, clicked)

                    # Else if it's not a mine, just show that cell and end the cycle
                    elif numbered_board[(row + i, column + j)] > 0:
                        clicked.append([row + i, column + j])
                        show_cell(row + i, column + j, alpha, screen, numbered_board, clicked)

        pygame.display.flip()
    return clicked


def get_size():
    return (400 - 10 * 2 - (9 - 1) * 3) / 9, (400 - 10 * 2 - (9 - 1) * 3) / 9


def game_over(row, column, alpha, screen, numbered_board, clicked):
    mine = pygame.image.load("static/bomb-red.png").convert()
    mine_others = pygame.image.load("static/bomb-gray.png").convert()

    size = get_size()

    scaled_image = pygame.transform.scale(mine, size)
    scaled_image_others = pygame.transform.scale(mine_others, size)

    x = 10 + column * (size[0] + alpha)
    y = 10 + row * (size[1] + alpha)

    screen.blit(scaled_image, (x, y))

    for key, value in numbered_board.items():
        if value == -1 and key != (row, column):
            x = 10 + key[1] * (size[0] + alpha)
            y = 10 + key[0] * (size[1] + alpha)

            screen.blit(scaled_image_others, (x, y))

    font = pygame.font.Font("static/mine-sweeper.ttf", 55)
    text = font.render("GAME OVER!", False, (255, 0, 0))
    font = pygame.font.Font("static/mine-sweeper.ttf", 25)
    thanks = font.render("Thank you for playing!", False, (255, 255, 255))
    stats = font.render(f"You uncovered {len(clicked)} cells.", False, (32, 255, 255))
    screen.blit(text, (40, 150))
    screen.blit(thanks, (40, 300))
    screen.blit(stats, (20, 400))
    pygame.display.flip()

    while True:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                raise SystemExit


def play_button(screen, rect_color, rect_position, text, text_color):
    """ Draws a rectangle on the screen based on color, position, and text given"""

    pygame.draw.rect(screen, rect_color, rect_position)

    font = pygame.font.Font("static/mine-sweeper.ttf", 34)
    text_surface = font.render(text, True, text_color)
    text_rect = text_surface.get_rect(
        center=(rect_position[0] + rect_position[2] // 2, rect_position[1] + rect_position[3] // 2))

    screen.blit(text_surface, text_rect)


def board_drawer(size: int, alpha: int, mines: int):
    screen = pygame.display.set_mode((600, 500))
    bg_color = (70, 80, 90)
    screen.fill(bg_color)

    padding = 10  # So that squares don't touch precisely the edge
    square_size = (400 - padding * 2 - (size - 1) * alpha) / size

    for row in range(size):
        for column in range(size):
            # Determine the x and y positions of the square to place
            x = padding + column * (square_size + alpha)
            y = padding + row * (square_size + alpha)

            # Draw a rectangle of area square_size^2 in the x,y position, gray
            pygame.draw.rect(screen, (198, 198, 198), (x, y, square_size, square_size))

    # Add 10 mines, store values of (row, column) in a list
    mine_locations = []
    while mines:
        new_mine = random.randint(0, size * size - 1)
        new_mine_location = [new_mine // 9, new_mine % 9]

        if new_mine_location in mine_locations:
            continue  # Try again if that spot is taken
        else:
            mine_locations.append([new_mine // 9, new_mine % 9])
            mines -= 1

    pygame.display.flip()
    return mine_locations, screen


def place_mines(locations: list[list[int]], size=9) -> dict:
    # Dictionary holding the number of mines adjacent to each cell
    adjacent_mines = {}

    for row in range(size):
        for column in range(size):

            if [row, column] in locations:
                # Bomb cells are assigned a value of -1
                adjacent_mines[(row, column)] = - 1
            else:
                adj_count = 0

                # Loop that checks for adjacent mines in the case that the cell itself is not a mine
                for i in range(-1, 2):
                    for j in range(-1, 2):

                        # Ignore the cell itself, as we want the mines next to it
                        if not (i == 0 and j == 0):
                            # If the adjacent cell exists (by being between (0,0) and (size - 1, size - 1)),
                            # and it has a mine
                            if 0 <= row + i < size and 0 <= column + j < size and [row + i, column + j] in locations:
                                adj_count += 1

                adjacent_mines[(row, column)] = adj_count

    return adjacent_mines


if __name__ == "__main__":
    main()
