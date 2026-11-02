import os
import random
import string

# Constants for the game configuration
ROWS = 6
COLUMNS = 7
MIN_PLAYERS = 2
MAX_PLAYERS = 5
PLAYERS = 2  # Change up to 5 if desired, but for submission set to 2
CHECKERS = ["X", "O", "V", "H", "M"][:PLAYERS]
WIN_LENGTH = 4
COLUMN_LETTERS = string.ascii_uppercase[:COLUMNS]

def clear_screen():
    os.system('clear')

def create_board(rows, columns):
    return [[" " for _ in range(columns)] for _ in range(rows)]

def print_board(board):
    clear_screen()
    # Print column headers
    header = "  " + "   ".join(COLUMN_LETTERS)
    print(header)
    # Print separator line
    sep = "+" + "---+" * COLUMNS
    for row in board:
        print(sep)
        print("| " + " | ".join(row) + " |")
    print(sep)

def is_valid_column_input(user_input):
    return len(user_input) == 1 and user_input in COLUMN_LETTERS

def get_column_index(letter):
    return COLUMN_LETTERS.index(letter)

def column_full(board, col_idx):
    # If top cell in column already occupied, column is full
    return board[0][col_idx] != " "

def place_checker(board, col_idx, checker):
    # Place checker in lowest empty spot in the column
    for row_idx in range(ROWS - 1, -1, -1):
        if board[row_idx][col_idx] == " ":
            board[row_idx][col_idx] = checker
            return row_idx, col_idx
    # Column full, return None meaning placement failed
    return None

def check_direction(board, start_r, start_c, dr, dc, checker):
    count = 0
    r, c = start_r, start_c
    while 0 <= r < ROWS and 0 <= c < COLUMNS and board[r][c] == checker:
        count += 1
        r += dr
        c += dc
    return count

def check_win(board, row, col, checker):
    # Check all directions for 4 in a row:
    # Horizontal: left(-1,0), right(1,0)
    # Vertical: up(0,-1), down(0,1)
    # Diagonal1: up-left(-1,-1), down-right(1,1)
    # Diagonal2: up-right(1,-1), down-left(-1,1)

    directions = [
        ((0, -1), (0, 1)),     # vertical
        ((-1, 0), (1, 0)),     # horizontal
        ((-1, -1), (1, 1)),    # diag down-right
        ((-1, 1), (1, -1))     # diag down-left
    ]
    for (dr1, dc1), (dr2, dc2) in directions:
        count = 1  # starting point itself
        count += check_direction(board, row + dr1, col + dc1, dr1, dc1, checker) - 1 + 1
        count += check_direction(board, row + dr2, col + dc2, dr2, dc2, checker) - 1 + 1
        # Actually, the above double counts start cell, let's fix counting logic with a helper function.
        # Let's do it better:
        count = 1 + \
                count_direction(board, row, col, dr1, dc1, checker) + \
                count_direction(board, row, col, dr2, dc2, checker)
        if count >= WIN_LENGTH:
            return True
    return False

def count_direction(board, row, col, dr, dc, checker):
    count = 0
    r, c = row + dr, col + dc
    while 0 <= r < ROWS and 0 <= c < COLUMNS and board[r][c] == checker:
        count += 1
        r += dr
        c += dc
    return count

def board_full(board):
    for col in range(COLUMNS):
        if board[0][col] == " ":
            return False
    return True

def input_column(player_checker):
    while True:
        user_input = input(f"Player {player_checker}, please enter a column: ").strip().upper()
        if not is_valid_column_input(user_input):
            print(f"Invalid input. Please enter a letter between {COLUMN_LETTERS[0]} and {COLUMN_LETTERS[-1]}.")
            continue
        col_idx = get_column_index(user_input)
        if column_full(board, col_idx):
            # Per instructions the player loses turn if column full
            return None
        return col_idx

def main():
    global board
    board = create_board(ROWS, COLUMNS)

    current_player_index = random.randint(0, PLAYERS - 1)
    print_board(board)

    while True:
        checker = CHECKERS[current_player_index]
        col_idx = input_column(checker)
        if col_idx is None:
            # Player loses turn for trying to place in full column
            print(f"Column {COLUMN_LETTERS[col_idx] if col_idx is not None else ''} is full. Player {checker} loses this turn.")
        else:
            pos = place_checker(board, col_idx, checker)
            print_board(board)
            if pos is not None:
                r, c = pos
                if check_win(board, r, c, checker):
                    print(f"Player {checker} won!")
                    break
                if board_full(board):
                    print("The game is a draw.")
                    break
        current_player_index = (current_player_index + 1) % PLAYERS

if __name__ == "__main__":
    main()
