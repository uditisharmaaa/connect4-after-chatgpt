import random
import os

# Constants
ROWS = 6
COLS = 7
PLAYERS = 2
CHECKERS = ['X', 'O', 'V', 'H', 'M'][:PLAYERS]
COLUMN_NAMES = [chr(i) for i in range(ord('A'), ord('A') + COLS)]

def create_board():
    return [[' ' for _ in range(COLS)] for _ in range(ROWS)]

def print_board(board):
    os.system('clear')
    print("  " + "   ".join(COLUMN_NAMES))
    for row in board:
        print("+---" * COLS + "+")
        print("| " + " | ".join(row) + " |")
    print("+---" * COLS + "+")

def get_valid_input():
    while True:
        col = input(f"Player {CHECKERS[current_player]}, please enter a column: ").strip().upper()
        if col in COLUMN_NAMES:
            col_index = COLUMN_NAMES.index(col)
            if board[0][col_index] == ' ':
                return col_index
            else:
                print("Column full. Turn lost.")
                return None
        else:
            print("Invalid input. Try again.")

def place_checker(board, col_index, checker):
    for row in reversed(board):
        if row[col_index] == ' ':
            row[col_index] = checker
            break

def check_winner(board, checker):
    # Horizontal
    for row in board:
        for i in range(COLS - 3):
            if row[i] == checker and row[i + 1] == checker and row[i + 2] == checker and row[i + 3] == checker:
                return True
    # Vertical
    for col in range(COLS):
        for row in range(ROWS - 3):
            if board[row][col] == checker and board[row + 1][col] == checker and board[row + 2][col] == checker and board[row + 3][col] == checker:
                return True
    
    # Diagonal \
    for row in range(ROWS - 3):
        for col in range(COLS - 3):
            if board[row][col] == checker and board[row + 1][col + 1] == checker and board[row + 2][col + 2] == checker and board[row + 3][col + 3] == checker:
                return True

    # Diagonal /
    for row in range(3, ROWS):
        for col in range(COLS - 3):
            if board[row][col] == checker and board[row - 1][col + 1] == checker and board[row - 2][col + 2] == checker and board[row - 3][col + 3] == checker:
                return True

    return False

def check_draw(board):
    for row in board:
        if ' ' in row:
            return False
    return True

board = create_board()
current_player = random.randint(0, PLAYERS - 1)
print_board(board)

while True:
    col_index = get_valid_input()
    if col_index is None:
        current_player = (current_player + 1) % PLAYERS
        continue
    
    place_checker(board, col_index, CHECKERS[current_player])
    print_board(board)
    
    if check_winner(board, CHECKERS[current_player]):
        print(f"Player {CHECKERS[current_player]} won!")
        break
    
    if check_draw(board):
        print("The game is a draw!")
        break
    
    current_player = (current_player + 1) % PLAYERS
