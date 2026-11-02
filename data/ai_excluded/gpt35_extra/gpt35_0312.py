import os
import random

# Constants
ROWS = 6
COLUMNS = 7
NUM_PLAYERS = 2
MAX_PLAYERS = 5
CHECKERS = ["X", "O", "V", "H", "M"]
WIN_LEN = 4

def clear_screen():
    os.system('clear')

def create_board(rows, cols):
    return [[" " for _ in range(cols)] for _ in range(rows)]

def print_board(board):
    clear_screen()
    cols = len(board[0])
    rows = len(board)
    # Print column headers
    header = "  "
    for c in range(cols):
        header += f" {chr(ord('A') + c)}  "
    print(header)
    # Print the board rows with separators
    sep_line = "+" + "---+" * cols
    for r in range(rows):
        print(sep_line)
        row_str = "|"
        for c in range(cols):
            row_str += f" {board[r][c]} |"
        print(row_str)
    print(sep_line)

def input_column(player_checker, columns, board):
    valid_cols = [chr(ord('A') + i) for i in range(columns)]
    while True:
        inp = input(f"Player {player_checker}, please enter a column: ").strip().upper()
        if len(inp) != 1 or inp not in valid_cols:
            # Invalid letter
            continue
        col_index = ord(inp) - ord('A')
        # Check if column is full
        if board[0][col_index] != " ":
            # Column full, lose turn
            return -1
        return col_index

def place_checker(board, col, checker):
    # Place checker at lowest available row in column col
    rows = len(board)
    for r in range(rows-1, -1, -1):
        if board[r][col] == " ":
            board[r][col] = checker
            return r, col
    return None  # Column full (should not be reached with earlier check)

def check_win(board, r, c, checker):
    rows = len(board)
    cols = len(board[0])

    def count_dir(dr, dc):
        count = 0
        rr, cc = r + dr, c + dc
        while 0 <= rr < rows and 0 <= cc < cols and board[rr][cc] == checker:
            count += 1
            rr += dr
            cc += dc
        return count

    # Check horizontally (left + right)
    total = 1 + count_dir(0, -1) + count_dir(0, 1)
    if total >= WIN_LEN:
        return True

    # Check vertically (up + down)
    total = 1 + count_dir(-1, 0) + count_dir(1, 0)
    if total >= WIN_LEN:
        return True

    # Check diagonal 1 (up-left + down-right)
    total = 1 + count_dir(-1, -1) + count_dir(1, 1)
    if total >= WIN_LEN:
        return True

    # Check diagonal 2 (up-right + down-left)
    total = 1 + count_dir(-1, 1) + count_dir(1, -1)
    if total >= WIN_LEN:
        return True

    return False

def board_full(board):
    return all(cell != " " for cell in board[0])

def main():
    # Initialize game
    players_checkers = CHECKERS[:NUM_PLAYERS]
    board = create_board(ROWS, COLUMNS)
    current_player = random.randint(0, NUM_PLAYERS - 1)

    print_board(board)

    while True:
        checker = players_checkers[current_player]
        col = input_column(checker, COLUMNS, board)
        if col == -1:
            # Column full, lose turn
            current_player = (current_player + 1) % NUM_PLAYERS
            print_board(board)
            continue

        r, c = place_checker(board, col, checker)
        print_board(board)

        if check_win(board, r, c, checker):
            print(f"Player {checker} won!")
            break

        if board_full(board):
            print("Draw!")
            break

        current_player = (current_player + 1) % NUM_PLAYERS

if __name__ == "__main__":
    main()
