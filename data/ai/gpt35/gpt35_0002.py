import os
import random

# Constants for the game configuration
ROWS = 6
COLUMNS = 7  # max 26
NUM_PLAYERS = 2  # between 2 and 5
CHECKERS = ['X', 'O', 'V', 'H', 'M']  # Player checkers in order

def clear_screen():
    """Clear the terminal screen."""
    os.system('clear')

def create_board(rows, cols):
    """Create and return an empty board filled with spaces."""
    return [[' ' for _ in range(cols)] for _ in range(rows)]

def print_board(board):
    """Print the Connect 4 board with column labels."""
    cols = len(board[0])
    # Column labels A, B, C, ...
    labels = [chr(ord('A') + i) for i in range(cols)]
    print("  " + "   ".join(labels))
    # Print the board row by row
    for row in range(len(board)):
        print("+" + "---+" * cols)
        print("|" + "|".join(f" {board[row][col]} " for col in range(cols)) + "|")
    print("+" + "---+" * cols)

def valid_column_input(user_input, cols):
    """Check if input is a single uppercase letter within board range."""
    if len(user_input) != 1:
        return False
    if not user_input.isalpha():
        return False
    if not ('A' <= user_input <= chr(ord('A') + cols - 1)):
        return False
    return True

def get_column_index(user_input):
    """Convert column letter to zero-based index."""
    return ord(user_input) - ord('A')

def place_checker(board, col, checker):
    """
    Place checker in the specified column.
    Drops down to the lowest empty spot.
    Returns True if placed successfully, False if column full.
    """
    # Start from bottom row up to top row
    for row in range(len(board)-1, -1, -1):
        if board[row][col] == ' ':
            board[row][col] = checker
            return True
    return False  # Column full

def check_winner(board, checker):
    """Check if the current checker has 4 in row horizontally, vertically or diagonally."""
    rows = len(board)
    cols = len(board[0])
    connect = 4

    # Horizontal check
    for r in range(rows):
        count = 0
        for c in range(cols):
            if board[r][c] == checker:
                count += 1
                if count == connect:
                    return True
            else:
                count = 0

    # Vertical check
    for c in range(cols):
        count = 0
        for r in range(rows):
            if board[r][c] == checker:
                count += 1
                if count == connect:
                    return True
            else:
                count = 0

    # Diagonal (top-left to bottom-right)
    for r in range(rows - connect + 1):
        for c in range(cols - connect + 1):
            if all(board[r + i][c + i] == checker for i in range(connect)):
                return True

    # Diagonal (bottom-left to top-right)
    for r in range(connect - 1, rows):
        for c in range(cols - connect + 1):
            if all(board[r - i][c + i] == checker for i in range(connect)):
                return True

    return False

def board_full(board):
    """Check if the board is completely full (draw)."""
    for row in board:
        if ' ' in row:
            return False
    return True

def main():
    # Initialize game
    board = create_board(ROWS, COLUMNS)
    players = CHECKERS[:NUM_PLAYERS]

    # Choose random starting player index
    current_player_idx = random.randint(0, NUM_PLAYERS - 1)

    while True:
        clear_screen()
        print_board(board)
        current_checker = players[current_player_idx]
        print(f"Player {current_checker}, please enter a column:")

        while True:
            user_input = input().strip().upper()
            if not valid_column_input(user_input, COLUMNS):
                print("Invalid input. Please enter a valid column letter:")
                continue
            col = get_column_index(user_input)

            # Attempt to place checker
            placed = place_checker(board, col, current_checker)
            if not placed:
                # Column full: player loses turn (skip to next player)
                break
            else:
                # Successful placement, break input loop
                break

        # If successfully placed, check for win or draw
        if placed:
            if check_winner(board, current_checker):
                clear_screen()
                print_board(board)
                print(f"Player {current_checker} won!")
                break
            if board_full(board):
                clear_screen()
                print_board(board)
                print("The game is a draw!")
                break

        # Switch to next player (even if column full and turn lost)
        current_player_idx = (current_player_idx + 1) % NUM_PLAYERS

if __name__ == "__main__":
    main()
