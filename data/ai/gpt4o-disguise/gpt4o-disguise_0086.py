import os
import random

# Constants
ROWS = 6
COLS = 7
PLAYERS = 2
CHECKERS = ['X', 'O', 'V', 'H', 'M'][:PLAYERS]

def create_board():
    return [[' ' for _ in range(COLS)] for _ in range(ROWS)]

def print_board(board):
    os.system('clear')
    print("  " + "   ".join(chr(65+i) for i in range(COLS)))
    print("+---" * COLS + "+")
    for row in board:
        print("| " + " | ".join(row) + " |")
        print("+---" * COLS + "+")

def get_column():
    while True:
        col = input("Enter a column: ").strip().upper()
        if len(col) == 1 and col in [chr(65+i) for i in range(COLS)]:
            return ord(col) - 65
        else:
            print("Invalid input! Try again.")

def is_valid_location(board, col):
    return board[0][col] == ' '

def get_next_open_row(board, col):
    for r in range(ROWS-1, -1, -1):
        if board[r][col] == ' ':
            return r

def place_checker(board, row, col, checker):
    board[row][col] = checker

def check_winning(board, checker):
    # Check horizontal locations
    for r in range(ROWS):
        for c in range(COLS-3):
            if board[r][c] == checker and board[r][c+1] == checker and board[r][c+2] == checker and board[r][c+3] == checker:
                return True

    # Check vertical locations
    for r in range(ROWS-3):
        for c in range(COLS):
            if board[r][c] == checker and board[r+1][c] == checker and board[r+2][c] == checker and board[r+3][c] == checker:
                return True

    # Check diagonal / locations
    for r in range(ROWS-3):
        for c in range(COLS-3):
            if board[r][c] == checker and board[r+1][c+1] == checker and board[r+2][c+2] == checker and board[r+3][c+3] == checker:
                return True

    # Check diagonal \ locations
    for r in range(3, ROWS):
        for c in range(COLS-3):
            if board[r][c] == checker and board[r-1][c+1] == checker and board[r-2][c+2] == checker and board[r-3][c+3] == checker:
                return True

    return False

def check_draw(board):
    for r in range(ROWS):
        for c in range(COLS):
            if board[r][c] == ' ':
                return False
    return True

board = create_board()
print_board(board)
current_player_index = random.randint(0, PLAYERS-1)

game_over = False
while not game_over:
    checker = CHECKERS[current_player_index]
    print(f"Player {checker}, please enter a column:")

    col = get_column()

    if is_valid_location(board, col):
        row = get_next_open_row(board, col)
        place_checker(board, row, col, checker)

        if check_winning(board, checker):
            print_board(board)
            print(f"Player {checker} won!")
            game_over = True
        elif check_draw(board):
            print_board(board)
            print("The game is a draw!")
            game_over = True
        else:
            current_player_index = (current_player_index + 1) % PLAYERS

    print_board(board)
