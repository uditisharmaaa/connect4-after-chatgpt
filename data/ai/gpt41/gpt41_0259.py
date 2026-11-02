import os
import random
import sys

# CONSTANTS
NUM_ROWS = 6
NUM_COLS = 7           # Max 26
PLAYER_NUM = 2         # 2 to 5
CHECKERS = ['X', 'O', 'V', 'H', 'M']

def clear_screen():
    os.system('clear' if os.name == 'posix' else 'cls')

def create_board(rows, cols):
    return [[" " for _ in range(cols)] for _ in range(rows)]

def print_board(board):
    cols = len(board[0])
    # Print column headers (A, B, ...)
    header = "  " + "   ".join(chr(ord('A') + i) for i in range(cols))
    print(header)
    print("+" + "---+" * cols)
    for row in board:
        row_str = "|" + "|".join(" {0} ".format(cell) for cell in row) + "|"
        print(row_str)
        print("+" + "---+" * cols)

def get_valid_input(valid_cols):
    while True:
        col_input = input().strip().upper()
        if len(col_input) != 1 or not col_input.isalpha():
            print("Invalid input. Please enter a single valid column letter:")
            continue
        col_index = ord(col_input) - ord('A')
        if col_index not in valid_cols:
            print("Invalid column. Please enter a valid column letter:")
            continue
        return col_index

def place_checker(board, col, checker):
    # Place marker in the lowest available row in specified column
    for row in reversed(board):
        if row[col] == " ":
            row[col] = checker
            return True
    # Column full
    return False

def check_win(board, checker):
    rows = len(board)
    cols = len(board[0])
    # Check horizontal
    for r in range(rows):
        for c in range(cols-3):
            if all(board[r][c+i] == checker for i in range(4)):
                return True
    # Check vertical
    for c in range(cols):
        for r in range(rows-3):
            if all(board[r+i][c] == checker for i in range(4)):
                return True
    # Check diagonal (top-left to bottom-right)
    for r in range(rows-3):
        for c in range(cols-3):
            if all(board[r+i][c+i] == checker for i in range(4)):
                return True
    # Check diagonal (bottom-left to top-right)
    for r in range(3, rows):
        for c in range(cols-3):
            if all(board[r-i][c+i] == checker for i in range(4)):
                return True
    return False

def check_draw(board):
    # Board is full if all top cells are filled
    return all(cell != " " for cell in board[0])

def main():
    # Setup
    board = create_board(NUM_ROWS, NUM_COLS)
    player_checkers = CHECKERS[:PLAYER_NUM]
    player_names = ["Player {0}".format(i+1) for i in range(PLAYER_NUM)]

    col_indices = list(range(NUM_COLS))

    # Choose random first player
    current_player = random.randint(0, PLAYER_NUM-1)

    # Game loop
    game_over = False
    clear_screen()
    print_board(board)

    while not game_over:
        checker = player_checkers[current_player]
        player_label = player_names[current_player]
        col_letters = [chr(ord('A') + col) for col in col_indices]
        print(f"{player_label} ({checker}), please enter a column ({', '.join(col_letters)}):")
        col = get_valid_input(col_indices)
        if not place_checker(board, col, checker):
            print("Column is full. You lose your turn.")
        else:
            clear_screen()
            print_board(board)
            if check_win(board, checker):
                print(f"{player_label} ({checker}) won!")
                game_over = True
                continue
            elif check_draw(board):
                print("It's a draw!")
                game_over = True
                continue

        # Next player's turn
        current_player = (current_player + 1) % PLAYER_NUM

if __name__ == '__main__':
    main()
