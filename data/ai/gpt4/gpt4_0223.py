import os
import random

# Constants
ROWS = 6
COLS = 7
MAX_PLAYERS = 5
PLAYER_SYMBOLS = ["X", "O", "V", "H", "M"]

def clear_screen():
    """Clears the terminal screen."""
    os.system('clear')

def initialize_board():
    """Creates and returns an empty game board."""
    return [[" " for _ in range(COLS)] for _ in range(ROWS)]

def print_board(board):
    """Prints the game board to the terminal."""
    clear_screen()

    # Print column labels
    print("  " + "   ".join(chr(65 + i) for i in range(COLS)))
    
    # Print the rows of the board
    for row in board:
        print("+---" * COLS + "+")
        print("| " + " | ".join(row) + " |")
    print("+---" * COLS + "+")

def get_player_input(board):
    """Prompts the current player for input until valid input is given."""
    while True:
        column = input(f"Player {PLAYER_SYMBOLS[current_player]}, please enter a column: ").upper()
        
        # Validate input
        if len(column) != 1 or not column.isalpha():
            print("Invalid input. Please enter a valid column letter.")
            continue

        col_index = ord(column) - 65
        if col_index < 0 or col_index >= COLS:
            print(f"Invalid column. Please select a column between A and {chr(64 + COLS)}.")
            continue

        if board[0][col_index] != " ":
            print("Column is full. Please choose a different column.")
            continue

        return col_index

def place_checker(board, col_index, player):
    """Places the player's checker in the specified column."""
    for row in reversed(board):
        if row[col_index] == " ":
            row[col_index] = PLAYER_SYMBOLS[player]
            break

def check_for_win(board, player):
    """Checks if the current player has won the game."""
    symbol = PLAYER_SYMBOLS[player]
    
    # Check horizontally
    for row in board:
        for col in range(COLS - 3):
            if all(cell == symbol for cell in row[col:col + 4]):
                return True

    # Check vertically
    for col in range(COLS):
        for row in range(ROWS - 3):
            if all(board[row + i][col] == symbol for i in range(4)):
                return True

    # Check diagonally (top-left to bottom-right)
    for row in range(ROWS - 3):
        for col in range(COLS - 3):
            if all(board[row + i][col + i] == symbol for i in range(4)):
                return True

    # Check diagonally (bottom-left to top-right)
    for row in range(3, ROWS):
        for col in range(COLS - 3):
            if all(board[row - i][col + i] == symbol for i in range(4)):
                return True

    return False

def check_for_draw(board):
    """Checks if the board is completely filled (resulting in a draw)."""
    return all(cell != " " for row in board for cell in row)

# Game initialization
board = initialize_board()
num_players = 2  # Set to 2 players for now
current_player = random.randint(0, num_players - 1)

# Print initial board
print_board(board)

# Game loop
while True:
    col_index = get_player_input(board)
    place_checker(board, col_index, current_player)
    print_board(board)

    # Check for win
    if check_for_win(board, current_player):
        print(f"Player {PLAYER_SYMBOLS[current_player]} won!")
        break

    # Check for draw
    if check_for_draw(board):
        print("The game is a draw!")
        break

    # Switch to the next player
    current_player = (current_player + 1) % num_players
