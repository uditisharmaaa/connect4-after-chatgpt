import os
import random

# Constants
ROWS = 6
COLUMNS = 7
PLAYER_COUNT = 2
MARKERS = ["X", "O", "V", "H", "M"]  # Potential markers for up to 5 players

# Initialize board
def create_board():
    return [[" " for _ in range(COLUMNS)] for _ in range(ROWS)]

# Display board
def print_board(board):
    os.system('clear')  # Clear the screen
    print("  " + "   ".join([chr(65 + i) for i in range(COLUMNS)]))
    for row in board:
        print("+---" * COLUMNS + "+")
        print("| " + " | ".join(row) + " |")
    print("+---" * COLUMNS + "+")

# Check if a column is valid and has space
def is_valid_column(board, column):
    return 0 <= column < COLUMNS and board[0][column] == " "

# Get the next available row in a column
def get_next_open_row(board, col):
    for r in range(ROWS-1, -1, -1):
        if board[r][col] == " ":
            return r
    return None

# Drop marker in chosen column
def drop_checker(board, row, col, checker):
    board[row][col] = checker

# Win checking logic
def check_win(board, checker):
    # Check horizontal locations
    for c in range(COLUMNS-3):
        for r in range(ROWS):
            if all(board[r][c+i] == checker for i in range(4)):
                return True

    # Check vertical locations
    for c in range(COLUMNS):
        for r in range(ROWS-3):
            if all(board[r+i][c] == checker for i in range(4)):
                return True

    # Check positively sloped diagonals
    for c in range(COLUMNS-3):
        for r in range(ROWS-3):
            if all(board[r+i][c+i] == checker for i in range(4)):
                return True

    # Check negatively sloped diagonals
    for c in range(COLUMNS-3):
        for r in range(3, ROWS):
            if all(board[r-i][c+i] == checker for i in range(4)):
                return True

    return False

# Check for draw
def check_draw(board):
    return all(board[0][c] != " " for c in range(COLUMNS))

# Main game loop
def play_game():
    board = create_board()
    game_over = False
    turn = random.randint(0, PLAYER_COUNT - 1)  # Randomly select first player

    while not game_over:
        print_board(board)
        print(f"Player {MARKERS[turn]}'s turn")
        col_input = input("Please enter a column (A-G): ").upper()

        if len(col_input) != 1 or not ('A' <= col_input <= 'G'):
            print("Invalid input! Please enter a letter from A to G.")
            continue

        col = ord(col_input) - ord('A')  # Convert column letter to index

        if not is_valid_column(board, col):
            print(f"Column {col_input} is full! Try another column.")
            continue

        row = get_next_open_row(board, col)
        drop_checker(board, row, col, MARKERS[turn])

        if check_win(board, MARKERS[turn]):
            print_board(board)
            print(f"Player {MARKERS[turn]} won!")
            game_over = True
        elif check_draw(board):
            print_board(board)
            print("The game is a draw!")
            game_over = True
        else:
            turn = (turn + 1) % PLAYER_COUNT  # Alternate turns

# Set board dimensions and number of players for submission requirement
ROWS = 6
COLUMNS = 7
PLAYER_COUNT = 2

if __name__ == "__main__":
    play_game()
