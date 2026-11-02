import os
import random

# Constants
ROWS = 6
COLS = 7
PLAYERS = ['X', 'O']

def initialize_board():
    """Create the Connect 4 board."""
    return [[' ' for _ in range(COLS)] for _ in range(ROWS)]

def print_board(board):
    """Prints the current state of the board."""
    os.system('clear')  # Clear the screen (Linux/Unix)
    print("  " + "   ".join(chr(65 + i) for i in range(COLS)))  # Column headers
    print("+---" * COLS + "+")  # Top border
    for row in board:
        print("| " + " | ".join(row) + " |")  # Row data
        print("+---" * COLS + "+")  # Row border

def is_valid_input(col):
    """Check if the input is a valid column."""
    return col.isalpha() and len(col) == 1 and 'A' <= col.upper() <= chr(65 + COLS - 1)

def get_column_index(col):
    """Return the column index given a letter."""
    return ord(col.upper()) - 65

def is_column_full(board, col):
    """Check if the specified column is full."""
    return board[0][col] != ' '

def place_checker(board, col, checker):
    """Place a checker in the specified column."""
    for row in reversed(board):
        if row[col] == ' ':
            row[col] = checker
            return True
    return False

def check_winner(board, checker):
    """Check for a win condition."""
    # Check horizontal, vertical and diagonal
    for row in range(ROWS):
        for col in range(COLS):
            if board[row][col] == checker:
                # Check horizontal
                if col + 3 < COLS and all(board[row][col + i] == checker for i in range(4)):
                    return True
                # Check vertical
                if row + 3 < ROWS and all(board[row + i][col] == checker for i in range(4)):
                    return True
                # Check diagonal (down-right)
                if row + 3 < ROWS and col + 3 < COLS and all(board[row + i][col + i] == checker for i in range(4)):
                    return True
                # Check diagonal (down-left)
                if row + 3 < ROWS and col - 3 >= 0 and all(board[row + i][col - i] == checker for i in range(4)):
                    return True
    return False

def is_draw(board):
    """Check if the game is a draw."""
    return all(is_column_full(board, col) for col in range(COLS))

def play_game():
    """Main function to play the Connect 4 game."""
    board = initialize_board()
    current_player = random.choice(PLAYERS)  # Randomly choose the starting player
    print_board(board)

    while True:
        print(f"Player {current_player}, please enter a column (A-G): ")
        col_input = input().strip()

        if not is_valid_input(col_input):
            print("Invalid input. Please enter a letter from A to G.")
            continue

        col = get_column_index(col_input)

        if is_column_full(board, col):
            print("Column is full, please choose another column.")
            continue

        place_checker(board, col, current_player)
        print_board(board)

        if check_winner(board, current_player):
            print(f"Player {current_player} won!")
            break
            
        if is_draw(board):
            print("The game is a draw!")
            break

        # Switch to next player
        current_player = PLAYERS[(PLAYERS.index(current_player) + 1) % len(PLAYERS)]

if __name__ == "__main__":
    play_game()
