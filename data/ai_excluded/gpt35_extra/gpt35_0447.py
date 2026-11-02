import os
import random
import string

# Constants (set to assignment submission requirements)
ROWS = 6       # number of rows
COLS = 7       # number of columns
PLAYER_COUNT = 2  # number of players (2..5)

CHECKERS = ["X", "O", "V", "H", "M"]

# Validation of constants
assert 2 <= PLAYER_COUNT <= 5
assert 1 <= ROWS <= 100     # practical upper bound
assert 1 <= COLS <= 26

def clear_screen():
    os.system('clear')

def create_board(rows, cols):
    return [[" " for _ in range(cols)] for _ in range(rows)]

def print_board(board):
    rows = len(board)
    cols = len(board[0])
    header = "  " + "   ".join(string.ascii_uppercase[:cols])
    print(header)
    line = "+---" * cols + "+"
    for row in range(rows):
        print(line)
        row_cells = "| " + " | ".join(board[row]) + " |"
        print(row_cells)
    print(line)

def get_player_input(player_char, board):
    cols = len(board[0])
    valid_cols = string.ascii_uppercase[:cols]
    while True:
        inp = input(f"Player {player_char}, please enter a column: ").strip().upper()
        if len(inp) != 1 or inp not in valid_cols:
            continue
        col = valid_cols.index(inp)
        if board[0][col] != " ":  # column full -> player loses turn
            return None
        return col

def place_checker(board, col, player_char):
    rows = len(board)
    for row in reversed(range(rows)):  # check from bottom up
        if board[row][col] == " ":
            board[row][col] = player_char
            return row, col
    return None  # should never happen if column was validated before

def check_win(board, row, col, player_char):
    rows = len(board)
    cols = len(board[0])
    directions = [
        (0, 1),   # horizontal right
        (1, 0),   # vertical down
        (1, 1),   # diagonal down-right
        (1, -1),  # diagonal down-left
    ]
    for dr, dc in directions:
        count = 1
        # check in positive direction
        r, c = row + dr, col + dc
        while 0 <= r < rows and 0 <= c < cols and board[r][c] == player_char:
            count += 1
            r += dr
            c += dc
        # check in negative direction
        r, c = row - dr, col - dc
        while 0 <= r < rows and 0 <= c < cols and board[r][c] == player_char:
            count += 1
            r -= dr
            c -= dc
        if count >= 4:
            return True
    return False

def board_full(board):
    return all(cell != " " for cell in board[0])

def main():
    # initialize
    board = create_board(ROWS, COLS)
    players = CHECKERS[:PLAYER_COUNT]
    current_player_index = random.randrange(PLAYER_COUNT)

    clear_screen()
    print_board(board)

    while True:
        player_char = players[current_player_index]
        col = get_player_input(player_char, board)

        if col is None:
            # Full column -> lose turn, switch player
            current_player_index = (current_player_index + 1) % PLAYER_COUNT
            clear_screen()
            print_board(board)
            continue

        row, col = place_checker(board, col, player_char)
        clear_screen()
        print_board(board)

        if check_win(board, row, col, player_char):
            print(f"Player {player_char} won!")
            break

        if board_full(board):
            print("The game is a draw!")
            break

        current_player_index = (current_player_index + 1) % PLAYER_COUNT


if __name__ == "__main__":
    main()
