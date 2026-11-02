import os
import random

# Constants
ROWS = 6
COLS = 7
MAX_PLAYERS = 5
MIN_PLAYERS = 2
NUM_PLAYERS = 2  # set to 2 for submission
CHECKERS = ["X", "O", "V", "H", "M"]
WIN_LENGTH = 4
COLUMN_LABELS = [chr(ord('A') + i) for i in range(COLS)]

def clear_screen():
    os.system('clear')

def create_board():
    return [[" " for _ in range(COLS)] for _ in range(ROWS)]

def print_board(board):
    clear_screen()
    # Print column headers
    print(" ", end=" ")
    for label in COLUMN_LABELS:
        print(f" {label} ", end="")
    print()
    
    # Print board rows with horizontal lines
    for row in range(ROWS):
        print("+" + "---+" * COLS)
        print("|", end="")
        for col in range(COLS):
            print(f" {board[row][col]} |", end="")
        print()
    print("+" + "---+" * COLS)

def is_valid_column_input(user_input):
    if len(user_input) != 1:
        return False
    if user_input not in COLUMN_LABELS:
        return False
    return True

def column_full(board, col):
    # If top row in the column is occupied, column is full
    return board[0][col] != " "

def place_checker(board, col, checker):
    # Start from bottom row, place checker in the lowest empty position
    for row in range(ROWS-1, -1, -1):
        if board[row][col] == " ":
            board[row][col] = checker
            return row, col
    return None  # column full, cannot place

def check_direction(board, start_row, start_col, d_row, d_col, checker):
    count = 0
    row = start_row
    col = start_col
    while 0 <= row < ROWS and 0 <= col < COLS and board[row][col] == checker:
        count += 1
        row += d_row
        col += d_col
    return count

def check_win(board, row, col, checker):
    # Check horizontal
    left = check_direction(board, row, col, 0, -1, checker) - 1
    right = check_direction(board, row, col, 0, 1, checker)
    if left + right >= WIN_LENGTH:
        return True
    
    # Check vertical
    up = check_direction(board, row, col, -1, 0, checker) - 1
    down = check_direction(board, row, col, 1, 0, checker)
    if up + down >= WIN_LENGTH:
        return True
    
    # Check diagonal /
    up_left = check_direction(board, row, col, -1, -1, checker) - 1
    down_right = check_direction(board, row, col, 1, 1, checker)
    if up_left + down_right >= WIN_LENGTH:
        return True
    
    # Check diagonal \
    up_right = check_direction(board, row, col, -1, 1, checker) - 1
    down_left = check_direction(board, row, col, 1, -1, checker)
    if up_right + down_left >= WIN_LENGTH:
        return True
    
    return False

def board_full(board):
    for col in range(COLS):
        if board[0][col] == " ":
            return False
    return True

def get_player_input(current_player_checker):
    while True:
        user_input = input(f"Player {current_player_checker}, please enter a column: ").strip().upper()
        if not is_valid_column_input(user_input):
            # invalid input format - retry
            continue
        col_index = ord(user_input) - ord('A')
        if column_full(board, col_index):
            # column full, player loses turn as per spec
            return None
        return col_index

# Initialize game
board = create_board()
players = CHECKERS[:NUM_PLAYERS]
# Randomly select first player
current_player_index = random.randint(0, NUM_PLAYERS -1)

print_board(board)

game_over = False

while not game_over:
    checker = players[current_player_index]
    col = get_player_input(checker)
    if col is None:
        # Turn lost due to full column
        current_player_index = (current_player_index + 1) % NUM_PLAYERS
        continue
    pos = place_checker(board, col, checker)
    print_board(board)
    if pos is not None:
        row, col_placed = pos
        if check_win(board, row, col_placed, checker):
            print(f"Player {checker} won!")
            game_over = True
            break
        if board_full(board):
            print("Game is a draw!")
            game_over = True
            break
    current_player_index = (current_player_index + 1) % NUM_PLAYERS
