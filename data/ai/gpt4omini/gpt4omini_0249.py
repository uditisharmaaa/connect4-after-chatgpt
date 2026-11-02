import os
import random

# Constants
ROWS = 6
COLS = 7
PLAYERS = 2
CHECKERS = ['X', 'O']  # Can be expanded to ['X', 'O', 'V', 'H', 'M'] for more players

def create_board():
    """Create a new game board."""
    return [[" " for _ in range(COLS)] for _ in range(ROWS)]

def print_board(board):
    """Print the current state of the game board."""
    os.system('clear')  # For Linux/Unix systems
    print("  " + "   ".join(chr(65 + i) for i in range(COLS)))
    print("+" + "---+" * COLS)
    for row in board:
        print("| " + " | ".join(row) + " |")
        print("+" + "---+" * COLS)

def get_valid_input(player):
    """Prompt the player for input until a valid column is given."""
    while True:
        user_input = input(f"Player {CHECKERS[player]}, please enter a column: ").upper()
        if len(user_input) == 1 and 'A' <= user_input <= 'G':
            col = ord(user_input) - 65
            if board[0][col] == " ":
                return col
            else:
                print("Column is full, try again.")
        else:
            print("Invalid input, please enter a letter from A to G.")

def place_checker(board, col, player):
    """Place the player's checker in the chosen column."""
    for row in reversed(board):  # Start from the bottom of the column
        if row[col] == " ":
            row[col] = CHECKERS[player]
            return True
    return False  # Should not happen because of prior validation

def check_win(board):
    """Check for a win in the game."""
    # Check horizontal
    for r in range(ROWS):
        for c in range(COLS - 3):
            if board[r][c] != " " and all(board[r][c] == board[r][c + i] for i in range(4)):
                return True

    # Check vertical
    for c in range(COLS):
        for r in range(ROWS - 3):
            if board[r][c] != " " and all(board[r][c] == board[r + i][c] for i in range(4)):
                return True

    # Check diagonal (bottom-left to top-right)
    for r in range(ROWS - 3):
        for c in range(COLS - 3):
            if board[r][c] != " " and all(board[r][c] == board[r + i][c + i] for i in range(4)):
                return True

    # Check diagonal (top-left to bottom-right)
    for r in range(3, ROWS):
        for c in range(COLS - 3):
            if board[r][c] != " " and all(board[r][c] == board[r - i][c + i] for i in range(4)):
                return True

    return False

def check_draw(board):
    """Check for a draw in the game."""
    return all(board[0][c] != " " for c in range(COLS))

# Game setup
board = create_board()
current_player = random.randint(0, PLAYERS - 1)

# Game loop
while True:
    print_board(board)
    col = get_valid_input(current_player)
    place_checker(board, col, current_player)

    if check_win(board):
        print_board(board)
        print(f"Player {CHECKERS[current_player]} won!")
        break
    
    if check_draw(board):
        print_board(board)
        print("The game is a draw!")
        break
    
    current_player = (current_player + 1) % PLAYERS
