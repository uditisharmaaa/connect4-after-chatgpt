import os
import random

# Game configuration
ROWS = 6
COLUMNS = 7
COLUMN_LABELS = 'ABCDEFG'
PLAYERS = ['X', 'O', 'V', 'H', 'M']
NUM_PLAYERS = 3  # Set number of players between 2 to 5

# Initialize board
board = [[' ' for _ in range(COLUMNS)] for _ in range(ROWS)]

def print_board():
    os.system('clear')
    print(' '.join(COLUMN_LABELS))
    for row in board:
        print(' '.join(row))

def get_valid_input():
    while True:
        choice = input(f"Choose a column ({COLUMN_LABELS}), {current_player}: ").upper()
        if choice in COLUMN_LABELS:
            col_idx = COLUMN_LABELS.index(choice)
            if board[0][col_idx] == ' ':
                return col_idx
        print("Invalid input or full column. Try again.")

def place_piece(col, player):
    for row in reversed(board):
        if row[col] == ' ':
            row[col] = player
            break

def check_winner(player):
    # Check horizontal, vertical, and diagonal wins
    for row in range(ROWS):
        for col in range(COLUMNS):
            if (col <= COLUMNS - 4 and all(board[row][col+i] == player for i in range(4))) or \
               (row <= ROWS - 4 and all(board[row+i][col] == player for i in range(4))) or \
               (col <= COLUMNS - 4 and row <= ROWS - 4 and all(board[row+i][col+i] == player for i in range(4))) or \
               (col >= 3 and row <= ROWS - 4 and all(board[row+i][col-i] == player for i in range(4))):
                return True
    return False

def check_draw():
    return all(board[0][col] != ' ' for col in range(COLUMNS))

# Game loop
current_player = random.choice(PLAYERS[:NUM_PLAYERS])
while True:
    print_board()
    col_choice = get_valid_input()
    place_piece(col_choice, current_player)

    if check_winner(current_player):
        print_board()
        print(f"Player {current_player} wins!")
        break
    
    if check_draw():
        print_board()
        print("It's a draw!")
        break

    # Switch to next player
    current_player = PLAYERS[(PLAYERS.index(current_player) + 1) % NUM_PLAYERS]
