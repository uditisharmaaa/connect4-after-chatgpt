import random
import os

# Constants
ROWS = 6
COLUMNS = 7
PLAYER_COUNT = 4    # Change this number to have between 2-5 players.
PLAYERS = ['X', 'O', 'V', 'H', 'M'][:PLAYER_COUNT]
COLUMN_LABELS = 'ABCDEFG'

# Initialize the board
board = [[' ' for _ in range(COLUMNS)] for _ in range(ROWS)]

def print_board():
    os.system('clear')
    print(' '.join(COLUMN_LABELS))
    for row in board:
        print('|'.join(row))
    print('-' * (COLUMNS * 2 - 1))

def get_column_input():
    while True:
        choice = input(f"Player {PLAYERS[current_player]}, choose a column (A-G): ").upper()
        if choice in COLUMN_LABELS:
            col = COLUMN_LABELS.index(choice)
            if board[0][col] == ' ':
                return col
        print("Invalid input. Please try again.")

def make_move(col, player):
    for row in reversed(board):
        if row[col] == ' ':
            row[col] = player
            break

def check_winner():
    # Check horizontal, vertical, and diagonal wins
    directions = [(0, 1), (1, 0), (1, 1), (1, -1)]
    for row in range(ROWS):
        for col in range(COLUMNS):
            if board[row][col] != ' ':
                for dr, dc in directions:
                    if all((0 <= row + dr*i < ROWS and 0 <= col + dc*i < COLUMNS and 
                            board[row + dr*i][col + dc*i] == board[row][col]) for i in range(4)):
                        return True
    return False

def check_draw():
    return all(board[0][col] != ' ' for col in range(COLUMNS))

# Main game loop
current_player = random.randint(0, PLAYER_COUNT - 1)

while True:
    print_board()
    column = get_column_input()
    make_move(column, PLAYERS[current_player])

    if check_winner():
        print_board()
        print(f"Player {PLAYERS[current_player]} wins!")
        break

    if check_draw():
        print_board()
        print("It's a draw!")
        break

    current_player = (current_player + 1) % PLAYER_COUNT
