import os
import random
import sys

# ========== Constants ==========
ROWS = 6
COLUMNS = 7
NUM_PLAYERS = 2  # (set for 2 players on submission)
WIN_CONDITION = 4  # number of checkers for win

MAX_COLUMNS = 26
PLAYER_SYMBOLS = ["X", "O", "V", "H", "M"]
COLUMN_LABELS = [chr(ord("A") + i) for i in range(MAX_COLUMNS)]

EMPTY_CELL = " "

# ========== Board Functions ==========

def create_board(rows, columns):
    """Create board with given rows and columns filled with EMPTY_CELL."""
    return [[EMPTY_CELL for _ in range(columns)] for _ in range(rows)]

def clear_screen():
    """Clear the terminal screen."""
    os.system('clear')

def print_board(board, columns):
    """Print the board with column labels."""
    print()
    labels = [f" {COLUMN_LABELS[c]} " for c in range(columns)]
    print(" " + " ".join(labels))
    print("+" + "---+" * columns)
    for row in board:
        print("| " + " | ".join(row) + " |")
        print("+" + "---+" * columns)

def get_active_player(turn, num_players):
    """Determine current player based on turn number."""
    return turn % num_players

def available_row(board, col):
    """Return the row index where the checker would land or None if column full."""
    for row in reversed(range(len(board))):
        if board[row][col] == EMPTY_CELL:
            return row
    return None

def is_board_full(board):
    """Check if the board is fully occupied."""
    for col in range(len(board[0])):
        if board[0][col] == EMPTY_CELL:
            return False
    return True

def drop_checker(board, row, col, checker):
    """Place the player's checker at board[row][col]."""
    board[row][col] = checker

def valid_column_input(inp, columns):
    """Check if the input is a valid column label within the playing board."""
    if len(inp) != 1:
        return False
    if inp not in COLUMN_LABELS[:columns]:
        return False
    return True

# ========== Win Checking ==========

def check_win(board, row, col, win_condition):
    """Check if placing at (row, col) causes a win."""
    checker = board[row][col]
    directions = [
        (0, 1),    # Horizontal
        (1, 0),    # Vertical
        (1, 1),    # Diagonal /
        (1, -1),   # Diagonal \
    ]
    rows = len(board)
    cols = len(board[0])

    for dr, dc in directions:
        count = 1
        # Check one direction
        r, c = row + dr, col + dc
        while 0 <= r < rows and 0 <= c < cols and board[r][c] == checker:
            count += 1
            r += dr
            c += dc
        # Check the opposite direction
        r, c = row - dr, col - dc
        while 0 <= r < rows and 0 <= c < cols and board[r][c] == checker:
            count += 1
            r -= dr
            c -= dc
        if count >= win_condition:
            return True
    return False

# ========== Main Game Loop ==========

def main():
    random.seed()
    board = create_board(ROWS, COLUMNS)
    player_syms = PLAYER_SYMBOLS[:NUM_PLAYERS]

    start_player = random.randint(0, NUM_PLAYERS - 1)
    # Used to alternate, start from the randomly selected player
    cur_turn = start_player

    while True:
        clear_screen()
        print_board(board, COLUMNS)
        if is_board_full(board):
            print("Game ended in a draw!")
            break

        player_idx = get_active_player(cur_turn, NUM_PLAYERS)
        player_sym = player_syms[player_idx]
        valid = False

        # Input Loop: Prompt until valid input or player loses turn on full column
        while not valid:
            inp = input(f"Player {player_sym}, please enter a column: ").strip().upper()
            if not valid_column_input(inp, COLUMNS):
                print("Invalid input. Please use column letters (A-G). Try again.")
                continue

            col = COLUMN_LABELS.index(inp)
            row_idx = available_row(board, col)
            if row_idx is None:
                print("Column is full. You lose your turn.")
                valid = True  # player loses turn
            else:
                drop_checker(board, row_idx, col, player_sym)
                if check_win(board, row_idx, col, WIN_CONDITION):
                    clear_screen()
                    print_board(board, COLUMNS)
                    print(f"Player {player_sym} won!")
                    return
                valid = True  # successful turn

        cur_turn += 1  # Move to next player

if __name__ == "__main__":
    main()
