import os
import random

# Constants
ROWS = 6
COLS = 7
MAX_PLAYERS = 5
PLAYER_SYMBOLS = ['X', 'O', 'V', 'H', 'M']

def clear_screen():
    """Clears the terminal screen."""
    os.system('clear')

def initialize_board(rows, cols):
    """Creates a board with given rows and columns filled with blank spaces."""
    return [[" " for _ in range(cols)] for _ in range(rows)]

def print_board(board):
    """Prints the game board to the console."""
    clear_screen()
    col_labels = "  ".join(chr(65 + i) for i in range(len(board[0])))
    print(f"  {col_labels}")  # Column labels
    print("+---" * len(board[0]) + "+")
    for row in board:
        print("| " + " | ".join(row) + " |")
        print("+---" * len(board[0]) + "+")

def get_valid_column(board, col_input):
    """Validates and converts input column into a valid index."""
    if len(col_input) == 1 and 'A' <= col_input <= chr(65 + len(board[0]) - 1):
        col = ord(col_input) - 65
        if board[0][col] == " ":  # Check if column is not full
            return col
    return None

def drop_checker(board, col, player_symbol):
    """Drops the player's checker into the chosen column."""
    for row in reversed(board):
        if row[col] == " ":
            row[col] = player_symbol
            break

def check_win(board, player_symbol):
    """Checks if the given player has won the game."""
    rows, cols = len(board), len(board[0])
    
    # Check horizontal
    for r in range(rows):
        for c in range(cols - 3):
            if all(board[r][c+i] == player_symbol for i in range(4)):
                return True

    # Check vertical
    for r in range(rows - 3):
        for c in range(cols):
            if all(board[r+i][c] == player_symbol for i in range(4)):
                return True

    # Check diagonal (bottom-left to top-right)
    for r in range(rows - 3):
        for c in range(cols - 3):
            if all(board[r+i][c+i] == player_symbol for i in range(4)):
                return True

    # Check diagonal (top-left to bottom-right)
    for r in range(3, rows):
        for c in range(cols - 3):
            if all(board[r-i][c+i] == player_symbol for i in range(4)):
                return True

    return False

def check_draw(board):
    """Checks if the game is a draw."""
    return all(board[0][col] != " " for col in range(len(board[0])))

def main():
    # Setup game
    board = initialize_board(ROWS, COLS)
    num_players = 2  # Set to 2 initially for this task
    players = PLAYER_SYMBOLS[:num_players]
    current_player_index = random.randint(0, num_players - 1)
    
    print_board(board)

    # Game loop
    while True:
        current_player = players[current_player_index]
        print(f"Player {current_player}, please enter a column:")
        col_input = input().strip().upper()

        col = get_valid_column(board, col_input)

        if col is None:
            print("Invalid input. Please try again.")
            continue
        
        drop_checker(board, col, current_player)
        print_board(board)

        # Check win
        if check_win(board, current_player):
            print(f"Player {current_player} won!")
            break

        # Check draw
        if check_draw(board):
            print("The game is a draw!")
            break

        # Switch to next player
        current_player_index = (current_player_index + 1) % num_players

if __name__ == "__main__":
    main()
