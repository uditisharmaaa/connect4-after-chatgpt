import os
import random
import string

# Constants (you may change these for testing, but final submission should be ROWS=6, COLS=7, NUM_PLAYERS=2)
ROWS = 6
COLS = 7  # Max 26
NUM_PLAYERS = 2  # Between 2 and 5

# Player symbols in order
PLAYER_SYMBOLS = ["X", "O", "V", "H", "M"]

# Ensure configuration is valid
if not (2 <= NUM_PLAYERS <= 5):
    raise ValueError("NUM_PLAYERS must be between 2 and 5.")
if COLS > 26:
    raise ValueError("COLS must be at most 26 (A-Z).")
if ROWS < 1 or COLS < 1:
    raise ValueError("ROWS and COLS must be positive integers.")

# Build the list of players in order
PLAYERS = PLAYER_SYMBOLS[:NUM_PLAYERS]

def clear_screen():
    os.system('clear')

def create_board(rows, cols):
    return [[" " for _ in range(cols)] for _ in range(rows)]

def print_board(board):
    rows = len(board)
    cols = len(board[0])

    # Header
    header = "  " + "   ".join(string.ascii_uppercase[:cols])
    print(header)

    # Rows
    horiz = "+" + ("---+" * cols)
    for r in range(rows):
        print(horiz)
        row_cells = []
        for c in range(cols):
            row_cells.append(f"| {board[r][c]} ")
        print("".join(row_cells) + "|")
    print(horiz)

def col_letter_to_index(letter):
    letter = letter.upper()
    if len(letter) != 1 or letter < 'A' or letter >= chr(ord('A') + COLS):
        return None
    return ord(letter) - ord('A')

def drop_checker(board, col_idx, symbol):
    # Place in the lowest available row (from bottom up)
    for r in range(ROWS - 1, -1, -1):
        if board[r][col_idx] == " ":
            board[r][col_idx] = symbol
            return r
    return None  # Column full

def is_within(r, c):
    return 0 <= r < ROWS and 0 <= c < COLS

def check_win(board, symbol):
    # Check 4 in a row: right, down, diag down-right, diag up-right
    directions = [
        (0, 1),   # right
        (1, 0),   # down
        (1, 1),   # diag down-right
        (-1, 1),  # diag up-right
    ]
    for r in range(ROWS):
        for c in range(COLS):
            if board[r][c] != symbol:
                continue
            for dr, dc in directions:
                count = 1
                rr, cc = r, c
                for _ in range(3):
                    rr += dr
                    cc += dc
                    if is_within(rr, cc) and board[rr][cc] == symbol:
                        count += 1
                    else:
                        break
                if count == 4:
                    return True
    return False

def board_full(board):
    # If no spaces left anywhere, it's full
    for r in range(ROWS):
        for c in range(COLS):
            if board[r][c] == " ":
                return False
    return True

def main():
    board = create_board(ROWS, COLS)
    current_player_idx = random.randrange(len(PLAYERS))

    # Initial print
    clear_screen()
    print_board(board)

    while True:
        current_symbol = PLAYERS[current_player_idx]
        # Prompt for column input (validate until a valid column letter is given)
        while True:
            user_input = input(f"Player {current_symbol}, please enter a column: ").strip().upper()
            if len(user_input) != 1:
                print("Invalid input. Please enter a single column letter.")
                continue
            if not user_input.isalpha():
                print("Invalid input. Please enter a letter (A-Z).")
                continue
            col_idx = col_letter_to_index(user_input)
            if col_idx is None:
                print("Invalid column. Please enter a valid letter within the board.")
                continue
            # We have a valid column letter
            break

        # Try to drop the checker
        placed_row = drop_checker(board, col_idx, current_symbol)
        if placed_row is None:
            # Column is full; turn is lost
            clear_screen()
            print_board(board)
            print(f"Column {string.ascii_uppercase[col_idx]} is full. Turn lost.")
            # Next player's turn
            current_player_idx = (current_player_idx + 1) % len(PLAYERS)
            continue

        # After a (successful) turn, check for win or draw
        if check_win(board, current_symbol):
            clear_screen()
            print_board(board)
            print(f"Player {current_symbol} won!")
            break

        if board_full(board):
            clear_screen()
            print_board(board)
            print("The game is a draw.")
            break

        # Next player's turn
        clear_screen()
        print_board(board)
        current_player_idx = (current_player_idx + 1) % len(PLAYERS)

if __name__ == "__main__":
    main()
