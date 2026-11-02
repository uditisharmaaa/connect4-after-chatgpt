import os
import random

# Constants
ROWS = 6
COLUMNS = 7
NUM_PLAYERS = 2
WIN_COUNT = 4
CHECKERS = ["X", "O", "V", "H", "M"]
COLUMN_LETTERS = [chr(ord('A') + i) for i in range(COLUMNS)]

def clear_screen():
    os.system('clear')

def create_board():
    board = [[" " for _ in range(COLUMNS)] for _ in range(ROWS)]
    return board

def print_board(board):
    clear_screen()
    # Print column headers
    print("  " + "   ".join(COLUMN_LETTERS))
    # Print rows with borders
    for row in range(ROWS):
        print("+" + "---+" * COLUMNS)
        row_str = "|"
        for col in range(COLUMNS):
            row_str += " {} |".format(board[row][col])
        print(row_str)
    print("+" + "---+" * COLUMNS)

def is_valid_column(col_letter):
    return col_letter in COLUMN_LETTERS

def column_index(col_letter):
    return ord(col_letter) - ord('A')

def is_column_full(board, col):
    return board[0][col] != " "

def place_checker(board, col, checker):
    # Place checker in the lowest empty spot in the column
    for row in range(ROWS-1, -1, -1):
        if board[row][col] == " ":
            board[row][col] = checker
            return row, col
    return None

def check_win(board, checker, row, col):
    # Directions: horizontal, vertical, diagonal up-right, diagonal down-right
    directions = [
        (0, 1),   # horizontal right
        (1, 0),   # vertical down
        (1, 1),   # diagonal down-right
        (1, -1),  # diagonal down-left
    ]
    for dr, dc in directions:
        count = 1
        # Check one direction
        r, c = row + dr, col + dc
        while 0 <= r < ROWS and 0 <= c < COLUMNS and board[r][c] == checker:
            count += 1
            r += dr
            c += dc
        # Check opposite direction
        r, c = row - dr, col - dc
        while 0 <= r < ROWS and 0 <= c < COLUMNS and board[r][c] == checker:
            count += 1
            r -= dr
            c -= dc
        if count >= WIN_COUNT:
            return True
    return False

def is_draw(board):
    for col in range(COLUMNS):
        if board[0][col] == " ":
            return False
    return True

def get_player_input(current_checker):
    while True:
        col_letter = input(f"Player {current_checker}, please enter a column: ").strip().upper()
        if not col_letter:
            continue
        if not is_valid_column(col_letter):
            continue
        col = column_index(col_letter)
        if is_column_full(board, col):
            # Player loses this turn if column is full
            return None
        return col

# Main Game Loop
board = create_board()
players = CHECKERS[:NUM_PLAYERS]

current_player_index = random.randint(0, NUM_PLAYERS - 1)
current_checker = players[current_player_index]

print_board(board)

while True:
    col = get_player_input(current_checker)
    if col is None:
        # Column full, player loses turn
        current_player_index = (current_player_index + 1) % NUM_PLAYERS
        current_checker = players[current_player_index]
        print_board(board)
        continue

    placed = place_checker(board, col, current_checker)
    print_board(board)

    if placed is not None:
        row, placed_col = placed
        if check_win(board, current_checker, row, placed_col):
            print(f"Player {current_checker} won!")
            break
        if is_draw(board):
            print("The game is a draw!")
            break
        # Next player's turn
        current_player_index = (current_player_index + 1) % NUM_PLAYERS
        current_checker = players[current_player_index]
