import os
import random

# Constants
ROWS = 6
COLS = 7
MIN_PLAYERS = 2
MAX_PLAYERS = 5
WIN_COUNT = 4

# Players' checkers in order
CHECKERS = ['X', 'O', 'V', 'H', 'M']

# Using only 2 players for submission as required
NUM_PLAYERS = 2
PLAYERS = CHECKERS[:NUM_PLAYERS]

def clear_screen():
    os.system('clear')

def create_board(rows, cols):
    # Board is represented as list of rows, each row is list of cols
    # Initialize with spaces
    return [[" " for _ in range(cols)] for _ in range(rows)]

def print_board(board):
    clear_screen()
    cols = len(board[0])
    rows = len(board)
    # Print column labels
    labels = [chr(ord('A') + i) for i in range(cols)]
    print("  " + "   ".join(labels))
    horizontal_line = "+" + "---+" * cols
    for r in range(rows):
        print(horizontal_line)
        row_cells = [" {} ".format(board[r][c]) for c in range(cols)]
        print("|" + "|".join(row_cells) + "|")
    print(horizontal_line)

def input_column(player):
    cols = COLS
    while True:
        col_input = input(f"Player {player}, please enter a column: ").strip().upper()
        if len(col_input) != 1:
            print(f"Invalid input. Please enter exactly one letter between A and {chr(ord('A')+cols-1)}.")
            continue
        if not ('A' <= col_input <= chr(ord('A') + cols - 1)):
            print(f"Invalid input. Please enter a letter between A and {chr(ord('A')+cols-1)}.")
            continue
        return ord(col_input) - ord('A')

def place_checker(board, col, checker):
    rows = len(board)
    # Find lowest empty slot in the column
    for r in range(rows - 1, -1, -1):
        if board[r][col] == " ":
            board[r][col] = checker
            return True
    return False  # Column full

def check_winner(board, checker):
    rows = len(board)
    cols = len(board[0])

    # Check horizontal
    for r in range(rows):
        count = 0
        for c in range(cols):
            if board[r][c] == checker:
                count += 1
                if count == WIN_COUNT:
                    return True
            else:
                count = 0

    # Check vertical
    for c in range(cols):
        count = 0
        for r in range(rows):
            if board[r][c] == checker:
                count += 1
                if count == WIN_COUNT:
                    return True
            else:
                count = 0

    # Check diagonal_down_right (\ direction)
    for r in range(rows - WIN_COUNT + 1):
        for c in range(cols - WIN_COUNT + 1):
            if all(board[r + i][c + i] == checker for i in range(WIN_COUNT)):
                return True

    # Check diagonal_down_left (/ direction)
    for r in range(rows - WIN_COUNT + 1):
        for c in range(WIN_COUNT - 1, cols):
            if all(board[r + i][c - i] == checker for i in range(WIN_COUNT)):
                return True

    return False

def board_full(board):
    return all(cell != " " for row in board for cell in row)

def main():
    board = create_board(ROWS, COLS)
    # Random first player
    current_player_index = random.randint(0, NUM_PLAYERS - 1)

    print_board(board)

    while True:
        checker = PLAYERS[current_player_index]
        col = input_column(checker)
        placed = place_checker(board, col, checker)
        if not placed:
            # Turn is lost if column full (per assignment)
            print(f"Column {chr(ord('A') + col)} is full. Player {checker} loses turn.")
            # Next player turn
            current_player_index = (current_player_index + 1) % NUM_PLAYERS
            print_board(board)
            continue

        print_board(board)

        if check_winner(board, checker):
            print(f"Player {checker} won!")
            break

        if board_full(board):
            print("The game is a draw!")
            break

        # Next player turn
        current_player_index = (current_player_index + 1) % NUM_PLAYERS

if __name__ == "__main__":
    main()
