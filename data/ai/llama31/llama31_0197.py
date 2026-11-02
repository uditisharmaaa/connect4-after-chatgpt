import os
import random
import string

# Constants
ROWS = 6
COLS = 7
PLAYERS = 2

# Checkers for each player
CHECKERS = ['X', 'O', 'V', 'H', 'M']

# Create the game board
def create_board():
    board = [[' ' for _ in range(COLS)] for _ in range(ROWS)]
    return board

# Print the game board
def print_board(board):
    os.system('clear')
    print('  ' + ' '.join(string.ascii_uppercase[:COLS]))
    for row in board:
        print('+---' * COLS + '+')
        print('| ' + ' | '.join(row) + ' |')
    print('+---' * COLS + '+')

# Get the player's move
def get_move(player):
    while True:
        move = input(f"Player {CHECKERS[player]}, please enter a column: ").strip().upper()
        if move in string.ascii_uppercase[:COLS] and board[0][string.ascii_uppercase.index(move)] == ' ':
            return string.ascii_uppercase.index(move)
        print("Invalid move, please try again.")

# Check if a player has won
def check_win(board, player):
    checker = CHECKERS[player]
    # Check horizontal
    for row in board:
        for i in range(COLS - 3):
            if row[i] == checker and row[i + 1] == checker and row[i + 2] == checker and row[i + 3] == checker:
                return True
    # Check vertical
    for col in range(COLS):
        for i in range(ROWS - 3):
            if board[i][col] == checker and board[i + 1][col] == checker and board[i + 2][col] == checker and board[i + 3][col] == checker:
                return True
    # Check diagonal (top-left to bottom-right)
    for row in range(ROWS - 3):
        for col in range(COLS - 3):
            if board[row][col] == checker and board[row + 1][col + 1] == checker and board[row + 2][col + 2] == checker and board[row + 3][col + 3] == checker:
                return True
    # Check diagonal (bottom-left to top-right)
    for row in range(3, ROWS):
        for col in range(COLS - 3):
            if board[row][col] == checker and board[row - 1][col + 1] == checker and board[row - 2][col + 2] == checker and board[row - 3][col + 3] == checker:
                return True
    return False

# Check if the game is a draw
def check_draw(board):
    for row in board:
        for cell in row:
            if cell == ' ':
                return False
    return True

# Main game loop
board = create_board()
current_player = random.randint(0, PLAYERS - 1)
while True:
    print_board(board)
    move = get_move(current_player)
    for row in range(ROWS - 1, -1, -1):
        if board[row][move] == ' ':
            board[row][move] = CHECKERS[current_player]
            break
    if check_win(board, current_player):
        print_board(board)
        print(f"Player {CHECKERS[current_player]} won!")
        break
    elif check_draw(board):
        print_board(board)
        print("It's a draw!")
        break
    current_player = (current_player + 1) % PLAYERS
