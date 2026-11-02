import os
import random
import sys

# Constants
ROWS = 6
COLS = 7
MIN_PLAYERS = 2
MAX_PLAYERS = 5
WIN_LENGTH = 4
PLAYERS = ["X", "O", "V", "H", "M"]  # Up to 5 players

def clear_screen():
    os.system('clear')

def create_board(rows, cols):
    return [[" " for _ in range(cols)] for _ in range(rows)]

def print_board(board):
    clear_screen()
    cols = len(board[0])
    # Print column labels
    col_labels = [chr(ord('A') + i) for i in range(cols)]
    print("  " + "   ".join(col_labels))
    print("+---" * cols + "+")
    for row in board:
        print("| " + " | ".join(row) + " |")
        print("+---" * cols + "+")

def get_col_index(inp, cols):
    if len(inp) != 1:
        return None
    c = inp.upper()
    if c < 'A' or c >= chr(ord('A') + cols):
        return None
    return ord(c) - ord('A')

def place_checker(board, col, checker):
    # place checker at lowest available row in the column
    for row in reversed(range(len(board))):
        if board[row][col] == " ":
            board[row][col] = checker
            return row
    # column full
    return -1

def board_full(board):
    for row in board:
        for cell in row:
            if cell == " ":
                return False
    return True

def check_win(board, row, col, checker):
    rows = len(board)
    cols = len(board[0])

    def count_dir(r_offset, c_offset):
        count = 0
        r, c = row + r_offset, col + c_offset
        while 0 <= r < rows and 0 <= c < cols and board[r][c] == checker:
            count += 1
            r += r_offset
            c += c_offset
        return count

    # directions: horizontal, vertical, diag \, diag /
    directions = [(0,1), (1,0), (1,1), (1,-1)]

    for dr, dc in directions:
        count = 1  # count the placed checker itself
        count += count_dir(dr, dc)
        count += count_dir(-dr, -dc)
        if count >= WIN_LENGTH:
            return True
    return False

def main():
    # Settings for submission: 6x7 board, 2 players
    rows = ROWS
    cols = COLS
    num_players = 2
    players = PLAYERS[:num_players]

    board = create_board(rows, cols)
    current_player_idx = random.randint(0, num_players-1)

    print_board(board)

    while True:
        checker = players[current_player_idx]
        prompt = f"Player {checker}, please enter a column: "
        while True:
            inp = input(prompt).strip()
            col_idx = get_col_index(inp, cols)
            if col_idx is None:
                # invalid input
                continue
            placed_row = place_checker(board, col_idx, checker)
            if placed_row == -1:
                # column full, lose turn
                break
            else:
                # valid placement
                break

        print_board(board)

        if placed_row != -1:
            if check_win(board, placed_row, col_idx, checker):
                print(f"Player {checker} won!")
                sys.exit(0)
            if board_full(board):
                print("Draw!")
                sys.exit(0)

        current_player_idx = (current_player_idx + 1) % num_players

if __name__ == "__main__":
    main()
