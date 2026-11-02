import os
import random

# Constants
NUM_ROWS = 6
NUM_COLS = 7
MAX_PLAYERS = 5
CHECKERS = ["X", "O", "V", "H", "M"]
NUM_PLAYERS = 2

# Initialize the board
def init_board():
    return [[" " for _ in range(NUM_COLS)] for _ in range(NUM_ROWS)]

# Print the board
def print_board(board):
    os.system('clear')
    print("  A   B   C   D   E   F   G")
    for row in board:
        print("+---" * NUM_COLS + "+")
        print("| " + " | ".join(row) + " |")
    print("+---" * NUM_COLS + "+")

# Check if a move is valid
def is_valid_move(board, col):
    return board[0][col] == " "

# Make a move
def make_move(board, player, col):
    for row in reversed(board):
        if row[col] == " ":
            row[col] = CHECKERS[player]
            break

# Check for a win
def check_win(board, player):
    checker = CHECKERS[player]
    # Check horizontal
    for row in board:
        for i in range(NUM_COLS - 3):
            if row[i] == row[i+1] == row[i+2] == row[i+3] == checker:
                return True
    # Check vertical
    for col in range(NUM_COLS):
        for i in range(NUM_ROWS - 3):
            if board[i][col] == board[i+1][col] == board[i+2][col] == board[i+3][col] == checker:
                return True
    # Check diagonal (top-left to bottom-right)
    for row in range(NUM_ROWS - 3):
        for col in range(NUM_COLS - 3):
            if board[row][col] == board[row+1][col+1] == board[row+2][col+2] == board[row+3][col+3] == checker:
                return True
    # Check diagonal (bottom-left to top-right)
    for row in range(3, NUM_ROWS):
        for col in range(NUM_COLS - 3):
            if board[row][col] == board[row-1][col+1] == board[row-2][col+2] == board[row-3][col+3] == checker:
                return True
    return False

# Check for a draw
def check_draw(board):
    return all(cell!= " " for row in board for cell in row)

# Main game loop
def game_loop():
    board = init_board()
    current_player = random.randint(0, NUM_PLAYERS - 1)
    while True:
        print_board(board)
        col = input(f"Player {CHECKERS[current_player]}, please enter a column (A-{chr(64+NUM_COLS)}): ").upper()
        col = ord(col) - 65
        if not (0 <= col < NUM_COLS):
            print("Invalid column, please try again.")
            continue
        if not is_valid_move(board, col):
            print("Column is full, please try again.")
            continue
        make_move(board, current_player, col)
        if check_win(board, current_player):
            print_board(board)
            print(f"Player {CHECKERS[current_player]} won!")
            break
        if check_draw(board):
            print_board(board)
            print("It's a draw!")
            break
        current_player = (current_player + 1) % NUM_PLAYERS

game_loop()
