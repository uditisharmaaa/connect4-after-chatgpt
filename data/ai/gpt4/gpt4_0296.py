import os
import random

# Constants
ROWS = 6
COLS = 7
PLAYERS = 2
CHECKERS = ["X", "O", "V", "H", "M"]
EMPTY = " "

# Helper functions
def clear_screen():
    os.system('clear')  # Use 'cls' on Windows

def initialize_board(rows, cols):
    return [[EMPTY for _ in range(cols)] for _ in range(rows)]

def print_board(board):
    clear_screen()
    headers = "  " + "   ".join(chr(65 + i) for i in range(COLS))
    print(headers)
    print("+" + "---+" * COLS)
    for row in board:
        print("|" + "|".join(f" {cell} " for cell in row) + "|")
        print("+" + "---+" * COLS)

def is_valid_input(column, board):
    if not column.isalpha() or len(column) != 1:
        return False
    col_index = ord(column.upper()) - 65
    if col_index < 0 or col_index >= COLS:
        return False
    return board[0][col_index] == EMPTY

def get_lowest_empty_row(board, col_index):
    for row in range(ROWS - 1, -1, -1):
        if board[row][col_index] == EMPTY:
            return row
    return -1

def place_checker(board, col_index, checker):
    row_index = get_lowest_empty_row(board, col_index)
    if row_index != -1:
        board[row_index][col_index] = checker
    return row_index

def check_for_win(board, checker):
    # Check horizontal
    for row in range(ROWS):
        for col in range(COLS - 3):
            if all(board[row][col + i] == checker for i in range(4)):
                return True

    # Check vertical
    for row in range(ROWS - 3):
        for col in range(COLS):
            if all(board[row + i][col] == checker for i in range(4)):
                return True

    # Check diagonal (bottom-left to top-right)
    for row in range(ROWS - 3):
        for col in range(COLS - 3):
            if all(board[row + i][col + i] == checker for i in range(4)):
                return True

    # Check diagonal (top-left to bottom-right)
    for row in range(3, ROWS):
        for col in range(COLS - 3):
            if all(board[row - i][col + i] == checker for i in range(4)):
                return True
    
    return False

def check_for_draw(board):
    return all(cell != EMPTY for cell in board[0])

# Main game loop
def play_game():
    board = initialize_board(ROWS, COLS)
    players = [CHECKERS[i] for i in range(PLAYERS)]
    current_player_index = random.randint(0, PLAYERS - 1)

    print_board(board)
    print(f"Randomly chosen player to start: {players[current_player_index]}")

    while True:
        print_board(board)
        current_player = players[current_player_index]
        column = input(f"Player {current_player}, please enter a column: ").strip().upper()

        if not is_valid_input(column, board):
            print("Invalid input. Please try again.")
            continue

        col_index = ord(column) - 65
        place_checker(board, col_index, current_player)

        # Check for win
        if check_for_win(board, current_player):
            print_board(board)
            print(f"Player {current_player} won!")
            break

        # Check for draw
        if check_for_draw(board):
            print_board(board)
            print("The game is a draw!")
            break

        # Move to the next player
        current_player_index = (current_player_index + 1) % PLAYERS

if __name__ == "__main__":
    play_game()
