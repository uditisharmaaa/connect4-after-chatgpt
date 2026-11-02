import os
import random

# Constants
ROWS = 6
COLS = 7
PLAYERS = ['X', 'O', 'V', 'H', 'M']

# Initialize the board
def create_board():
    return [[' ' for _ in range(COLS)] for _ in range(ROWS)]

# Print the board
def print_board(board):
    os.system('clear')
    print("  " + "   ".join(chr(65 + i) for i in range(COLS)))
    print("+---" + "+---" * (COLS - 1) + "+")
    for row in board:
        print("| " + " | ".join(row) + " |")
        print("+---" + "+---" * (COLS - 1) + "+")

# Check for a win
def check_win(board, player):
    for r in range(ROWS):
        for c in range(COLS):
            if board[r][c] == player:
                if check_direction(board, player, r, c, 1, 0) or \
                   check_direction(board, player, r, c, 0, 1) or \
                   check_direction(board, player, r, c, 1, 1) or \
                   check_direction(board, player, r, c, 1, -1):
                    return True
    return False

# Check in a specific direction
def check_direction(board, player, row, col, row_inc, col_inc):
    count = 0
    for _ in range(4):
        if 0 <= row < ROWS and 0 <= col < COLS and board[row][col] == player:
            count += 1
        else:
            break
        row += row_inc
        col += col_inc
    return count == 4

# Check for a draw
def check_draw(board):
    return all(board[0][c] != ' ' for c in range(COLS))

# Place the checker
def place_checker(board, col, player):
    for r in range(ROWS - 1, -1, -1):
        if board[r][col] == ' ':
            board[r][col] = player
            return True
    return False

# Get valid column input
def get_column_input():
    while True:
        col = input(f"Player {current_player}, please enter a column: ").upper()
        if len(col) == 1 and 'A' <= col <= chr(65 + COLS - 1):
            return ord(col) - 65
        print("Invalid input. Please enter a valid column letter.")

# Game loop
board = create_board()
current_player = random.choice(PLAYERS)
print_board(board)

while True:
    col = get_column_input()
    if not place_checker(board, col, current_player):
        print("Column full! Try again.")
        continue
    print_board(board)

    if check_win(board, current_player):
        print(f"Player {current_player} won!")
        break
    if check_draw(board):
        print("It's a draw!")
        break

    current_player = PLAYERS[(PLAYERS.index(current_player) + 1) % len(PLAYERS)]
