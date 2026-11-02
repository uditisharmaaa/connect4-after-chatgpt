import os
import random

# Constants for the board dimensions and player symbols
ROWS = 6
COLS = 7
PLAYERS = ['X', 'O', 'V', 'H', 'M']  # Up to 5 players

def create_board():
    """Create a 2D board initialized with empty spaces."""
    return [[" " for _ in range(COLS)] for _ in range(ROWS)]

def print_board(board):
    """Print the current state of the board."""
    os.system('clear')  # Clear the terminal screen
    print("  " + "   ".join(chr(65 + i) for i in range(COLS)))  # Print column headers
    print("+---+" + "---+" * (COLS - 1))

    for row in board:
        print("| " + " | ".join(row) + " |")
        print("+---+" + "---+" * (COLS - 1))

def valid_input(user_input):
    """Check if the input is valid: a single letter (A-G) corresponding to a column."""
    return user_input.isalpha() and user_input.isupper() and 'A' <= user_input <= chr(65 + COLS - 1)

def drop_checker(board, column, checker):
    """Place a checker in the designated column. Returns True if successful, else False."""
    col_index = ord(column) - 65
    for row in reversed(board):
        if row[col_index] == " ":
            row[col_index] = checker
            return True
    return False  # Column is full

def check_win(board, checker):
    """Check if the given player has won the game."""
    # Check horizontal, vertical, and diagonal (both directions) for a connect 4
    for r in range(ROWS):
        for c in range(COLS):
            if board[r][c] == checker:
                if c + 3 < COLS and all(board[r][c + i] == checker for i in range(4)):  # Horizontal
                    return True
                if r + 3 < ROWS and all(board[r + i][c] == checker for i in range(4)):  # Vertical
                    return True
                if r + 3 < ROWS and c + 3 < COLS and all(board[r + i][c + i] == checker for i in range(4)):  # Diagonal /
                    return True
                if r - 3 >= 0 and c + 3 < COLS and all(board[r - i][c + i] == checker for i in range(4)):  # Diagonal \
                    return True
    return False

def check_draw(board):
    """Check if the game is a draw."""
    return all(cell != " " for row in board for cell in row)

def main():
    """Main game loop."""
    board = create_board()
    players = PLAYERS[:2]  # Using only 2 players for the assignment
    current_player = random.choice(players)

    print_board(board)

    while True:
        print(f"Player {current_player}, please enter a column:")
        user_input = input().strip()
        
        while not valid_input(user_input):
            print("Invalid input. Please enter a column (A to {}):".format(chr(65 + COLS - 1)))
            user_input = input().strip()

        if drop_checker(board, user_input, current_player):
            print_board(board)
            if check_win(board, current_player):
                print(f"Player {current_player} won!")
                break
            if check_draw(board):
                print("The game is a draw!")
                break
            current_player = players[(players.index(current_player) + 1) % len(players)]
        else:
            print("The column is full. Try again.")

if __name__ == "__main__":
    main()
