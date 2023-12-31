import pygame
import sys
import random
import math
import time


def main() -> None:
    """Outline of the actions that occur during the game"""

    # Initializes the game window and fetches the play button object
    play_btn = window_init()

    # Checks whether the "play" button is pressed
    play_pressed(play_btn)

    # Generate a 9x9 board
    alpha = 3  # alpha is the gap between cells, in pixels
    mine_locations, screen = board_drawer(9, alpha, 10)

    # "Place" the mines based on their locations by implementing the number logic
    numbered_board = place_mines(mine_locations)

    # Initialize the mine counter (at 10 initially, is called repeatedly when appropriate)
    mine_counter(screen)

    # Run the game normally
    running(alpha, numbered_board, screen)

    pygame.quit()
    sys.exit()


def window_init() -> pygame:
    """Prepare the game window and the elements related to the main menu"""
    # Initialize pygame's window, showing title and coloring the background
    pygame.init()

    bg_color = (70, 80, 90)
    screen = pygame.display.set_mode((600, 500))
    pygame.display.set_caption("Minesweeper")

    title_font = pygame.font.Font("static/mine-sweeper.ttf", 42)
    title_text = title_font.render("MINESWEEPER", False, (255, 255, 255))
    title_rect = title_text.get_rect(center=(300, 50))
    screen.fill(bg_color)
    screen.blit(title_text, title_rect)

    # Draw rectangle objects to start playing
    play = pygame.Rect(50, 150, 500, 100)

    darker_gray = (39, 39, 39)

    # Draws the play button
    play_button(screen, (245, 230, 232), play, "Play", darker_gray)

    pygame.display.flip()
    return play


def play_pressed(btn: pygame):
    """Wait for the user to click the play button"""

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


def board_drawer(size: int, alpha: int, mines: int) -> tuple[list[list[int]], pygame]:
    """Draws a board given a size, alpha and mine count"""

    screen = pygame.display.set_mode((600, 500))
    bg_color = (70, 80, 90)
    screen.fill(bg_color)
    square_size = (400 - 10 * 2 - (size - 1) * alpha) / size  # Calculations determined beforehand, adding 10px padding.

    for row in range(size):
        for column in range(size):
            # Determine the x and y positions of the square to place (considering the 10px padding)
            x = 10 + column * (square_size + alpha)
            y = 10 + row * (square_size + alpha)

            # Draw a gray rectangle of area square_size^2 in the x,y position
            pygame.draw.rect(screen, (198, 198, 198), (x, y, square_size, square_size))

    # Add 10 mines, store values of (row, column) in a list
    mine_locations = []
    while mines:
        # Choose a number between 0 and 80, then convert to a (row, column) tuple
        new_mine = random.randint(0, size * size - 1)
        new_mine_location = [new_mine // 9, new_mine % 9]

        if new_mine_location in mine_locations:
            continue  # Try again if that spot is taken
        else:
            mine_locations.append(new_mine_location)
            mines -= 1

    pygame.display.flip()
    return mine_locations, screen


def place_mines(locations: list[list[int]], size=9) -> dict:
    """Stores the number of mines adjacent to each cell in a dict. This number will be displayed when a player clicks
    on a cell (1-9). 0 is an empty space, -1 is a mine."""

    # Dictionary that is to hold the number of mines adjacent to each cell
    adjacent_mines = {}

    for row in range(size):
        for column in range(size):

            if [row, column] in locations:
                # Cells with mines are assigned a value of -1
                adjacent_mines[(row, column)] = - 1

            else:
                adj_count = 0

                # Loop that checks for adjacent mines in the case that the cell itself is not a mine
                for i in range(-1, 2):
                    for j in range(-1, 2):

                        # Ignore the cell itself, as we want the mines next to it
                        if not (i == 0 and j == 0):
                            # If the adjacent cell exists (by being between (0,0) and (size - 1, size - 1)),
                            # and it has a mine, increase the counter
                            if 0 <= row + i < size and 0 <= column + j < size and [row + i, column + j] in locations:
                                adj_count += 1

                # Associate that particular row and column to its adjacent mine count
                adjacent_mines[(row, column)] = adj_count

    return adjacent_mines


def mine_counter(screen, num: int = 0) -> None:
    """Updates the mine counter. Starts at 10, then decreases by one each time a flag is placed. Can't be less than 0"""

    bg_color = (70, 80, 90)
    pygame.draw.rect(screen, bg_color, (450, 0, 150, 40))
    count = 10 + num

    counter_font = pygame.font.Font("static/Seven-Segment.ttf", 32)
    counter_text = counter_font.render("Mines:" + str(count), False, (255, 0, 0))
    screen.blit(counter_text, (450, 0))
    pygame.display.flip()


def running(alpha: int, numbered_board: dict, screen) -> None:
    """Checks for in-game actions"""
    runs = True

    # Lists holding flagged and clicked cells
    flagged = []
    clicked = []

    # Counter of flags placed
    ct = 0

    # Start a timer
    time_start = time.time()

    while runs:

        for event in pygame.event.get():

            # If user closes the window, end game
            if event.type == pygame.QUIT:
                runs = False

            # Every action implies a click
            elif event.type == pygame.MOUSEBUTTONDOWN:

                # Get the position of said click
                mouse_x, mouse_y = pygame.mouse.get_pos()

                # Check it is within the bounds of the board
                if 390 - alpha >= mouse_x >= 10 and 390 - alpha >= mouse_y >= 10:

                    # Use the position to gather which cell was clicked
                    column = get_cell(mouse_x, alpha)
                    row = get_cell(mouse_y, alpha)

                    # If it was a left click
                    if event.button == 1:

                        # If it had not been clicked, then show that cell
                        if [row, column] not in clicked:

                            # If it was a flag beforehand, remove the flag and then show the cell
                            if [row, column] in flagged:
                                flagged.remove([row, column])
                                remove_flag(row, column, alpha, screen)
                                clicked.append([row, column])

                            # continue_game is a boolean. True if the cell shown was not a mine, False otherwise.
                            continue_game = show_cell(row, column, alpha, screen, numbered_board, clicked)

                            # Game ends if a mine is clicked
                            if not continue_game:
                                runs = False

                            # If it's not a mine, add the cell to the list of clicked cells
                            else:
                                if [row, column] not in clicked:
                                    clicked.append([row, column])

                        # If the cell had been clicked, check if it can be "chorded" (which handles extra concatenations
                        # to the clicked list).
                        elif [row, column] in clicked:
                            clicked = chord(row, column, alpha, numbered_board, screen, flagged, clicked)

                            if win_condition(clicked):
                                time_end = time.time()
                                time_elapsed = time_end - time_start
                                win(screen, time_elapsed)

                    # If it's a right click
                    elif event.button == 3:

                        if [row, column] not in clicked:
                            # If it has been flagged before, remove the flag and update the mine counter
                            if [row, column] in flagged:
                                flagged.remove([row, column])
                                remove_flag(row, column, alpha, screen)
                                ct += 1
                                mine_counter(screen, ct)

                            # If the max number of flags hasn't been placed, add a flag and update the mine counter
                            elif len(flagged) < 10:
                                flagged.append([row, column])
                                place_flag(row, column, alpha, screen)
                                ct -= 1
                                mine_counter(screen, ct)


def chord(row: int, column: int, alpha: int, numbered_board: dict, screen, flagged: list, clicked: list) -> list:
    """Handles the action of chording"""

    close_flags = 0

    # Check surrounding cells for flags.
    for i in range(-1, 2):
        for j in range(-1, 2):
            if not (i == 0 and j == 0):
                if [row + i, column + j] in flagged and (row + i >= 0 and column + j >= 0) and (
                        row + i < 9 and column + j < 9):
                    close_flags += 1

    # If the number in the cell matches the flag count, show all remaining cells
    if numbered_board[(row, column)] == close_flags and numbered_board[(row, column)] != 0:
        for i in range(-1, 2):
            for j in range(-1, 2):
                if not (i == 0 and j == 0):
                    if [row + i, column + j] not in clicked and [row + i, column + j] not in flagged and (
                            row + i >= 0 and column + j >= 0) and (row + i < 9 and column + j < 9):
                        show_cell(row + i, column + j, alpha, screen, numbered_board, clicked)
                        if [row + i, column + j] not in clicked:
                            clicked.append([row + i, column + j])
    return clicked


def win(screen, time_elapsed: float) -> None:
    """Shows the win screen if a player wins the game"""

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
    """Handles the calculation of the cell based on the position of a mouse click"""

    return math.floor((9 * (pos - 10)) / (380 - alpha))


def place_flag(row: int, column: int, alpha: int, screen) -> None:
    """Places a flag visually on the clicked cell"""

    flag = pygame.image.load("static/flag.png").convert()

    size = get_size()

    scaled_image = pygame.transform.scale(flag, size)

    x = 10 + column * (size[0] + alpha)
    y = 10 + row * (size[1] + alpha)

    screen.blit(scaled_image, (x, y))
    pygame.display.flip()


def remove_flag(row: int, column: int, alpha: int, screen) -> None:
    """Removes a placed flag visually on the clicked cell"""

    size = get_size()

    x = 10 + column * (size[0] + alpha)
    y = 10 + row * (size[1] + alpha)

    # Draw a rectangle of area size^2 in the x,y position, gray
    pygame.draw.rect(screen, (198, 198, 198), (x, y, size[0], size[1]))
    pygame.display.flip()


def show_cell(row: int, column: int, alpha: int, screen, numbered_board: dict, clicked: list):
    """Shows a cell visually on the board"""

    # Colors used for the numbers, as per the original Minesweeper game
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

    # If the cell is a mine, game over, end the game
    if numbered_board[(row, column)] == -1:
        game_over(row, column, alpha, screen, numbered_board, clicked)
        return False

    # Else, if it's not empty, show the number using the appropriate color
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

    # If it is empty, initiate a cascade and return the altered list
    else:
        clicked = cascading_0s(row, column, alpha, screen, numbered_board, clicked)
        return clicked


def cascading_0s(row: int, column: int, alpha: int, screen, numbered_board: dict, clicked: list) -> list:
    """Handles the case where a blank space is clicked"""

    # If it has not been clicked before, add it to the clicked list, and determine what's next with a for loop.
    if [row, column] not in clicked:
        clicked.append([row, column])

        size = get_size()

        x = 10 + column * (size[0] + alpha)
        y = 10 + row * (size[1] + alpha)

        # Draw a rectangle of area size^2 in the x,y position, gray.
        pygame.draw.rect(screen, (128, 128, 128), (x, y, size[0], size[1]))

        # Check all surrounding squares for non-mines.
        for i in range(-1, 2):
            for j in range(-1, 2):
                if (not (i == 0 and j == 0) and 0 <= row + i < 9 and 0 <= column + j < 9 and
                        [row + i, column + j] not in clicked):
                    # If it's a zero, keep checking (by calling the function again).
                    if numbered_board[(row + i, column + j)] == 0:
                        cascading_0s(row + i, column + j, alpha, screen, numbered_board, clicked)

                    # Else if it's not a mine, just show that cell and end the cycle.
                    elif numbered_board[(row + i, column + j)] > 0:

                        if [row + i, column + j] not in clicked:
                            clicked.append([row + i, column + j])

                        show_cell(row + i, column + j, alpha, screen, numbered_board, clicked)

        pygame.display.flip()
    return clicked


def get_size() -> tuple[float, float]:
    """Returns the size of a cell"""

    return (400 - 10 * 2 - (9 - 1) * 3) / 9, (400 - 10 * 2 - (9 - 1) * 3) / 9


def game_over(row: int, column: int, alpha: int, screen: pygame, numbered_board: dict, clicked: list) -> None:
    """Handle the loss of a player, i.e. when they click a mine or a mine is triggered by wrongful chording."""

    # Load mine images to show, and transform them to the size of a square
    mine = pygame.image.load("static/bomb-red.png").convert()
    mine_others = pygame.image.load("static/bomb-gray.png").convert()
    size = get_size()
    scaled_image = pygame.transform.scale(mine, size)
    scaled_image_others = pygame.transform.scale(mine_others, size)

    # Show the clicked mine
    x = 10 + column * (size[0] + alpha)
    y = 10 + row * (size[1] + alpha)
    screen.blit(scaled_image, (x, y))

    # Show the rest of the mines
    for key, value in numbered_board.items():
        if value == -1 and key != (row, column):
            x = 10 + key[1] * (size[0] + alpha)
            y = 10 + key[0] * (size[1] + alpha)

            screen.blit(scaled_image_others, (x, y))

    # Show game over text
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


def play_button(screen: pygame, rect_color: tuple, rect_position: pygame, text: str, text_color: tuple) -> None:
    """ Draws a rectangle on the screen based on color, position, and text given"""

    pygame.draw.rect(screen, rect_color, rect_position)

    font = pygame.font.Font("static/mine-sweeper.ttf", 34)
    text_surface = font.render(text, True, text_color)
    text_rect = text_surface.get_rect(
        center=(rect_position[0] + rect_position[2] // 2, rect_position[1] + rect_position[3] // 2))

    screen.blit(text_surface, text_rect)


def win_condition(clicked: list) -> bool:
    """Check if the max cells have been clicked by way of the length of clicked. If so, win."""
    if len(clicked) == 71:
        print(clicked)
        return True
    return False


if __name__ == "__main__":
    main()

'''
References:

Gezoda. (2018, March). MINE-SWEEPER. Fontstruct. https://fontstruct.com/fontstructions/show/1501665/mine-sweeper
Krafti Lab. (2018, July). Seven Segment. Dafont.com. https://www.dafont.com/seven-segment.font
Johnson, C. (1990). Minesweeper (Online Version) [Video Game]. Microsoft.
'''