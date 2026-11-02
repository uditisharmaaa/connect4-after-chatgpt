import os
import random

# Constants for board dimensions and player symbols
ROWS = 6
COLS = 7
PLAYER_SYMBOLS = ['X', 'O', 'V', 'H', 'M']

def create_board():
    """Create and return a new Connect 4 board."""
    return [[" " for _ in range(COLS)] for _ in range(ROWS)]

def print_board(board):
    """Print the Connect 4 board."""
    os.system('clear')
    print("  " + "   ".join(chr(65 + i) for i in range(COLS)))  # A, B, C, ...
    print("+" + "---+" * COLS)
    for row in board:
        print("| " + " | ".join(row) + " |")
        print("+" + "---+" * COLS)

def get_player_choice(player_index):
    """Prompt the current player for a column choice and validate the input."""
    while True:
        choice = input(f"Player {PLAYER_SYMBOLS[player_index]}, please enter a column (A-{chr(65 + COLS - 1)}): ").strip().upper()
        if len(choice) == 1 and 'A' <= choice <= chr(65 + COLS - 1):
            column = ord(choice) - 65
            return column
        print("Invalid input. Please enter a valid column.")

def place_checker(board, column, symbol):
    """Place the checker in the specified column."""
    for row in reversed(board):  # Start from the bottom row
        if row[column] == " ":
            row[column] = symbol
            return True
    return False  # Column is full

def check_win(board, symbol):
    """Check if the current player has won the game."""
    
    # Check horizontal, vertical, and diagonal
    for r in range(ROWS):
        for c in range(COLS):
            if c + 3 < COLS and all(board[r][c + i] == symbol for i in range(4)):  # horizontal
                return True
            if r + 3 < ROWS and all(board[r + i][c] == symbol for i in range(4)):  # vertical
                return True
            if r + 3 < ROWS and c + 3 < COLS and all(board[r + i][c + i] == symbol for i in range(4)):  # diagonal \
                return True
            if r + 3 < ROWS and c - 3 >= 0 and all(board[r + i][c - i] == symbol for i in range(4)):  # diagonal /
                return True
    return False

def check_draw(board):
    """Check if the board is full and thus the game is a draw."""
    return all(cell != " " for row in board for cell in row)

def main():
    """Main function to run the Connect 4 game."""
    board = create_board()
    current_player = random.randint(0, len(PLAYER_SYMBOLS) - 1)  # Randomly select first player

    print_board(board)
    
    while True:
        column = get_player_choice(current_player)
        
        if place_checker(board, column, PLAYER_SYMBOLS[current_player]):
            print_board(board)
            if check_win(board, PLAYER_SYMBOLS[current_player]):
                print(f"Player {PLAYER_SYMBOLS[current_player]} won!")
                break
            if check_draw(board):
                print("The game is a draw!")
                break
            current_player = (current_player + 1) % len(PLAYER_SYMBOLS)  # Switch player
        else:
            print("Column is full, please choose another column.")

if __name__ == "__main__":
    main()
