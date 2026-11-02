import os
import random

# Constants
ROWS = 6
COLS = 7
PLAYERS = 2
CHECKERS = ["X", "O", "V", "H", "M"]  # Checker symbols for up to 5 players
VALID_INPUT = [chr(i) for i in range(ord('A'), ord('A') + COLS)]

# Initialize board
def create_board():
    return [[" " for _ in range(COLS)] for _ in range(ROWS)]

# Print the board
def print_board(board):
    os.system('clear')  # Use 'cls' for Windows if needed
    print("  " + "   ".join(VALID_INPUT))
    print("+---" * COLS + "+")
    for row in board:
        print("| " + " | ".join(row) + " |")
        print("+---" * COLS + "+")

# Select starting player randomly
def select_starting_player():
    return random.randint(0, PLAYERS - 1)

# Get valid column input
def get_valid_input(board, player):
    while True:
        col = input(f"Player {CHECKERS[player]}, please enter a column: ").upper()
        if col in VALID_INPUT and board[0][VALID_INPUT.index(col)] == " ":
            return VALID_INPUT.index(col)
        print("Invalid input, please try again.")

# Place checker in column
def place_checker(board, col, checker):
    for row in reversed(board):
        if row[col] == " ":
            row[col] = checker
            return

# Check for win
def check_win(board, checker):
    # Horizontal check
    for row in board:
        for col in range(COLS - 3):
            if all(cell == checker for cell in row[col:col+4]):
                return True

    # Vertical check
    for col in range(COLS):
        for row in range(ROWS - 3):
            if all(board[row+i][col] == checker for i in range(4)):
                return True

    # Diagonal checks
    for row in range(ROWS - 3):
        for col in range(COLS - 3):
            if all(board[row+i][col+i] == checker for i in range(4)):
                return True
        for col in range(3, COLS):
            if all(board[row+i][col-i] == checker for i in range(4)):
                return True

    return False

# Check for draw
def check_draw(board):
    return all(board[0][col] != " " for col in range(COLS))

# Main game loop
def play_game():
    board = create_board()
    current_player = select_starting_player()
    print_board(board)

    while True:
        col = get_valid_input(board, current_player)
        place_checker(board, col, CHECKERS[current_player])
        print_board(board)

        if check_win(board, CHECKERS[current_player]):
            print(f"Player {CHECKERS[current_player]} won!")
            break
        elif check_draw(board):
            print("The game is a draw!")
            break

        current_player = (current_player + 1) % PLAYERS

play_game()
