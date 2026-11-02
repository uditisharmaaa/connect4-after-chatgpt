import os
import random
import string
import sys

# ======= CONSTANTS =======
ROWS = 6
COLS = 7
PLAYERS = 2
CHECKERS = ["X", "O", "V", "H", "M"]
MIN_PLAYERS = 2
MAX_PLAYERS = 5
MIN_ROWS = 4
MIN_COLS = 4
MAX_COLS = 26

# ======= BOARD FUNCTIONS =======
def create_board(rows, cols):
    return [[" " for _ in range(cols)] for _ in range(rows)]

def print_board(board):
    os.system('clear')  # or 'cls' for Windows
    cols = len(board[0])
    # Print column headers
    headers = "  " + "   ".join([string.ascii_uppercase[i] for i in range(cols)])
    print(headers)
    print("+" + "---+" * cols)
    for row in board:
        print("| " + " | ".join(row) + " |")
        print("+" + "---+" * cols)

# ======= INPUT VALIDATION =======
def get_column_input(board, valid_columns):
    while True:
        col_input = input("Please enter a column: ").strip().upper()
        if len(col_input) != 1 or col_input not in valid_columns:
            print("Invalid column letter! Try again.")
            continue
        col_index = valid_columns.index(col_input)
        # Check if column is full
        if board[0][col_index] != " ":
            print("Column is full! You lose your turn.")
            return None
        else:
            return col_index

# ======= GAME LOGIC =======
def place_checker(board, col, checker):
    """Place checker in the lowest available slot in specified column. Return row number."""
    for row in reversed(range(len(board))):
        if board[row][col] == " ":
            board[row][col] = checker
            return row
    return None  # Should not happen if column input validation is done properly

def check_winner(board, last_row, last_col, checker):
    """Check 4 in a row for the last placed checker"""
    directions = [(0,1), (1,0), (1,1), (1,-1)]  # horiz, vert, diag-down, diag-up
    for dr, dc in directions:
        count = 1
        # Check in positive direction
        r, c = last_row + dr, last_col + dc
        while 0 <= r < len(board) and 0 <= c < len(board[0]) and board[r][c] == checker:
            count += 1
            r += dr
            c += dc
        # Check in negative direction
        r, c = last_row - dr, last_col - dc
        while 0 <= r < len(board) and 0 <= c < len(board[0]) and board[r][c] == checker:
            count += 1
            r -= dr
            c -= dc
        if count >= 4:
            return True
    return False

def is_draw(board):
    """Returns True if no empty slots remain"""
    return all(cell != " " for cell in board[0])

def switch_player(current_idx, num_players):
    return (current_idx + 1) % num_players

def get_valid_columns(cols):
    return [string.ascii_uppercase[i] for i in range(cols)]

def main():
    # Initialization
    if not (MIN_PLAYERS <= PLAYERS <= MAX_PLAYERS):
        print(f"Number of players must be between {MIN_PLAYERS} and {MAX_PLAYERS}.")
        sys.exit(1)
    if not (MIN_ROWS <= ROWS) or not (MIN_COLS <= COLS <= MAX_COLS):
        print(f"Board size must be at least {MIN_ROWS}x{MIN_COLS} and max {MAX_COLS} columns.")
        sys.exit(1)
    board = create_board(ROWS, COLS)
    players = [CHECKERS[i] for i in range(PLAYERS)]
    valid_columns = get_valid_columns(COLS)

    # Random first player
    current_player_index = random.randint(0, PLAYERS-1)
    print_board(board)
    print(f"Player {players[current_player_index]} starts!")

    while True:
        checker = players[current_player_index]
        print(f"Player {checker},", end=' ')
        col_index = get_column_input(board, valid_columns)
        if col_index is None:
            # Column was full, player loses turn
            current_player_index = switch_player(current_player_index, PLAYERS)
            continue

        row_index = place_checker(board, col_index, checker)
        print_board(board)

        # Check for winner
        if check_winner(board, row_index, col_index, checker):
            print(f"Player {checker} won!")
            break

        # Check for draw
        if is_draw(board):
            print("It's a draw!")
            break

        current_player_index = switch_player(current_player_index, PLAYERS)

if __name__ == "__main__":
    main()
