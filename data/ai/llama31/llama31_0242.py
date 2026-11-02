import os
import random

# Constants
BOARD_ROWS = 6
BOARD_COLS = 7
NUM_PLAYERS = 2
CHECKERS = ['X', 'O', 'V', 'H', 'M']

# Initialize the board with whitespaces
def initialize_board():
    board = [[' ' for _ in range(BOARD_COLS)] for _ in range(BOARD_ROWS)]
    return board

# Print the board
def print_board(board):
    os.system('clear')
    print('  ' + ' '.join([chr(65 + i) for i in range(BOARD_COLS)]))
    print('+---' * BOARD_COLS + '+')
    for row in board:
        print('| ' + ' | '.join(row) + ' |')
        print('+---' * BOARD_COLS + '+')
    print()

# Check for invalid input
def validate_input(column):
    if not column.isalpha():
        return False
    column = ord(column) - 65
    if column < 0 or column >= BOARD_COLS:
        return False
    return True

# Get the next available row in a column
def get_next_row(board, column):
    for row in reversed(board):
        if row[column] == ' ':
            return board.index(row)
    return -1

# Check for a win
def check_win(board, player):
    # Check horizontal locations for win
    for c in range(BOARD_COLS - 3):
        for r in range(BOARD_ROWS):
            if board[r][c] == player and board[r][c + 1] == player and board[r][c + 2] == player and board[r][c + 3] == player:
                return True

    # Check vertical locations for win
    for c in range(BOARD_COLS):
        for r in range(BOARD_ROWS - 3):
            if board[r][c] == player and board[r + 1][c] == player and board[r + 2][c] == player and board[r + 3][c] == player:
                return True

    # Check positively sloped diagonals
    for c in range(BOARD_COLS - 3):
        for r in range(BOARD_ROWS - 3):
            if board[r][c] == player and board[r + 1][c + 1] == player and board[r + 2][c + 2] == player and board[r + 3][c + 3] == player:
                return True

    # Check negatively sloped diagonals
    for c in range(BOARD_COLS - 3):
        for r in range(3, BOARD_ROWS):
            if board[r][c] == player and board[r - 1][c + 1] == player and board[r - 2][c + 2] == player and board[r - 3][c + 3] == player:
                return True

    return False

# Check for a draw
def check_draw(board):
    for row in board:
        if ' ' in row:
            return False
    return True

# Main game loop
def play_game():
    board = initialize_board()
    players = CHECKERS[:NUM_PLAYERS]
    current_player = random.choice(players)

    while True:
        print_board(board)
        column = input(f"Player {current_player}, please enter a column: ").upper()
        if not validate_input(column):
            print("Invalid input. Please try again.")
            continue
        column = ord(column) - 65
        next_row = get_next_row(board, column)
        if next_row == -1:
            print("Column is full. Please try again.")
            continue
        board[next_row][column] = current_player
        if check_win(board, current_player):
            print_board(board)
            print(f"Player {current_player} won!")
            break
        if check_draw(board):
            print_board(board)
            print("It's a draw!")
            break
        current_player = players[(players.index(current_player) + 1) % NUM_PLAYERS]

play_game()
