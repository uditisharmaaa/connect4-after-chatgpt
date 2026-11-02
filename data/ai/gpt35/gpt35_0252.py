import os
import random

# Constants
ROWS = 6
COLS = 7
PLAYERS = 2
CHECKERS = ["X", "O", "V", "H", "M"]
WIN_COUNT = 4

def clear_screen():
    os.system('clear')

def create_board(rows, cols):
    return [[" " for _ in range(cols)] for _ in range(rows)]

def print_board(board):
    clear_screen()
    # Print column headers
    headers = [chr(ord('A') + i) for i in range(len(board[0]))]
    print("  " + "   ".join(headers))
    # Print board rows with grid lines
    for row in board:
        print("+" + "---+" * len(row))
        print("| " + " | ".join(row) + " |")
    print("+" + "---+" * len(board[0]))

def is_valid_column(col_char, cols):
    if len(col_char) != 1:
        return False
    col = ord(col_char) - ord('A')
    return 0 <= col < cols

def get_column_index(col_char):
    return ord(col_char) - ord('A')

def place_checker(board, col, checker):
    # Check from bottom row upward for empty spot
    for r in reversed(range(len(board))):
        if board[r][col] == " ":
            board[r][col] = checker
            return r, col
    # Column full
    return None

def check_direction(board, start_row, start_col, delta_row, delta_col, checker):
    count = 0
    r, c = start_row, start_col
    rows = len(board)
    cols = len(board[0])

    while 0 <= r < rows and 0 <= c < cols and board[r][c] == checker:
        count += 1
        r += delta_row
        c += delta_col
    return count

def check_win(board, r, c, checker):
    # Check all 4 directions (horizontal, vertical, two diagonals)
    directions = [
        ((0, 1), (0, -1)),    # horizontal
        ((1, 0), (-1, 0)),    # vertical
        ((1, 1), (-1, -1)),   # diagonal down-right / up-left
        ((1, -1), (-1, 1)),   # diagonal down-left / up-right
    ]

    for dir1, dir2 in directions:
        count = 1  # Count the placed checker
        count += check_direction(board, r + dir1[0], c + dir1[1], dir1[0], dir1[1], checker)
        count += check_direction(board, r + dir2[0], c + dir2[1], dir2[0], dir2[1], checker)
        if count >= WIN_COUNT:
            return True
    return False

def board_full(board):
    for c in range(len(board[0])):
        if board[0][c] == " ":
            return False
    return True

def get_player_input(board, checker):
    cols = len(board[0])
    while True:
        col_char = input(f"Player {checker}, please enter a column: ").strip().upper()
        if not is_valid_column(col_char, cols):
            # invalid input
            continue
        col = get_column_index(col_char)
        if board[0][col] != " ":
            # column full, lose turn
            return None
        return col

def main():
    board = create_board(ROWS, COLS)
    players = CHECKERS[:PLAYERS]
    current_player_index = random.randint(0, PLAYERS - 1)

    print_board(board)

    while True:
        checker = players[current_player_index]
        col = get_player_input(board, checker)
        if col is None:
            # Lost turn due to full column, just switch player
            current_player_index = (current_player_index + 1) % PLAYERS
            continue
        
        pos = place_checker(board, col, checker)
        if pos is None:
            # This should not happen here because we check before
            current_player_index = (current_player_index + 1) % PLAYERS
            continue
        
        r, c = pos
        print_board(board)
        
        if check_win(board, r, c, checker):
            print(f"Player {checker} won!")
            break
        
        if board_full(board):
            print("The game is a draw.")
            break

        current_player_index = (current_player_index + 1) % PLAYERS

if __name__ == "__main__":
    main()
