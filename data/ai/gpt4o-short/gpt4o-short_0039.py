import random
import os
import sys

# Constants
PLAYER_SYMBOLS = ['X', 'O', 'V', 'H', 'M']
NUM_PLAYERS = 3  # Adjust the number of players (2 to 5)
ROWS = 6
COLS = 7
COL_LABELS = ['A', 'B', 'C', 'D', 'E', 'F', 'G']

def create_board():
    return [[' ' for _ in range(COLS)] for _ in range(ROWS)]

def print_board(board):
    os.system('clear')
    print('  ' + ' '.join(COL_LABELS))
    print(' +' + '-' * (COLS * 2 - 1) + '+')
    for row in board:
        print(' |' + '|'.join(row) + '|')
    print(' +' + '-' * (COLS * 2 - 1) + '+')

def get_valid_input(board):
    while True:
        choice = input("Choose a column: ").strip().upper()
        if choice in COL_LABELS:
            col = COL_LABELS.index(choice)
            if board[0][col] == ' ':  # Check if column is not full
                return col
            else:
                print("Column is full. Try another one.")
        else:
            print("Invalid input. Choose A-G.")

def drop_piece(board, col, symbol):
    for row in reversed(board):
        if row[col] == ' ':
            row[col] = symbol
            return

def check_win(board, symbol):
    # Check horizontal
    for row in range(ROWS):
        for col in range(COLS - 3):
            if board[row][col] == symbol and all(board[row][col + i] == symbol for i in range(4)):
                return True

    # Check vertical
    for col in range(COLS):
        for row in range(ROWS - 3):
            if board[row][col] == symbol and all(board[row + i][col] == symbol for i in range(4)):
                return True

    # Check diagonal \
    for row in range(ROWS - 3):
        for col in range(COLS - 3):
            if board[row][col] == symbol and all(board[row + i][col + i] == symbol for i in range(4)):
                return True

    # Check diagonal /
    for row in range(3, ROWS):
        for col in range(COLS - 3):
            if board[row][col] == symbol and all(board[row - i][col + i] == symbol for i in range(4)):
                return True

    return False

def check_draw(board):
    return all(cell != ' ' for row in board for cell in row)

def connect4_game():
    board = create_board()
    players = PLAYER_SYMBOLS[:NUM_PLAYERS]
    player_index = random.randint(0, NUM_PLAYERS - 1)

    while True:
        current_player = players[player_index]
        print_board(board)
        print(f"Player {current_player}'s turn.")
        
        col = get_valid_input(board)
        drop_piece(board, col, current_player)

        if check_win(board, current_player):
            print_board(board)
            print(f"Player {current_player} wins!")
            break
        if check_draw(board):
            print_board(board)
            print("It's a draw!")
            break
        
        player_index = (player_index + 1) % NUM_PLAYERS

if __name__ == "__main__":
    connect4_game()
