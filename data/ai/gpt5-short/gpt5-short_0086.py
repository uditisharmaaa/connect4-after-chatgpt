import os
import random

# Game settings
ROWS = 6
COLS = 7
COLUMN_LABELS = ['A', 'B', 'C', 'D', 'E', 'F', 'G']

# Player settings: choose 2 to 5 players
NUM_PLAYERS = 2  # change to 3, 4, or 5 if you want more players
PLAYER_SYMBOLS = ['X', 'O', 'V', 'H', 'M'][:NUM_PLAYERS]


def clear_screen():
    os.system('clear')  # use 'cls' on Windows


def create_board():
    return [['.' for _ in range(COLS)] for _ in range(ROWS)]


def draw_board(board):
    print("  " + " ".join(COLUMN_LABELS))
    for r in range(ROWS):
        print(str(ROWS - r) + " " + " ".join(board[r]))
    print()


def letter_to_col(letter):
    letter = letter.upper()
    if letter in COLUMN_LABELS:
        return COLUMN_LABELS.index(letter)
    return -1


def find_drop_row(board, col):
    # Return the row index where a piece will land in this column, or -1 if full
    for r in range(ROWS - 1, -1, -1):
        if board[r][col] == '.':
            return r
    return -1


def in_bounds(r, c):
    return 0 <= r < ROWS and 0 <= c < COLS


def check_direction(board, r, c, dr, dc, symbol):
    count = 0
    rr, cc = r, c
    while in_bounds(rr, cc) and board[rr][cc] == symbol:
        count += 1
        rr += dr
        cc += dc
    return count


def check_win(board, r, c, symbol):
    # Check all 4 directions passing through (r, c)
    # Horizontal
    left = check_direction(board, r, c, 0, -1, symbol) - 1
    right = check_direction(board, r, c, 0, 1, symbol)
    if left + right >= 4:
        return True

    # Vertical
    up = check_direction(board, r, c, -1, 0, symbol) - 1
    down = check_direction(board, r, c, 1, 0, symbol)
    if up + down >= 4:
        return True

    # Diagonal down-right / up-left
    ul = check_direction(board, r, c, -1, -1, symbol) - 1
    dr = check_direction(board, r, c, 1, 1, symbol)
    if ul + dr >= 4:
        return True

    # Diagonal up-right / down-left
    ur = check_direction(board, r, c, -1, 1, symbol) - 1
    dl = check_direction(board, r, c, 1, -1, symbol)
    if ur + dl >= 4:
        return True

    return False


def is_draw(board):
    for c in range(COLS):
        if board[0][c] == '.':
            return False
    return True


def prompt_move(current_symbol):
    while True:
        move = input(f"Player {current_symbol}, choose a column (A-G): ").strip()
        if len(move) != 1:
            print("Please enter a single letter A-G.")
            continue
        col = letter_to_col(move)
        if col == -1:
            print("Invalid column. Use letters A-G.")
            continue
        return col


def game_loop():
    if NUM_PLAYERS < 2 or NUM_PLAYERS > 5:
        print("NUM_PLAYERS must be between 2 and 5.")
        return

    board = create_board()
    current_idx = random.randrange(NUM_PLAYERS)

    while True:
        clear_screen()
        print("Connect 4 - 6 rows x 7 columns")
        print(f"Players: {' '.join(PLAYER_SYMBOLS)}")
        draw_board(board)

        symbol = PLAYER_SYMBOLS[current_idx]

        # Get a valid column with space
        while True:
            col = prompt_move(symbol)
            row = find_drop_row(board, col)
            if row == -1:
                print("That column is full. Choose another one.")
            else:
                break

        # Place the piece
        board[row][col] = symbol

        # Check for win
        if check_win(board, row, col, symbol):
            clear_screen()
            draw_board(board)
            print(f"Player {symbol} wins!")
            break

        # Check for draw
        if is_draw(board):
            clear_screen()
            draw_board(board)
            print("It's a draw!")
            break

        # Next player's turn
        current_idx = (current_idx + 1) % NUM_PLAYERS


if __name__ == "__main__":
    game_loop()
