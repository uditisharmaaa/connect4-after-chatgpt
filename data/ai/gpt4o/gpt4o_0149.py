import os
import random

# Constants
ROWS = 6
COLS = 7
PLAYERS = 2
CHECKERS = ['X', 'O', 'V', 'H', 'M'][:PLAYERS]
START_COLUMN = 'A'

# Initialize the board
def initialize_board(rows, cols):
    return [[' ' for _ in range(cols)] for _ in range(rows)]

# Print the board
def print_board(board):
    os.system('clear')
    col_labels = '   '.join(chr(ord(START_COLUMN) + i) for i in range(COLS))
    print(f"  {col_labels}")
    print("+---" * COLS + "+")
    for row in board:
        print('|' + '|'.join(f" {cell} " for cell in row) + '|')
        print("+---" * COLS + "+")

# Check for a win
def check_win(board, checker):
    # Horizontal, Vertical, Diagonal (\ and /)
    for row in range(ROWS):
        for col in range(COLS - 3):
            if all(board[row][col + i] == checker for i in range(4)):
                return True
    for row in range(ROWS - 3):
        for col in range(COLS):
            if all(board[row + i][col] == checker for i in range(4)):
                return True
    for row in range(ROWS - 3):
        for col in range(COLS - 3):
            if all(board[row + i][col + i] == checker for i in range(4)):
                return True
    for row in range(3, ROWS):
        for col in range(COLS - 3):
            if all(board[row - i][col + i] == checker for i in range(4)):
                return True
    return False

# Check for a draw
def check_draw(board):
    return all(board[0][col] != ' ' for col in range(COLS))

# Place a checker
def place_checker(board, column, checker):
    col_idx = ord(column.upper()) - ord(START_COLUMN)
    if board[0][col_idx] != ' ':
        return False
    for row in reversed(range(ROWS)):
        if board[row][col_idx] == ' ':
            board[row][col_idx] = checker
            return True
    return False

# Get player input with validation
def get_player_input():
    while True:
        player_input = input("Please enter a column: ").strip().upper()
        if len(player_input) == 1 and START_COLUMN <= player_input < chr(ord(START_COLUMN) + COLS):
            return player_input
        print("Invalid input, please enter a valid column.")

def main():
    board = initialize_board(ROWS, COLS)
    current_player = random.choice(CHECKERS)
    print_board(board)

    while True:
        print(f"Player {current_player}, it's your turn.")
        column = get_player_input()
        if place_checker(board, column, current_player):
            print_board(board)
            if check_win(board, current_player):
                print(f"Player {current_player} won!")
                break
            if check_draw(board):
                print("The game is a draw!")
                break
            current_player = CHECKERS[(CHECKERS.index(current_player) + 1) % PLAYERS]
        else:
            print("Column is full. Turn lost.")

if __name__ == "__main__":
    main()
