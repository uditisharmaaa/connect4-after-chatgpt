import os
import random

# Constants
ROWS = 6
COLS = 7
MAX_COLS = 26
MIN_PLAYERS = 2
MAX_PLAYERS = 5

# Configure game parameters here:
NUM_PLAYERS = 2  # Must be between MIN_PLAYERS and MAX_PLAYERS
PLAYER_CHECKERS = ["X", "O", "V", "H", "M"]
WIN_LENGTH = 4

# Validate constants
if not (MIN_PLAYERS <= NUM_PLAYERS <= MAX_PLAYERS):
    raise ValueError(f"NUM_PLAYERS must be between {MIN_PLAYERS} and {MAX_PLAYERS}")
if COLS > MAX_COLS:
    raise ValueError(f"COLS cannot be greater than {MAX_COLS}")

def clear_screen():
    os.system('clear')

def create_board(rows, cols):
    return [[" " for _ in range(cols)] for _ in range(rows)]

def print_board(board):
    cols = len(board[0])
    header = "  " + "   ".join(chr(ord('A') + i) for i in range(cols))
    line = "+---" * cols + "+"
    print(header)
    for row in range(len(board)):
        print(line)
        print("| " + " | ".join(board[row]) + " |")
    print(line)

def get_column_index(user_input, max_cols):
    if len(user_input) != 1:
        return -1
    c = user_input.upper()
    if 'A' <= c <= chr(ord('A') + max_cols - 1):
        return ord(c) - ord('A')
    return -1

def is_column_full(board, col_idx):
    return board[0][col_idx] != " "

def place_checker(board, col_idx, checker):
    """
    Place checker in specified column.
    Checker falls to the lowest empty row.
    Return True if placed, False if column is full.
    """
    rows = len(board)
    for row in range(rows-1, -1, -1):
        if board[row][col_idx] == " ":
            board[row][col_idx] = checker
            return True
    return False

def check_win(board, checker):
    rows = len(board)
    cols = len(board[0])

    def in_bounds(r, c):
        return 0 <= r < rows and 0 <= c < cols

    # check all directions for a sequence of WIN_LENGTH checkers
    directions = [
        (0, 1),   # horizontal right
        (1, 0),   # vertical down
        (1, 1),   # diagonal down-right
        (1, -1),  # diagonal down-left
    ]

    for r in range(rows):
        for c in range(cols):
            if board[r][c] != checker:
                continue
            for dr, dc in directions:
                count = 1
                nr, nc = r + dr, c + dc
                while in_bounds(nr, nc) and board[nr][nc] == checker:
                    count += 1
                    if count == WIN_LENGTH:
                        return True
                    nr += dr
                    nc += dc
    return False

def board_full(board):
    # If top row has no empty cells, board is full
    return all(cell != " " for cell in board[0])

def input_column(player):
    while True:
        usr = input(f"Player {player}, please enter a column: ").strip()
        col_idx = get_column_index(usr, COLS)
        if col_idx == -1:
            # Invalid column input
            continue
        return col_idx

def main():
    # Setup game
    board = create_board(ROWS, COLS)
    players = PLAYER_CHECKERS[:NUM_PLAYERS]
    current_player_idx = random.randint(0, NUM_PLAYERS - 1)

    while True:
        clear_screen()
        print_board(board)
        current_checker = players[current_player_idx]

        # Player input & validate
        col_idx = None
        while True:
            col_idx = input_column(current_checker)
            if is_column_full(board, col_idx):
                # Column full, player loses turn (skip placement)
                break
            else:
                # Place checker and break input loop
                place_checker(board, col_idx, current_checker)
                break

        # After move or skipped turn:
        # Check win only if a checker was placed (not skipped)
        # If column full and player loses turn, just check draw
        won = False
        if not is_column_full(board, col_idx) or board[col_idx][0] != " ":
            if check_win(board, current_checker):
                won = True

        if won:
            clear_screen()
            print_board(board)
            print(f"Player {current_checker} won!")
            break

        if board_full(board):
            clear_screen()
            print_board(board)
            print("The game is a draw!")
            break

        # Next player's turn
        current_player_idx = (current_player_idx + 1) % NUM_PLAYERS


if __name__ == "__main__":
    main()
