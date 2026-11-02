import os
import random

# Constants for board dimensions and player symbols
ROWS = 6
COLS = 7
PLAYER_SYMBOLS = ['X', 'O', 'V', 'H', 'M']  # Up to 5 players

# Create the empty game board
def create_board():
    return [[" " for _ in range(COLS)] for _ in range(ROWS)]

# Print the game board
def print_board(board):
    os.system('clear')  # Clear the terminal screen
    print("  " + "   ".join(chr(65 + i) for i in range(COLS)))  # Column headers (A-G)
    print("+---" + "---+".join([""] * COLS) + "-+")
    for row in board:
        print("| " + " | ".join(row) + " |")
        print("+---" + "---+".join([""] * COLS) + "-+")

# Validate the player's input
def validate_input(column):
    if len(column) != 1 or not ('A' <= column <= chr(65 + COLS - 1)):
        return False
    return True

# Place the checker in the board
def place_checker(board, col, symbol):
    for row in reversed(board):
        if row[col] == " ":
            row[col] = symbol
            return True
    return False  # Column is full

# Check for a win condition
def check_win(board, symbol):
    # Check horizontal, vertical, and diagonal wins
    for r in range(ROWS):
        for c in range(COLS):
            if board[r][c] == symbol:
                # Check horizontal
                if c + 3 < COLS and all(board[r][c + i] == symbol for i in range(4)):
                    return True
                # Check vertical
                if r + 3 < ROWS and all(board[r + i][c] == symbol for i in range(4)):
                    return True
                # Check diagonal (bottom-left to top-right)
                if r - 3 >= 0 and c + 3 < COLS and all(board[r - i][c + i] == symbol for i in range(4)):
                    return True
                # Check diagonal (top-left to bottom-right)
                if r + 3 < ROWS and c + 3 < COLS and all(board[r + i][c + i] == symbol for i in range(4)):
                    return True
    return False

# Check for a draw condition
def check_draw(board):
    return all(cell != " " for row in board for cell in row)

def main():
    board = create_board()

    # Randomly select the starting player
    current_player_index = random.randint(0, len(PLAYER_SYMBOLS) - 1)

    # Game loop
    while True:
        print_board(board)
        current_symbol = PLAYER_SYMBOLS[current_player_index]
        print(f"Player {current_symbol}, please enter a column:")
        
        # Input validation
        while True:
            column_input = input().upper()
            if validate_input(column_input):
                column = ord(column_input) - 65
                if place_checker(board, column, current_symbol):
                    break
                else:
                    print("Column is full, please choose another column.")
            else:
                print("Invalid input. Please enter a valid column (A-G).")
        
        if check_win(board, current_symbol):
            print_board(board)
            print(f"Player {current_symbol} won!")
            break

        if check_draw(board):
            print_board(board)
            print("The game is a draw!")
            break
        
        # Switch to the next player
        current_player_index = (current_player_index + 1) % len(PLAYER_SYMBOLS)

if __name__ == "__main__":
    main()
