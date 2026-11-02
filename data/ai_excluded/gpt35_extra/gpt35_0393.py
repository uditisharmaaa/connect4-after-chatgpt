import os
import random

# Constants
ROWS = 6
COLUMNS = 7
PLAYERS = 2
CHECKERS = ["X", "O", "V", "H", "M"]

def clear_screen():
    os.system('clear')

def create_board():
    board = []
    for _ in range(ROWS):
        row = [" " for _ in range(COLUMNS)]
        board.append(row)
    return board

def print_board(board):
    clear_screen()
    # Print column headers
    headers = "  "
    for i in range(COLUMNS):
        headers += "  " + chr(ord('A') + i) + " "
    print(headers)
    # Print board rows with separators
    for row in board:
        print("+---" * COLUMNS + "+")
        row_line = "|"
        for cell in row:
            row_line += " " + cell + " |"
        print(row_line)
    print("+---" * COLUMNS + "+")

def is_valid_column(column_char):
    if len(column_char) != 1:
        return False
    col = ord(column_char) - ord('A')
    if 0 <= col < COLUMNS:
        return True
    else:
        return False

def get_next_open_row(board, col):
    # Return the lowest empty row index for the given column or -1 if full
    for r in range(ROWS - 1, -1, -1):
        if board[r][col] == " ":
            return r
    return -1

def insert_checker(board, col, checker):
    row = get_next_open_row(board, col)
    if row != -1:
        board[row][col] = checker
        return True
    else:
        return False  # column full

def check_win(board, checker):
    # Check horizontal
    for r in range(ROWS):
        for c in range(COLUMNS - 3):
            if board[r][c] == checker and board[r][c+1] == checker and board[r][c+2] == checker and board[r][c+3] == checker:
                return True
    # Check vertical
    for c in range(COLUMNS):
        for r in range(ROWS - 3):
            if board[r][c] == checker and board[r+1][c] == checker and board[r+2][c] == checker and board[r+3][c] == checker:
                return True
    # Check positively sloped diagonal
    for r in range(ROWS - 3):
        for c in range(COLUMNS - 3):
            if board[r][c] == checker and board[r+1][c+1] == checker and board[r+2][c+2] == checker and board[r+3][c+3] == checker:
                return True
    # Check negatively sloped diagonal
    for r in range(3, ROWS):
        for c in range(COLUMNS - 3):
            if board[r][c] == checker and board[r-1][c+1] == checker and board[r-2][c+2] == checker and board[r-3][c+3] == checker:
                return True
    return False

def is_draw(board):
    for r in range(ROWS):
        for c in range(COLUMNS):
            if board[r][c] == " ":
                return False
    return True

def get_player_input(current_player, checker):
    while True:
        user_input = input(f"Player {checker}, please enter a column: ").strip().upper()
        if not is_valid_column(user_input):
            continue
        col = ord(user_input) - ord('A')
        # Check if column full
        if get_next_open_row(board, col) == -1:
            # turn is lost
            return -1
        return col

board = create_board()

current_player_index = random.randint(0, PLAYERS -1)
current_checker = CHECKERS[current_player_index]

print_board(board)

while True:
    col = get_player_input(current_player_index, current_checker)
    if col == -1:
        # column full, player loses turn
        current_player_index = (current_player_index + 1) % PLAYERS
        current_checker = CHECKERS[current_player_index]
        continue
    inserted = insert_checker(board, col, current_checker)
    print_board(board)
    if check_win(board, current_checker):
        print(f"Player {current_checker} won!")
        break
    if is_draw(board):
        print("Game is a draw!")
        break
    current_player_index = (current_player_index + 1) % PLAYERS
    current_checker = CHECKERS[current_player_index]
