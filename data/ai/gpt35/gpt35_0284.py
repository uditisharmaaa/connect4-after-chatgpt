import os
import random
import string

# Constants for board dimensions and players
ROWS = 6
COLUMNS = 7
PLAYERS_COUNT = 2
# Player checkers ordered for 2 to 5 players
PLAYER_CHECKERS = ["X", "O", "V", "H", "M"]
WIN_COUNT = 4

def clear_screen():
    os.system('clear')

def create_board(rows, columns):
    return [[" " for _ in range(columns)] for _ in range(rows)]

def print_board(board):
    clear_screen()
    columns = len(board[0])
    rows = len(board)
    # Print column headers
    headers = "  " + "   ".join(string.ascii_uppercase[:columns])
    print(headers)
    # Print rows with separators
    for r in range(rows):
        line = "+"
        for _ in range(columns):
            line += "---+"
        print(line)
        row_str = "|"
        for c in range(columns):
            row_str += f" {board[r][c]} |"
        print(row_str)
    print(line)

def choose_starting_player(players):
    return random.randint(0, players - 1)

def is_valid_column(input_col, columns):
    if len(input_col) != 1:
        return False
    if input_col not in string.ascii_uppercase[:columns]:
        return False
    return True

def get_column_index(input_col):
    return string.ascii_uppercase.index(input_col)

def place_checker(board, col_idx, checker):
    rows = len(board)
    # Place from bottom row upwards: find lowest empty spot in column
    for row in range(rows - 1, -1, -1):
        if board[row][col_idx] == " ":
            board[row][col_idx] = checker
            return row, col_idx
    # Column full
    return None

def check_win(board, row, col, checker):
    rows = len(board)
    cols = len(board[0])

    # Directions: horizontal, vertical, diagonal up-right, diagonal down-right
    directions = [
        (0, 1),  # horizontal right
        (1, 0),  # vertical down
        (1, 1),  # diagonal down-right
        (1, -1)  # diagonal down-left
    ]

    for dr, dc in directions:
        count = 1

        # Check forward direction
        r, c = row + dr, col + dc
        while 0 <= r < rows and 0 <= c < cols and board[r][c] == checker:
            count += 1
            r += dr
            c += dc

        # Check backward direction
        r, c = row - dr, col - dc
        while 0 <= r < rows and 0 <= c < cols and board[r][c] == checker:
            count += 1
            r -= dr
            c -= dc

        if count >= WIN_COUNT:
            return True
    return False

def is_board_full(board):
    # If any cell in top row is empty, board is not full
    for cell in board[0]:
        if cell == " ":
            return False
    return True

def read_player_input(current_checker, columns):
    while True:
        inp = input(f"Player {current_checker}, please enter a column: ").strip().upper()
        if not is_valid_column(inp, columns):
            # Invalid column letter or length
            continue
        col_idx = get_column_index(inp)
        return col_idx

def main():
    board = create_board(ROWS, COLUMNS)
    players = PLAYERS_COUNT
    checkers = PLAYER_CHECKERS[:players]
    current_player = choose_starting_player(players)

    print_board(board)

    while True:
        current_checker = checkers[current_player]

        col_idx = read_player_input(current_checker, COLUMNS)
        placed_pos = place_checker(board, col_idx, current_checker)

        if placed_pos is None:
            # Column full, player loses turn, no error message needed per spec
            current_player = (current_player + 1) % players
            print_board(board)
            continue

        row, col = placed_pos
        print_board(board)

        if check_win(board, row, col, current_checker):
            print(f"Player {current_checker} won!")
            break

        if is_board_full(board):
            print("The game is a draw!")
            break

        current_player = (current_player + 1) % players

if __name__ == "__main__":
    main()
