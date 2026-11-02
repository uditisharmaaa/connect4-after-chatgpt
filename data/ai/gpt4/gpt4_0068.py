import os
import random

# Constants
ROWS = 6
COLS = 7
PLAYERS = 2
CHECKERS = ["X", "O", "V", "H", "M"]  # Maximum for 5 players
ALPHABET = "ABCDEFGHIJKLMNOPQRSTUVWXYZ"

def create_board():
    """Create an initial empty board."""
    return [[" " for _ in range(COLS)] for _ in range(ROWS)]

def print_board(board):
    """Print the current board."""
    os.system('clear')
    print("  " + "   ".join(ALPHABET[:COLS]))
    print("+---" * COLS + "+")
    for row in board:
        print("| " + " | ".join(row) + " |")
        print("+---" * COLS + "+")

def is_valid_input(column):
    """Check if input column is valid and on the board."""
    return column in ALPHABET[:COLS]

def get_available_row(board, col_idx):
    """Get the lowest available row in a given column."""
    for row in range(ROWS-1, -1, -1):
        if board[row][col_idx] == " ":
            return row
    return -1

def check_winner(board, checker):
    """Check for a win condition (horizontal, vertical, diagonal)."""
    # Check horizontal
    for row in range(ROWS):
        for col in range(COLS - 3):
            if board[row][col:col+4] == [checker]*4:
                return True

    # Check vertical
    for col in range(COLS):
        for row in range(ROWS - 3):
            if all(board[row+i][col] == checker for i in range(4)):
                return True

    # Check diagonal (bottom-left to top-right)
    for row in range(ROWS - 3):
        for col in range(COLS - 3):
            if all(board[row+i][col+i] == checker for i in range(4)):
                return True

    # Check diagonal (top-left to bottom-right)
    for row in range(3, ROWS):
        for col in range(COLS - 3):
            if all(board[row-i][col+i] == checker for i in range(4)):
                return True

    return False

def check_draw(board):
    """Check if the board is full."""
    return all(board[0][col] != " " for col in range(COLS))

def main():
    board = create_board()
    player_count = PLAYERS
    players = CHECKERS[:player_count]
    current_player = random.choice(players)

    print_board(board)
    print(f"Randomly selected first player: {current_player}")

    while True:
        print_board(board)
        print(f"Player {current_player}, please enter a column:")
        col_input = input().strip().upper()

        # Validate input
        if not is_valid_input(col_input):
            print("Invalid column. Please try again.")
            continue

        col_idx = ALPHABET.index(col_input)
        row = get_available_row(board, col_idx)

        if row == -1:
            print("Column is full. Please try another column.")
            continue

        # Place checker
        board[row][col_idx] = current_player

        # Check win condition
        if check_winner(board, current_player):
            print_board(board)
            print(f"Player {current_player} won!")
            break

        # Check for draw
        if check_draw(board):
            print_board(board)
            print("It's a draw!")
            break

        # Switch to next player
        current_player = players[(players.index(current_player) + 1) % player_count]

if __name__ == "__main__":
    main()
