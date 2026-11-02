import os
import random

# Constants for players
PLAYERS = ['X', 'O', 'V', 'H', 'M']
NUM_PLAYERS = 2  # Change this from 2 to 5 as needed

ROWS = 6
COLS = 7
COLUMN_LABELS = ['A', 'B', 'C', 'D', 'E', 'F', 'G']

def create_board():
    return [[' ' for _ in range(COLS)] for _ in range(ROWS)]

def print_board(board):
    os.system('clear')
    print(' ' + ' '.join(COLUMN_LABELS))
    for row in board:
        print('|' + '|'.join(row) + '|')
    print('-' * (COLS * 2 + 1))

def is_valid_move(board, col):
    return board[0][col] == ' '

def make_move(board, col, player):
    for row in reversed(board):
        if row[col] == ' ':
            row[col] = player
            break

def check_win(board, player):
    # Check horizontal, vertical, and diagonal (both directions) for win
    for row in range(ROWS):
        for col in range(COLS - 3):
            if all(board[row][col + i] == player for i in range(4)):
                return True

    for col in range(COLS):
        for row in range(ROWS - 3):
            if all(board[row + i][col] == player for i in range(4)):
                return True
    
    for row in range(ROWS - 3):
        for col in range(COLS - 3):
            if all(board[row + i][col + i] == player for i in range(4)):
                return True
            if all(board[row + 3 - i][col + i] == player for i in range(4)):
                return True

    return False

def check_draw(board):
    return all(board[0][col] != ' ' for col in range(COLS))

def play_game():
    board = create_board()
    current_player_index = random.randint(0, NUM_PLAYERS - 1)
    
    while True:
        print_board(board)
        current_player = PLAYERS[current_player_index]

        while True:
            move = input(f"Player {current_player}'s turn (A-G): ").strip().upper()
            if move in COLUMN_LABELS and is_valid_move(board, COLUMN_LABELS.index(move)):
                break
            print("Invalid move. Try again.")

        make_move(board, COLUMN_LABELS.index(move), current_player)

        if check_win(board, current_player):
            print_board(board)
            print(f"Player {current_player} wins!")
            break

        if check_draw(board):
            print_board(board)
            print("It's a draw!")
            break

        current_player_index = (current_player_index + 1) % NUM_PLAYERS

print("Welcome to Connect 4!")
play_game()
