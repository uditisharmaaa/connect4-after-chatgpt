import os
import random

# Constants for the game
ROWS = 6
COLUMNS = 7
NUM_PLAYERS = 2
CHECKERS = ["X", "O", "V", "H", "M"]
WIN_COUNT = 4
COLUMN_LABELS = [chr(ord('A') + i) for i in range(COLUMNS)]


def clear_screen():
    os.system('clear')


def create_board():
    return [[" " for _ in range(COLUMNS)] for _ in range(ROWS)]


def print_board(board):
    clear_screen()
    # Print column labels
    print("  " + "   ".join(COLUMN_LABELS))
    # Print top border
    print("+" + "---+" * COLUMNS)
    # Print rows
    for row in board:
        print("| " + " | ".join(row) + " |")
        print("+" + "---+" * COLUMNS)


def is_valid_column(col):
    # Check if input char is a valid column label
    return col in COLUMN_LABELS


def get_column_index(col):
    return COLUMN_LABELS.index(col)


def column_full(board, col_idx):
    # If top row in a column is occupied, column is full
    return board[0][col_idx] != " "


def place_checker(board, col_idx, checker):
    # Place checker "falling" down the column to lowest empty row
    for row_idx in range(ROWS - 1, -1, -1):
        if board[row_idx][col_idx] == " ":
            board[row_idx][col_idx] = checker
            return row_idx, col_idx
    # If no empty space, return None
    return None


def check_line(board, start_row, start_col, delta_row, delta_col, checker):
    count = 0
    row, col = start_row, start_col
    while 0 <= row < ROWS and 0 <= col < COLUMNS:
        if board[row][col] == checker:
            count += 1
            if count == WIN_COUNT:
                return True
        else:
            count = 0
        row += delta_row
        col += delta_col
    return False


def check_win(board, checker):
    # Horizontal
    for row in range(ROWS):
        if check_line(board, row, 0, 0, 1, checker):
            return True
    # Vertical
    for col in range(COLUMNS):
        if check_line(board, 0, col, 1, 0, checker):
            return True
    # Diagonal /
    for row in range(ROWS - WIN_COUNT + 1):
        for col in range(WIN_COUNT - 1, COLUMNS):
            count = 0
            for i in range(WIN_COUNT):
                if board[row + i][col - i] == checker:
                    count += 1
                else:
                    break
            if count == WIN_COUNT:
                return True
    # Diagonal \
    for row in range(ROWS - WIN_COUNT + 1):
        for col in range(COLUMNS - WIN_COUNT + 1):
            count = 0
            for i in range(WIN_COUNT):
                if board[row + i][col + i] == checker:
                    count += 1
                else:
                    break
            if count == WIN_COUNT:
                return True
    return False


def check_draw(board):
    # If any cell in top row is empty, still possible to play
    for col in range(COLUMNS):
        if board[0][col] == " ":
            return False
    return True


def get_valid_input(player):
    while True:
        col = input(f"Player {player}, please enter a column: ").strip().upper()
        if len(col) != 1:
            # Invalid length
            continue
        if not is_valid_column(col):
            # Not a valid column letter
            continue
        col_idx = get_column_index(col)
        if column_full(board, col_idx):
            # Column full, player loses turn (returns None)
            return None
        return col_idx


# Main program start
board = create_board()
players = CHECKERS[:NUM_PLAYERS]
current_player_index = random.randint(0, NUM_PLAYERS - 1)

print_board(board)

while True:
    player_checker = players[current_player_index]
    col_idx = get_valid_input(player_checker)

    if col_idx is None:
        # Column full, lose turn
        current_player_index = (current_player_index + 1) % NUM_PLAYERS
        continue

    pos = place_checker(board, col_idx, player_checker)
    print_board(board)

    if check_win(board, player_checker):
        print(f"Player {player_checker} won!")
        break
    if check_draw(board):
        print("The game is a draw!")
        break

    current_player_index = (current_player_index + 1) % NUM_PLAYERS
