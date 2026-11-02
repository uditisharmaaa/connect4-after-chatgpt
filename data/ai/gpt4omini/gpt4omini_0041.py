import os
import random

# Constants for board dimensions and player symbols
ROWS = 6
COLS = 7
PLAYERS = ['X', 'O', 'V', 'H', 'M']  # Players symbols

def create_board():
    """Create a game board initialized with spaces."""
    return [[" " for _ in range(COLS)] for _ in range(ROWS)]

def print_board(board):
    """Prints the current state of the board."""
    os.system('clear')  # Clear the console
    print("  " + "   ".join(chr(65 + i) for i in range(COLS)))  # Column labels A-G
    print("+" + "---+" * COLS)
    for row in board:
        print("| " + " | ".join(row) + " |")  # Print each row
        print("+" + "---+" * COLS)

def is_valid_input(col):
    """Check if the input is a valid column ('A' through the number of columns)."""
    return col.isalpha() and len(col) == 1 and ord(col.upper()) - 65 < COLS

def get_column_index(col):
    """Return the column index corresponding to the input."""
    return ord(col.upper()) - 65

def is_column_full(board, col_index):
    """Check if the specified column is full."""
    return board[0][col_index] != " "

def place_checker(board, col_index, checker):
    """Place a checker in the specified column."""
    for row in reversed(board):
        if row[col_index] == " ":
            row[col_index] = checker
            return True
    return False

def check_winner(board, checker):
    """Check if the specified checker has won the game."""
    # Check horizontal
    for row in board:
        for col in range(COLS - 3):
            if all(row[col + i] == checker for i in range(4)):
                return True

    # Check vertical
    for col in range(COLS):
        for row in range(ROWS - 3):
            if all(board[row + i][col] == checker for i in range(4)):
                return True

    # Check diagonal /
    for row in range(3, ROWS):
        for col in range(COLS - 3):
            if all(board[row - i][col + i] == checker for i in range(4)):
                return True

    # Check diagonal \
    for row in range(ROWS - 3):
        for col in range(COLS - 3):
            if all(board[row + i][col + i] == checker for i in range(4)):
                return True

    return False

def is_draw(board):
    """Check if the game is a draw (board is full)."""
    return all(board[0][col] != " " for col in range(COLS))

def main():
    # Initialize game
    board = create_board()
    current_player_index = random.randint(0, len(PLAYERS) - 1)
    
    print_board(board)
    
    while True:
        current_player = PLAYERS[current_player_index]
        col_input = input(f"Player {current_player}, please enter a column: ").strip()
        
        if not is_valid_input(col_input):
            print("Invalid input. Please enter a letter from A to G.")
            continue
        
        col_index = get_column_index(col_input)
        
        if is_column_full(board, col_index):
            print("Column is full. Please choose a different column.")
            continue
        
        place_checker(board, col_index, current_player)
        print_board(board)
        
        if check_winner(board, current_player):
            print(f"Player {current_player} won!")
            break
        
        if is_draw(board):
            print("The game is a draw!")
            break
        
        current_player_index = (current_player_index + 1) % len(PLAYERS)

if __name__ == "__main__":
    main()
