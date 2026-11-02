import os
import random

# Constants
ROWS = 6
COLS = 7
PLAYERS = 2  # Between 2 and 5
CHECKERS = ["X", "O", "V", "H", "M"]
WIN_COUNT = 4
COLUMN_LABELS = [chr(ord('A') + i) for i in range(COLS)]

def clear_screen():
    os.system('clear')

def create_board():
    return [[" " for _ in range(COLS)] for _ in range(ROWS)]

def print_board(board):
    clear_screen()
    # Print column headers
    print("  " + "   ".join(COLUMN_LABELS))
    line = "+---" * COLS + "+"
    for row in board:
        print(line)
        print("| " + " | ".join(row) + " |")
    print(line)

def valid_column_input(user_input):
    if len(user_input) != 1:
        return False
    if user_input not in COLUMN_LABELS:
        return False
    return True

def place_checker(board, column, checker):
    col_idx = COLUMN_LABELS.index(column)
    # Start from bottom row and find first empty space
    for row_idx in range(ROWS-1, -1, -1):
        if board[row_idx][col_idx] == " ":
            board[row_idx][col_idx] = checker
            return True
    # Column full
    return False

def board_full(board):
    for row in board:
        for cell in row:
            if cell == " ":
                return False
    return True

def check_win(board, checker):
    # Horizontal check
    for r in range(ROWS):
        for c in range(COLS - WIN_COUNT + 1):
            if all(board[r][c+i] == checker for i in range(WIN_COUNT)):
                return True
    # Vertical check
    for c in range(COLS):
        for r in range(ROWS - WIN_COUNT + 1):
            if all(board[r+i][c] == checker for i in range(WIN_COUNT)):
                return True
    # Diagonal / check (bottom-left to top-right)
    for r in range(WIN_COUNT - 1, ROWS):
        for c in range(COLS - WIN_COUNT + 1):
            if all(board[r - i][c + i] == checker for i in range(WIN_COUNT)):
                return True
    # Diagonal \ check (top-left to bottom-right)
    for r in range(ROWS - WIN_COUNT + 1):
        for c in range(COLS - WIN_COUNT + 1):
            if all(board[r + i][c + i] == checker for i in range(WIN_COUNT)):
                return True
    return False

def main():
    board = create_board()
    players = CHECKERS[:PLAYERS]

    current_idx = random.randint(0, PLAYERS - 1)

    print_board(board)

    while True:
        checker = players[current_idx]
        prompt = f"Player {checker}, please enter a column: "
        while True:
            user_input = input(prompt).strip().upper()

            if not valid_column_input(user_input):
                continue  # Invalid: not single letter or not in columns

            col_idx = COLUMN_LABELS.index(user_input)

            # Check if column full: if full, turn lost
            if board[0][col_idx] != " ":
                # Column full - turn lost, no retry
                break

            # Place checker
            placed = place_checker(board, user_input, checker)
            if placed:
                break  # Valid turn done, break input loop
            else:
                # Column full, also turn lost
                break

        print_board(board)

        # If checker placed (not turn lost), check win & draw
        if board[0][col_idx] == checker:
            if check_win(board, checker):
                print(f"Player {checker} won!")
                return
            if board_full(board):
                print("The game is a draw.")
                return

        # Next player's turn
        current_idx = (current_idx + 1) % PLAYERS

if __name__ == "__main__":
    main()
