import os
import random

# Constants
ROWS = 6
COLS = 7
NUM_PLAYERS = 2
PLAYER_SYMBOLS = ["X", "O", "V", "H", "M"]

def initialize_board():
    return [[" " for _ in range(COLS)] for _ in range(ROWS)]

def clear_screen():
    os.system('clear')

def print_board(board):
    # Print column headers
    header = "  " + "   ".join([chr(65 + i) for i in range(COLS)]) + "  "
    print(header)
    
    # Print top border
    top_border = "+" + ("---+" * COLS)
    print(top_border)
    
    # Print each row
    for row in board:
        row_str = "| " + " | ".join(row) + " |"
        print(row_str)
        print(top_border)

def get_valid_column(board):
    while True:
        column = input(f"Player {current_player}, please enter a column: ").upper()
        if len(column) != 1 or not column.isalpha():
            print("Invalid input. Please enter a single letter (A-{}).".format(chr(65 + COLS - 1)))
            continue
        col_index = ord(column) - ord('A')
        if col_index < 0 or col_index >= COLS:
            print("Column out of range. Please enter a letter between A and {}.".format(chr(65 + COLS - 1)))
            continue
        if board[0][col_index] != " ":
            print("Column is full. Please choose another column.")
            continue
        return col_index

def place_checker(board, col, symbol):
    for row in range(ROWS - 1, -1, -1):
        if board[row][col] == " ":
            board[row][col] = symbol
            return row
    return -1

def check_win(board, row, col, symbol):
    # Check horizontal
    count = 1
    left = col - 1
    while left >= 0 and board[row][left] == symbol:
        count += 1
        left -= 1
    right = col + 1
    while right < COLS and board[row][right] == symbol:
        count += 1
        right += 1
    if count >= 4:
        return True

    # Check vertical
    count = 1
    up = row - 1
    while up >= 0 and board[up][col] == symbol:
        count += 1
        up -= 1
    down = row + 1
    while down < ROWS and board[down][col] == symbol:
        count += 1
        down += 1
    if count >= 4:
        return True

    # Check diagonal (top-left to bottom-right)
    count = 1
    up_left_row, up_left_col = row - 1, col - 1
    while up_left_row >= 0 and up_left_col >= 0 and board[up_left_row][up_left_col] == symbol:
        count += 1
        up_left_row -= 1
        up_left_col -= 1
    down_right_row, down_right_col = row + 1, col + 1
    while down_right_row < ROWS and down_right_col < COLS and board[down_right_row][down_right_col] == symbol:
        count += 1
        down_right_row += 1
        down_right_col += 1
    if count >= 4:
        return True

    # Check diagonal (top-right to bottom-left)
    count = 1
    up_right_row, up_right_col = row - 1, col + 1
    while up_right_row >= 0 and up_right_col < COLS and board[up_right_row][up_right_col] == symbol:
        count += 1
        up_right_row -= 1
        up_right_col += 1
    down_left_row, down_left_col = row + 1, col - 1
    while down_left_row < ROWS and down_left_col >= 0 and board[down_left_row][down_left_col] == symbol:
        count += 1
        down_left_row += 1
        down_left_col -= 1
    if count >= 4:
        return True

    return False

def is_draw(board):
    return all(cell != " " for row in board for cell in row)

# Initialize the game
board = initialize_board()
players = PLAYER_SYMBOLS[:NUM_PLAYERS]
current_player = random.choice(players)
clear_screen()
print_board(board)

# Game loop
while True:
    col = get_valid_column(board)
    row = place_checker(board, col, current_player)
    clear_screen()
    print_board(board)
    
    if check_win(board, row, col, current_player):
        print(f"Player {current_player} won!")
        break
    
    if is_draw(board):
        print("The game is a draw!")
        break
    
    # Switch to next player
    current_player = players[(players.index(current_player) + 1) % NUM_PLAYERS]
