import os
import random

# Constants
ROWS = 6
COLS = 7
NUM_PLAYERS = 2
CHECKERS = ["X", "O", "V", "H", "M"]
WIN_LENGTH = 4

def clear_screen():
    os.system('clear')

def create_board(rows, cols):
    return [[" " for _ in range(cols)] for _ in range(rows)]

def print_board(board):
    clear_screen()
    # Print column headers
    headers = [chr(ord('A') + i) for i in range(len(board[0]))]
    print("  " + "   ".join(headers))
    # Print rows and separators
    separator = "+" + "---+" * len(board[0])
    for row in board:
        print(separator)
        print("| " + " | ".join(row) + " |")
    print(separator)

def is_valid_column(col_char, cols):
    if len(col_char) != 1:
        return False
    if not ('A' <= col_char <= chr(ord('A') + cols - 1)):
        return False
    return True

def get_column_index(col_char):
    return ord(col_char) - ord('A')

def is_column_full(board, col):
    return board[0][col] != " "

def place_checker(board, col, checker):
    for row in range(len(board) - 1, -1, -1):
        if board[row][col] == " ":
            board[row][col] = checker
            return row
    return None  # Full column

def check_direction(board, start_row, start_col, delta_row, delta_col, checker):
    count = 0
    row, col = start_row, start_col
    while 0 <= row < len(board) and 0 <= col < len(board[0]) and board[row][col] == checker:
        count += 1
        row += delta_row
        col += delta_col
    return count

def check_win(board, row, col, checker):
    directions = [
        ((0, 1), (0, -1)),    # Horizontal right and left
        ((1, 0), (-1, 0)),    # Vertical down and up
        ((1, 1), (-1, -1)),   # Diagonal down-right and up-left
        ((1, -1), (-1, 1))    # Diagonal down-left and up-right
    ]
    for dir1, dir2 in directions:
        count = 1  # Current piece
        count += check_direction(board, row + dir1[0], col + dir1[1], dir1[0], dir1[1], checker) 
        count += check_direction(board, row + dir2[0], col + dir2[1], dir2[0], dir2[1], checker)
        if count >= WIN_LENGTH:
            return True
    return False

def board_full(board):
    for c in range(len(board[0])):
        if not is_column_full(board, c):
            return False
    return True

def get_valid_input(player_checker, cols):
    while True:
        col_char = input(f"Player {player_checker}, please enter a column: ").strip().upper()
        if not is_valid_column(col_char, cols):
            print(f"Invalid input. Please enter a letter between A and {chr(ord('A') + cols -1)}.")
            continue
        col_idx = get_column_index(col_char)
        if is_column_full(board, col_idx):
            print("That column is full. Turn lost.")
            return None
        return col_idx

# Main game loop
board = create_board(ROWS, COLS)

# Choose starting player randomly
current_player_idx = random.randint(0, NUM_PLAYERS - 1)
players = CHECKERS[:NUM_PLAYERS]

print_board(board)

while True:
    player_checker = players[current_player_idx]
    col_idx = get_valid_input(player_checker, COLS)
    if col_idx is None:
        # Column full: lose turn, switch player
        current_player_idx = (current_player_idx + 1) % NUM_PLAYERS
        print_board(board)
        continue

    row_idx = place_checker(board, col_idx, player_checker)
    print_board(board)

    if check_win(board, row_idx, col_idx, player_checker):
        print(f"Player {player_checker} won!")
        break

    if board_full(board):
        print("It's a draw!")
        break

    current_player_idx = (current_player_idx + 1) % NUM_PLAYERS
