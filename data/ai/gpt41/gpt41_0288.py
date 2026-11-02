import os
import random
import string
import sys

# Constants
ROWS = 6
COLUMNS = 7
MAX_COLUMNS = 26
PLAYERS = 2  # Can set between 2 and 5
CHECKERS = ["X", "O", "V", "H", "M"]

def clear_screen():
    # Clear screen for Linux/Unix/Mac
    os.system('clear')

def create_board(rows, cols):
    # Create a board with spaces
    return [[" " for _ in range(cols)] for _ in range(rows)]

def print_board(board):
    clear_screen()
    cols = len(board[0])
    # Print column letters
    col_labels = [chr(ord('A') + i) for i in range(cols)]
    print("  " + "   ".join(col_labels))
    print("+" + "---+" * cols)
    for row in board:
        print("| " + " | ".join(row) + " |")
        print("+" + "---+" * cols)

def get_column_number(input_letter, cols):
    # Return 0-based column index from input letter if valid, else -1
    if len(input_letter) != 1 or not input_letter.isalpha():
        return -1
    index = ord(input_letter.upper()) - ord('A')
    if 0 <= index < cols:
        return index
    return -1

def is_column_full(board, col):
    # If the top row of column is not empty, then column is full
    return board[0][col] != " "

def place_checker(board, col, checker):
    # Place the checker in the specified column
    for row in reversed(board):
        if row[col] == " ":
            row[col] = checker
            return True
    return False  # Column is full

def is_valid_column_input(user_input, board):
    col = get_column_number(user_input, len(board[0]))
    if col == -1:
        return False
    return not is_column_full(board, col)

def check_win(board, checker):
    rows, cols = len(board), len(board[0])
    for r in range(rows):
        for c in range(cols):
            if board[r][c] != checker:
                continue
            # Check right
            if c <= cols - 4 and all(board[r][c+i] == checker for i in range(4)):
                return True
            # Check down
            if r <= rows - 4 and all(board[r+i][c] == checker for i in range(4)):
                return True
            # Check diagonal right-down
            if r <= rows - 4 and c <= cols - 4 and all(board[r+i][c+i] == checker for i in range(4)):
                return True
            # Check diagonal left-down
            if r <= rows - 4 and c >= 3 and all(board[r+i][c-i] == checker for i in range(4)):
                return True
    return False

def is_board_full(board):
    return all(cell != " " for row in board for cell in row)

def main():
    # Set up configuration
    rows, cols = ROWS, COLUMNS
    num_players = PLAYERS
    checkers = CHECKERS[:num_players]
    board = create_board(rows, cols)

    # Randomly select start player
    player_idx = random.randint(0, num_players - 1)

    print_board(board)
    print(f"Player {checkers[player_idx]}, you start first!")

    while True:
        print_board(board)
        current_checker = checkers[player_idx]
        print(f"Player {current_checker}, please enter a column:")

        # Validate input
        while True:
            user_input = input().strip()
            col = get_column_number(user_input, cols)
            if col == -1:
                print("Invalid column. Please enter a valid column letter (e.g. A-G):")
                continue
            if is_column_full(board, col):
                print("This column is full. You lose your turn!")
                break  # Lose turn if column full
            # Place checker
            placed = place_checker(board, col, current_checker)
            if not placed:
                print("Unexpected error placing checker. Try again.")
                continue
            break

        # Check for win
        if check_win(board, current_checker):
            print_board(board)
            print(f"Player {current_checker} won!")
            break

        # Check for draw
        if is_board_full(board):
            print_board(board)
            print("It's a draw!")
            break

        # Next player's turn
        player_idx = (player_idx + 1) % num_players

if __name__ == "__main__":
    main()
