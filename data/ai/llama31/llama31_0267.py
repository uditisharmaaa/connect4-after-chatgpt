import os
import random

# Constants
BOARD_ROWS = 6
BOARD_COLS = 7
MAX_PLAYERS = 5
CHECKERS = ['X', 'O', 'V', 'H', 'M']

# Initialize the board
def initialize_board(rows, cols):
    return [[' ' for _ in range(cols)] for _ in range(rows)]

# Print the board
def print_board(board):
    os.system('clear')
    print('  A   B   C   D   E   F   G')
    for i in range(BOARD_ROWS):
        row = '|'
        for j in range(BOARD_COLS):
            row += ' ' + board[i][j] + ' |'
        print(row)
        print('+---+---+---+---+---+---+---+')

# Check if a column is full
def is_column_full(board, col):
    return board[0][col]!= ' '

# Get the lowest available row in a column
def get_lowest_available_row(board, col):
    for i in range(BOARD_ROWS - 1, -1, -1):
        if board[i][col] == ' ':
            return i
    return -1

# Place a checker in a column
def place_checker(board, player, col):
    row = get_lowest_available_row(board, col)
    if row!= -1:
        board[row][col] = player
        return True
    return False

# Check for a win
def check_win(board, player):
    # Check horizontal locations for win
    for c in range(BOARD_COLS - 3):
        for r in range(BOARD_ROWS):
            if board[r][c] == player and board[r][c+1] == player and board[r][c+2] == player and board[r][c+3] == player:
                return True

    # Check vertical locations for win
    for c in range(BOARD_COLS):
        for r in range(BOARD_ROWS - 3):
            if board[r][c] == player and board[r+1][c] == player and board[r+2][c] == player and board[r+3][c] == player:
                return True

    # Check positively sloped diagonals
    for c in range(BOARD_COLS - 3):
        for r in range(BOARD_ROWS - 3):
            if board[r][c] == player and board[r+1][c+1] == player and board[r+2][c+2] == player and board[r+3][c+3] == player:
                return True

    # Check negatively sloped diagonals
    for c in range(BOARD_COLS - 3):
        for r in range(3, BOARD_ROWS):
            if board[r][c] == player and board[r-1][c+1] == player and board[r-2][c+2] == player and board[r-3][c+3] == player:
                return True

# Check for a draw
def check_draw(board):
    for row in board:
        for cell in row:
            if cell == ' ':
                return False
    return True

# Main game loop
def play_game():
    num_players = 2
    players = CHECKERS[:num_players]
    current_player = random.choice(players)
    board = initialize_board(BOARD_ROWS, BOARD_COLS)
    print_board(board)
    while True:
        col = input(f"Player {current_player}, please enter a column (A-G): ").upper()
        col = ord(col) - ord('A')
        if col < 0 or col >= BOARD_COLS:
            print("Invalid column. Please try again.")
            continue
        if is_column_full(board, col):
            print("Column is full. Please try again.")
            continue
        if not place_checker(board, current_player, col):
            print("Error placing checker. Please try again.")
            continue
        print_board(board)
        if check_win(board, current_player):
            print(f"Player {current_player} won!")
            break
        if check_draw(board):
            print("It's a draw!")
            break
        current_player = players[(players.index(current_player) + 1) % num_players]

play_game()
