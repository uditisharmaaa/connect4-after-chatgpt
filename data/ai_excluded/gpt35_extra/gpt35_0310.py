import os
import random

# Constants
ROWS = 6
COLS = 7
PLAYERS = 2
CHECKERS = ["X", "O", "V", "H", "M"]
EMPTY = " "
WIN_LENGTH = 4

def clear_screen():
    os.system('clear')

def create_board():
    board = []
    for _ in range(ROWS):
        row = [EMPTY] * COLS
        board.append(row)
    return board

def print_board(board):
    clear_screen()
    # Print column labels
    labels = "  "
    for i in range(COLS):
        labels += "  " + chr(ord('A') + i) + " "
    print(labels)
    # Print board rows
    for row in board:
        print("+---" * COLS + "+")
        line = ""
        for cell in row:
            line += "| " + cell + " "
        line += "|"
        print(line)
    print("+---" * COLS + "+")

def is_valid_column(ch):
    if len(ch) != 1:
        return False
    col = ord(ch) - ord('A')
    if col < 0 or col >= COLS:
        return False
    return True

def get_column_index(ch):
    return ord(ch) - ord('A')

def is_column_full(board, col):
    return board[0][col] != EMPTY

def place_checker(board, col, checker):
    # place checker in the lowest available position in column col
    for row in range(ROWS - 1, -1, -1):
        if board[row][col] == EMPTY:
            board[row][col] = checker
            return row, col
    # Column full, return None (should not happen if checked before)
    return None, None

def check_line(board, start_row, start_col, delta_row, delta_col, checker):
    count = 0
    row, col = start_row, start_col
    while 0 <= row < ROWS and 0 <= col < COLS:
        if board[row][col] == checker:
            count += 1
            if count == WIN_LENGTH:
                return True
        else:
            count = 0
        row += delta_row
        col += delta_col
    return False

def check_win(board, checker):
    # Check horizontal lines
    for row in range(ROWS):
        if check_line(board, row, 0, 0, 1, checker):
            return True
    # Check vertical lines
    for col in range(COLS):
        if check_line(board, 0, col, 1, 0, checker):
            return True
    # Check diagonals (/ direction)
    for row in range(ROWS - WIN_LENGTH + 1):
        for col in range(COLS - WIN_LENGTH + 1):
            count = 0
            for i in range(WIN_LENGTH):
                if board[row + i][col + i] == checker:
                    count += 1
                else:
                    break
            if count == WIN_LENGTH:
                return True
    # Check diagonals (\ direction)
    for row in range(WIN_LENGTH - 1, ROWS):
        for col in range(COLS - WIN_LENGTH + 1):
            count = 0
            for i in range(WIN_LENGTH):
                if board[row - i][col + i] == checker:
                    count += 1
                else:
                    break
            if count == WIN_LENGTH:
                return True
    return False

def check_draw(board):
    for col in range(COLS):
        if not is_column_full(board, col):
            return False
    return True

def get_player_input(player_checker):
    while True:
        inp = input(f"Player {player_checker}, please enter a column: ").strip().upper()
        if not is_valid_column(inp):
            print("Invalid input. Please enter a valid column letter.")
            continue
        col = get_column_index(inp)
        if is_column_full(board, col):
            # player loses turn if column full
            print(f"Column {inp} is full. You lose your turn.")
            return None
        return col

# --- Main Program ---
board = create_board()
players = CHECKERS[:PLAYERS]

current_player_idx = random.randint(0, PLAYERS - 1)

print_board(board)

while True:
    player_checker = players[current_player_idx]
    col = get_player_input(player_checker)
    if col is not None:
        place_checker(board, col, player_checker)
        print_board(board)
        if check_win(board, player_checker):
            print(f"Player {player_checker} won!")
            break
        if check_draw(board):
            print("Game is a draw!")
            break
    else:
        # Player lost turn (column full)
        print_board(board)
    current_player_idx = (current_player_idx + 1) % PLAYERS
