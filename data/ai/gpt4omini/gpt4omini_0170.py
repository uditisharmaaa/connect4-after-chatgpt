import os
import random

# Constants for board dimensions and players
ROWS = 6
COLS = 7
PLAYER_SYMBOLS = ["X", "O", "V", "H", "M"]  # Up to 5 players

def clear_screen():
    """Clears the terminal screen."""
    os.system('clear')

def create_board():
    """Creates a game board initialized with spaces."""
    return [[" " for _ in range(COLS)] for _ in range(ROWS)]

def print_board(board):
    """Prints the game board in a user-friendly format."""
    clear_screen()
    print("  " + "   ".join([chr(65 + i) for i in range(COLS)]))  # Column Labels A, B, C, ...
    print("+" + "---+" * COLS)  # Top border of the board
    for row in board:
        print("| " + " | ".join(row) + " |")  # Row content
        print("+" + "---+" * COLS)  # Bottom border of the row

def is_valid_input(column):
    """Validates the input for column selection."""
    return column.isalpha() and len(column) == 1 and 'A' <= column <= chr(65 + COLS - 1)

def find_row(board, column):
    """Finds the next available row in the specified column."""
    for row in range(ROWS - 1, -1, -1):  # Check from bottom to top
        if board[row][column] == " ":
            return row
    return -1  # Column is full

def place_checker(board, column, symbol):
    """Places the checker for the current player in the specified column."""
    row = find_row(board, column)
    if row != -1:
        board[row][column] = symbol
        return True
    return False

def check_winner(board, symbol):
    """Checks if the current player has won the game."""
    # Check horizontal, vertical, and diagonal (both directions)
    for row in range(ROWS):
        for col in range(COLS):
            if board[row][col] == symbol:
                # Check horizontal
                if col <= COLS - 4 and all(board[row][col + i] == symbol for i in range(4)):
                    return True
                # Check vertical
                if row <= ROWS - 4 and all(board[row + i][col] == symbol for i in range(4)):
                    return True
                # Check diagonal \
                if row <= ROWS - 4 and col <= COLS - 4 and all(board[row + i][col + i] == symbol for i in range(4)):
                    return True
                # Check diagonal /
                if row >= 3 and col <= COLS - 4 and all(board[row - i][col + i] == symbol for i in range(4)):
                    return True
    return False

def check_draw(board):
    """Checks if the board is full and there is no winner."""
    return all(board[0][col] != " " for col in range(COLS))

def main():
    # Initialize the game board
    board = create_board()
    
    # Randomly choose the starting player
    current_player = random.randint(0, len(PLAYER_SYMBOLS) - 1)

    while True:
        print_board(board)  # Display the board
        symbol = PLAYER_SYMBOLS[current_player]  # Current player's symbol
        print(f"Player {symbol}, please enter a column (A-{chr(65 + COLS - 1)}):")
        
        # Get a valid column input from the player
        while True:
            column_input = input().upper()  # Convert input to uppercase
            if is_valid_input(column_input):
                column = ord(column_input) - 65  # Convert character to index
                if place_checker(board, column, symbol):
                    break  # Valid placement
                else:
                    print("Column is full! Please choose another column.")
            else:
                print("Invalid input! Please enter a valid column letter.")
        
        # Check for a win
        if check_winner(board, symbol):
            print_board(board)
            print(f"Player {symbol} won!")
            break
        
        # Check for a draw
        if check_draw(board):
            print_board(board)
            print("The game is a draw!")
            break
        
        # Move to the next player
        current_player = (current_player + 1) % len(PLAYER_SYMBOLS)  # Cycle through players

if __name__ == "__main__":
    main()
