import os
import random

# Constants
ROWS = 6
COLS = 7
PLAYERS = 2
CHECKERS = ["X", "O", "V", "H", "M"]
WIN_COUNT = 4  # Number of checkers in a row needed to win
COLUMN_LABELS = [chr(ord('A') + i) for i in range(COLS)]

def clear_screen():
    os.system('clear')

def create_board():
    return [[" " for _ in range(COLS)] for _ in range(ROWS)]

def print_board(board):
    # Print column labels
    print(" ", end=" ")
    for c in COLUMN_LABELS:
        print(f" {c}  ", end="")
    print()
    
    # Print board rows
    for row in range(ROWS):
        print("+" + "---+" * COLS)
        print("|", end="")
        for col in range(COLS):
            print(f" {board[row][col]} |", end="")
        print()
    print("+" + "---+" * COLS)

def get_next_player_index(current):
    return (current + 1) % PLAYERS

def is_valid_column(col_char):
    if col_char in COLUMN_LABELS:
        col_index = COLUMN_LABELS.index(col_char)
        return col_index
    return -1

def place_checker(board, col_index, checker):
    # place checker in lowest empty spot in col_index
    for row in range(ROWS - 1, -1, -1):
        if board[row][col_index] == " ":
            board[row][col_index] = checker
            return row, col_index
    return -1, -1  # Column full

def check_win(board, row, col, checker):
    # Check horizontally
    count = 0
    for c in range(COLS):
        if board[row][c] == checker:
            count += 1
            if count == WIN_COUNT:
                return True
        else:
            count = 0

    # Check vertically
    count = 0
    for r in range(ROWS):
        if board[r][col] == checker:
            count += 1
            if count == WIN_COUNT:
                return True
        else:
            count = 0

    # Check diagonal (top-left to bottom-right)
    start_row = row
    start_col = col
    while start_row > 0 and start_col > 0:
        start_row -= 1
        start_col -= 1
    count = 0
    r, c = start_row, start_col
    while r < ROWS and c < COLS:
        if board[r][c] == checker:
            count += 1
            if count == WIN_COUNT:
                return True
        else:
            count = 0
        r += 1
        c += 1

    # Check diagonal (bottom-left to top-right)
    start_row = row
    start_col = col
    while start_row < ROWS -1 and start_col > 0:
        start_row += 1
        start_col -= 1
    count = 0
    r, c = start_row, start_col
    while r >= 0 and c < COLS:
        if board[r][c] == checker:
            count += 1
            if count == WIN_COUNT:
                return True
        else:
            count = 0
        r -= 1
        c += 1

    return False

def is_draw(board):
    # draw if no empty spaces in top row (no one can play)
    for c in range(COLS):
        if board[0][c] == " ":
            return False
    return True

def main():
    board = create_board()

    current_player = random.randint(0, PLAYERS -1)
    players_checkers = CHECKERS[:PLAYERS]

    while True:
        clear_screen()
        print_board(board)
        print(f"Player {players_checkers[current_player]}, please enter a column:")
        user_input = input().strip().upper()

        col_index = is_valid_column(user_input)
        if col_index == -1:
            # Invalid input, ask again
            continue

        row, col = place_checker(board, col_index, players_checkers[current_player])
        if row == -1:
            # Column full -> lose turn
            current_player = get_next_player_index(current_player)
            continue

        # Check if current player won
        if check_win(board, row, col, players_checkers[current_player]):
            clear_screen()
            print_board(board)
            print(f"Player {players_checkers[current_player]} won!")
            break

        if is_draw(board):
            clear_screen()
            print_board(board)
            print("The game is a draw!")
            break

        current_player = get_next_player_index(current_player)

if __name__ == "__main__":
    main()
