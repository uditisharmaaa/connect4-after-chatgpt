import os
import random
import string

# Constants (must set these for submission)
ROWS = 6
COLS = 7
NUM_PLAYERS = 2
CHECKERS = ["X", "O", "V", "H", "M"]  # max 5 players
WIN_LENGTH = 4

def clear_screen():
    os.system('clear')

def create_board(rows, cols):
    return [[" " for _ in range(cols)] for _ in range(rows)]

def print_board(board):
    clear_screen()
    cols = len(board[0])
    rows = len(board)
    # Print column headers (A, B, C, ...)
    header = "  " + "   ".join(string.ascii_uppercase[:cols])
    print(header)
    # Print board with +---+---+ ... and rows
    horizontal_line = "+" + "---+" * cols
    for r in range(rows):
        print(horizontal_line)
        row_str = "|"
        for c in range(cols):
            row_str += " {} |".format(board[r][c])
        print(row_str)
    print(horizontal_line)

def is_valid_column_input(input_str, cols):
    if len(input_str) != 1:
        return False
    c = input_str.upper()
    if c not in string.ascii_uppercase[:cols]:
        return False
    return True

def get_column_index(col_char):
    return ord(col_char.upper()) - ord('A')

def find_row_to_place(board, col):
    # Returns the row index where the checker can be placed in col, or None if full
    for row in reversed(range(len(board))):
        if board[row][col] == " ":
            return row
    return None

def place_checker(board, col, checker):
    row = find_row_to_place(board, col)
    if row is None:
        # Column full
        return False
    board[row][col] = checker
    return True

def check_win_from(board, row, col, checker):
    rows = len(board)
    cols = len(board[0])

    def count_dir(dr, dc):
        count = 0
        r, c = row + dr, col + dc
        while 0 <= r < rows and 0 <= c < cols and board[r][c] == checker:
            count += 1
            r += dr
            c += dc
        return count

    # directions: horizontal, vertical, diagonal /
    # We count continuous checkers in 2 directions and sum + 1 (current)
    # Horizontal (left and right)
    total_h = 1 + count_dir(0, -1) + count_dir(0, 1)
    if total_h >= WIN_LENGTH:
        return True

    # Vertical (up and down)
    total_v = 1 + count_dir(-1, 0) + count_dir(1, 0)
    if total_v >= WIN_LENGTH:
        return True

    # Diagonal "\" (top-left to bottom-right)
    total_d1 = 1 + count_dir(-1, -1) + count_dir(1, 1)
    if total_d1 >= WIN_LENGTH:
        return True

    # Diagonal "/" (bottom-left to top-right)
    total_d2 = 1 + count_dir(1, -1) + count_dir(-1, 1)
    if total_d2 >= WIN_LENGTH:
        return True

    return False

def board_full(board):
    for row in board:
        if " " in row:
            return False
    return True

def main():
    board = create_board(ROWS, COLS)
    players = CHECKERS[:NUM_PLAYERS]
    # Random starting player
    current_player_idx = random.randint(0, NUM_PLAYERS - 1)

    print_board(board)

    while True:
        checker = players[current_player_idx]
        prompt = f"Player {checker}, please enter a column: "
        # Get valid input
        while True:
            col_input = input(prompt).strip().upper()
            if not is_valid_column_input(col_input, COLS):
                continue
            col = get_column_index(col_input)
            # Check if column full
            if find_row_to_place(board, col) is None:
                # Column full -> player loses turn (immediate break)
                break
            else:
                # Valid move
                placed = place_checker(board, col, checker)
                if not placed:
                    # should not happen, fallback
                    break
                else:
                    break

        print_board(board)

        # If player placed a checker (not lost turn due to full column)
        if find_row_to_place(board, col) is not None:
            # find row just placed checker at
            placed_row = find_row_to_place(board, col)
            if placed_row is None:
                # Since the piece is placed at lowest free slot, the occupied slot is one row below
                placed_row = 0
            else:
                # If place_checker placed checker on row r, then find_row_to_place will return row above that,
                # so correct placed_row is find_row_to_place + 1
                placed_row += 1
            # Actually, better to find the row with checker now:
            # scan from bottom up in the column to find checker
            placed_row = None
            for r in range(ROWS):
                if board[r][col] == checker:
                    placed_row = r
            # Check win
            if placed_row is not None and check_win_from(board, placed_row, col, checker):
                print(f"Player {checker} won!")
                break
            # Check draw
            if board_full(board):
                print("Draw!")
                break

        else:
            # Player lost turn due to full column, no piece placed, just continue
            # but current_player_idx will move to next, so no change needed
            pass

        # Next player's turn
        current_player_idx = (current_player_idx + 1) % NUM_PLAYERS


if __name__ == "__main__":
    main()
