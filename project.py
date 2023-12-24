import pygame
import sys
import random
import math

def main():

    # Initializes the game window and fetches the rectangles drawn
    difficulty_list = windowinit()

    # Check for mouse collision with the shapes to obtain a difficulty
    '''
    9 = beginner
    16 = intermediate
    30 = expert
    '''
    difficulty = get_difficulty(difficulty_list)

    # Generate a board accordingly
    match difficulty:
        case 9:
            # Generate a 9x9 board
            alpha = 3 # alpha is the gap between cells, in pixels
            mine_locations, screen = board_drawer(9, alpha, 10)
        case 16:
            # Generate a 16x16 board
            alpha = 2
            mine_locations, screen = board_drawer(16, alpha, 40)
        case 30:
            # Generate a 30x30 board
            alpha = 1
            mine_locations, screen = board_drawer(30, alpha, 99)

    # "Place" the mines based on their locations by implementing the number logic
    numbered_board = place_mines(mine_locations, difficulty)
    print(numbered_board)

    # Show remaining mines:
    mine_counter(difficulty, screen)

    # Run the game normally
    running(alpha, numbered_board, screen, difficulty)

    pygame.quit()
    sys.exit()


def mine_counter(difficulty, screen, num=0):
    bg_color = (70, 80, 90)
    pygame.draw.rect(screen, bg_color, (450, 0, 150, 40))

    match difficulty:
        case 9:
            count = 10 + num
        case 16:
            count = 40 + num
        case 30:
            count = 99 + num

    counter_font = pygame.font.Font("static/Seven-Segment.ttf", 32)   
    counter_text =  counter_font.render("Mines:" + str(count), False, (255, 0, 0))
    screen.blit(counter_text, (450, 0))
    pygame.display.flip()
    


def generate_board(difficulty, alpha):
    
    match difficulty:
        case 9:
            # Generate a 9x9 board
            mine_locations = board_drawer(9, alpha, 10)
        case 16:
            # Generate a 16x16 board
            mine_locations = board_drawer(16, alpha, 40)
        case 30:
            # Generate a 30x30 board
            mine_locations = board_drawer(30, alpha, 99)
    
    return mine_locations


def windowinit():

    # Initialize pygame's window
    pygame.init()

    bg_color = (70, 80, 90)
    screen = pygame.display.set_mode((600, 600))
    pygame.display.set_caption("Minesweeper")

    ### Show title

    # Minesweeper font, size 52
    title_font = pygame.font.Font("static/mine-sweeper.ttf", 42)

    # Render the "MINESWEEPER" text, white
    title_text = title_font.render("MINESWEEPER", False, (255, 255, 255))

    # Center the text
    title_rect = title_text.get_rect(center=(300, 50))

    # Prompt for difficulty
    difficulty_font = pygame.font.Font(None, 30)
    difficulty_text = difficulty_font.render("Select Difficulty: ", False, (169, 169, 169))
    difficulty_rect = difficulty_text.get_rect(center=(150, 125))

    # Show that part of the screen
    screen.fill(bg_color)
    screen.blit(title_text, title_rect)
    screen.blit(difficulty_text, difficulty_rect)

    # Draw rectangle objects for difficulty selection
    beginner = pygame.Rect(50, 150, 500, 100)
    intermediate = pygame.Rect(50, 300, 500, 100)
    expert = pygame.Rect(50, 450, 500, 100)

    difficulties = list((beginner, intermediate, expert))
    
    light_gray = (248, 233, 235)
    dark_gray = (111, 111, 111)
    darker_gray = (39, 39, 39)

    difficulty_drawer(screen, (245, 230, 232), beginner, "Beginner", darker_gray)
    difficulty_drawer(screen, (213, 198, 224), intermediate, "Intermediate", dark_gray)
    difficulty_drawer(screen, (53, 1, 44), expert, "Expert", light_gray)

    pygame.display.flip()

    return difficulties


def get_difficulty(difficulty_list) -> int:
    # Prompt the user for a difficulty level
    running = True
    while running:
        
        for event in pygame.event.get():

            # Check for events

            if event.type == pygame.QUIT:
                raise SystemExit
            
            elif event.type == pygame.MOUSEBUTTONDOWN:
                if event.button == 1:

                    # Get the position of the mouseclick and return the difficulty selected
                    mouse_x, mouse_y = pygame.mouse.get_pos()

                    # Number returned is equal to the size of the board, nxn
                    if difficulty_list[0].collidepoint(mouse_x, mouse_y):
                        return 9 # For instance, this queues a 9x9 board
                    elif difficulty_list[1].collidepoint(mouse_x, mouse_y):
                        return 16
                    elif difficulty_list[2].collidepoint(mouse_x, mouse_y):
                        return 30 
                    

def running(alpha, numbered_board, screen, difficulty):
    running = True
    flagged = []
    clicked = []
    ct = 0
    while running:
        
        for event in pygame.event.get():

            if event.type == pygame.QUIT:
                running = False

            elif event.type == pygame.MOUSEBUTTONDOWN:

                mouse_x, mouse_y = pygame.mouse.get_pos()
                print(mouse_x, mouse_y)

                if mouse_x <= 390 - alpha and mouse_y <= 390 - alpha and mouse_x >= 10 and mouse_y >= 10:

                    column = get_cell(mouse_x, alpha)
                    row = get_cell(mouse_y, alpha)

                    if event.button == 1:
                        if [row, column] in clicked:
                            pass
                        else:
                            clicked.append([row, column])
                            if [row, column] in flagged:
                                flagged.remove([row, column])
                                remove_flag(row, column, alpha, screen)
                            show_cell(row, column, alpha, screen, numbered_board, clicked, difficulty)

                    elif event.button == 3:
                        if [row, column] in flagged:
                            flagged.remove([row, column])
                            remove_flag(row, column, alpha, screen)
                            ct += 1
                            mine_counter(difficulty, screen, ct)
                        elif [row, column] in clicked:
                            pass
                        else:
                            flagged.append([row, column])
                            place_flag(row, column, alpha, screen)
                            ct -= 1
                            mine_counter(difficulty, screen, ct)



def get_cell(pos: int, alpha: int) -> int:
    return math.floor((9 * (pos - 10)) / (380 - alpha))


def place_flag(row, column, alpha, screen):

    flag = pygame.image.load("static/flag.png").convert()

    size = get_size(alpha)
    
    scaled_image = pygame.transform.scale(flag, size)

    x = 10 + column * (size[0] + alpha)
    y = 10 + row * (size[1] + alpha)

    screen.blit(scaled_image, (x, y))
    pygame.display.flip()


def remove_flag(row, column, alpha, screen):

    size = get_size(alpha)

    x = 10 + column * (size[0] + alpha)
    y = 10 + row * (size[1] + alpha)

    # Draw a rectangle of area size^2 in the x,y position, gray
    pygame.draw.rect(screen, (198, 198, 198), (x, y, size[0], size[1]))
    pygame.display.flip()

def show_cell(row, column, alpha, screen, numbered_board, clicked, difficulty):

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
        game_over(row, column, alpha, screen, numbered_board, clicked, difficulty)
    elif numbered_board[(row, column)] != 0:
        num_font = pygame.font.Font("static/mine-sweeper.ttf", 7 * alpha)
        mine_count = num_font.render(f"{numbered_board[(row, column)]}", False, colors[numbered_board[(row, column)] - 1])

        size = get_size(alpha)

        x = 10 + 3.5 * alpha + column * (size[0] + alpha)
        y = 10 + 2 * alpha + row * (size[1] + alpha)

        screen.blit(mine_count, (x, y))
        pygame.display.flip()
    else:
        clicked = cascading_0s(row, column, alpha, screen, numbered_board, clicked, difficulty)


def cascading_0s(row, column, alpha, screen, numbered_board, clicked, difficulty):
    clicked.append([row, column])
    size = get_size(alpha)

    x = 10 + column * (size[0] + alpha)
    y = 10 + row * (size[1] + alpha)

    # Draw a rectangle of area size^2 in the x,y position, gray
    pygame.draw.rect(screen, (128, 128, 128), (x, y, size[0], size[1]))

    
    
    # Check all surrounding squares for zeroes
    if row + 1 < difficulty and column + 1 < difficulty and numbered_board[(row + 1, column + 1)] == 0 and [row + 1, column + 1] not in clicked:
        cascading_0s(row + 1, column + 1, alpha, screen, numbered_board, clicked, difficulty)
    if row + 1 < difficulty and column - 1 >= 0 and numbered_board[(row + 1, column - 1)] == 0 and [row + 1, column - 1] not in clicked:
        cascading_0s(row + 1, column - 1, alpha, screen, numbered_board, clicked, difficulty)
    if row - 1 >= 0 and column + 1 < difficulty and numbered_board[(row - 1, column + 1)] == 0 and [row - 1, column + 1] not in clicked:
        cascading_0s(row - 1, column + 1, alpha, screen, numbered_board, clicked, difficulty)
    if row - 1 >= 0 and column - 1 >= 0 and numbered_board[(row - 1, column - 1)] == 0 and [row - 1, column - 1] not in clicked:
        cascading_0s(row - 1, column - 1, alpha, screen, numbered_board, clicked, difficulty)
    if row - 1 >= 0 and column >= 0 and numbered_board[(row - 1, column)] == 0 and [row - 1, column] not in clicked:
        cascading_0s(row - 1, column, alpha, screen, numbered_board, clicked, difficulty)
    if row + 1 < difficulty and column >= 0 and numbered_board[(row + 1, column)] == 0 and [row + 1, column] not in clicked:
        cascading_0s(row + 1, column, alpha, screen, numbered_board, clicked, difficulty)
    if row >= 0 and column - 1 >= 0 and numbered_board[(row, column - 1)] == 0 and [row, column - 1] not in clicked:
        cascading_0s(row, column - 1, alpha, screen, numbered_board, clicked, difficulty)
    if row >= 0 and column + 1 < difficulty and numbered_board[(row, column + 1)] == 0 and [row, column + 1] not in clicked:
        cascading_0s(row, column + 1, alpha, screen, numbered_board, clicked, difficulty)

    # if it's a number other than 0, show that cell. This ends the cycle
    if row + 1 < difficulty and column + 1 < difficulty and numbered_board[(row + 1, column + 1)] > 0 and [row + 1, column + 1] not in clicked:
        show_cell(row + 1, column + 1, alpha, screen, numbered_board, clicked, difficulty)
    if row + 1 < difficulty and column - 1 >= 0 and numbered_board[(row + 1, column - 1)] > 0 and [row + 1, column - 1] not in clicked:
        show_cell(row + 1, column - 1, alpha, screen, numbered_board, clicked, difficulty)
    if row - 1 >= 0 and column + 1 < difficulty and numbered_board[(row - 1, column + 1)] > 0 and [row - 1, column + 1] not in clicked:
        show_cell(row - 1, column + 1, alpha, screen, numbered_board, clicked, difficulty)
    if row - 1 >= 0 and column - 1 >= 0 and numbered_board[(row - 1, column - 1)] > 0 and [row - 1, column - 1] not in clicked:
        show_cell(row - 1, column - 1, alpha, screen, numbered_board, clicked, difficulty)
    if row - 1 >= 0 and column >= 0 and numbered_board[(row - 1, column)] > 0 and [row - 1, column] not in clicked:
        show_cell(row - 1, column, alpha, screen, numbered_board, clicked, difficulty)
    if row + 1 < difficulty and column >= 0 and numbered_board[(row + 1, column)] > 0 and [row + 1, column] not in clicked:
        show_cell(row + 1, column, alpha, screen, numbered_board, clicked, difficulty)
    if row >= 0 and column - 1 >= 0 and numbered_board[(row, column - 1)] > 0 and [row, column - 1] not in clicked:
        show_cell(row, column - 1, alpha, screen, numbered_board, clicked, difficulty)
    if row >= 0 and column + 1 < difficulty and numbered_board[(row, column + 1)] > 0 and [row, column + 1] not in clicked:
        show_cell(row, column + 1, alpha, screen, numbered_board, clicked, difficulty)

    pygame.display.flip()



def get_size(alpha):
    match alpha:
        case 3:
            return ((400 - 10 * 2 - (9 - 1) * alpha) / 9, (400 - 10 * 2 - (9 - 1) * alpha) / 9)
        case 2:
            return ((400 - 10 * 2 - (16 - 1) * alpha) / 16, (400 - 10 * 2 - (16 - 1) * alpha) / 16)
        case 1:
            return ((400 - 10 * 2 - (30 - 1) * alpha) / 30, (400 - 10 * 2 - (30 - 1) * alpha) / 30)
        

def game_over(row, column, alpha, screen, numbered_board, clicked, difficulty):
    mine = pygame.image.load("static/bomb-red.png").convert()
    mine_others = pygame.image.load("static/bomb-gray.png").convert()

    size = get_size(alpha)
    
    scaled_image = pygame.transform.scale(mine, size)
    scaled_image_others = pygame.transform.scale(mine_others, size)

    x = 10 + column * (size[0] + alpha)
    y = 10 + row * (size[1] + alpha)

    screen.blit(scaled_image, (x, y))

    for key, value in numbered_board.items():
        if value == -1 and key != (row, column):
            x = 10 + key[0] * (size[0] + alpha)
            y = 10 + key[1] * (size[1] + alpha)

            screen.blit(scaled_image_others, (x,y))

    pygame.display.flip()



def difficulty_drawer(screen, rect_color, rect_position, text, text_color):
    ''' Draws a rectangle on the screen based on color, position, and text given'''

    pygame.draw.rect(screen, rect_color, rect_position)
    
    font = pygame.font.Font("static/mine-sweeper.ttf", 34)
    text_surface = font.render(text, True, text_color)
    text_rect = text_surface.get_rect(center=(rect_position[0] + rect_position[2] // 2, rect_position[1] + rect_position[3] // 2))

    screen.blit(text_surface, text_rect)


def board_drawer(size: int, alpha: int, mines: int):
    screen = pygame.display.set_mode((600, 600))
    bg_color = (70, 80, 90)
    screen.fill(bg_color)

    padding = 10 # So that squares don't touch precisely the edge
    square_size = (400 - padding * 2 - (size - 1) * alpha) / size

    for row in range(size):
        for column in range(size):
            
            # Determine the x and y positions of the square to place
            x = padding + column * (square_size + alpha)
            y = padding + row * (square_size + alpha)

            # Draw a rectangle of area square_size^2 in the x,y position, gray
            pygame.draw.rect(screen, (198, 198, 198), (x, y, square_size, square_size))

    # Add mines based on difficulty (10 for beginner, 40 for intermediate, 99 for expert), store values of (row, column) in a list
    mine_locations = []
    while mines:
        new_mine = random.randint(0, size * size - 1)
        new_mine_location = [new_mine // 9, new_mine % 9]
        
        if new_mine_location in mine_locations:
            continue # Try again if that spot is taken
        else:
            mine_locations.append([new_mine // 9, new_mine % 9])
            mines -= 1

    pygame.display.flip()
    return mine_locations, screen


def place_mines(locations: list[list[int]], size: int) -> dict:

    # Dictionary holding the number of mines adjacent to each cell
    adjacent_mines = {}

    for row in range(size):
        for column in range(size):

            if [row, column] not in locations:

                # Check (literal) edge cases accordingly
                if row == 0 and column == 0:
                    if [1, 0] in locations:
                        adjacent_mines[(row, column)] = adjacent_mines.get((row, column), 0) + 1
                    if [0, 1] in locations:
                        adjacent_mines[(row, column)] = adjacent_mines.get((row, column), 0) + 1
                    if [1, 1] in locations:
                        adjacent_mines[(row, column)] = adjacent_mines.get((row, column), 0) + 1
                
                elif row == size - 1 and column == size - 1:
                    if [size - 1, size - 2] in locations:
                        adjacent_mines[(row, column)] = adjacent_mines.get((row, column), 0) + 1
                    if [size - 2, size - 1] in locations:
                        adjacent_mines[(row, column)] = adjacent_mines.get((row, column), 0) + 1
                    if [size - 2, size - 2] in locations:
                        adjacent_mines[(row, column)] = adjacent_mines.get((row, column), 0) + 1
                
                elif row == size - 1 and column == 0:
                    if [size - 1, 1] in locations:
                        adjacent_mines[(row, column)] = adjacent_mines.get((row, column), 0) + 1
                    if [size - 2, 0] in locations:
                        adjacent_mines[(row, column)] = adjacent_mines.get((row, column), 0) + 1
                    if [size - 2, 1] in locations:
                        adjacent_mines[(row, column)] = adjacent_mines.get((row, column), 0) + 1
                
                elif row == 0 and column == size - 1:
                    if [1, size - 1] in locations:
                        adjacent_mines[(row, column)] = adjacent_mines.get((row, column), 0) + 1
                    if [0, size - 2] in locations:
                        adjacent_mines[(row, column)] = adjacent_mines.get((row, column), 0) + 1
                    if [1, size - 2] in locations:
                        adjacent_mines[(row, column)] = adjacent_mines.get((row, column), 0) + 1
                
                elif row == 0:
                    if [0, column - 1] in locations:
                        adjacent_mines[(row, column)] = adjacent_mines.get((row, column), 0) + 1
                    if [0, column + 1] in locations:
                        adjacent_mines[(row, column)] = adjacent_mines.get((row, column), 0) + 1
                    if [1, column - 1] in locations:
                        adjacent_mines[(row, column)] = adjacent_mines.get((row, column), 0) + 1
                    if [1, column] in locations:
                        adjacent_mines[(row, column)] = adjacent_mines.get((row, column), 0) + 1
                    if [1, column + 1] in locations:
                        adjacent_mines[(row, column)] = adjacent_mines.get((row, column), 0) + 1
                
                elif column == 0:
                    if [row - 1, 0] in locations:
                        adjacent_mines[(row, column)] = adjacent_mines.get((row, column), 0) + 1
                    if [row + 1, 0] in locations:
                        adjacent_mines[(row, column)] = adjacent_mines.get((row, column), 0) + 1
                    if [row - 1, 1] in locations:
                        adjacent_mines[(row, column)] = adjacent_mines.get((row, column), 0) + 1
                    if [row, 1] in locations:
                        adjacent_mines[(row, column)] = adjacent_mines.get((row, column), 0) + 1
                    if [row + 1, 1] in locations:
                        adjacent_mines[(row, column)] = adjacent_mines.get((row, column), 0) + 1
                
                elif row == size - 1:
                    if [size - 1, column - 1] in locations:
                        adjacent_mines[(row, column)] = adjacent_mines.get((row, column), 0) + 1
                    if [size - 1, column + 1] in locations:
                        adjacent_mines[(row, column)] = adjacent_mines.get((row, column), 0) + 1
                    if [size - 2, column - 1] in locations:
                        adjacent_mines[(row, column)] = adjacent_mines.get((row, column), 0) + 1
                    if [size - 2, column] in locations:
                        adjacent_mines[(row, column)] = adjacent_mines.get((row, column), 0) + 1
                    if [size - 2, column + 1] in locations:
                        adjacent_mines[(row, column)] = adjacent_mines.get((row, column), 0) + 1
                
                elif column == size - 1:
                    if [row - 1, size - 1] in locations:
                        adjacent_mines[(row, column)] = adjacent_mines.get((row, column), 0) + 1
                    if [row + 1, size - 1] in locations:
                        adjacent_mines[(row, column)] = adjacent_mines.get((row, column), 0) + 1
                    if [row - 1, size - 2] in locations:
                        adjacent_mines[(row, column)] = adjacent_mines.get((row, column), 0) + 1
                    if [row, size - 2] in locations:
                        adjacent_mines[(row, column)] = adjacent_mines.get((row, column), 0) + 1
                    if [row + 1, size - 2] in locations:
                        adjacent_mines[(row, column)] = adjacent_mines.get((row, column), 0) + 1
                
                # Treat all center cells
                else: 
                    if [row - 1, column - 1] in locations:
                        adjacent_mines[(row, column)] = adjacent_mines.get((row, column), 0) + 1
                    if [row - 1, column] in locations:
                        adjacent_mines[(row, column)] = adjacent_mines.get((row, column), 0) + 1
                    if [row - 1, column + 1] in locations:
                        adjacent_mines[(row, column)] = adjacent_mines.get((row, column), 0) + 1
                    if [row, column - 1] in locations:
                        adjacent_mines[(row, column)] = adjacent_mines.get((row, column), 0) + 1
                    if [row, column + 1] in locations:
                        adjacent_mines[(row, column)] = adjacent_mines.get((row, column), 0) + 1
                    if [row + 1, column - 1] in locations:
                        adjacent_mines[(row, column)] = adjacent_mines.get((row, column), 0) + 1
                    if [row + 1, column] in locations:
                        adjacent_mines[(row, column)] = adjacent_mines.get((row, column), 0) + 1
                    if [row + 1, column + 1] in locations:
                        adjacent_mines[(row, column)] = adjacent_mines.get((row, column), 0) + 1

                adjacent_mines[(row, column)] = adjacent_mines.get((row, column), 0)

            # Bomb cells will have a value of -1 for easy access
            else:
                adjacent_mines[(row, column)] = adjacent_mines.get((row, column), -1)
    
    return adjacent_mines


if __name__ == "__main__":
    main()
