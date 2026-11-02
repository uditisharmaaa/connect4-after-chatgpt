import os
import random

# Constants
ROWS = 6
COLS = 7
PLAYERS = ["X", "O", "V", "H", "M"]  # Supports up to 5 players

def create_board():
    """Initialize the Connect 4 board."""
    return [[" " for _ in range(COLS)] for _ in range(ROWS)]

def print_board(board):
    """Print the current state of the board."""
    os.system('clear')  # Clear the screen
    print("  " + "   ".join(chr(65 + i) for i in range(COLS)))
    print("+" + "---+" * COLS)
    for row in board:
        print("| " + " | ".join(row) + " |")
        print("+" + "---+" * COLS)

def get_valid_input():
    """Prompt the user for a valid column and return the corresponding index."""
    while True:
        try:
            column = input(f"Player {current_player}, please enter a column: ").upper()
            if len(column) != 1 or column < 'A' or column >= chr(65 + COLS):
                raise ValueError("Invalid column input.")
            col_index = ord(column) - 65
            return col_index
        except ValueError as e:
            print(f"Invalid input: {e}")

def place_checker(board, col_index, player):
    """Place the player's checker on the board in the specified column."""
    for row in reversed(board):
        if row[col_index] == " ":
            row[col_index] = player
            return True
    return False  # Column is full

def check_winner(board):
    """Check if there is a winner on the board."""
    # Check horizontal, vertical, and diagonal
    for r in range(ROWS):
        for c in range(COLS - 3):
            if (board[r][c] == board[r][c + 1] == board[r][c + 2] == board[r][c + 3] != " "):
                return True

    for c in range(COLS):
        for r in range(ROWS - 3):
            if (board[r][c] == board[r + 1][c] == board[r + 2][c] == board[r + 3][c] != " "):
                return True

    for r in range(ROWS - 3):
        for c in range(COLS - 3):
            if (board[r][c] == board[r + 1][c + 1] == board[r + 2][c + 2] == board[r + 3][c + 3] != " "):
                return True

    for r in range(3, ROWS):
        for c in range(COLS - 3):
            if (board[r][c] == board[r - 1][c + 1] == board[r - 2][c + 2] == board[r - 3][c + 3] != " "):
                return True

    return False

def check_draw(board):
    """Check if the game is a draw."""
    return all(cell != " " for row in board for cell in row)

# Main game loop
board = create_board()
current_player_index = random.randint(0, len(PLAYERS) - 1)
is_winner = False

while not is_winner and not check_draw(board):
    current_player = PLAYERS[current_player_index]
    print_board(board)
    col_index = get_valid_input()

    while not place_checker(board, col_index, current_player):
        print("Column is full, please choose another column.")
        col_index = get_valid_input()

    is_winner = check_winner(board)
    current_player_index = (current_player_index + 1) % len(PLAYERS)

if is_winner:
    print_board(board)
    print(f"Player {current_player} won!")
else:
    print_board(board)
    print("The game is a draw!")
