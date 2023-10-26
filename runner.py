# runner.py

import pygame
import sys
from sudoku_game import print_board, is_valid_move, solve_sudoku, generate_sudoku

# Initialize Pygame
pygame.init()

# Constants
SCREEN_WIDTH = 600
SCREEN_HEIGHT = 650
GRID_SIZE = 9
CELL_SIZE = SCREEN_WIDTH // GRID_SIZE
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
RED = (255, 0, 0)
GREEN = (0, 255, 0)
BLUE = (0, 0, 255)

# Create a Pygame screen
screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
pygame.display.set_caption("Sudoku")

# Create a Sudoku board
board = generate_sudoku()
selected_cell = (0, 0)
error_message = ""

# Define the Next Move (AI) button aligned to the bottom left
next_move_button = pygame.Rect(10, SCREEN_HEIGHT - 60, SCREEN_WIDTH // 3 - 20, 50)
next_move_font = pygame.font.Font(None, 36)
next_move_text = next_move_font.render("Next Move (AI)", True, WHITE)
next_move_text_rect = next_move_text.get_rect(center=next_move_button.center)

# Define the Play Again button aligned to the bottom right
play_again_button = pygame.Rect(SCREEN_WIDTH - SCREEN_WIDTH // 4 + 10, SCREEN_HEIGHT - 60, SCREEN_WIDTH // 4 - 20, 50)
play_again_font = pygame.font.Font(None, 36)
play_again_text = play_again_font.render("Play Again", True, WHITE)
play_again_text_rect = play_again_text.get_rect(center=play_again_button.center)

game_completed = False

def draw_board():
    # Clear the screen
    screen.fill(WHITE)

    # Draw gridlines
    for x in range(0, SCREEN_WIDTH, CELL_SIZE):
        line_color = BLACK if x % (3 * CELL_SIZE) == 0 else (150, 150, 150)  # Darker lines for 3x3 boxes
        pygame.draw.line(screen, line_color, (x, 0), (x, SCREEN_HEIGHT))
    for y in range(0, SCREEN_HEIGHT, CELL_SIZE):
        line_color = BLACK if y % (3 * CELL_SIZE) == 0 else (150, 150, 150)  # Darker lines for 3x3 boxes
        pygame.draw.line(screen, line_color, (0, y), (SCREEN_WIDTH, y))

    # Draw numbers
    for row in range(GRID_SIZE):
        for col in range(GRID_SIZE):
            cell_value = board[row][col]
            if cell_value != 0:
                font = pygame.font.Font(None, 36)
                text = font.render(str(cell_value), True, BLUE)
                text_rect = text.get_rect(center=(col * CELL_SIZE + CELL_SIZE // 2, row * CELL_SIZE + CELL_SIZE // 2))
                screen.blit(text, text_rect)

    # Display error message
    if error_message:
        font = pygame.font.Font(None, 28)
        text = font.render(error_message, True, RED)
        text_rect = text.get_rect(center=(SCREEN_WIDTH // 2, SCREEN_HEIGHT - 60))
        screen.blit(text, text_rect)

    # Draw Next Move (AI) button
    pygame.draw.rect(screen, GREEN, next_move_button)
    screen.blit(next_move_text, next_move_text_rect)

    # Draw Play Again button
    pygame.draw.rect(screen, GREEN, play_again_button)
    screen.blit(play_again_text, play_again_text_rect)

def is_sudoku_complete(board):
    for row in board:
        if 0 in row:
            return False
    return True


def make_ai_move(board):
    for row in range(9):
        for col in range(9):
            if board[row][col] == 0:
                for num in range(1, 10):
                    if is_valid_move(board, row, col, num):
                        temp_board = [row[:] for row in board]
                        temp_board[row][col] = num
                        if solve_sudoku(temp_board):
                            board[row][col] = num
                            return True
    return False

def main():
    global selected_cell, error_message, game_completed, board
    ai_moved = False  # Variable to track if the AI has made a move

    while True:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()

            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_UP:
                    selected_cell = (max(selected_cell[0] - 1, 0), selected_cell[1])
                elif event.key == pygame.K_DOWN:
                    selected_cell = (min(selected_cell[0] + 1, GRID_SIZE - 1), selected_cell[1])
                elif event.key == pygame.K_LEFT:
                    selected_cell = (selected_cell[0], max(selected_cell[1] - 1, 0))
                elif event.key == pygame.K_RIGHT:
                    selected_cell = (selected_cell[0], min(selected_cell[1] + 1, GRID_SIZE - 1))
                elif pygame.K_1 <= event.key <= pygame.K_9:
                    num = event.key - pygame.K_0  # Convert key code to number
                    if board[selected_cell[0]][selected_cell[1]] == 0:  # Check if it's an empty cell
                        if is_valid_move(board, *selected_cell, num):
                            board[selected_cell[0]][selected_cell[1]] = num
                            error_message = ""
                        else:
                            error_message = "Invalid move!"
                    else:
                        error_message = "Can't modify initial values!"
                elif event.key == pygame.K_BACKSPACE:
                    if board[selected_cell[0]][selected_cell[1]] != 0:
                        board[selected_cell[0]][selected_cell[1]] = 0
                        error_message = ""

            # Mouse click event handling
            if event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:  # Left mouse button
                mouse_x, mouse_y = event.pos
                clicked_row = mouse_y // CELL_SIZE
                clicked_col = mouse_x // CELL_SIZE

                if 0 <= clicked_row < GRID_SIZE and 0 <= clicked_col < GRID_SIZE:  # Check if the coordinates are within the valid range
                    if board[clicked_row][clicked_col] == 0:
                        selected_cell = (clicked_row, clicked_col)

            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_r and game_completed:
                    board = generate_sudoku()
                    selected_cell = (0, 0)
                    error_message = ""
                    game_completed = False
                if event.key == pygame.K_m:  # Press 'M' key to make an AI move
                    ai_moved = make_ai_move(board)

            # Handle Next Move (AI) button click
            if event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:
                mouse_x, mouse_y = event.pos
                if next_move_button.collidepoint(mouse_x, mouse_y):
                    ai_moved = make_ai_move(board)

            # Handle Play Again button click
            if event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:
                mouse_x, mouse_y = event.pos
                if play_again_button.collidepoint(mouse_x, mouse_y):
                    board = generate_sudoku()
                    selected_cell = (0, 0)
                    error_message = ""
                    game_completed = False

        draw_board()
        pygame.draw.rect(screen, GREEN, (selected_cell[1] * CELL_SIZE, selected_cell[0] * CELL_SIZE, CELL_SIZE, CELL_SIZE), 2)

        if is_sudoku_complete(board) and not game_completed:
            error_message = "Sudoku Completed!"
            game_completed = True

        if game_completed:
            # Display "Play Again" message
            font = pygame.font.Font(None, 36)
            text = font.render("Play Again (Press R) or Click the Button", True, GREEN)
            text_rect = text.get_rect(center=(SCREEN_WIDTH // 2, SCREEN_HEIGHT // 2))
            screen.blit(text, text_rect)

        pygame.display.flip()

if __name__ == "__main__":
    main()