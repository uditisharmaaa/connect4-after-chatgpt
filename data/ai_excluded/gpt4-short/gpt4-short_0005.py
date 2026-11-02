import os
import random

# Constants
ROWS, COLS = 6, 7
PLAYERS = ['X', 'O', 'V', 'H', 'M']
NUM_PLAYERS = 3  # Change this to 2-5 players

def create_board():
    return [[' ' for _ in range(COLS)] for _ in range(ROWS)]

def print_board(board):
    os.system('clear')
    print(" A B C D E F G")
    for row in board:
        print('|' + '|'.join(row) + '|')

def get_column_index(col_label):
    return ord(col_label.upper()) - ord('A')

def get_valid_column():
    while True:
        col = input("Select a column (A-G): ").strip().upper()
        if col in 'ABCDEFG' and board[0][get_column_index(col)] == ' ':
            return get_column_index(col)
        print("Invalid column. Try again.")

def drop_piece(board, col, player):
    for row in reversed(board):
        if row[col] == ' ':
            row[col] = player
            return

def is_winner(board, player):
    for r in range(ROWS):
        for c in range(COLS):
            if c + 3 < COLS and all(board[r][c + i] == player for i in range(4)): return True  # Horizontal
            if r + 3 < ROWS and all(board[r + i][c] == player for i in range(4)): return True  # Vertical
            if r + 3 < ROWS and c + 3 < COLS and all(board[r + i][c + i] == player for i in range(4)): return True  # Diagonal /
            if r + 3 < ROWS and c - 3 >= 0 and all(board[r + i][c - i] == player for i in range(4)): return True  # Diagonal \
    return False

def is_draw(board):
    return all(col != ' ' for col in board[0])

# Game Setup
board = create_board()
current_player = random.choice(PLAYERS[:NUM_PLAYERS])

# Main Game Loop
while True:
    print_board(board)
    print(f"Player {current_player}'s turn")
    col = get_valid_column()
    drop_piece(board, col, current_player)

    if is_winner(board, current_player):
        print_board(board)
        print(f"Player {current_player} wins!")
        break
    if is_draw(board):
        print_board(board)
        print("It's a draw!")
        break

    current_player = PLAYERS[(PLAYERS.index(current_player) + 1) % NUM_PLAYERS]
