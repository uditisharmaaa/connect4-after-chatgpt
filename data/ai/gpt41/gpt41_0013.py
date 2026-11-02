import os
import random
import sys

# ==== CONSTANTS ====
ROWS = 6
COLS = 7
MAX_COLS = 26   # Max column limit for letter labels
CHECKERS = ["X", "O", "V", "H", "M"]
PLAYERS = 2     # Change this for more players, up to 5

# ==== GAME STATE ====
board = [[" " for _ in range(COLS)] for _ in range(ROWS)]
player_symbols = CHECKERS[:PLAYERS]
column_labels = [chr(ord('A') + i) for i in range(COLS)]

# ==== FUNCTIONS ====

def clear_screen():
    os.system('clear')

def print_board():
    clear_screen()
    print("  " + "   ".join(column_labels))
    print("+---" * COLS + "+")
    for r in range(ROWS):
        row_str = "| " + " | ".join(board[r]) + " |"
        print(row_str)
        print("+---" * COLS + "+")

def is_valid_column(col_input):
    if len(col_input) != 1 or not col_input.isalpha():
        return False
    col_input = col_input.upper()
    if col_input not in column_labels:
        return False
    col_idx = column_labels.index(col_input)
    # If there's an empty spot in the column, it's valid
    return board[0][col_idx] == " "

def get_column_index(col_input):
    return column_labels.index(col_input.upper())

def place_checker(col_idx, player_symbol):
    # Place checker at lowest empty cell in column
    for row in reversed(range(ROWS)):
        if board[row][col_idx] == " ":
            board[row][col_idx] = player_symbol
            return row, col_idx
    return None  # Should not happen if column is checked as valid

def check_win(row, col, player_symbol):
    # Check all directions for 4 in a row
    def count_dir(dr, dc):
        r, c = row+dr, col+dc
        count = 0
        while 0 <= r < ROWS and 0 <= c < COLS and board[r][c] == player_symbol:
            count += 1
            r += dr
            c += dc
        return count
    # directions: (vertical, horizontal, both diagonals)
    directions = [ (1,0), (0,1), (1,1), (1,-1) ]
    for dr, dc in directions:
        total = 1 + count_dir(dr, dc) + count_dir(-dr, -dc)
        if total >= 4:
            return True
    return False

def board_full():
    return all(board[0][col] != " " for col in range(COLS))

def input_column(player_symbol):
    while True:
        col_input = input(f"Player {player_symbol}, please enter a column: ").strip().upper()
        if not is_valid_column(col_input):
            print("Invalid column. Please enter a valid column label (A-{}) for a non-full column.".format(column_labels[-1]))
            continue
        col_idx = get_column_index(col_input)
        return col_idx

# ==== GAME LOOP ====

def main():
    # Choose starting player randomly
    current_player = random.randint(0, PLAYERS - 1)
    print_board()
    while True:
        player_symbol = player_symbols[current_player]
        col_idx = input_column(player_symbol)
        placed = place_checker(col_idx, player_symbol)
        print_board()
        if placed:  # (row, col) tuple
            row, col = placed
            if check_win(row, col, player_symbol):
                print(f"Player {player_symbol} won!")
                sys.exit(0)
            if board_full():
                print("It's a draw!")
                sys.exit(0)
        current_player = (current_player + 1) % PLAYERS

if __name__ == "__main__":
    main()
