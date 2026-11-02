import os
import random

# Constants
ROWS = 6
COLS = 7
PLAYERS = 2
CHECKERS = ['X', 'O', 'V', 'H', 'M']

# Initialize board
board = [[" " for _ in range(COLS)] for _ in range(ROWS)]

# Print the board
def print_board():
    os.system('clear')
    print("  " + "   ".join(chr(65 + i) for i in range(COLS)))
    print("+---" * COLS + "+")
    for row in board:
        print("| " + " | ".join(row) + " |")
        print("+---" * COLS + "+")

# Check if input is valid
def is_valid_input(input_col):
    if len(input_col) != 1 or not input_col.isalpha():
        return False
    col = ord(input_col.upper()) - 65
    if col < 0 or col >= COLS or board[0][col] != " ":
        return False
    return True

# Drop checker into column
def place_checker(col, checker):
    for row in reversed(range(ROWS)):
        if board[row][col] == " ":
            board[row][col] = checker
            return row

# Check if a player has won
def check_winner(row, col, checker):
    # Check horizontal
    count = 0
    for c in range(COLS):
        if board[row][c] == checker:
            count += 1
            if count == 4:
                return True
        else:
            count = 0

    # Check vertical
    count = 0
    for r in range(ROWS):
        if board[r][col] == checker:
            count += 1
            if count == 4:
                return True
        else:
            count = 0

    # Check descending diagonal
    count = 0
    for i in range(-min(row, col), min(ROWS - row, COLS - col)):
        if board[row + i][col + i] == checker:
            count += 1
            if count == 4:
                return True
        else:
            count = 0

    # Check ascending diagonal
    count = 0
    for i in range(-min(row, COLS - col - 1), min(ROWS - row, col + 1)):
        if board[row + i][col - i] == checker:
            count += 1
            if count == 4:
                return True
        else:
            count = 0

    return False

# Check if the board is full (draw)
def is_draw():
    for col in range(COLS):
        if board[0][col] == " ":
            return False
    return True

# Game loop
def play_game():
    current_player = random.randint(0, PLAYERS - 1)
    print_board()

    while True:
        print(f"Player {CHECKERS[current_player]}, please enter a column:")
        player_input = input().strip().upper()

        if not is_valid_input(player_input):
            print("Invalid input. Please try again.")
            continue

        col = ord(player_input) - 65
        row = place_checker(col, CHECKERS[current_player])
        print_board()

        if check_winner(row, col, CHECKERS[current_player]):
            print(f"Player {CHECKERS[current_player]} won!")
            break

        if is_draw():
            print("It's a draw!")
            break

        current_player = (current_player + 1) % PLAYERS

# Run the game
play_game()
