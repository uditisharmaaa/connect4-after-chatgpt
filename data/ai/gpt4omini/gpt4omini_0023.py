import os
import random

# Constants for game settings
ROWS = 6
COLS = 7
PLAYERS = ['X', 'O', 'V', 'H', 'M']  # Up to 5 players

def create_board():
    """Create the Connect 4 board."""
    return [[' ' for _ in range(COLS)] for _ in range(ROWS)]

def print_board(board):
    """Print the game board."""
    os.system('clear')
    print("  " + "   ".join(chr(65 + i) for i in range(COLS)))  # Column labels A-G
    print("+" + "---+" * COLS)
    for row in board:
        print("| " + " | ".join(row) + " |")
        print("+" + "---+" * COLS)

def get_valid_input(current_player):
    """Get valid column input from the current player."""
    while True:
        column = input(f"Player {current_player}, please enter a column (A-{chr(65 + COLS - 1)}): ").upper()
        if len(column) == 1 and 'A' <= column <= chr(65 + COLS - 1):
            col_index = ord(column) - 65
            if board[0][col_index] == ' ':  # Check if the column is not full
                return col_index
            else:
                print("Column is full. Try another column.")
        else:
            print("Invalid input. Please enter a valid column letter.")

def place_checker(board, column, checker):
    """Place a checker in the specified column."""
    for row in reversed(board):  # Start from the bottom of the column
        if row[column] == ' ':
            row[column] = checker
            return True
    return False

def check_win(board, checker):
    """Check all possible win conditions for the current player."""
    # Horizontal check
    for r in range(ROWS):
        for c in range(COLS - 3):
            if all(board[r][c + i] == checker for i in range(4)):
                return True

    # Vertical check
    for c in range(COLS):
        for r in range(ROWS - 3):
            if all(board[r + i][c] == checker for i in range(4)):
                return True

    # Diagonal checks
    for r in range(ROWS - 3):
        for c in range(COLS - 3):
            if all(board[r + i][c + i] == checker for i in range(4)):
                return True
        for c in range(3, COLS):
            if all(board[r + i][c - i] == checker for i in range(4)):
                return True

    return False

def check_draw(board):
    """Check if the board is full and there are no winners."""
    return all(board[0][c] != ' ' for c in range(COLS))

# Initialize the game
board = create_board()
current_player_index = random.randint(0, len(PLAYERS) - 1)
game_over = False

print_board(board)

# Game loop
while not game_over:
    current_player = PLAYERS[current_player_index]
    column = get_valid_input(current_player)
    place_checker(board, column, current_player)

    print_board(board)

    if check_win(board, current_player):
        print(f"Player {current_player} won!")
        game_over = True
    elif check_draw(board):
        print("The game is a draw!")
        game_over = True
    else:
        current_player_index = (current_player_index + 1) % len(PLAYERS)
