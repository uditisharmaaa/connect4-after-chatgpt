import os
import random

# Constants for game configuration
ROWS = 6
COLUMNS = 7
MAX_PLAYERS = 5
PLAYER_SYMBOLS = ["X", "O", "V", "H", "M"]

def clear_screen():
    """Clear the console screen."""
    os.system('clear')

def create_board(rows, cols):
    """Create a 2D board initialized with empty spaces."""
    return [[" " for _ in range(cols)] for _ in range(rows)]

def print_board(board):
    """Print the current state of the board."""
    clear_screen()
    # Print column headers (A, B, C, ...)
    print("  " + "   ".join(chr(65 + i) for i in range(len(board[0]))))
    print("+---" * len(board[0]) + "+")
    # Print each row with borders
    for row in board:
        print("| " + " | ".join(row) + " |")
        print("+---" * len(board[0]) + "+")

def get_valid_column(board, input_prompt):
    """Prompt the user for a column, and ensure it is valid."""
    while True:
        column_input = input(input_prompt).strip().upper()
        if len(column_input) != 1 or not column_input.isalpha():
            print("Invalid input. Please enter a single letter corresponding to a column.")
            continue
        column_index = ord(column_input) - 65
        if column_index < 0 or column_index >= len(board[0]):
            print("Column out of range. Please try again.")
            continue
        if board[0][column_index] != " ":
            print("Column full. Please choose a different column.")
            continue
        return column_index

def place_checker(board, column, symbol):
    """Place the player's checker in the selected column."""
    for row in reversed(board):  # Start from the bottom row
        if row[column] == " ":
            row[column] = symbol
            return

def check_winner(board, symbol):
    """Check if the given player has won."""
    rows, cols = len(board), len(board[0])
    
    # Check horizontal win
    for r in range(rows):
        for c in range(cols - 3):
            if board[r][c] == board[r][c+1] == board[r][c+2] == board[r][c+3] == symbol:
                return True

    # Check vertical win
    for r in range(rows - 3):
        for c in range(cols):
            if board[r][c] == board[r+1][c] == board[r+2][c] == board[r+3][c] == symbol:
                return True

    # Check diagonals (\ direction)
    for r in range(rows - 3):
        for c in range(cols - 3):
            if board[r][c] == board[r+1][c+1] == board[r+2][c+2] == board[r+3][c+3] == symbol:
                return True

    # Check diagonals (/ direction)
    for r in range(3, rows):
        for c in range(cols - 3):
            if board[r][c] == board[r-1][c+1] == board[r-2][c+2] == board[r-3][c+3] == symbol:
                return True

    return False

def is_draw(board):
    """Check if the game is a draw (board is full)."""
    return all(cell != " " for row in board for cell in row)

def play_game():
    """Main game loop."""
    # Initialize game variables
    board = create_board(ROWS, COLUMNS)
    players = 2  # Set number of players (can be changed later)
    player_symbols = PLAYER_SYMBOLS[:players]
    current_player_index = random.randint(0, players - 1)

    print_board(board)
    print(f"Player {player_symbols[current_player_index]} goes first!")

    # Main game loop
    while True:
        current_player = player_symbols[current_player_index]
        print_board(board)
        column = get_valid_column(board, f"Player {current_player}, please enter a column: ")
        place_checker(board, column, current_player)

        # Check for a winner or draw
        if check_winner(board, current_player):
            print_board(board)
            print(f"Player {current_player} won!")
            break
        elif is_draw(board):
            print_board(board)
            print("It's a draw!")
            break

        # Switch to next player
        current_player_index = (current_player_index + 1) % players

if __name__ == "__main__":
    play_game()
