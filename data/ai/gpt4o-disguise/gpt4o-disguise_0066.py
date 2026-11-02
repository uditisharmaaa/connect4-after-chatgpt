import os
import random

# Constants
ROWS = 6
COLS = 7
PLAYERS = 2
CHECKERS = ["X", "O", "V", "H", "M"]

# Create board
def create_board():
    return [[" " for _ in range(COLS)] for _ in range(ROWS)]

# Print the board
def print_board(board):
    os.system('clear')
    print("  " + "   ".join(chr(65 + i) for i in range(COLS)))
    for row in board:
        print("+---" * COLS + "+")
        print("| " + " | ".join(row) + " |")
    print("+---" * COLS + "+")

# Validate input
def valid_input(column, board):
    if len(column) != 1 or not column.isalpha():
        return False
    col_idx = ord(column.upper()) - 65
    if col_idx < 0 or col_idx >= COLS:
        return False
    return board[0][col_idx] == " "

# Place checker
def place_checker(board, column, checker):
    col_idx = ord(column.upper()) - 65
    for row_idx in range(ROWS-1, -1, -1):
        if board[row_idx][col_idx] == " ":
            board[row_idx][col_idx] = checker
            break

# Check for win
def check_win(board, checker):
    # Horizontal check
    for row in board:
        for col in range(COLS - 3):
            if row[col] == checker and row[col+1] == checker and row[col+2] == checker and row[col+3] == checker:
                return True
    
    # Vertical check
    for col in range(COLS):
        for row in range(ROWS - 3):
            if board[row][col] == checker and board[row+1][col] == checker and board[row+2][col] == checker and board[row+3][col] == checker:
                return True

    # Diagonal check (/)
    for row in range(3, ROWS):
        for col in range(COLS - 3):
            if board[row][col] == checker and board[row-1][col+1] == checker and board[row-2][col+2] == checker and board[row-3][col+3] == checker:
                return True

    # Diagonal check (\)
    for row in range(ROWS - 3):
        for col in range(COLS - 3):
            if board[row][col] == checker and board[row+1][col+1] == checker and board[row+2][col+2] == checker and board[row+3][col+3] == checker:
                return True

    return False

# Check for draw
def check_draw(board):
    for row in board:
        for cell in row:
            if cell == " ":
                return False
    return True

# Main game loop
def play_game():
    board = create_board()
    current_player = random.randint(0, PLAYERS - 1)
    print_board(board)

    while True:
        checker = CHECKERS[current_player]
        column = input(f"Player {checker}, please enter a column: ")

        while not valid_input(column, board):
            column = input(f"Invalid column. Player {checker}, please enter a column: ")

        place_checker(board, column, checker)
        print_board(board)

        if check_win(board, checker):
            print(f"Player {checker} won!")
            break
        
        if check_draw(board):
            print("The game is a draw!")
            break

        current_player = (current_player + 1) % PLAYERS

if __name__ == "__main__":
    play_game()
