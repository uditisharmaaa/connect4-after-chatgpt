import os
import random
import string

# --- Constants ---
BOARD_ROWS = 6           # Number of rows (default 6)
BOARD_COLS = 7           # Number of columns (default 7, max 26 for A-Z)
PLAYER_COUNT = 2         # Number of players (2-5 allowed)
PLAYER_SYMBOLS = ["X", "O", "V", "H", "M"]

# --- Helper Functions ---

def clear_screen():
    os.system('clear')

def create_board(rows=BOARD_ROWS, cols=BOARD_COLS):
    return [[" " for _ in range(cols)] for _ in range(rows)]

def print_board(board):
    cols = len(board[0])
    header = "  " + "   ".join(string.ascii_uppercase[:cols])
    print(header)
    print("+" + "---+" * cols)
    for row in board:
        print("| " + " | ".join(row) + " |")
        print("+" + "---+" * cols)

def get_player_symbols(num_players):
    return PLAYER_SYMBOLS[:num_players]

def is_valid_column(col, board):
    cols = len(board[0])
    return col in range(cols)

def get_col_index(col_letter, cols):
    col_letter = col_letter.strip().upper()
    if len(col_letter) != 1:
        return None
    idx = ord(col_letter) - ord("A")
    if 0 <= idx < cols:
        return idx
    return None

def get_next_open_row(board, col):
    for row in reversed(range(len(board))):
        if board[row][col] == " ":
            return row
    return None

def is_column_full(board, col):
    return board[0][col] != " "

def drop_checker(board, row, col, checker):
    board[row][col] = checker

def is_draw(board):
    return all(board[0][col] != " " for col in range(len(board[0])))

def in_bounds(r, c, rows, cols):
    return 0 <= r < rows and 0 <= c < cols

def check_winner(board, row, col, checker):
    rows = len(board)
    cols = len(board[0])

    def count_direction(dr, dc):
        count = 0
        r, c = row + dr, col + dc
        while in_bounds(r, c, rows, cols) and board[r][c] == checker:
            count += 1
            r += dr
            c += dc
        return count

    # Check in all 4 directions
    # Horizontal
    if (1 + count_direction(0, 1) + count_direction(0, -1)) >= 4:
        return True
    # Vertical
    if (1 + count_direction(1, 0) + count_direction(-1, 0)) >= 4:
        return True
    # Diagonal /
    if (1 + count_direction(-1, 1) + count_direction(1, -1)) >= 4:
        return True
    # Diagonal \
    if (1 + count_direction(1, 1) + count_direction(-1, -1)) >= 4:
        return True

    return False

def get_user_column(player, cols):
    while True:
        col_input = input(f"Player {player}, please enter a column: ").strip().upper()
        if not col_input or len(col_input) != 1 or not col_input.isalpha():
            print("Invalid input. Please enter a single column letter (A-G).")
            continue
        idx = get_col_index(col_input, cols)
        if idx is None:
            print(f"Column '{col_input}' is out of range.")
            continue
        return idx

# --- Main Game Function ---

def main():
    random.seed()  # (Optional) Seed can be set for deterministic testing
    rows, cols = BOARD_ROWS, BOARD_COLS
    num_players = PLAYER_COUNT
    player_symbols = get_player_symbols(num_players)
    board = create_board(rows, cols)
    current_player = random.randint(0, num_players - 1)

    clear_screen()
    print_board(board)
    print(f"\nPlayer {player_symbols[current_player]} goes first!\n")

    while True:
        # Print the board before every move
        print_board(board)
        player_symbol = player_symbols[current_player]
        col = get_user_column(player_symbol, cols)

        if is_column_full(board, col):
            print(f"Column '{string.ascii_uppercase[col]}' is full! You lose your turn.")
            current_player = (current_player + 1) % num_players
            continue

        row = get_next_open_row(board, col)
        drop_checker(board, row, col, player_symbol)

        clear_screen()

        print_board(board)

        if check_winner(board, row, col, player_symbol):
            print(f"Player {player_symbol} won!")
            break

        if is_draw(board):
            print("The game is a draw!")
            break

        current_player = (current_player + 1) % num_players

if __name__ == "__main__":
    main()
