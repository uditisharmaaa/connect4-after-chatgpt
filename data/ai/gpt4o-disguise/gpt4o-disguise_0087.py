import os
import random

ROWS = 6
COLS = 7
PLAYERS = 2
CHECKERS = ['X', 'O', 'V', 'H', 'M']

board = [[' ' for _ in range(COLS)] for _ in range(ROWS)]

def print_board():
    os.system('clear')
    print("  " + "   ".join(chr(65 + i) for i in range(COLS)))
    for row in board:
        print("+---" * COLS + "+")
        print("| " + " | ".join(row) + " |")
    print("+---" * COLS + "+")

def get_col_input():
    while True:
        move = input(f"Player {CHECKERS[current_player]}, please enter a column: ").upper()
        if len(move) == 1 and 'A' <= move <= 'A' + COLS and board[0][ord(move) - 65] == ' ':
            return ord(move) - 65
        print("Invalid input. Try again.")

def make_move(col):
    for row in reversed(board):
        if row[col] == ' ':
            row[col] = CHECKERS[current_player]
            break

def check_win():
    b = ''.join(''.join(board[i][j] for i in range(ROWS)) for j in range(COLS))  # Vertical
    b += ''.join(''.join(board[i]) for i in range(ROWS))  # Horizontal
    b += ''.join(board[i + d][j + d] for j in range(COLS - 4 + 1) for i in range(ROWS - 4 + 1) for d in range(4))  # Diagonal \
    b += ''.join(board[i - d][j + d] for j in range(COLS - 4 + 1) for i in range(3, ROWS) for d in range(4))  # Diagonal /
    win_str = CHECKERS[current_player] * 4
    return win_str in b

def check_draw():
    return all(board[0][col] != ' ' for col in range(COLS))

current_player = random.randint(0, PLAYERS - 1)
print_board()

while True:
    col = get_col_input()
    make_move(col)
    print_board()
    
    if check_win():
        print(f"Player {CHECKERS[current_player]} won!")
        break
    if check_draw():
        print("The game is a draw!")
        break
    
    current_player = (current_player + 1) % PLAYERS
