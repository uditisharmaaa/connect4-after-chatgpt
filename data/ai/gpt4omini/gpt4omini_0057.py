import os
import random

# Constants
ROWS = 6
COLS = 7
MAX_PLAYERS = 5
PLAYERS = ['X', 'O', 'V', 'H', 'M']

def create_board():
    """Create an empty board."""
    return [[' ' for _ in range(COLS)] for _ in range(ROWS)]

def print_board(board):
    """Print the current state of the board."""
    os.system('clear')  # Clear the console
    print("  " + "   ".join(chr(65 + i) for i in range(COLS)))  # Column headers
    print("+---" + "+---" * (COLS - 1) + "+")
    for row in board:
        print("| " + " | ".join(row) + " |")
        print("+---" + "+---" * (COLS - 1) + "+")

def is_valid_input(col_input):
    """Check if the input is a valid column."""
    if len(col_input) != 1:
        return False
    return col_input.upper() in [chr(65 + i) for i in range(COLS)]

def drop_checker(board, column, checker):
    """Place a checker in the board."""
    for row in reversed(board):  # Start from the bottom
        if row[column] == ' ':
            row[column] = checker
            return True
    return False  # Column is full

def check_win(board, checker):
    """Check for a win condition."""
    for r in range(ROWS):
        for c in range(COLS):
            if board[r][c] == checker:
                # Check horizontal
                if c + 3 < COLS and all(board[r][c+i] == checker for i in range(4)):
                    return True
                # Check vertical
                if r + 3 < ROWS and all(board[r+i][c] == checker for i in range(4)):
                    return True
                # Check diagonal /
                if r + 3 < ROWS and c - 3 >= 0 and all(board[r+i][c-i] == checker for i in range(4)):
                    return True
                # Check diagonal \
                if r + 3 < ROWS and c + 3 < COLS and all(board[r+i][c+i] == checker for i in range(4)):
                    return True
    return False

def check_draw(board):
    """Check if the game is a draw."""
    return all(board[0][c] != ' ' for c in range(COLS))

def main():
    board = create_board()
    random_player = random.randint(0, min(len(PLAYERS), MAX_PLAYERS) - 1)
    
    current_player = random_player
    while True:
        print_board(board)
        print(f"Player {PLAYERS[current_player]}, please enter a column:")
        
        # Input Loop
        while True:
            user_input = input().strip().upper()
            if is_valid_input(user_input):
                column = ord(user_input) - 65
                if drop_checker(board, column, PLAYERS[current_player]):
                    break  # Valid move
                else:
                    print("Column is full, please choose another column.")
            else:
                print("Invalid input. Please enter a valid column (A-G).")
        
        if check_win(board, PLAYERS[current_player]):
            print_board(board)
            print(f"Player {PLAYERS[current_player]} won!")
            break
        
        if check_draw(board):
            print_board(board)
            print("The game is a draw!")
            break

        # Switch player
        current_player = (current_player + 1) % len(PLAYERS)

if __name__ == "__main__":
    main()
