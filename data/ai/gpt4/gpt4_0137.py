import os
import random

# Global constants
ROWS = 6
COLUMNS = 7
PLAYERS = 2
CHECKER_SYMBOLS = ["X", "O", "V", "H", "M"]

def create_board():
    """Initialize the game board with empty spaces."""
    return [[" " for _ in range(COLUMNS)] for _ in range(ROWS)]

def print_board(board):
    """Print the current state of the board."""
    os.system('clear')  # Clear the screen
    column_labels = "  " + "   ".join(chr(65 + i) for i in range(COLUMNS))
    print(column_labels)
    print("+---" * COLUMNS + "+")
    for row in board:
        print("| " + " | ".join(row) + " |")
        print("+---" * COLUMNS + "+")

def is_valid_input(input_col):
    """Validate if the input column is valid."""
    return len(input_col) == 1 and input_col.isalpha() and 'A' <= input_col < chr(65 + COLUMNS)

def get_column_index(input_col):
    """Convert column letter to zero-based index."""
    return ord(input_col) - 65

def place_checker(board, column_index, checker):
    """Place the player's checker in the chosen column."""
    for row in range(ROWS - 1, -1, -1):  # Start from the bottom row
        if board[row][column_index] == " ":
            board[row][column_index] = checker
            return True
    return False  # Column is full

def check_winner(board, checker):
    """Check if the given checker forms a line of 4."""
    # Check horizontal
    for row in range(ROWS):
        for col in range(COLUMNS - 3):
            if all(board[row][col + i] == checker for i in range(4)):
                return True

    # Check vertical
    for col in range(COLUMNS):
        for row in range(ROWS - 3):
            if all(board[row + i][col] == checker for i in range(4)):
                return True

    # Check diagonal (bottom-left to top-right)
    for row in range(ROWS - 3):
        for col in range(COLUMNS - 3):
            if all(board[row + i][col + i] == checker for i in range(4)):
                return True

    # Check diagonal (top-left to bottom-right)
    for row in range(3, ROWS):
        for col in range(COLUMNS - 3):
            if all(board[row - i][col + i] == checker for i in range(4)):
                return True

    return False

def is_draw(board):
    """Check if the board is full (draw)."""
    for row in board:
        if " " in row:
            return False
    return True

def main():
    # Setup the game
    board = create_board()
    players = [CHECKER_SYMBOLS[i] for i in range(PLAYERS)]
    current_player = random.choice(players)
    
    print_board(board)
    print(f"Player {current_player} starts first!\n")
    
    while True:
        # Player turn
        print_board(board)
        input_col = input(f"Player {current_player}, please enter a column: ").strip().upper()
        
        if not is_valid_input(input_col):
            print("Invalid input. Please enter a valid column letter.")
            continue
        
        column_index = get_column_index(input_col)
        if not place_checker(board, column_index, current_player):
            print("Column is full. Choose a different column.")
            continue
        
        # Check for a winner or draw
        if check_winner(board, current_player):
            print_board(board)
            print(f"Player {current_player} won!")
            break
        if is_draw(board):
            print_board(board)
            print("It's a draw!")
            break
        
        # Switch to the next player
        current_index = players.index(current_player)
        current_player = players[(current_index + 1) % PLAYERS]

if __name__ == "__main__":
    main()
