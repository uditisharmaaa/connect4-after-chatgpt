import os
import random

COLS = 7
ROWS = 6
PLAYERS = 2
CHECKERS = ["X", "O", "V", "H", "M"]
BOARD_EMPTY_CELL = " "

def init_board(rows, cols):
    return [[BOARD_EMPTY_CELL]*cols for _ in range(rows)]

def print_board(board):
    os.system('clear')
    header = '  '.join([chr(ord('A') + i) for i in range(len(board[0]))])
    print(f"  {header} ")
    for row in board:
        print("+---" * len(row) + "+")
        print("| " + " | ".join(row) + " |")
    print("+---" * len(board[0]) + "+")

def input_column():
    while True:
        col = input(f"Player {CHECKERS[current_player]}, please enter a column: ").upper()
        if len(col) == 1 and 'A' <= col <= 'G' and col_to_index(col) in range(COLS):
            return col_to_index(col)
        print("Invalid input, please try again.")

def col_to_index(col):
    return ord(col) - ord('A')

def is_valid_placement(board, col):
    return board[0][col] == BOARD_EMPTY_CELL

def place_checker(board, col, player):
    for row in reversed(board):
        if row[col] == BOARD_EMPTY_CELL:
            row[col] = CHECKERS[player]
            break

def check_winner(board, player):
    checker = CHECKERS[player]
    for row in range(ROWS):
        for col in range(COLS):
            if board[row][col] == checker:
                if all(board[row][c] == checker for c in range(col, min(col+4, COLS))):
                    return True
                if all(board[r][col] == checker for r in range(row, min(row+4, ROWS))):
                    return True
                if all(r < ROWS and c < COLS and board[r][c] == checker for r, c in zip(range(row, row+4), range(col, col+4))):
                    return True
                if all(r < ROWS and c >= 0 and board[r][c] == checker for r, c in zip(range(row, row+4), range(col, col-4, -1))):
                    return True
    return False

def check_draw(board):
    return all(board[0][col] != BOARD_EMPTY_CELL for col in range(COLS))

board = init_board(ROWS, COLS)
current_player = random.choice(range(PLAYERS))
print_board(board)

while True:
    col = input_column()
    if is_valid_placement(board, col):
        place_checker(board, col, current_player)
        print_board(board)
        if check_winner(board, current_player):
            print(f"Player {CHECKERS[current_player]} won!")
            break
        if check_draw(board):
            print("It's a draw!")
            break
        current_player = (current_player + 1) % PLAYERS
