import os
import random

# Constants
ROWS = 6
COLS = 7
PLAYERS = 2
CHECKERS = ["X", "O", "V", "H", "M"]
WIN_CONDITION = 4
COLUMN_LABELS = [chr(ord('A') + i) for i in range(COLS)]

def clear_screen():
    os.system('clear')

def create_board():
    return [[" " for _ in range(COLS)] for _ in range(ROWS)]

def print_board(board):
    clear_screen()
    # Print column labels
    print("  " + "   ".join(COLUMN_LABELS))
    # Print board rows
    for row in range(ROWS):
        print("+---" * COLS + "+")
        line = "|"
        for col in range(COLS):
            line += " " + board[row][col] + " |"
        print(line)
    print("+---" * COLS + "+")

def is_valid_column(col_char):
    if col_char in COLUMN_LABELS:
        col_index = COLUMN_LABELS.index(col_char)
        return col_index
    return -1

def is_column_full(board, col):
    return board[0][col] != " "

def place_checker(board, col, checker):
    # Start from bottom row and place checker in the first empty spot
    for row in range(ROWS-1, -1, -1):
        if board[row][col] == " ":
            board[row][col] = checker
            return row
    # Column full
    return -1

def check_horizontal(board, row, col, checker):
    count = 0
    for c in range(COLS):
        if board[row][c] == checker:
            count += 1
            if count == WIN_CONDITION:
                return True
        else:
            count = 0
    return False

def check_vertical(board, row, col, checker):
    count = 0
    for r in range(ROWS):
        if board[r][col] == checker:
            count += 1
            if count == WIN_CONDITION:
                return True
        else:
            count = 0
    return False

def check_diagonal(board, row, col, checker):
    # Check / diagonal (bottom-left to top-right)
    count = 0
    start_row = row
    start_col = col
    # Move to bottom-left as far as possible on / diagonal
    while start_row < ROWS-1 and start_col > 0:
        start_row += 1
        start_col -= 1
    r, c = start_row, start_col
    count = 0
    while r >= 0 and c < COLS:
        if board[r][c] == checker:
            count += 1
            if count == WIN_CONDITION:
                return True
        else:
            count = 0
        r -= 1
        c += 1

    # Check \ diagonal (top-left to bottom-right)
    # Move to top-left as far as possible on \ diagonal
    start_row = row
    start_col = col
    while start_row > 0 and start_col > 0:
        start_row -= 1
        start_col -= 1
    r, c = start_row, start_col
    count = 0
    while r < ROWS and c < COLS:
        if board[r][c] == checker:
            count += 1
            if count == WIN_CONDITION:
                return True
        else:
            count = 0
        r += 1
        c += 1

    return False

def check_win(board, row, col, checker):
    return (check_horizontal(board, row, col, checker) or
            check_vertical(board, row, col, checker) or
            check_diagonal(board, row, col, checker))

def check_draw(board):
    for c in range(COLS):
        if board[0][c] == " ":
            return False
    return True

def get_player_input(board, player_checker):
    while True:
        col_input = input(f"Player {player_checker}, please enter a column: ").upper()
        col_index = is_valid_column(col_input)
        if col_index == -1:
            # Invalid column character
            continue
        if is_column_full(board, col_index):
            # Column full - lose turn as per assignment
            return -1
        return col_index

def main():
    board = create_board()
    players = CHECKERS[:PLAYERS]
    current_player_idx = random.randint(0, PLAYERS -1)

    print_board(board)

    while True:
        player_checker = players[current_player_idx]

        col = get_player_input(board, player_checker)
        if col == -1:
            # Turn lost due to full column
            current_player_idx = (current_player_idx + 1) % PLAYERS
            continue

        row = place_checker(board, col, player_checker)
        print_board(board)

        if check_win(board, row, col, player_checker):
            print(f"Player {player_checker} won!")
            break

        if check_draw(board):
            print("The game is a draw!")
            break

        # Next player's turn
        current_player_idx = (current_player_idx + 1) % PLAYERS

if __name__ == "__main__":
    main()
