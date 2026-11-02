import os
import random

# Constants for the board dimensions and player symbols
ROWS = 6
COLS = 7
PLAYERS = ["X", "O", "V", "H", "M"]  # Up to 5 players

def create_board():
    """Create a 2D board initialized with whitespace."""
    return [[" " for _ in range(COLS)] for _ in range(ROWS)]

def print_board(board):
    """Print the current state of the board."""
    os.system('clear')  # Clear the terminal
    print("  " + "   ".join(chr(65 + col) for col in range(COLS)))
    print("+---" + "+---" * (COLS - 1) + "+")
    for row in board:
        print("| " + " | ".join(row) + " |")
        print("+---" + "+---" * (COLS - 1) + "+")

def is_valid_input(column):
    """Validate the user input for column selection."""
    return column.isalpha() and len(column) == 1 and 'A' <= column <= chr(65 + COLS - 1)

def get_column_index(column):
    """Convert a column letter to its corresponding index."""
    return ord(column) - 65

def place_checker(board, column, checker):
    """Place the checker in the specified column."""
    for row in reversed(board):
        if row[column] == " ":
            row[column] = checker
            return True
    return False  # Column is full

def check_win(board, checker):
    """Check if the specified checker has four in a row."""
    # Check horizontal, vertical, and both diagonal directions
    for r in range(ROWS):
        for c in range(COLS):
            if board[r][c] == checker:
                # Check horizontal
                if c + 3 < COLS and all(board[r][c + i] == checker for i in range(4)):
                    return True
                # Check vertical
                if r + 3 < ROWS and all(board[r + i][c] == checker for i in range(4)):
                    return True
                # Check diagonal (/)
                if r + 3 < ROWS and c - 3 >= 0 and all(board[r + i][c - i] == checker for i in range(4)):
                    return True
                # Check diagonal (\)
                if r + 3 < ROWS and c + 3 < COLS and all(board[r + i][c + i] == checker for i in range(4)):
                    return True
    return False

def check_draw(board):
    """Check if the board is full (draw)."""
    return all(cell != " " for row in board for cell in row)

def main():
    """Main function to run the Connect 4 game."""
    board = create_board()
    current_player = random.choice(PLAYERS)
    print_board(board)

    while True:
        print(f"Player {current_player}, please enter a column:")
        column = input().strip().upper()

        while not is_valid_input(column):
            print("Invalid input. Please enter a column (A-G):")
            column = input().strip().upper()

        col_index = get_column_index(column)

        if place_checker(board, col_index, current_player):
            print_board(board)

            if check_win(board, current_player):
                print(f"Player {current_player} won!")
                break
            elif check_draw(board):
                print("The game is a draw!")
                break
            
            # Swap player
            current_player = PLAYERS[(PLAYERS.index(current_player) + 1) % len(PLAYERS)]
        else:
            print("Column is full! Please choose another column.")

if __name__ == "__main__":
    main()
