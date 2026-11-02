import os
import random

# Constants
ROWS = 6
COLS = 7
NUM_PLAYERS = 2
CHECKERS = ['X', 'O', 'V', 'H', 'M']
WIN_COUNT = 4
COLUMN_LABELS = [chr(ord('A') + i) for i in range(COLS)]

def clear_screen():
    os.system('clear')

def create_board():
    return [[' ' for _ in range(COLS)] for _ in range(ROWS)]

def print_board(board):
    clear_screen()
    # Print column headers
    print("  " + "   ".join(COLUMN_LABELS))
    # Print board rows with separator lines
    line_sep = "+" + "---+" * COLS
    for r in range(ROWS):
        print(line_sep)
        row_str = "|"
        for c in range(COLS):
            row_str += " {} |".format(board[r][c])
        print(row_str)
    print(line_sep)

def is_valid_column_input(col_input):
    if len(col_input) != 1:
        return False
    col = col_input.upper()
    return col in COLUMN_LABELS

def column_index(col_input):
    return ord(col_input.upper()) - ord('A')

def place_checker(board, col_idx, checker):
    # The checker falls to the lowest empty row in the column
    # Rows indexed 0(top) to ROWS-1(bottom)
    # So we start from the bottom and go up to find the first empty spot
    for row in range(ROWS-1, -1, -1):
        if board[row][col_idx] == ' ':
            board[row][col_idx] = checker
            return row, col_idx
    # Column full
    return None

def check_horizontal(board, row, col, checker):
    count = 0
    for c in range(COLS):
        if board[row][c] == checker:
            count += 1
            if count == WIN_COUNT:
                return True
        else:
            count = 0
    return False

def check_vertical(board, row, col, checker):
    count = 0
    for r in range(ROWS):
        if board[r][col] == checker:
            count += 1
            if count == WIN_COUNT:
                return True
        else:
            count = 0
    return False

def check_diagonal(board, row, col, checker):
    # Top-left to bottom-right
    start_r, start_c = row, col
    while start_r > 0 and start_c > 0:
        start_r -= 1
        start_c -= 1
    count = 0
    r, c = start_r, start_c
    while r < ROWS and c < COLS:
        if board[r][c] == checker:
            count += 1
            if count == WIN_COUNT:
                return True
        else:
            count = 0
        r += 1
        c += 1

    # Top-right to bottom-left
    start_r, start_c = row, col
    while start_r > 0 and start_c < COLS-1:
        start_r -= 1
        start_c += 1
    count = 0
    r, c = start_r, start_c
    while r < ROWS and c >= 0:
        if board[r][c] == checker:
            count += 1
            if count == WIN_COUNT:
                return True
        else:
            count = 0
        r += 1
        c -= 1
    return False

def check_win(board, row, col, checker):
    return (check_horizontal(board, row, col, checker) or
            check_vertical(board, row, col, checker) or
            check_diagonal(board, row, col, checker))

def is_draw(board):
    # If every cell in top row is filled, no more moves possible
    for c in range(COLS):
        if board[0][c] == ' ':
            return False
    return True

def get_next_player_idx(current_idx):
    return (current_idx + 1) % NUM_PLAYERS

def get_valid_input(prompt, board):
    while True:
        player_input = input(prompt).strip().upper()
        # Check if input valid column letter
        if not is_valid_column_input(player_input):
            print("Invalid input. Please enter a letter from A to", COLUMN_LABELS[-1])
            continue
        col_idx = column_index(player_input)
        # Check if column full
        if board[0][col_idx] != ' ':
            # Turn lost on full column,
            return None
        return col_idx

def main():
    board = create_board()
    players = CHECKERS[:NUM_PLAYERS]
    current_player_idx = random.randrange(NUM_PLAYERS)

    print_board(board)
    while True:
        checker = players[current_player_idx]
        prompt = f"Player {checker}, please enter a column: "
        col_idx = get_valid_input(prompt, board)

        if col_idx is None:
            # Column is full - turn lost
            print(f"Column full! Player {checker} loses this turn.")
            input("Press Enter to continue...")
            current_player_idx = get_next_player_idx(current_player_idx)
            print_board(board)
            continue

        placed_pos = place_checker(board, col_idx, checker)
        if placed_pos is None:
            # Should never happen since full column checked above
            print(f"Unexpected error placing checker.")
            continue
        r, c = placed_pos

        print_board(board)

        if check_win(board, r, c, checker):
            print(f"Player {checker} won!")
            break

        if is_draw(board):
            print("The game is a draw!")
            break

        current_player_idx = get_next_player_idx(current_player_idx)


if __name__ == "__main__":
    main()
