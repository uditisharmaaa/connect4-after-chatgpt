import os
import random

# Constants for the game
ROWS = 6
COLS = 7
PLAYERS = ['X', 'O']  # You can extend this with ['X', 'O', 'V', 'H', 'M'] for more players if needed

def create_board():
    """Initialize the game board."""
    return [[' ' for _ in range(COLS)] for _ in range(ROWS)]

def print_board(board):
    """Print the game board."""
    os.system('clear')  # Clears the terminal screen (Linux/Unix)
    print("  " + "   ".join(chr(65 + col) for col in range(COLS)))  # Column labels A, B, C, ...
    print("+" + "---+" * COLS)
    for row in board:
        print("| " + " | ".join(row) + " |")
        print("+" + "---+" * COLS)

def is_valid_input(column):
    """Check if the input column is valid."""
    return column.isalpha() and len(column) == 1 and 'A' <= column <= chr(65 + COLS - 1)

def get_column_index(column):
    """Convert letter column to index."""
    return ord(column) - 65

def is_column_full(board, col):
    """Check if the column is full."""
    return board[0][col] != ' '

def place_checker(board, col, checker):
    """Place a checker in the board."""
    for row in reversed(range(ROWS)):
        if board[row][col] == ' ':
            board[row][col] = checker
            return True
    return False

def check_winner(board, checker):
    """Check if the given checker has won the game."""
    # Check horizontal
    for row in range(ROWS):
        for col in range(COLS - 3):
            if all(board[row][col + i] == checker for i in range(4)):
                return True

    # Check vertical
    for col in range(COLS):
        for row in range(ROWS - 3):
            if all(board[row + i][col] == checker for i in range(4)):
                return True

    # Check diagonal (bottom-left to top-right)
    for row in range(ROWS - 3):
        for col in range(COLS - 3):
            if all(board[row + i][col + i] == checker for i in range(4)):
                return True

    # Check diagonal (top-left to bottom-right)
    for row in range(3, ROWS):
        for col in range(COLS - 3):
            if all(board[row - i][col + i] == checker for i in range(4)):
                return True

    return False

def is_draw(board):
    """Check if the board is full without a winner."""
    return all(board[0][col] != ' ' for col in range(COLS))

def main():
    """Main function to run the game."""
    board = create_board()
    current_player = random.choice(PLAYERS)

    while True:
        print_board(board)
        print(f"Player {current_player}, please enter a column:")
        
        column = input().upper()
        
        while not is_valid_input(column):
            print("Invalid input. Please enter a valid column letter:")
            column = input().upper()
        
        col_index = get_column_index(column)

        if is_column_full(board, col_index):
            print("Column is full! Try another column.")
            continue

        place_checker(board, col_index, current_player)

        if check_winner(board, current_player):
            print_board(board)
            print(f"Player {current_player} won!")
            break

        if is_draw(board):
            print_board(board)
            print("The game is a draw!")
            break

        # Switch player
        current_player = PLAYERS[(PLAYERS.index(current_player) + 1) % len(PLAYERS)]

if __name__ == "__main__":
    main()
